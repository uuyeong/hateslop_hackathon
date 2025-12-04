# 학습 가이드 Agent 🎓

사용자가 배우고 싶은 주제를 입력하면 단계별 학습 계획을 자동으로 생성하는 AI Agent입니다.

## 주요 기능

- **카테고리별 맞춤 학습 가이드**: 5가지 카테고리에 따라 최적화된 학습 계획 생성
- **단계별 계획**: 3~6단계로 구성된 체계적인 학습 로드맵
- **날짜 자동 배분**: 각 단계별 시작일과 종료일 자동 계산
- **투두리스트**: 각 단계마다 체크 가능한 구체적인 할 일 목록
- **자료 추천**: 교재, 유튜브, 블로그, 깃허브 등 최신 자료 추천
- **비용 계산**: 예상 비용(교재, 강의, 장비 등) 자동 계산
- **후기 요약**: 해당 주제를 학습한 사람들의 후기 정리
- **Word 문서 생성**: 결과를 Word 파일로 자동 저장

## 5가지 카테고리

### 🔴 1. Academic / STEM (학술·STEM)
수학, 과학, 물리, 화학, 생명과학, 사회과학, 언어학습 등
- 교재 기반 학습 중심
- 개념 이해 → 문제 풀이 순서

### 🟠 2. Career / Tech Skills (커리어·기술)
코딩, 데이터 분석, AI, 웹 개발, 보안, 디자인, PM, 비즈니스 스킬 등
- 프로젝트 기반 학습 중심
- 포트폴리오 구축 필요

### 🟢 3. Sports / Physical Skills (스포츠·신체 기술)
축구, 농구, 야구, 골프, 헬스, 달리기, 요가 등
- 기술 단계별 훈련 중심
- 장비 비용 포함

### 🟣 4. Arts / Creative (예술·창작)
춤, 음악, 그림, 사진, 영상편집, 작곡, 연기 등
- 실습 기반 학습 중심
- 창작물 생성 필수

### 🟡 5. Lifestyle / Hobby (취미·생활)
요리, 여행 준비, 생산성, 글쓰기, 정리, 원예, 뜨개질, 주식 등
- 루틴 관리 중심
- 가벼운 실천 중심

## 프로젝트 구조

```
hateslop_hackathon/
├── main.py                    # 메인 실행 스크립트
├── requirements.txt           # 패키지 의존성
├── README.md                  # 프로젝트 설명
├── .gitignore                 # Git ignore 파일
├── .env                       # 환경 변수 (API 키)
│
├── tool/                      # Agent 함수들
│   ├── __init__.py
│   ├── category_agents.py     # 5가지 카테고리별 Agent
│   └── category_router.py     # 카테고리 분류 및 라우팅
│
├── utils/                     # 유틸리티 함수들
│   ├── __init__.py
│   ├── json_parser.py         # JSON 파싱
│   └── word_generator.py      # Word 파일 생성
│
└── [팀원1]/                   # 팀원 1 작업 폴더
└── [팀원2]/                   # 팀원 2 작업 폴더
```

## 설치 방법

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 API 키를 설정하세요:

```env
TAVILY_API_KEY=your_tavily_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 실행

```bash
python main.py
```

## 사용 예시

### 커맨드라인 실행

```bash
python main.py
```

프롬프트에 따라:
1. 학습 주제 입력 (예: "머신러닝", "축구", "뜨개질")
2. 시작 날짜 입력 (선택사항, 엔터 시 오늘)
3. 자동으로 카테고리 분류 및 학습 가이드 생성
4. Word 파일로 결과 저장

### Python 스크립트에서 사용

```python
from main import create_learning_guide
from utils.word_generator import save_learning_guide_to_word

# 학습 가이드 생성
guide = create_learning_guide("머신러닝", start_date="2025-12-05")

# Word 파일로 저장
if "error" not in guide:
    save_learning_guide_to_word(guide)
```

## 기술 스택

- **LangChain**: Agent 프레임워크
- **OpenAI GPT-4 Turbo**: LLM
- **Tavily**: 최신 정보 검색
- **python-docx**: Word 문서 생성

## 사용된 학습 내용 (hw1~hw11)

- **hw3**: 프롬프트 엔지니어링 (Role Prompting, Few-shot, CoT)
- **hw11**: LangChain Agent + Tavily Tool 활용
- **hw2**: 데이터 크롤링 패턴 (참고)
- **hw5**: 문서 생성 패턴 (참고)

## 협업 가이드

### 팀원 폴더 생성

각 팀원은 자신의 이름/닉네임으로 폴더를 생성하여 작업하세요:

```bash
mkdir 팀원1
mkdir 팀원2
```

### 개발 워크플로우

1. 기능별로 브랜치 생성
2. 각자의 폴더에서 작업 및 테스트
3. `tool/` 또는 `utils/` 폴더에 공통 기능 추가
4. Pull Request 생성

### 코드 컨벤션

- 함수명: `snake_case`
- 클래스명: `PascalCase`
- 상수: `UPPER_CASE`
- 주석: 한국어 또는 영어

## 주요 파일 설명

### `tool/category_agents.py`
5가지 카테고리별 Agent 함수 구현
- 각 카테고리마다 최적화된 프롬프트와 가이드라인

### `tool/category_router.py`
학습 주제를 카테고리로 자동 분류하고 해당 Agent로 라우팅

### `utils/json_parser.py`
LLM 출력에서 JSON을 추출하고 파싱

### `utils/word_generator.py`
파싱된 학습 가이드를 Word 문서로 변환

### `main.py`
메인 실행 스크립트 - 사용자 입력 받아 전체 프로세스 실행

## 향후 개선 사항

- [ ] RAG를 활용한 학습 자료 캐싱
- [ ] 진행 상황 추적 기능
- [ ] 학습 일정 캘린더 생성
- [ ] 여러 주제 동시 학습 지원

## 라이선스

MIT License

## 작성자

헤이트슬롭 3기 미니 해커톤 팀
