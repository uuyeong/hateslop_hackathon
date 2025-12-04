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
from langchain import hub


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


def create_category_agent(category_name: str, category_guidelines: str) -> AgentExecutor:
    """카테고리별 Agent 생성"""
    llm = get_base_llm()
    tools = [get_tavily_tool()]
    
    # LangChain hub에서 기본 프롬프트 가져오기
    base_prompt = hub.pull("hwchase17/openai-functions-agent")
    
    # 시스템 메시지만 커스터마이징 - JSON 형식 설명을 단순화
    system_message = f"""너는 {category_name} 전문 교육 설계자야.

{category_guidelines}

사용자가 배우고 싶은 주제에 대해 단계별 학습 가이드를 작성해. Tavily 검색을 활용하여 최신 정보, 교재, 강의, 후기를 수집해.

출력 형식:
반드시 JSON 형식으로 출력해야 해. 다음 구조를 따라야 해:

1. topic: 학습 주제명
2. category: {category_name}
3. total_duration_days: 총 학습 일수 (숫자)
4. start_date: 시작일 (YYYY-MM-DD 형식)
5. end_date: 종료일 (YYYY-MM-DD 형식)
6. estimated_cost: 비용 정보 (books, courses, equipment, total 키 포함)
7. reviews_summary: 학습자 후기 요약 (2-3문단)
8. steps: 단계 배열, 각 단계는 step_number, title, duration_days, start_date, end_date, learning_content, recommended_books, recommended_sites, todos, estimated_cost 포함

각 단계는 3~6단계로 구성하고, 날짜는 연속적으로 계산해.

중요: JSON 형식만 출력하고, 추가 설명이나 텍스트는 포함하지 마."""
    
    # 기본 프롬프트의 메시지 구조를 가져와서 시스템 메시지만 교체
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
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
    
    try:
        agent = create_category_agent("Academic / STEM", ACADEMIC_GUIDELINES)
        
        query = f"'{topic}'를 배우고 싶어. 단계별 학습 가이드를 만들어줘. 시작 날짜는 {start_date}야. Tavily 검색을 사용해서 최신 교재, 강의, 후기 정보를 수집해."
        
        result = agent.invoke({"input": query})
        output = result.get("output", "")
        if not output:
            return {
                "error": "Agent가 출력을 생성하지 못했습니다.",
                "category": "Academic / STEM",
                "raw_output": ""
            }
        return {"raw_output": output, "category": "Academic / STEM"}
    except Exception as e:
        return {
            "error": f"Agent 실행 중 오류 발생: {str(e)}",
            "category": "Academic / STEM",
            "raw_output": ""
        }


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
    
    try:
        agent = create_category_agent("Career / Tech Skills", CAREER_TECH_GUIDELINES)
        
        query = f"'{topic}'를 배우고 싶어. 단계별 학습 가이드를 만들어줘. 시작 날짜는 {start_date}야. Tavily 검색을 사용해서 최신 교재, 강의, 후기 정보를 수집해."
        
        result = agent.invoke({"input": query})
        output = result.get("output", "")
        if not output:
            return {
                "error": "Agent가 출력을 생성하지 못했습니다.",
                "category": "Career / Tech Skills",
                "raw_output": ""
            }
        return {"raw_output": output, "category": "Career / Tech Skills"}
    except Exception as e:
        return {
            "error": f"Agent 실행 중 오류 발생: {str(e)}",
            "category": "Career / Tech Skills",
            "raw_output": ""
        }


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
    
    try:
        agent = create_category_agent("Sports / Physical Skills", SPORTS_GUIDELINES)
        
        query = f"'{topic}'를 배우고 싶어. 단계별 학습 가이드를 만들어줘. 시작 날짜는 {start_date}야. Tavily 검색을 사용해서 최신 교재, 강의, 후기 정보를 수집해."
        
        result = agent.invoke({"input": query})
        output = result.get("output", "")
        if not output:
            return {
                "error": "Agent가 출력을 생성하지 못했습니다.",
                "category": "Sports / Physical Skills",
                "raw_output": ""
            }
        return {"raw_output": output, "category": "Sports / Physical Skills"}
    except Exception as e:
        return {
            "error": f"Agent 실행 중 오류 발생: {str(e)}",
            "category": "Sports / Physical Skills",
            "raw_output": ""
        }


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
    
    try:
        agent = create_category_agent("Arts / Creative", ARTS_GUIDELINES)
        
        query = f"'{topic}'를 배우고 싶어. 단계별 학습 가이드를 만들어줘. 시작 날짜는 {start_date}야. Tavily 검색을 사용해서 최신 교재, 강의, 후기 정보를 수집해."
        
        result = agent.invoke({"input": query})
        output = result.get("output", "")
        if not output:
            return {
                "error": "Agent가 출력을 생성하지 못했습니다.",
                "category": "Arts / Creative",
                "raw_output": ""
            }
        return {"raw_output": output, "category": "Arts / Creative"}
    except Exception as e:
        return {
            "error": f"Agent 실행 중 오류 발생: {str(e)}",
            "category": "Arts / Creative",
            "raw_output": ""
        }


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
    
    try:
        agent = create_category_agent("Lifestyle / Hobby", LIFESTYLE_GUIDELINES)
        
        query = f"'{topic}'를 배우고 싶어. 단계별 학습 가이드를 만들어줘. 시작 날짜는 {start_date}야. Tavily 검색을 사용해서 최신 교재, 강의, 후기 정보를 수집해."
        
        result = agent.invoke({"input": query})
        output = result.get("output", "")
        if not output:
            return {
                "error": "Agent가 출력을 생성하지 못했습니다.",
                "category": "Lifestyle / Hobby",
                "raw_output": ""
            }
        return {"raw_output": output, "category": "Lifestyle / Hobby"}
    except Exception as e:
        return {
            "error": f"Agent 실행 중 오류 발생: {str(e)}",
            "category": "Lifestyle / Hobby",
            "raw_output": ""
        }

