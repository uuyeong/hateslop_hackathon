"""
학습 가이드 Agent 메인 실행 스크립트

사용자 입력을 받아 학습 주제를 카테고리로 분류하고,
해당 카테고리의 Agent를 실행하여 학습 가이드를 생성합니다.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tool.category_router import route_to_category_agent
from utils.json_parser import parse_learning_guide
from utils.word_generator import save_learning_guide_to_word
from utils.date_validator import validate_and_fix_dates
from utils.price_fetcher import enrich_estimated_cost


def load_env():
    """환경 변수 로드"""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        # 상위 디렉터리에서 찾기
        env_path = Path(__file__).parent.parent / ".env"
    
    load_dotenv(dotenv_path=env_path)
    
    # API 키 확인
    if "TAVILY_API_KEY" not in os.environ or os.environ["TAVILY_API_KEY"] == "YOUR_KEY":
        print("❌ 경고: TAVILY_API_KEY 환경변수가 설정되지 않았습니다.")
        print(f"   .env 파일 경로: {env_path.absolute()}")
        return False
    
    if "OPENAI_API_KEY" not in os.environ or os.environ["OPENAI_API_KEY"] == "YOUR_KEY":
        print("❌ 경고: OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
        print(f"   .env 파일 경로: {env_path.absolute()}")
        return False
    
    print("✅ 환경 변수가 설정되었습니다.")
    return True


def create_learning_guide(topic: str, start_date: str = None) -> dict:
    """
    학습 가이드 생성 메인 함수
    
    Args:
        topic: 학습 주제
        start_date: 시작 날짜 (YYYY-MM-DD 형식, None이면 오늘)
    
    Returns:
        파싱된 학습 가이드 딕셔너리
    """
    if start_date is None:
        start_date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"\n{'='*60}")
    print(f"📚 '{topic}' 학습 가이드 생성 중...")
    print(f"{'='*60}\n")
    
    # 카테고리 분류 및 Agent 실행
    result = route_to_category_agent(topic, start_date)
    
    # JSON 파싱
    if "raw_output" in result:
        parsed_guide = parse_learning_guide(result["raw_output"])
        if "error" not in parsed_guide:
            parsed_guide["category"] = result.get("category", "Unknown")
            # 날짜 검증 및 수정
            parsed_guide = validate_and_fix_dates(parsed_guide)
            # Tavily 기반 실제 비용 정보 주입
            parsed_guide = enrich_estimated_cost(parsed_guide)
        return parsed_guide
    
    return result


def print_learning_guide_summary(guide: dict):
    """학습 가이드 요약 출력"""
    if "error" in guide:
        print("\n❌ 학습 가이드 생성 실패:")
        error_msg = guide.get("error", "")
        raw_output = guide.get("raw_output", "")
        if error_msg:
            print(f"오류: {error_msg}")
        if raw_output:
            print(f"원본 출력:\n{raw_output}")
        if not error_msg and not raw_output:
            print("알 수 없는 오류가 발생했습니다.")
        return
    
    print("\n" + "="*60)
    print(f"✅ 학습 가이드 생성 완료!")
    print(f"{'='*60}")
    print(f"📖 주제: {guide.get('topic', 'N/A')}")
    print(f"🏷️  카테고리: {guide.get('category', 'N/A')}")
    print(f"📅 학습 기간: {guide.get('start_date', 'N/A')} ~ {guide.get('end_date', 'N/A')}")
    print(f"⏱️  총 학습 일수: {guide.get('total_duration_days', 'N/A')}일")
    
    if guide.get('estimated_cost'):
        cost = guide['estimated_cost']
        if isinstance(cost, dict):
            print(f"💰 총 예상 금액: {cost.get('total', 0):,}원")
    
    steps = guide.get("steps", [])
    print(f"📌 총 {len(steps)}단계로 구성됩니다.\n")
    
    # 각 단계 요약
    for step in steps:
        print(f"  {step.get('step_number', 'N/A')}. {step.get('title', 'N/A')}")
        print(f"     기간: {step.get('start_date', 'N/A')} ~ {step.get('end_date', 'N/A')} ({step.get('duration_days', 'N/A')}일)")


def main():
    """메인 실행 함수"""
    # 환경 변수 로드
    if not load_env():
        print("\n❌ 환경 변수 설정 후 다시 실행해주세요.")
        return
    
    # 사용자 입력 받기
    print("\n" + "="*60)
    print("🎓 학습 가이드 Agent")
    print("="*60)
    print("\n어떤 것을 배우고 싶으신가요?")
    print("예시: 머신러닝, 파이썬, 축구, 뜨개질, 주식, C언어, 춤 등")
    
    topic = input("\n학습 주제를 입력하세요: ").strip()
    
    if not topic:
        print("❌ 학습 주제를 입력해주세요.")
        return
    
    # 시작 날짜 입력 (선택사항)
    start_date_input = input("시작 날짜를 입력하세요 (YYYY-MM-DD, 엔터 시 오늘): ").strip()
    start_date = start_date_input if start_date_input else None
    
    # 학습 가이드 생성
    guide = create_learning_guide(topic, start_date)
    
    # 요약 출력
    print_learning_guide_summary(guide)
    
    # Word 파일 저장
    if "error" not in guide:
        print("\n" + "="*60)
        word_file = save_learning_guide_to_word(guide)
        if word_file:
            print(f"\n📄 전체 내용은 워드 파일에서 확인하세요: {word_file}")
            print("="*60)
    else:
        print("\n❌ Word 파일을 생성할 수 없습니다.")


if __name__ == "__main__":
    main()

