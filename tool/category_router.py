"""
학습 주제를 카테고리로 분류하는 Router Agent

사용자 입력을 받아 5가지 카테고리 중 하나로 분류하고 해당 카테고리 Agent로 라우팅
"""

import os
from typing import Dict, Any, Callable
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from .category_agents import (
    create_academic_guide,
    create_career_tech_guide,
    create_sports_guide,
    create_arts_guide,
    create_lifestyle_guide
)

# 카테고리 정의
CATEGORIES = {
    "Academic / STEM": {
        "keywords": ["수학", "과학", "물리", "화학", "생명", "사회과학", "언어학습", "학술", "이론", "교재"],
        "description": "학술·STEM (수학, 과학, 물리, 화학, 생명, 사회과학, 언어학습)",
        "function": create_academic_guide
    },
    "Career / Tech Skills": {
        "keywords": ["코딩", "프로그래밍", "데이터", "분석", "AI", "머신러닝", "웹", "개발", "보안", "디자인", "PM", "비즈니스", "기술"],
        "description": "커리어·기술 (코딩, 데이터 분석, AI, 웹 개발, 보안, 디자인, PM, 비즈니스 스킬)",
        "function": create_career_tech_guide
    },
    "Sports / Physical Skills": {
        "keywords": ["축구", "농구", "야구", "골프", "헬스", "달리기", "요가", "운동", "스포츠", "체육"],
        "description": "스포츠·신체 기술 (축구, 농구, 야구, 골프, 헬스, 달리기, 요가 등)",
        "function": create_sports_guide
    },
    "Arts / Creative": {
        "keywords": ["춤", "음악", "그림", "사진", "영상", "편집", "작곡", "연기", "예술", "창작", "디자인"],
        "description": "예술·창작 (춤, 음악, 그림, 사진, 영상편집, 작곡, 연기 등)",
        "function": create_arts_guide
    },
    "Lifestyle / Hobby": {
        "keywords": ["요리", "여행", "생산성", "글쓰기", "정리", "원예", "취미", "생활", "뜨개질", "리듬게임", "주식"],
        "description": "취미·생활 (요리, 여행 준비, 생산성, 글쓰기, 정리, 원예 등)",
        "function": create_lifestyle_guide
    }
}


def classify_category(topic: str) -> str:
    """
    주제를 카테고리로 분류
    
    Args:
        topic: 학습 주제
    
    Returns:
        분류된 카테고리명
    """
    topic_lower = topic.lower()
    
    # 키워드 기반 간단한 분류
    category_scores = {}
    for category, info in CATEGORIES.items():
        score = sum(1 for keyword in info["keywords"] if keyword in topic_lower)
        if score > 0:
            category_scores[category] = score
    
    if category_scores:
        # 가장 높은 점수의 카테고리 반환
        return max(category_scores.items(), key=lambda x: x[1])[0]
    
    # LLM을 사용한 분류 (키워드 매칭 실패 시)
    return classify_with_llm(topic)


def classify_with_llm(topic: str) -> str:
    """LLM을 사용하여 카테고리 분류"""
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
    
    categories_description = "\n".join([
        f"- {cat}: {info['description']}" 
        for cat, info in CATEGORIES.items()
    ])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""너는 학습 주제를 카테고리로 분류하는 전문가야.

다음 5가지 카테고리 중 하나를 선택해야 해:
{categories_description}

사용자의 학습 주제를 분석하여 가장 적합한 카테고리명만 출력해.
카테고리명은 반드시 위의 5가지 중 정확히 하나여야 해."""),
        ("human", f"학습 주제: {topic}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({})
    category = result.content.strip()
    
    # 결과가 유효한 카테고리인지 확인
    if category in CATEGORIES:
        return category
    
    # 기본값: Lifestyle / Hobby
    return "Lifestyle / Hobby"


def route_to_category_agent(topic: str, start_date: str = None) -> Dict[str, Any]:
    """
    주제를 카테고리로 분류하고 해당 Agent로 라우팅
    
    Args:
        topic: 학습 주제
        start_date: 시작 날짜 (YYYY-MM-DD 형식, None이면 오늘)
    
    Returns:
        학습 가이드 결과 (raw_output, category 포함)
    """
    # 카테고리 분류
    category = classify_category(topic)
    print(f"📌 분류된 카테고리: {category}")
    
    # 해당 카테고리의 Agent 함수 호출
    agent_function = CATEGORIES[category]["function"]
    result = agent_function(topic, start_date)
    
    return result


# 카테고리별 Agent 함수들을 export
__all__ = [
    "classify_category",
    "route_to_category_agent",
    "CATEGORIES"
]

