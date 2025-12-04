# 협업 가이드

2명 팀을 위한 협업 가이드입니다.

## 프로젝트 구조

```
hateslop_hackathon/
├── main.py                    # 메인 실행 스크립트 (공통)
├── requirements.txt           # 패키지 의존성 (공통)
├── README.md                  # 프로젝트 설명 (공통)
├── COLLABORATION.md           # 협업 가이드 (현재 파일)
│
├── tool/                      # Agent 함수들 (공통)
│   ├── __init__.py
│   ├── category_agents.py     # 5가지 카테고리별 Agent
│   └── category_router.py     # 카테고리 분류 및 라우팅
│
├── utils/                     # 유틸리티 함수들 (공통)
│   ├── __init__.py
│   ├── json_parser.py         # JSON 파싱
│   └── word_generator.py      # Word 파일 생성
│
├── [팀원1]/                   # 팀원 1 개인 작업 폴더
│   ├── experiments/           # 실험 코드
│   ├── tests/                 # 테스트 코드
│   └── notes.md               # 작업 노트
│
└── [팀원2]/                   # 팀원 2 개인 작업 폴더
    ├── experiments/
    ├── tests/
    └── notes.md
```

## 작업 분담 제안

### 팀원 1
- **카테고리 Agent 개선**: 5가지 카테고리별 프롬프트 최적화
- **Word 문서 스타일링**: 문서 디자인 및 레이아웃 개선
- **비용 계산 로직**: 책 가격 크롤링/검색 자동화

### 팀원 2
- **카테고리 라우팅 개선**: 더 정확한 주제 분류
- **후기 수집 기능**: Tavily를 활용한 후기 검색 및 요약 개선
- **테스트 코드 작성**: 각 함수별 단위 테스트

## Git 워크플로우

### 1. 브랜치 전략

```bash
# 메인 브랜치
main                    # 안정된 버전

# 기능 브랜치 (각자 작업)
feature/category-improvement   # 팀원 1
feature/routing-improvement    # 팀원 2
```

### 2. 커밋 메시지 컨벤션

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 추가
chore: 빌드 설정 등

예시:
feat: Academic 카테고리 Agent 프롬프트 개선
fix: JSON 파싱 오류 수정
docs: README에 설치 방법 추가
```

### 3. 작업 흐름

```bash
# 1. 최신 코드 가져오기
git checkout main
git pull origin main

# 2. 기능 브랜치 생성
git checkout -b feature/my-feature

# 3. 작업 및 커밋
# ... 작업 ...
git add .
git commit -m "feat: 설명"

# 4. Push
git push origin feature/my-feature

# 5. Pull Request 생성
# GitHub에서 Pull Request 생성
```

## 코드 리뷰 가이드

### 리뷰 체크리스트

- [ ] 코드가 요구사항을 만족하는가?
- [ ] 테스트가 통과하는가?
- [ ] 코드 스타일이 일관성 있는가?
- [ ] 주석이 충분한가?
- [ ] 에러 처리가 적절한가?

### 리뷰 코멘트 예시

```
✅ 좋은 코드
❌ 개선 필요
💡 제안
⚠️ 주의
```

## 일정 관리

### 1주차: 기본 구조 완성
- [x] 프로젝트 기본 틀 생성
- [ ] 각자 담당 기능 확인

### 2주차: 기능 개발
- [ ] 팀원 1: 카테고리 Agent 개선
- [ ] 팀원 2: 라우팅 및 후기 기능 개선

### 3주차: 통합 및 테스트
- [ ] 코드 통합
- [ ] 전체 테스트
- [ ] 문서 작성

## 커뮤니케이션

### 회의 시간
- 매주 월요일 오후 2시: 주간 계획
- 매주 금요일 오후 6시: 주간 회고

### 소통 채널
- GitHub Issues: 버그 및 기능 요청
- GitHub Discussions: 기술 논의
- Pull Requests: 코드 리뷰

## 문제 해결

### 충돌 발생 시

```bash
# 1. 최신 코드 가져오기
git fetch origin
git checkout main
git pull origin main

# 2. 브랜치에 머지
git checkout feature/my-feature
git merge main

# 3. 충돌 해결
# ... 충돌 파일 수정 ...
git add .
git commit -m "fix: merge conflict 해결"
```

### 코드 리뷰 의견이 다를 때

1. 각자 근거 제시
2. 테스트 결과 공유
3. 팀원과 논의 후 결정

## 참고 자료

- [Git 브랜치 전략](https://nvie.com/posts/a-successful-git-branching-model/)
- [커밋 메시지 컨벤션](https://www.conventionalcommits.org/)
- [Python 코딩 스타일 (PEP 8)](https://pep8.org/)

