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
    
    return parsed

