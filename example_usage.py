"""
학습 가이드 Agent 사용 예시

다양한 주제로 학습 가이드를 생성하는 예시 코드
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# 환경 변수 로드
env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from main import create_learning_guide
from utils.word_generator import save_learning_guide_to_word
from utils.json_parser import parse_learning_guide


def example_academic():
    """Academic/STEM 카테고리 예시"""
    print("\n" + "="*60)
    print("예시 1: Academic / STEM - '운영체제'")
    print("="*60)
    
    guide = create_learning_guide("운영체제", start_date="2025-12-05")
    
    if "error" not in guide:
        print(f"✅ 카테고리: {guide.get('category')}")
        print(f"✅ 단계 수: {len(guide.get('steps', []))}")
        save_learning_guide_to_word(guide, "예시_운영체제_학습가이드.docx")
    else:
        print(f"❌ 오류: {guide.get('error')}")


def example_career_tech():
    """Career/Tech Skills 카테고리 예시"""
    print("\n" + "="*60)
    print("예시 2: Career / Tech Skills - '머신러닝'")
    print("="*60)
    
    guide = create_learning_guide("머신러닝", start_date="2025-12-05")
    
    if "error" not in guide:
        print(f"✅ 카테고리: {guide.get('category')}")
        print(f"✅ 단계 수: {len(guide.get('steps', []))}")
        save_learning_guide_to_word(guide, "예시_머신러닝_학습가이드.docx")
    else:
        print(f"❌ 오류: {guide.get('error')}")


def example_sports():
    """Sports/Physical Skills 카테고리 예시"""
    print("\n" + "="*60)
    print("예시 3: Sports / Physical Skills - '축구'")
    print("="*60)
    
    guide = create_learning_guide("축구", start_date="2025-12-05")
    
    if "error" not in guide:
        print(f"✅ 카테고리: {guide.get('category')}")
        print(f"✅ 단계 수: {len(guide.get('steps', []))}")
        save_learning_guide_to_word(guide, "예시_축구_학습가이드.docx")
    else:
        print(f"❌ 오류: {guide.get('error')}")


def example_arts():
    """Arts/Creative 카테고리 예시"""
    print("\n" + "="*60)
    print("예시 4: Arts / Creative - '춤'")
    print("="*60)
    
    guide = create_learning_guide("춤", start_date="2025-12-05")
    
    if "error" not in guide:
        print(f"✅ 카테고리: {guide.get('category')}")
        print(f"✅ 단계 수: {len(guide.get('steps', []))}")
        save_learning_guide_to_word(guide, "예시_춤_학습가이드.docx")
    else:
        print(f"❌ 오류: {guide.get('error')}")


def example_lifestyle():
    """Lifestyle/Hobby 카테고리 예시"""
    print("\n" + "="*60)
    print("예시 5: Lifestyle / Hobby - '뜨개질'")
    print("="*60)
    
    guide = create_learning_guide("뜨개질", start_date="2025-12-05")
    
    if "error" not in guide:
        print(f"✅ 카테고리: {guide.get('category')}")
        print(f"✅ 단계 수: {len(guide.get('steps', []))}")
        save_learning_guide_to_word(guide, "예시_뜨개질_학습가이드.docx")
    else:
        print(f"❌ 오류: {guide.get('error')}")


if __name__ == "__main__":
    # API 키 확인
    if "TAVILY_API_KEY" not in os.environ:
        print("❌ TAVILY_API_KEY를 설정해주세요.")
        exit(1)
    
    if "OPENAI_API_KEY" not in os.environ:
        print("❌ OPENAI_API_KEY를 설정해주세요.")
        exit(1)
    
    print("="*60)
    print("학습 가이드 Agent 사용 예시")
    print("="*60)
    print("\n각 카테고리별로 예시를 실행합니다.")
    print("각 예시는 약 30초~1분 정도 소요될 수 있습니다.")
    
    # 원하는 예시만 실행하려면 주석을 해제하세요
    # example_academic()
    # example_career_tech()
    # example_sports()
    # example_arts()
    # example_lifestyle()
    
    print("\n⚠️  예시 실행을 원하시면 example_usage.py에서 주석을 해제하세요.")

