# 구현 상태 및 다음 단계

## 현재 상태 요약

### ✅ 완성된 부분
기본 틀은 모두 구현되었습니다! 다음과 같은 기능들이 준비되어 있습니다:

1. **5가지 카테고리별 Agent 함수**
   - Academic / STEM
   - Career / Tech Skills
   - Sports / Physical Skills
   - Arts / Creative
   - Lifestyle / Hobby

2. **카테고리 자동 분류**
   - 키워드 기반 분류
   - LLM 기반 분류 (키워드 매칭 실패 시)

3. **학습 가이드 생성 파이프라인**
   - Tavily 검색 통합
   - OpenAI LLM 활용
   - JSON 형식 출력

4. **Word 파일 생성**
   - 구조화된 문서 생성
   - 단계별 계획, 투두리스트, 비용, 후기 포함

---

## 🚨 즉시 해결해야 할 문제

현재 코드는 **기본 구조는 완성**되었지만, **실제 실행 시 문제**가 발생할 수 있는 부분들이 있습니다:

### 1. 날짜 계산이 LLM에만 의존
**문제**: LLM이 계산한 날짜가 논리적으로 맞지 않을 수 있음
- 예: 이전 단계 종료일과 다음 단계 시작일이 연속되지 않음
- 예: 총 학습 일수가 단계별 일수의 합과 맞지 않음

**해결책**: 날짜 검증 및 자동 수정 함수 구현

### 2. JSON 파싱 실패 가능성
**문제**: LLM이 항상 완벽한 JSON을 출력하지 않을 수 있음
- 예: JSON 형식 오류
- 예: 필수 필드 누락
- 예: 중괄호 미매칭

**해결책**: 
- JSON 파싱 로직 강화
- 부분 파싱 지원
- 기본값 설정

### 3. Tavily 검색 활용 부족
**문제**: Tavily Tool은 있지만, 프롬프트에만 의존하여 최적 활용 안됨
- 가격 정보 검색이 부정확할 수 있음
- 후기 수집이 제한적일 수 있음

**해결책**: 카테고리별 최적화된 검색 전략 구현

---

## 📋 구체적인 구현 작업

### 작업 1: 날짜 검증 및 수정 함수 생성 (우선순위: 높음)

**파일**: `utils/date_validator.py` (새로 생성)

```python
from datetime import datetime, timedelta
from typing import Dict, Any

def validate_and_fix_dates(guide: Dict[str, Any]) -> Dict[str, Any]:
    """
    학습 가이드의 날짜가 논리적으로 맞는지 검증하고 수정
    
    검증 항목:
    1. 각 단계의 시작일과 종료일이 유효한지
    2. 단계들이 연속적인지 (이전 단계 종료일 다음날 = 다음 단계 시작일)
    3. 총 학습 일수가 단계별 일수의 합과 일치하는지
    """
    if "error" in guide or "steps" not in guide:
        return guide
    
    steps = guide["steps"]
    if not steps:
        return guide
    
    # 첫 번째 단계의 시작일을 가이드의 시작일로 설정
    start_date = datetime.strptime(guide.get("start_date", steps[0]["start_date"]), "%Y-%m-%d")
    
    # 각 단계의 날짜를 검증하고 수정
    current_date = start_date
    total_days = 0
    
    for i, step in enumerate(steps, 1):
        # 시작일 설정
        step_start = current_date
        
        # 기간 일수 가져오기
        duration = step.get("duration_days", 7)
        
        # 종료일 계산 (시작일 + 기간 - 1일, 당일 포함)
        step_end = step_start + timedelta(days=duration - 1)
        
        # 단계 정보 업데이트
        step["start_date"] = step_start.strftime("%Y-%m-%d")
        step["end_date"] = step_end.strftime("%Y-%m-%d")
        step["duration_days"] = duration
        
        # 다음 단계 시작일 (현재 단계 종료일 다음날)
        current_date = step_end + timedelta(days=1)
        total_days += duration
    
    # 가이드 날짜 정보 업데이트
    guide["start_date"] = start_date.strftime("%Y-%m-%d")
    guide["end_date"] = steps[-1]["end_date"]
    guide["total_duration_days"] = total_days
    
    return guide
```

### 작업 2: JSON 파싱 강화 (우선순위: 높음)

**파일**: `utils/json_parser.py` 개선

기존 함수에 다음 기능 추가:
- 부분 파싱 (일부 필드만 추출)
- 필수 필드 검증
- 기본값 설정

### 작업 3: 메인 함수에 날짜 검증 추가 (우선순위: 높음)

**파일**: `main.py` 수정

`create_learning_guide` 함수에 날짜 검증 로직 추가:

```python
from utils.date_validator import validate_and_fix_dates

def create_learning_guide(topic: str, start_date: str = None) -> dict:
    # ... 기존 코드 ...
    
    # JSON 파싱
    if "raw_output" in result:
        parsed_guide = parse_learning_guide(result["raw_output"])
        if "error" not in parsed_guide:
            parsed_guide["category"] = result.get("category", "Unknown")
            # 날짜 검증 및 수정 추가
            parsed_guide = validate_and_fix_dates(parsed_guide)
        return parsed_guide
    
    return result
```

---

## 🧪 테스트 체크리스트

실제로 작동하는지 테스트해봐야 할 항목들:

### 기본 기능 테스트
- [ ] 각 카테고리로 학습 가이드 생성 테스트
- [ ] JSON 파싱 테스트
- [ ] Word 파일 생성 테스트

### 엣지 케이스 테스트
- [ ] 잘못된 형식의 JSON 처리
- [ ] 날짜 계산 오류 처리
- [ ] API 호출 실패 처리

### 통합 테스트
- [ ] 전체 파이프라인 테스트 (입력 → 출력)
- [ ] 여러 주제로 연속 테스트

---

## 🎯 다음 단계 권장 사항

### 1단계: 즉시 구현 (오늘)
1. ✅ 날짜 검증 함수 생성
2. ✅ 메인 함수에 날짜 검증 추가
3. ✅ 간단한 테스트 실행

### 2단계: 개선 작업 (이번 주)
1. JSON 파싱 강화
2. 에러 처리 개선
3. 기본 테스트 코드 작성

### 3단계: 최적화 (다음 주)
1. Tavily 검색 전략 개선
2. 프롬프트 최적화
3. 성능 개선

---

## 💡 팁

1. **먼저 테스트해보기**: 현재 코드로도 기본 기능은 작동할 수 있습니다. 먼저 실행해보고 문제를 발견한 후 개선하세요.

2. **단계적 접근**: 모든 기능을 한 번에 개선하려 하지 말고, 우선순위가 높은 것부터 하나씩 해결하세요.

3. **에러 로그 확인**: 실행 중 발생하는 에러를 자세히 기록하고, 이를 바탕으로 개선하세요.

---

## 📚 참고 자료

- [TODO.md](./TODO.md): 전체 기능 체크리스트
- [SETUP.md](./SETUP.md): 설치 및 실행 가이드
- [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md): 프로젝트 구조 설명

