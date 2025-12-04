"""
카테고리별 학습 가이드 Agent 함수들

5가지 카테고리:
1. Academic / STEM (학술·STEM)
2. Career / Tech Skills (커리어·기술)
3. Sports / Physical Skills (스포츠·신체 기술)
4. Arts / Creative (예술·창작)
5. Lifestyle / Hobby (취미·생활)
"""

import os
from datetime import datetime
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools.tavily_search import TavilySearchResults


# Tavily Tool 생성 (모든 카테고리에서 공통 사용)
def get_tavily_tool():
    """Tavily 검색 Tool 생성"""
    return TavilySearchResults(
        api_key=os.environ.get("TAVILY_API_KEY", ""),
        max_results=10
    )


def get_base_llm():
    """기본 LLM 생성"""
    return ChatOpenAI(model="gpt-4-turbo", temperature=0)


def create_category_prompt(category_name: str, category_guidelines: str) -> ChatPromptTemplate:
    """카테고리별 프롬프트 생성"""
    system_message = f"""너는 {category_name} 전문 교육 설계자야.

{category_guidelines}

사용자가 배우고 싶은 주제에 대해 다음을 포함한 학습 가이드를 작성해:

1. **단계별 구성**: 기초 → 중급 → 고급 순서로 3~6단계로 나눠 (난이도와 범위에 따라 조절)
2. **날짜 배분**: 각 단계별 시작일과 종료일을 명확히 지정
3. **실용적인 투두리스트**: 각 단계마다 체크 가능한 구체적인 할 일 목록
4. **검증된 자료 추천**: 
   - 교재 (책 제목과 가격 포함)
   - 유튜브 채널/강의
   - 블로그/사이트
   - 코딩의 경우 깃허브 레포지토리
5. **예상 금액**: 책 가격, 강의 비용, 장비 비용 등 포함
6. **후기 정리**: 해당 공부를 이미 한 사람들의 후기 요약

[출력 형식]
반드시 다음 JSON 형식으로 출력해:
{{
  "topic": "주제명",
  "category": "{category_name}",
  "total_duration_days": 총_학습_일수,
  "start_date": "시작일 (YYYY-MM-DD)",
  "end_date": "종료일 (YYYY-MM-DD)",
  "estimated_cost": {{
    "books": 총_책_가격,
    "courses": 총_강의_비용,
    "equipment": 장비_비용,
    "total": 총_예상_금액
  }},
  "reviews_summary": "후기 요약 (2-3문단)",
  "steps": [
    {{
      "step_number": 1,
      "title": "단계 제목",
      "duration_days": 단계별_일수,
      "start_date": "시작일 (YYYY-MM-DD)",
      "end_date": "종료일 (YYYY-MM-DD)",
      "learning_content": ["학습 내용 1", "학습 내용 2"],
      "recommended_books": [
        {{"title": "책 제목", "price": 책_가격, "reason": "추천 이유"}}
      ],
      "recommended_sites": [
        {{"name": "사이트명", "url": "URL", "type": "유튜브/블로그/깃허브"}}
      ],
      "todos": ["투두 1", "투두 2", "투두 3"],
      "estimated_cost": 단계별_예상_비용
    }}
  ]
}}

중요: 
- JSON 형식만 출력하고, 추가 설명은 하지 마.
- Tavily 검색을 활용하여 최신 정보와 가격 정보를 수집해.
- 각 단계의 날짜는 연속적으로 계산해 (이전 단계 종료일 다음날이 다음 단계 시작일).
"""

    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])


def create_category_agent(category_name: str, category_guidelines: str) -> AgentExecutor:
    """카테고리별 Agent 생성"""
    llm = get_base_llm()
    tools = [get_tavily_tool()]
    prompt = create_category_prompt(category_name, category_guidelines)
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
    
    return agent_executor


# 1. Academic / STEM Agent
ACADEMIC_GUIDELINES = """
학술·STEM 분야 학습 가이드:
- 교재 기반 학습 중심
- 개념 이해 → 문제 풀이 순서
- 수학, 과학, 물리, 화학, 생명과학, 사회과학, 언어학습 등
- 단계별로 이론 학습 후 실습/문제 풀이 구성
"""

def create_academic_guide(topic: str, start_date: str = None) -> Dict[str, Any]:
    """Academic/STEM 학습 가이드 생성"""
    if start_date is None:
        start_date = datetime.now().strftime('%Y-%m-%d')
    
    agent = create_category_agent("Academic / STEM", ACADEMIC_GUIDELINES)
    
    query = f"'{topic}'를 배우고 싶어. {ACADEMIC_GUIDELINES} 단계별 학습 계획을 만들어줘. 오늘은 {start_date}야."
    
    result = agent.invoke({"input": query})
    return {"raw_output": result["output"], "category": "Academic / STEM"}


# 2. Career / Tech Skills Agent
CAREER_TECH_GUIDELINES = """
커리어·기술 스킬 학습 가이드:
- 프로젝트 기반 학습 중심
- 포트폴리오 구축 필요
- 코딩, 데이터 분석, AI, 웹 개발, 보안, 디자인, PM, 비즈니스 스킬 등
- 각 단계마다 실전 프로젝트 포함
- 깃허브 레포지토리 추천 필수 (코딩 관련)
"""

def create_career_tech_guide(topic: str, start_date: str = None) -> Dict[str, Any]:
    """Career/Tech Skills 학습 가이드 생성"""
    if start_date is None:
        start_date = datetime.now().strftime('%Y-%m-%d')
    
    agent = create_category_agent("Career / Tech Skills", CAREER_TECH_GUIDELINES)
    
    query = f"'{topic}'를 배우고 싶어. {CAREER_TECH_GUIDELINES} 단계별 학습 계획을 만들어줘. 오늘은 {start_date}야."
    
    result = agent.invoke({"input": query})
    return {"raw_output": result["output"], "category": "Career / Tech Skills"}


# 3. Sports / Physical Skills Agent
SPORTS_GUIDELINES = """
스포츠·신체 기술 학습 가이드:
- 기술 단계별 훈련 중심
- 장비 비용 포함 필수
- 영상 분석 및 실제 연습 병행
- 축구, 농구, 야구, 골프, 헬스, 달리기, 요가 등
- 각 단계마다 구체적인 훈련 방법과 영상 자료 추천
"""

def create_sports_guide(topic: str, start_date: str = None) -> Dict[str, Any]:
    """Sports/Physical Skills 학습 가이드 생성"""
    if start_date is None:
        start_date = datetime.now().strftime('%Y-%m-%d')
    
    agent = create_category_agent("Sports / Physical Skills", SPORTS_GUIDELINES)
    
    query = f"'{topic}'를 배우고 싶어. {SPORTS_GUIDELINES} 단계별 학습 계획을 만들어줘. 오늘은 {start_date}야."
    
    result = agent.invoke({"input": query})
    return {"raw_output": result["output"], "category": "Sports / Physical Skills"}


# 4. Arts / Creative Agent
ARTS_GUIDELINES = """
예술·창작 학습 가이드:
- 실습 기반 학습 중심
- 창작물 생성 필수
- 레퍼런스 및 작품 분석 포함
- 춤, 음악, 그림, 사진, 영상편집, 작곡, 연기 등
- 각 단계마다 완성할 작품 목표 설정
"""

def create_arts_guide(topic: str, start_date: str = None) -> Dict[str, Any]:
    """Arts/Creative 학습 가이드 생성"""
    if start_date is None:
        start_date = datetime.now().strftime('%Y-%m-%d')
    
    agent = create_category_agent("Arts / Creative", ARTS_GUIDELINES)
    
    query = f"'{topic}'를 배우고 싶어. {ARTS_GUIDELINES} 단계별 학습 계획을 만들어줘. 오늘은 {start_date}야."
    
    result = agent.invoke({"input": query})
    return {"raw_output": result["output"], "category": "Arts / Creative"}


# 5. Lifestyle / Hobby Agent
LIFESTYLE_GUIDELINES = """
취미·생활 학습 가이드:
- 루틴 관리 중심
- 가벼운 실천 중심
- 요리, 여행 준비, 생산성, 글쓰기, 정리, 원예 등
- 각 단계를 일상 생활에 쉽게 접목할 수 있도록 구성
- 실용적인 팁과 트릭 포함
"""

def create_lifestyle_guide(topic: str, start_date: str = None) -> Dict[str, Any]:
    """Lifestyle/Hobby 학습 가이드 생성"""
    if start_date is None:
        start_date = datetime.now().strftime('%Y-%m-%d')
    
    agent = create_category_agent("Lifestyle / Hobby", LIFESTYLE_GUIDELINES)
    
    query = f"'{topic}'를 배우고 싶어. {LIFESTYLE_GUIDELINES} 단계별 학습 계획을 만들어줘. 오늘은 {start_date}야."
    
    result = agent.invoke({"input": query})
    return {"raw_output": result["output"], "category": "Lifestyle / Hobby"}

