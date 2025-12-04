"""
JSON 파싱 유틸리티 함수

LLM 출력에서 JSON을 추출하고 파싱하는 함수들
"""

import json
import re
from typing import Dict, Any, Optional


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    텍스트에서 JSON을 추출
    
    Args:
        text: JSON이 포함된 텍스트
    
    Returns:
        파싱된 JSON 딕셔너리 또는 None
    """
    # 마크다운 코드 블록에서 JSON 추출 시도
    if "```json" in text:
        json_str = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        # 코드 블록 찾기
        code_blocks = re.findall(r'```(?:json)?\s*\n(.*?)\n```', text, re.DOTALL)
        if code_blocks:
            json_str = code_blocks[0].strip()
        else:
            json_str = text.split("```")[1].split("```")[0].strip()
    else:
        # JSON 부분만 찾기
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            return None
    
    try:
        # JSON 파싱 시도
        parsed = json.loads(json_str)
        return parsed
    except json.JSONDecodeError:
        # 정리 후 재시도
        json_str_cleaned = clean_json_string(json_str)
        try:
            parsed = json.loads(json_str_cleaned)
            return parsed
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 실패: {e}")
            return None


def clean_json_string(json_str: str) -> str:
    """
    JSON 문자열 정리 (주석 제거, 줄바꿈 정리 등)
    
    Args:
        json_str: 정리할 JSON 문자열
    
    Returns:
        정리된 JSON 문자열
    """
    # 주석 제거 (// 주석)
    json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)
    
    # 여러 줄바꿈을 하나로
    json_str = re.sub(r'\n\s*\n', '\n', json_str)
    
    return json_str.strip()


def set_default_values(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """
    파싱된 JSON에 누락된 필드에 기본값 설정
    
    Args:
        parsed: 파싱된 JSON 딕셔너리
    
    Returns:
        기본값이 설정된 딕셔너리
    """
    from datetime import datetime
    
    # 기본값 설정
    parsed.setdefault("topic", "학습 가이드")
    parsed.setdefault("category", "Unknown")
    parsed.setdefault("total_duration_days", 30)
    
    # 날짜 기본값
    if "start_date" not in parsed:
        parsed["start_date"] = datetime.now().strftime("%Y-%m-%d")
    
    # steps 기본값
    if "steps" not in parsed:
        parsed["steps"] = []
    
    # 각 단계에 기본값 설정
    for i, step in enumerate(parsed.get("steps", []), 1):
        step.setdefault("step_number", i)
        step.setdefault("title", f"{i}단계")
        step.setdefault("duration_days", 7)
        step.setdefault("learning_content", [])
        step.setdefault("recommended_books", [])
        step.setdefault("recommended_sites", [])
        step.setdefault("todos", [])
        step.setdefault("estimated_cost", 0)
    
    # 비용 정보 기본값
    if "estimated_cost" not in parsed:
        parsed["estimated_cost"] = {
            "books": 0,
            "courses": 0,
            "equipment": 0,
            "total": 0
        }
    elif isinstance(parsed.get("estimated_cost"), dict):
        cost = parsed["estimated_cost"]
        cost.setdefault("books", 0)
        cost.setdefault("courses", 0)
        cost.setdefault("equipment", 0)
        cost.setdefault("total", cost.get("books", 0) + cost.get("courses", 0) + cost.get("equipment", 0))
    
    # 후기 기본값
    parsed.setdefault("reviews_summary", "후기 정보가 없습니다.")
    
    return parsed


def parse_learning_guide(raw_output: str) -> Dict[str, Any]:
    """
    학습 가이드 출력을 파싱하여 구조화된 딕셔너리로 변환
    
    Args:
        raw_output: Agent의 원본 출력
    
    Returns:
        파싱된 학습 가이드 또는 에러 정보가 포함된 딕셔너리
    """
    parsed = extract_json_from_text(raw_output)
    
    if parsed is None:
        return {
            "error": "JSON 파싱 실패",
            "raw_output": raw_output
        }
    
    # 기본값 설정
    parsed = set_default_values(parsed)
    
    return parsed

