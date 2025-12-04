"""
가격 정보 추출 유틸리티

Tavily API를 사용해 학습 주제 및 카테고리에 맞는 대표 품목의 가격을 검색하고
평균 비용을 계산합니다.
"""

import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from tavily import TavilyClient


@dataclass
class PriceItem:
    name: str
    cost_type: str  # books, courses, equipment


PRICE_PATTERN = re.compile(
    r"(?P<value>\d{1,3}(?:[,\.\s]?\d{3})*(?:\.\d+)?)\s*(?P<unit>만원|만 원|원|KRW|달러|USD|$)",
    re.IGNORECASE,
)


def _get_tavily_client() -> Optional[TavilyClient]:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None
    return TavilyClient(api_key=api_key)


def _parse_price(text: str) -> Optional[Dict]:
    match = PRICE_PATTERN.search(text)
    if not match:
        return None
    raw_value = match.group("value").replace(",", "").replace(" ", "")
    try:
        value = float(raw_value)
    except ValueError:
        return None

    unit = match.group("unit")
    currency = "KRW"

    if unit in {"달러", "USD", "$"}:
        currency = "USD"
    elif "만" in unit:
        value *= 10000

    return {"value": int(round(value)), "currency": currency, "raw": match.group(0)}


def infer_price_items(topic: str, category: str) -> List[PriceItem]:
    topic_lower = topic.lower()

    if category == "Sports / Physical Skills":
        if "축구" in topic_lower:
            return [
                PriceItem("축구화", "equipment"),
                PriceItem("축구공", "equipment"),
                PriceItem("축구 레슨", "courses"),
            ]
        if "농구" in topic_lower:
            return [
                PriceItem("농구화", "equipment"),
                PriceItem("농구공", "equipment"),
                PriceItem("농구 레슨", "courses"),
            ]
        return [
            PriceItem(f"{topic} 장비", "equipment"),
            PriceItem(f"{topic} 보호장비", "equipment"),
            PriceItem(f"{topic} 레슨", "courses"),
        ]

    if category == "Academic / STEM":
        return [
            PriceItem(f"{topic} 대표 교재", "books"),
            PriceItem(f"{topic} 문제집", "books"),
            PriceItem(f"{topic} 온라인 강의", "courses"),
        ]

    if category == "Career / Tech Skills":
        return [
            PriceItem(f"{topic} 온라인 부트캠프", "courses"),
            PriceItem(f"{topic} 실습 교재", "books"),
            PriceItem(f"{topic} 개발 환경/툴", "equipment"),
        ]

    if category == "Arts / Creative":
        return [
            PriceItem(f"{topic} 재료 키트", "equipment"),
            PriceItem(f"{topic} 워크숍/강의", "courses"),
            PriceItem(f"{topic} 레퍼런스 서적", "books"),
        ]

    # Lifestyle / Hobby
    if "뜨개" in topic_lower:
        return [
            PriceItem("뜨개 실 세트", "equipment"),
            PriceItem("코바늘 세트", "equipment"),
            PriceItem("온라인 뜨개질 강의", "courses"),
        ]
    return [
        PriceItem(f"{topic} 기본 재료", "equipment"),
        PriceItem(f"{topic} 도구 세트", "equipment"),
        PriceItem(f"{topic} 온라인 강의", "courses"),
    ]


def get_average_price(item_name: str, num_results: int = 3) -> Optional[Dict]:
    client = _get_tavily_client()
    if client is None:
        return None

    response = client.search(
        query=f"{item_name} 가격",
        search_depth="basic",
        max_results=num_results,
    )

    prices: List[Dict[str, Any]] = []

    for result in response.get("results", []):
        text = f"{result.get('title', '')} {result.get('content', '')}"
        parsed = _parse_price(text)
        if parsed:
            prices.append(
                {
                    "value": parsed["value"],
                    "currency": parsed["currency"],
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "snippet": parsed["raw"],
                }
            )
        if len(prices) >= num_results:
            break

    if not prices:
        return None

    avg_price = int(round(sum(item["value"] for item in prices) / len(prices)))
    currency = prices[0]["currency"] if prices else "KRW"

    return {
        "name": item_name,
        "average_price": avg_price,
        "currency": currency,
        "sources": [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("snippet", ""),
            }
            for item in prices[:3]
        ],
    }


def enrich_estimated_cost(guide: Dict[str, Any]) -> Dict[str, Any]:
    """가이드에 Tavily 기반 실제 비용 정보를 주입"""
    topic = guide.get("topic", "")
    category = guide.get("category", "Lifestyle / Hobby")

    items = infer_price_items(topic, category)
    if not items:
        return guide

    cost_data = guide.get("estimated_cost") or {"books": 0, "courses": 0, "equipment": 0, "total": 0}
    breakdown = []

    for item in items:
        price_info = get_average_price(item.name)
        if not price_info:
            continue
        breakdown.append({**price_info, "type": item.cost_type})
        cost_data[item.cost_type] = cost_data.get(item.cost_type, 0) + price_info["average_price"]

    if not breakdown:
        guide["estimated_cost"] = cost_data
        return guide

    cost_data["total"] = cost_data.get("books", 0) + cost_data.get("courses", 0) + cost_data.get("equipment", 0)
    cost_data["breakdown"] = breakdown
    guide["estimated_cost"] = cost_data
    return guide


