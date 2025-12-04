from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import re
import os
from datetime import datetime


# ------------------------------------------------------
# 하이퍼링크 생성
# ------------------------------------------------------
def add_hyperlink(paragraph, text, url, color="0066CC"):
    """Word 문서에 클릭 가능한 하이퍼링크 생성"""
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )

    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")

    # 색상
    c = OxmlElement("w:color")
    c.set(qn("w:val"), color)
    rPr.append(c)

    # 밑줄
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)

    r.append(rPr)

    t = OxmlElement("w:t")
    t.text = text
    r.append(t)

    hyperlink.append(r)
    paragraph._p.append(hyperlink)
    return hyperlink


# ------------------------------------------------------
# 텍스트 공백 / 개행 오염 제거
# ------------------------------------------------------
def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return text
    text = re.sub(r"\s*\n\s*", " ", text)  # 줄바꿈 제거
    text = re.sub(r"\s{2,}", " ", text)  # 연속 공백 제거
    return text.strip()


# ------------------------------------------------------
# bullet(•, -, *) 제거 + 문자 리스트 자동 문장 복원 (핵심)
# ------------------------------------------------------
def normalize_learning_items(items):
    """
    1) LLM이 리스트 요소에 bullet을 붙여버린 경우 제거 ("• I" → "I")
    2) 공백/개행 제거
    3) 문자 단위 배열이면 자동으로 문장으로 재조합
    4) 문장 종결 부호(. , ? !) 기준으로 문장 분해
    """
    if not isinstance(items, list):
        return items

    cleaned = []

    # ------------------------------
    # ① bullet 제거
    # ------------------------------
    for it in items:
        if not isinstance(it, str):
            continue

        t = it.strip()

        # bullet 제거
        if t.startswith("•"):
            t = t[1:].strip()
        if t.startswith("-"):
            t = t[1:].strip()
        if t.startswith("*"):
            t = t[1:].strip()

        cleaned.append(t)

    # ------------------------------
    # ② 문자 단위 리스트인지 판별
    # ------------------------------
    if len(cleaned) > 1 and all(isinstance(x, str) and len(x) == 1 for x in cleaned):
        # 문자 병합
        full_text = "".join(cleaned)

        # 문장 분리 (. , ! ?)
        sentences = re.split(r'(?<=[\.\?\!,])\s*', full_text)
        sentences = [s.strip() for s in sentences if s.strip()]

        return sentences

    # ------------------------------
    # ③ 정상 문장 리스트면 그대로 반환
    # ------------------------------
    return cleaned


# ------------------------------------------------------
# 카드 형태 헤더
# ------------------------------------------------------
def add_card_header(doc, text, color=RGBColor(0, 102, 204)):
    """카드 영역의 헤더 + 아래 구분선"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(20)
    run.font.bold = True
    run.font.color.rgb = color

    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)

    line = doc.add_paragraph("━" * 50)
    line.paragraph_format.space_after = Pt(14)
    return p


# ------------------------------------------------------
# 메인 Word 생성 함수
# ------------------------------------------------------
def save_learning_guide_to_word(guide: dict, save_dir=".", filename_prefix="학습가이드"):

    if "steps" not in guide or not isinstance(guide["steps"], list):
        return None

    doc = Document()

    # --------------------------------------------------
    # 표지 카드
    # --------------------------------------------------
    title = doc.add_paragraph()
    run = title.add_run(f"📘 {guide.get('topic', '학습 가이드')}")
    run.font.size = Pt(32)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 80, 160)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = doc.add_paragraph()
    sub = subtitle.add_run(guide.get("category", ""))
    sub.font.size = Pt(18)
    sub.font.color.rgb = RGBColor(100, 100, 100)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph("━" * 60).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(" ")

    # --------------------------------------------------
    # 학습 개요 카드
    # --------------------------------------------------
    add_card_header(doc, "📅 학습 개요")

    p1 = doc.add_paragraph()
    p1.add_run("• 학습 기간: ").bold = True
    p1.add_run(f"{guide.get('start_date')} ~ {guide.get('end_date')}")

    p2 = doc.add_paragraph()
    p2.add_run("• 총 학습 일수: ").bold = True
    p2.add_run(f"{guide.get('total_duration_days')}일")

    doc.add_paragraph(" ")

    # --------------------------------------------------
    # 비용 카드
    # --------------------------------------------------
    cost = guide.get("estimated_cost", {})
    if isinstance(cost, dict):
        add_card_header(doc, "💰 예상 비용 요약")

        for key, value in cost.items():
            row = doc.add_paragraph()
            row.add_run(f"• {key}: ").bold = True
            row.add_run(f"{value:,}원")

        doc.add_paragraph(" ")

    # --------------------------------------------------
    # Step 카드들
    # --------------------------------------------------
    for step in guide["steps"]:
        step_num = step.get("step_number", 0)
        stitle = clean_text(step.get("title", ""))

        add_card_header(doc, f"🔵 Step {step_num}: {stitle}")

        # 기간
        p = doc.add_paragraph()
        p.add_run("📅 기간: ").bold = True
        p.add_run(f"{step.get('start_date')} ~ {step.get('end_date')}")

        # ------------------------------
        # 📚 학습 내용 (핵심 문제 해결)
        # ------------------------------
        doc.add_paragraph("📚 학습 내용").bold = True

        contents = step.get("learning_content", [])
        contents = normalize_learning_items(contents)

        for item in contents:
            doc.add_paragraph(f"• {clean_text(item)}", style="List Bullet")

        # ------------------------------
        # 추천 교재
        # ------------------------------
        books = step.get("recommended_books", [])
        if books:
            doc.add_paragraph("📘 추천 교재").bold = True
            for book in books:
                btitle = clean_text(book.get("title", ""))
                price = book.get("price", 0)
                reason = clean_text(book.get("reason", ""))

                doc.add_paragraph(f"📚 {btitle} — {price:,}원")
                if reason:
                    doc.add_paragraph(f"   ▷ {reason}")

        # ------------------------------
        # 참고 사이트
        # ------------------------------
        sites = step.get("recommended_sites", [])
        if sites:
            doc.add_paragraph("🌐 참고 자료").bold = True
            for site in sites:
                name = clean_text(site.get("name", ""))
                url = site.get("url", "")

                para = doc.add_paragraph()
                para.add_run(f"🔗 {name}: ")
                if url:
                    add_hyperlink(para, url, url)

        # ------------------------------
        # To-do List
        # ------------------------------
        todos = normalize_learning_items(step.get("todos", []))
        if todos:
            doc.add_paragraph("📝 To-do List").bold = True
            for t in todos:
                doc.add_paragraph(f"☐ {clean_text(t)}")

        doc.add_paragraph(" ")

    # --------------------------------------------------
    # 후기 카드
    # --------------------------------------------------
    if "reviews_summary" in guide:
        add_card_header(doc, "📌 학습 후기 요약")
        review = clean_text(guide.get("reviews_summary", ""))
        doc.add_paragraph(review)

    # --------------------------------------------------
    # 저장
    # --------------------------------------------------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.docx"
    filepath = os.path.join(save_dir, filename)

    doc.save(filepath)
    return filepath
