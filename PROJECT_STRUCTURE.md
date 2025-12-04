# 프로젝트 구조 상세 설명

## 전체 구조

```
hateslop_hackathon/
│
├── 📄 main.py                    # 메인 실행 스크립트
├── 📄 example_usage.py           # 사용 예시 코드
├── 📄 requirements.txt           # 패키지 의존성
├── 📄 README.md                  # 프로젝트 설명
├── 📄 COLLABORATION.md           # 협업 가이드
├── 📄 PROJECT_STRUCTURE.md       # 프로젝트 구조 설명 (현재 파일)
├── 📄 .gitignore                 # Git ignore 파일
├── 📄 .env                       # 환경 변수 (API 키) - Git에 포함 안됨
│
├── 📁 tool/                      # Agent 함수들
│   ├── __init__.py
│   ├── category_agents.py        # 5가지 카테고리별 Agent 함수
│   └── category_router.py        # 카테고리 분류 및 라우팅
│
├── 📁 utils/                     # 유틸리티 함수들
│   ├── __init__.py
│   ├── json_parser.py            # JSON 파싱 유틸리티
│   └── word_generator.py         # Word 문서 생성 유틸리티
│
└── 📁 [팀원1]/                   # 팀원 1 작업 폴더 (각자 생성)
└── 📁 [팀원2]/                   # 팀원 2 작업 폴더 (각자 생성)
```

## 파일별 상세 설명

### 루트 디렉터리

#### `main.py`
- 메인 실행 스크립트
- 사용자 입력을 받아 학습 가이드를 생성하는 전체 프로세스를 실행
- 환경 변수 로드, 카테고리 분류, Word 파일 생성까지 전체 파이프라인 관리

#### `example_usage.py`
- 다양한 주제로 학습 가이드를 생성하는 예시 코드
- 5가지 카테고리별 예시 함수 포함
- 테스트 및 데모용

#### `requirements.txt`
- 프로젝트에 필요한 Python 패키지 목록
- `pip install -r requirements.txt`로 설치

#### `.env`
- API 키를 저장하는 환경 변수 파일
- `.gitignore`에 포함되어 Git에 업로드되지 않음
- 형식:
  ```
  TAVILY_API_KEY=your_key_here
  OPENAI_API_KEY=your_key_here
  ```

### `tool/` 디렉터리

#### `tool/category_agents.py`
5가지 카테고리별 Agent 함수들이 정의된 파일:

- `create_academic_guide()`: Academic/STEM 카테고리
- `create_career_tech_guide()`: Career/Tech Skills 카테고리
- `create_sports_guide()`: Sports/Physical Skills 카테고리
- `create_arts_guide()`: Arts/Creative 카테고리
- `create_lifestyle_guide()`: Lifestyle/Hobby 카테고리

각 함수는:
- 해당 카테고리에 최적화된 프롬프트 생성
- Tavily Tool을 사용하여 최신 정보 검색
- LangChain Agent를 통해 학습 가이드 생성

#### `tool/category_router.py`
학습 주제를 카테고리로 분류하고 해당 Agent로 라우팅:

- `classify_category()`: 키워드 기반 또는 LLM 기반 카테고리 분류
- `route_to_category_agent()`: 분류된 카테고리에 맞는 Agent 함수 호출
- `CATEGORIES`: 5가지 카테고리 정의 딕셔너리

### `utils/` 디렉터리

#### `utils/json_parser.py`
LLM 출력에서 JSON을 추출하고 파싱:

- `extract_json_from_text()`: 텍스트에서 JSON 추출
- `clean_json_string()`: JSON 문자열 정리 (주석 제거 등)
- `parse_learning_guide()`: 학습 가이드 출력을 구조화된 딕셔너리로 변환

#### `utils/word_generator.py`
파싱된 학습 가이드를 Word 문서로 변환:

- `save_learning_guide_to_word()`: 학습 가이드를 Word 파일로 저장
- `set_document_style()`: 문서 스타일 설정
- 단계별 계획, 투두리스트, 비용, 후기 등을 포함한 완전한 문서 생성

## 데이터 흐름

```
사용자 입력 (학습 주제)
    ↓
main.py: create_learning_guide()
    ↓
category_router.py: route_to_category_agent()
    ↓
category_router.py: classify_category()  [카테고리 분류]
    ↓
category_agents.py: [해당 카테고리 Agent 함수]
    ↓
[Tavily 검색] → [OpenAI LLM] → [JSON 형식 출력]
    ↓
json_parser.py: parse_learning_guide()  [JSON 파싱]
    ↓
word_generator.py: save_learning_guide_to_word()  [Word 파일 생성]
    ↓
결과: .docx 파일
```

## 확장 포인트

### 새로운 카테고리 추가
1. `tool/category_agents.py`에 새로운 Agent 함수 추가
2. `tool/category_router.py`의 `CATEGORIES` 딕셔너리에 추가
3. 가이드라인 작성

### 새로운 기능 추가
- `utils/` 디렉터리에 새로운 유틸리티 모듈 추가
- `tool/` 디렉터리에 새로운 Agent 도구 추가

### Word 문서 스타일 개선
- `utils/word_generator.py`의 `set_document_style()` 함수 수정
- 폰트, 색상, 레이아웃 등 커스터마이징

## 협업 시 주의사항

1. **공통 파일 수정 전 반드시 논의**
   - `tool/`, `utils/` 디렉터리 파일은 공유 자산
   - 수정 전 Pull Request 생성

2. **개인 작업은 각자 폴더에서**
   - `[팀원1]/`, `[팀원2]/` 폴더에서 실험 및 테스트
   - 안정화된 코드만 공통 디렉터리로 이동

3. **환경 변수 공유하지 않기**
   - `.env` 파일은 `.gitignore`에 포함되어 있음
   - API 키는 개별적으로 관리

## 참고

- [README.md](./README.md): 프로젝트 전체 설명
- [COLLABORATION.md](./COLLABORATION.md): 협업 가이드

