"""
Word 파일 생성 유틸리티

학습 가이드를 Word 문서로 변환하는 함수들
"""

from datetime import datetime
from typing import Dict, Any, Optional
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn


def save_learning_guide_to_word(guide: Dict[str, Any], filename: Optional[str] = None) -> Optional[str]:
    """
    학습 가이드를 워드 파일로 저장
    
    Args:
        guide: 학습 가이드 딕셔너리 (파싱된 JSON)
        filename: 저장할 파일명 (None이면 자동 생성)
    
    Returns:
        저장된 파일 경로 또는 None
    """
    if "error" in guide:
        print("❌ 가이드가 생성되지 않아 워드 파일을 만들 수 없습니다.")
        return None
    
    # 파일명 생성
    if filename is None:
        topic = guide.get('topic', '학습가이드').replace(' ', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{topic}_학습가이드_{timestamp}.docx"
    
    # 워드 문서 생성
    doc = Document()
    
    # 문서 스타일 설정
    set_document_style(doc)
    
    # 제목
    title = doc.add_heading(f"{guide.get('topic', '학습 가이드')} 학습 가이드", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 카테고리 정보
    if guide.get('category'):
        category_para = doc.add_paragraph()
        category_para.add_run("카테고리: ").bold = True
        category_para.add_run(guide.get('category', ''))
        doc.add_paragraph("")
    
    # 기본 정보
    info_para = doc.add_paragraph()
    info_para.add_run("학습 기간: ").bold = True
    info_para.add_run(f"{guide.get('start_date', 'N/A')} ~ {guide.get('end_date', 'N/A')}")
    
    duration_para = doc.add_paragraph()
    duration_para.add_run("총 학습 일수: ").bold = True
    duration_para.add_run(f"{guide.get('total_duration_days', 'N/A')}일")
    
    doc.add_paragraph("")  # 빈 줄
    
    # 예상 금액
    if guide.get('estimated_cost'):
        cost_para = doc.add_heading("💰 예상 비용", level=2)
        cost = guide['estimated_cost']
        if isinstance(cost, dict):
            cost_list = doc.add_paragraph(f"교재: {cost.get('books', 0):,}원", style='List Bullet')
            cost_list = doc.add_paragraph(f"강의: {cost.get('courses', 0):,}원", style='List Bullet')
            cost_list = doc.add_paragraph(f"장비/기타: {cost.get('equipment', 0):,}원", style='List Bullet')
            total_para = doc.add_paragraph(f"총 예상 금액: {cost.get('total', 0):,}원")
            total_para.runs[0].bold = True
        doc.add_paragraph("")
    
    # 후기 요약
    if guide.get('reviews_summary'):
        review_heading = doc.add_heading("💬 학습자 후기 요약", level=2)
        review_para = doc.add_paragraph(guide['reviews_summary'])
        doc.add_paragraph("")
    
    # 각 단계별 내용
    steps = guide.get("steps", [])
    for step in steps:
        # 단계 제목
        step_title = doc.add_heading(
            f"{step.get('step_number', 'N/A')}단계: {step.get('title', 'N/A')}", 
            level=1
        )
        
        # 기간 정보
        period_para = doc.add_paragraph()
        period_para.add_run(f"📅 기간: ").bold = True
        period_para.add_run(
            f"{step.get('start_date', 'N/A')} ~ {step.get('end_date', 'N/A')} "
            f"({step.get('duration_days', 'N/A')}일)"
        )
        doc.add_paragraph("")  # 빈 줄
        
        # 학습 내용
        if step.get("learning_content"):
            doc.add_paragraph("📚 학습 내용:", style='Heading 2')
            for content in step.get("learning_content", []):
                para = doc.add_paragraph(content, style='List Bullet')
            doc.add_paragraph("")  # 빈 줄
        
        # 추천 교재
        if step.get("recommended_books"):
            doc.add_paragraph("📖 추천 교재:", style='Heading 2')
            for book in step.get("recommended_books", []):
                if isinstance(book, dict):
                    book_para = doc.add_paragraph(
                        f"{book.get('title', 'N/A')} - {book.get('price', 0):,}원",
                        style='List Bullet'
                    )
                    if book.get('reason'):
                        reason_para = doc.add_paragraph(f"  (추천 이유: {book.get('reason')})", style='List Bullet 2')
                else:
                    doc.add_paragraph(str(book), style='List Bullet')
            doc.add_paragraph("")  # 빈 줄
        
        # 참고 사이트
        if step.get("recommended_sites"):
            doc.add_paragraph("🌐 참고 사이트:", style='Heading 2')
            for site in step.get("recommended_sites", []):
                if isinstance(site, dict):
                    para = doc.add_paragraph()
                    para.add_run(f"{site.get('name', 'N/A')}").bold = True
                    para.add_run(f" ({site.get('type', '')}): ")
                    para.add_run(site.get('url', 'N/A'))
                else:
                    doc.add_paragraph(str(site), style='List Bullet')
            doc.add_paragraph("")  # 빈 줄
        
        # 투두리스트
        if step.get("todos"):
            doc.add_paragraph("✅ 투두리스트:", style='Heading 2')
            for todo in step.get("todos", []):
                para = doc.add_paragraph(todo, style='List Bullet')
                # 체크박스 스타일을 위해 앞에 ☐ 추가
            doc.add_paragraph("")  # 빈 줄
        
        # 단계별 예상 비용
        if step.get("estimated_cost"):
            step_cost_para = doc.add_paragraph()
            step_cost_para.add_run(f"💵 단계별 예상 비용: ").bold = True
            step_cost_para.add_run(f"{step.get('estimated_cost'):,}원")
            doc.add_paragraph("")  # 빈 줄
        
        # 단계 구분선
        doc.add_paragraph("─" * 50)
        doc.add_paragraph("")  # 빈 줄
    
    # 파일 저장
    doc.save(filename)
    print(f"✅ 워드 파일이 저장되었습니다: {filename}")
    return filename


def set_document_style(doc: Document):
    """문서 스타일 설정"""
    # 기본 폰트 설정
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Malgun Gothic'  # 한글 폰트
    font.size = Pt(11)
    
    # 제목 스타일
    heading_style = doc.styles['Heading 1']
    heading_font = heading_style.font
    heading_font.name = 'Malgun Gothic'
    heading_font.bold = True
    heading_font.size = Pt(16)

