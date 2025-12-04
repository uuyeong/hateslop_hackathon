# 설치 및 시작 가이드

## 빠른 시작

### 1단계: 환경 설정

#### Python 버전 확인
```bash
python --version  # Python 3.9 이상 필요
```

#### 가상 환경 생성 (선택사항, 권장)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2단계: 패키지 설치

```bash
pip install -r requirements.txt
```

필요한 패키지:
- `langchain`: Agent 프레임워크
- `langchain-openai`: OpenAI 통합
- `langchain-community`: 커뮤니티 도구 (Tavily 포함)
- `tavily-python`: Tavily 검색 API
- `python-dotenv`: 환경 변수 관리
- `python-docx`: Word 문서 생성
- `openai`: OpenAI API

### 3단계: API 키 설정

#### Tavily API 키 발급
1. [Tavily 웹사이트](https://tavily.com/) 방문
2. 회원가입 및 로그인
3. API 키 발급

#### OpenAI API 키 발급
1. [OpenAI Platform](https://platform.openai.com/) 방문
2. 계정 생성 및 로그인
3. API 키 생성

#### .env 파일 생성

프로젝트 루트 디렉터리에 `.env` 파일을 생성하고 아래 내용을 추가하세요:

```env
TAVILY_API_KEY=your_tavily_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

**중요**: `.env` 파일은 Git에 업로드되지 않습니다 (`.gitignore`에 포함됨)

### 4단계: 실행

#### 방법 1: 메인 스크립트 실행
```bash
python main.py
```

프롬프트에 따라:
1. 학습 주제 입력 (예: "머신러닝", "축구", "뜨개질")
2. 시작 날짜 입력 (선택사항, 엔터 시 오늘)
3. 자동으로 학습 가이드 생성 및 Word 파일 저장

#### 방법 2: Python 스크립트에서 사용
```python
from main import create_learning_guide
from utils.word_generator import save_learning_guide_to_word

# 학습 가이드 생성
guide = create_learning_guide("머신러닝", start_date="2025-12-05")

# Word 파일로 저장
if "error" not in guide:
    save_learning_guide_to_word(guide)
```

## 문제 해결

### 문제 1: 패키지 설치 오류

**증상**: `pip install -r requirements.txt` 실행 시 오류 발생

**해결 방법**:
```bash
# pip 업그레이드
pip install --upgrade pip

# 패키지 하나씩 설치
pip install langchain
pip install langchain-openai
pip install langchain-community
pip install tavily-python
pip install python-dotenv
pip install python-docx
pip install openai
```

### 문제 2: API 키 오류

**증상**: "TAVILY_API_KEY 환경변수가 설정되지 않았습니다" 오류

**해결 방법**:
1. `.env` 파일이 프로젝트 루트에 있는지 확인
2. `.env` 파일 내용이 올바른지 확인 (공백 없이)
3. 환경 변수가 올바르게 로드되는지 확인:
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   print(os.getenv("TAVILY_API_KEY"))  # None이면 환경 변수 로드 실패
   ```

### 문제 3: Import 오류

**증상**: `ModuleNotFoundError: No module named 'langchain'`

**해결 방법**:
1. 가상 환경이 활성화되어 있는지 확인
2. 패키지가 설치되어 있는지 확인:
   ```bash
   pip list | grep langchain
   ```
3. 재설치:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

### 문제 4: Word 파일 생성 오류

**증상**: Word 파일이 생성되지 않거나 오류 발생

**해결 방법**:
1. `python-docx` 패키지가 설치되어 있는지 확인
2. 파일 쓰기 권한 확인
3. 파일명에 특수문자가 없는지 확인

### 문제 5: JSON 파싱 오류

**증상**: "JSON 파싱 실패" 오류

**해결 방법**:
1. LLM 출력이 너무 긴 경우, 프롬프트를 수정하여 JSON 형식만 출력하도록 요청
2. `utils/json_parser.py`의 파싱 로직 개선
3. 원본 출력(`raw_output`) 확인하여 문제 파악

## 개발 환경 설정

### VS Code 설정 (선택사항)

`.vscode/settings.json` 생성:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

### 코드 포맷터 설정 (선택사항)

```bash
pip install black
black .
```

## 다음 단계

1. [README.md](./README.md) 읽기: 프로젝트 전체 개요
2. [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) 읽기: 프로젝트 구조 이해
3. [COLLABORATION.md](./COLLABORATION.md) 읽기: 협업 가이드 (팀 프로젝트인 경우)
4. `example_usage.py` 실행: 사용 예시 확인

## 추가 리소스

- [LangChain 문서](https://python.langchain.com/)
- [Tavily 문서](https://docs.tavily.com/)
- [OpenAI API 문서](https://platform.openai.com/docs)

