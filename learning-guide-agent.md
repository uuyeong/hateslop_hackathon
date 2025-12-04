# 학습 가이드 에이전트 구현 가이드

## 필요한 기술 (hw에서 배운 내용)

### 1. **Tavily Agent (hw11)** - 핵심 검색 도구
- 최신 학습 자료, 블로그, 사이트 검색
- 교재 정보, 온라인 강의, 튜토리얼 검색

### 2. **프롬프트 엔지니어링 (hw3)** - 구조화된 출력
- **Role Prompting**: "교육 전문가" 역할 설정
- **Few-shot**: 학습 계획 형식 예시 제공
- **CoT (Chain of Thought)**: 단계별 학습 계획 생성

### 3. **LangChain Agent (hw11)** - 자동화
- Tavily 검색 → 정보 수집 → 구조화된 답변 생성

## 구현 구조

```
사용자 입력: "머신러닝 배우고 싶어"
  ↓
1. Tavily 검색 (여러 번 호출)
   - "머신러닝 입문 가이드"
   - "머신러닝 추천 교재"
   - "머신러닝 온라인 강의"
   - "머신러닝 학습 로드맵"
  ↓
2. 프롬프트 엔지니어링으로 구조화
   - Role: 교육 전문가
   - Few-shot: 학습 계획 형식 예시
   - CoT: 단계별 계획 생성
  ↓
3. JSON 형식으로 출력
   - 단계별 학습 계획
   - 날짜별 일정
   - 투두리스트
  ↓
4. 최종 답변 생성
```

## 구현 방법

### Step 1: Tavily Tool 설정 (hw11 기반)

```python
from langchain_community.tools.tavily_search import TavilySearchResults

tavily_tool = TavilySearchResults(
    api_key=os.environ.get("TAVILY_API_KEY"),
    max_results=10  # 더 많은 결과 수집
)
```

### Step 2: 커스텀 프롬프트 작성 (hw3 프롬프트 엔지니어링 활용)

```python
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Role Prompting + Few-shot + CoT 결합
learning_guide_prompt = ChatPromptTemplate.from_messages([
    ("system", """너는 경험이 풍부한 교육 전문가이자 학습 설계자야.

다음 형식으로 학습 가이드를 작성해야 해:

[Few-shot 예시]
주제: "Python 프로그래밍"
학습 계획:
1단계: 기초 문법 (2025-12-05 ~ 2025-12-15, 10일)
   - 학습 내용: 변수, 자료형, 조건문, 반복문
   - 추천 교재: "점프 투 파이썬"
   - 참고 사이트: https://wikidocs.net/book/1
   - 투두: [ ] 변수와 자료형 학습, [ ] 조건문 실습, [ ] 반복문 실습

2단계: 함수와 클래스 (2025-12-16 ~ 2025-12-25, 10일)
   - 학습 내용: 함수 정의, 클래스 개념
   - 추천 교재: "파이썬 코딩의 기술"
   - 참고 사이트: https://docs.python.org/3/
   - 투두: [ ] 함수 작성 실습, [ ] 클래스 구현

[CoT 지침]
1. 먼저 주제의 난이도와 범위를 파악해
2. 단계별로 나누어 (기초 → 중급 → 고급)
3. 각 단계에 적절한 시간 배분 (초보자 기준)
4. 최신 자료와 검증된 교재를 추천해
5. 실용적인 투두리스트를 만들어줘

[출력 형식]
반드시 다음 JSON 형식으로 출력해:
{
  "topic": "주제명",
  "total_duration_days": 총_학습_일수,
  "start_date": "시작일 (YYYY-MM-DD)",
  "end_date": "종료일 (YYYY-MM-DD)",
  "steps": [
    {
      "step_number": 1,
      "title": "단계 제목",
      "duration_days": 단계별_일수,
      "start_date": "시작일",
      "end_date": "종료일",
      "learning_content": ["학습 내용 1", "학습 내용 2"],
      "recommended_books": ["교재 1", "교재 2"],
      "recommended_sites": [
        {"name": "사이트명", "url": "URL"}
      ],
      "todos": ["투두 1", "투두 2"]
    }
  ]
}
"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])
```

### Step 3: Agent 생성 및 실행

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
import json
from datetime import datetime, timedelta

# LLM 초기화
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# Agent 생성
tools = [tavily_tool]
agent = create_openai_tools_agent(llm, tools, learning_guide_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 실행 함수
def create_learning_guide(topic: str):
    """학습 가이드 생성"""
    query = f"{topic} 학습 가이드, 추천 교재, 온라인 강의, 학습 로드맵"
    
    # Agent 실행
    result = agent_executor.invoke({
        "input": f"'{topic}'를 배우고 싶어. 단계별 학습 계획을 만들어줘. 오늘 날짜는 {datetime.now().strftime('%Y-%m-%d')}야."
    })
    
    # JSON 파싱 시도
    try:
        # LLM 출력에서 JSON 추출
        output = result["output"]
        # JSON 부분만 추출 (마크다운 코드 블록 제거)
        json_str = output.split("```json")[1].split("```")[0].strip() if "```json" in output else output
        guide = json.loads(json_str)
        return guide
    except:
        # JSON 파싱 실패 시 텍스트 반환
        return {"raw_output": result["output"]}

# 사용 예시
guide = create_learning_guide("머신러닝")
print(json.dumps(guide, indent=2, ensure_ascii=False))
```

### Step 4: 투두리스트 생성 함수

```python
def generate_todo_list(guide: dict):
    """학습 가이드에서 투두리스트 생성"""
    todos = []
    for step in guide.get("steps", []):
        step_num = step["step_number"]
        step_title = step["title"]
        for todo in step.get("todos", []):
            todos.append({
                "step": f"{step_num}. {step_title}",
                "todo": todo,
                "due_date": step["end_date"],
                "completed": False
            })
    return todos

# 마크다운 형식으로 출력
def print_todo_markdown(todos):
    """투두리스트를 마크다운 형식으로 출력"""
    markdown = "# 학습 투두리스트\n\n"
    current_step = None
    for todo in todos:
        if current_step != todo["step"]:
            if current_step is not None:
                markdown += "\n"
            markdown += f"## {todo['step']}\n"
            current_step = todo["step"]
        markdown += f"- [ ] {todo['todo']} (마감: {todo['due_date']})\n"
    return markdown
```

## 전체 통합 코드

```python
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from datetime import datetime
import json

# 환경 설정
env_path = Path.cwd() / ".env"
load_dotenv(dotenv_path=env_path)

# Tavily Tool
tavily_tool = TavilySearchResults(
    api_key=os.environ.get("TAVILY_API_KEY"),
    max_results=10
)

# 커스텀 프롬프트 (Role + Few-shot + CoT)
prompt = ChatPromptTemplate.from_messages([
    ("system", """너는 경험이 풍부한 교육 전문가야.

학습 가이드를 다음 형식으로 작성해:
1. 단계별 학습 계획 (기초 → 중급 → 고급)
2. 각 단계별 학습 내용, 추천 교재, 참고 사이트
3. 날짜별 일정 (오늘부터 시작)
4. 투두리스트

JSON 형식으로 출력해:
{
  "topic": "주제",
  "total_duration_days": 일수,
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "steps": [
    {
      "step_number": 1,
      "title": "단계명",
      "duration_days": 일수,
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD",
      "learning_content": ["내용1", "내용2"],
      "recommended_books": ["교재1"],
      "recommended_sites": [{"name": "사이트명", "url": "URL"}],
      "todos": ["투두1", "투두2"]
    }
  ]
}
"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Agent 생성
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
agent = create_openai_tools_agent(llm, [tavily_tool], prompt)
agent_executor = AgentExecutor(agent=agent, tools=[tavily_tool], verbose=True)

# 실행
def create_learning_guide(topic: str):
    today = datetime.now().strftime('%Y-%m-%d')
    result = agent_executor.invoke({
        "input": f"'{topic}'를 배우고 싶어. 단계별 학습 계획을 만들어줘. 오늘은 {today}야."
    })
    return result["output"]

# 사용
guide_text = create_learning_guide("머신러닝")
print(guide_text)
```

## 추가 개선 사항

### 1. RAG 활용 (선택사항, hw3)
- 검색된 학습 자료를 ChromaDB에 저장
- 유사한 주제 재검색 시 기존 자료 재사용

### 2. 날짜 계산 자동화
- 사용자 일정 입력 받기
- 주말 제외, 하루 학습 시간 고려

### 3. 진행 상황 추적
- 투두리스트 완료 체크
- 다음 단계 자동 추천

