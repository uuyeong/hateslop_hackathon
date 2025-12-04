"""
날짜 검증 및 수정 유틸리티

학습 가이드의 날짜가 논리적으로 맞는지 검증하고 자동으로 수정하는 함수들
"""

from datetime import datetime, timedelta
from typing import Dict, Any


def validate_and_fix_dates(guide: Dict[str, Any]) -> Dict[str, Any]:
    """
    학습 가이드의 날짜가 논리적으로 맞는지 검증하고 수정
    
    검증 및 수정 항목:
    1. 각 단계의 시작일과 종료일이 유효한지
    2. 단계들이 연속적인지 (이전 단계 종료일 다음날 = 다음 단계 시작일)
    3. 총 학습 일수가 단계별 일수의 합과 일치하는지
    
    Args:
        guide: 학습 가이드 딕셔너리
    
    Returns:
        날짜가 수정된 학습 가이드 딕셔너리
    """
    if "error" in guide or "steps" not in guide:
        return guide
    
    steps = guide.get("steps", [])
    if not steps:
        return guide
    
    # 첫 번째 단계의 시작일을 가이드의 시작일로 설정
    start_date_str = guide.get("start_date") or steps[0].get("start_date")
    
    if not start_date_str:
        # 시작일이 없으면 오늘 날짜 사용
        start_date = datetime.now()
        start_date_str = start_date.strftime("%Y-%m-%d")
    
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        # 날짜 형식이 잘못되었으면 오늘 날짜 사용
        start_date = datetime.now()
        start_date_str = start_date.strftime("%Y-%m-%d")
    
    # 각 단계의 날짜를 검증하고 수정
    current_date = start_date
    total_days = 0
    
    for i, step in enumerate(steps, 1):
        # 시작일 설정
        step_start = current_date
        
        # 기간 일수 가져오기 (기본값 7일)
        duration = step.get("duration_days", 7)
        if not isinstance(duration, (int, float)) or duration < 1:
            duration = 7
        
        # 종료일 계산 (시작일 + 기간 - 1일, 당일 포함)
        step_end = step_start + timedelta(days=int(duration) - 1)
        
        # 단계 정보 업데이트
        step["start_date"] = step_start.strftime("%Y-%m-%d")
        step["end_date"] = step_end.strftime("%Y-%m-%d")
        step["duration_days"] = int(duration)
        step["step_number"] = i
        
        # 다음 단계 시작일 (현재 단계 종료일 다음날)
        current_date = step_end + timedelta(days=1)
        total_days += int(duration)
    
    # 가이드 날짜 정보 업데이트
    guide["start_date"] = start_date_str
    guide["end_date"] = steps[-1]["end_date"]
    guide["total_duration_days"] = total_days
    
    return guide


def validate_date_format(date_str: str) -> bool:
    """
    날짜 형식이 유효한지 검증
    
    Args:
        date_str: 검증할 날짜 문자열 (YYYY-MM-DD 형식)
    
    Returns:
        유효한 날짜인지 여부
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False


def calculate_end_date(start_date_str: str, duration_days: int) -> str:
    """
    시작일과 기간으로 종료일 계산
    
    Args:
        start_date_str: 시작일 (YYYY-MM-DD)
        duration_days: 기간 (일수)
    
    Returns:
        종료일 (YYYY-MM-DD)
    """
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = start_date + timedelta(days=duration_days - 1)
        return end_date.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return start_date_str

