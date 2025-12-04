# 구현해야 할 기능 가이드

## 현재 상태

✅ **기본 틀은 완성되었습니다!**

다음 기능들이 구현되어 있습니다:
- 5가지 카테고리별 Agent 함수
- 카테고리 자동 분류
- 학습 가이드 생성 (단계별 계획, 투두리스트, 비용, 후기 포함)
- Word 파일 생성

---

## 🚨 즉시 구현한 것 (완료)

### 1. 날짜 검증 및 수정 함수 ✅
- `utils/date_validator.py` 생성
- 날짜가 논리적으로 맞는지 검증
- 자동으로 날짜 수정
- `main.py`에 통합 완료

### 2. JSON 파싱 개선 ✅
- 기본값 설정 함수 추가
- 누락된 필드 자동 채우기
- `utils/json_parser.py` 개선 완료

---

## ⚠️ 아직 구현해야 할 것

### 1. 에러 처리 강화 (우선순위: 높음)

**현재 문제**: API 호출 실패 시 에러 처리가 부족함

**구현 방법**:
```python
# tool/category_agents.py 개선

def create_academic_guide(topic: str, start_date: str = None, max_retries: int = 3) -> Dict[str, Any]:
    """재시도 로직 추가"""
    for attempt in range(max_retries):
        try:
            agent = create_category_agent("Academic / STEM", ACADEMIC_GUIDELINES)
            query = f"'{topic}'를 배우고 싶어..."
            result = agent.invoke({"input": query})
            return {"raw_output": result["output"], "category": "Academic / STEM"}
        except Exception as e:
            if attempt == max_retries - 1:
                return {"error": str(e), "category": "Academic / STEM"}
            time.sleep(2)  # 재시도 전 대기
```

### 2. Tavily 검색 최적화 (우선순위: 중간)

**현재 문제**: 프롬프트에만 의존하여 검색 결과가 부정확할 수 있음

**구현 방법**:
```python
# utils/search_utils.py 생성 (새 파일)

def search_book_prices(book_title: str) -> Dict[str, Any]:
    """책 가격 정보 검색"""
    tavily_tool = get_tavily_tool()
    results = tavily_tool.invoke({
        "query": f"{book_title} 책 가격 구매"
    })
    # 가격 정보 추출 및 반환
    return {"price": 25000, "source": "..."}

def search_reviews(topic: str) -> List[str]:
    """학습 후기 검색"""
    tavily_tool = get_tavily_tool()
    results = tavily_tool.invoke({
        "query": f"{topic} 학습 후기 경험"
    })
    # 후기 요약 및 반환
    return ["후기 1", "후기 2", ...]
```

### 3. 테스트 코드 작성 (우선순위: 중간)

**구현 방법**:
```python
# tests/test_category_agents.py 생성

import unittest
from tool.category_agents import create_academic_guide

class TestCategoryAgents(unittest.TestCase):
    def test_academic_guide_creation(self):
        guide = create_academic_guide("운영체제", "2025-12-05")
        self.assertIn("raw_output", guide)
        self.assertEqual(guide["category"], "Academic / STEM")
```

### 4. 프롬프트 최적화 (우선순위: 중간)

**현재 문제**: 프롬프트가 너무 길고 구체적이지 않을 수 있음

**개선 방법**:
- 각 카테고리별로 더 구체적인 예시 추가
- JSON 형식 명확화
- Tavily 검색 활용 지침 강화

---

## 📋 작업 순서 권장

### 즉시 해야 할 것 (오늘/내일)

1. **기본 테스트 실행**
   ```bash
   python main.py
   # "머신러닝" 입력하여 테스트
   ```

2. **발견된 문제 해결**
   - 실행 중 발생하는 에러 확인
   - JSON 파싱 오류 확인
   - 날짜 계산 오류 확인

3. **에러 처리 강화**
   - API 호출 재시도 로직
   - 명확한 에러 메시지

### 이번 주에 할 것

4. **Tavily 검색 최적화**
   - 가격 정보 전용 검색
   - 후기 수집 전용 검색

5. **프롬프트 개선**
   - 카테고리별 최적화
   - 예시 추가

6. **기본 테스트 코드**
   - 각 모듈별 단위 테스트

### 다음 주에 할 것 (선택사항)

7. **RAG 활용** (hw3 참고)
   - 벡터 DB에 학습 자료 저장
   - 재사용 가능하도록

8. **진행 상황 추적**
   - 투두리스트 완료 체크
   - 일정 캘린더 생성

---

## 🔧 구체적인 구현 방법

### 방법 1: 에러 처리 추가

**파일**: `tool/category_agents.py`

각 Agent 함수에 재시도 로직 추가:

```python
import time

def create_academic_guide(topic: str, start_date: str = None) -> Dict[str, Any]:
    """Academic/STEM 학습 가이드 생성 (재시도 로직 포함)"""
    if start_date is None:
        start_date = datetime.now().strftime('%Y-%m-%d')
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            agent = create_category_agent("Academic / STEM", ACADEMIC_GUIDELINES)
            query = f"'{topic}'를 배우고 싶어. {ACADEMIC_GUIDELINES} 단계별 학습 계획을 만들어줘. 오늘은 {start_date}야."
            result = agent.invoke({"input": query})
            return {"raw_output": result["output"], "category": "Academic / STEM"}
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️  재시도 중... ({attempt + 1}/{max_retries})")
                time.sleep(2)
            else:
                return {
                    "error": f"Agent 실행 실패: {str(e)}",
                    "category": "Academic / STEM",
                    "raw_output": ""
                }
```

### 방법 2: Tavily 검색 전용 함수 생성

**파일**: `utils/search_utils.py` (새로 생성)

```python
from tool.category_agents import get_tavily_tool

def search_book_info(book_title: str):
    """책 정보 및 가격 검색"""
    tavily = get_tavily_tool()
    results = tavily.invoke({
        "query": f"{book_title} 책 가격 구매 사이트"
    })
    # 결과에서 가격 정보 추출
    return results

def search_learning_reviews(topic: str):
    """학습 후기 검색"""
    tavily = get_tavily_tool()
    results = tavily.invoke({
        "query": f"{topic} 학습 후기 경험 수강"
    })
    return results
```

이 함수들을 프롬프트에서 참조하도록 수정하거나, Agent Tool로 등록 가능합니다.

---

## ✅ 체크리스트

### 기본 기능 (완료)
- [x] 프로젝트 구조 생성
- [x] 5가지 카테고리별 Agent
- [x] 카테고리 분류
- [x] JSON 파싱
- [x] Word 파일 생성
- [x] 날짜 검증 함수
- [x] 기본값 설정

### 개선 사항 (진행 필요)
- [ ] 에러 처리 강화
- [ ] Tavily 검색 최적화
- [ ] 프롬프트 개선
- [ ] 테스트 코드 작성

### 추가 기능 (선택사항)
- [ ] RAG 활용
- [ ] 진행 상황 추적
- [ ] 사용자 커스터마이징

---

## 💡 팁

1. **먼저 테스트하세요**: 현재 코드도 작동할 수 있으니 실행해보고 문제를 발견하세요.

2. **점진적 개선**: 모든 것을 한 번에 구현하려 하지 말고, 하나씩 개선하세요.

3. **에러 로그 확인**: 실행 중 발생하는 에러를 자세히 기록하세요.

4. **협업**: 2명이서 작업 분담하여 효율적으로 진행하세요.

---

## 📚 관련 문서

- [TODO.md](./TODO.md): 전체 기능 체크리스트
- [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md): 구현 상태 상세
- [SETUP.md](./SETUP.md): 설치 및 실행 가이드

