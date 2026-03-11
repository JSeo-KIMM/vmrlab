# 연구개발계획서 작성 Claude Code 플러그인

구어체 초안 마크다운 → 정부 제출용 연구개발계획서 자동 변환 플러그인

---

## 설치 방법

### 방법 1: 글로벌 설치 (모든 프로젝트에서 사용)

```bash
# 플러그인 디렉토리를 ~/.claude/plugins/에 복사
cp -r research-plan-plugin ~/.claude/plugins/

# Claude Code에서 플러그인 활성화
/plugin install ~/.claude/plugins/research-plan-plugin
```

### 방법 2: 프로젝트별 설치

```bash
# 프로젝트 루트에 복사
cp -r research-plan-plugin /your/project/.claude/plugins/

# Claude Code에서
/plugin install .claude/plugins/research-plan-plugin
```

### 방법 3: 수동 설치 (에이전트만)

에이전트 파일만 사용하려면:
```bash
# 글로벌 에이전트로 설치
cp agents/research-plan-pro.md ~/.claude/agents/

# 또는 프로젝트 에이전트로 설치
cp agents/research-plan-pro.md .claude/agents/
```

---

## 사용법

### 슬래시 커맨드

```
# 구어체 초안 → 전체 연구계획서 (세부목표 + 연차별 내용)
/research-plan-pro:research-plan ./내_초안.md

# 연구기간 지정 (기본: 3년)
/research-plan-pro:research-plan ./초안.md --years=4

# 세부목표만 작성 (연차별 내용 제외)
/research-plan-pro:research-plan ./초안.md --objectives-only

# 기존 세부목표 파일로 연차별 내용만 작성
/research-plan-pro:annual-plan ./세부목표_정제.md
```

### 자연어로 에이전트 직접 호출

```
# Claude Code 채팅창에서
"research-plan-pro 에이전트로 ./draft.md 파일을 연구계획서로 작성해줘"

"초안 파일 draft.md를 읽어서 4년 과제 기준으로 세부목표랑 연차별 연구내용 만들어줘"
```

---

## 초안 파일 작성 가이드

구어체로 자유롭게 작성하세요. 형식은 중요하지 않습니다.

### 권장 포함 내용

```markdown
# 내 연구 아이디어

## 전체적으로 뭘 하고 싶냐면
(자유롭게 설명)

## 세부적으로는 이런 걸 개발하고 싶어
- 이런 거
- 저런 거
- 요런 것도

## 기간이나 규모
- 몇 년짜리인지
- 어느 기관에서 하는지 (옵션)

## 기타 메모
(아무거나)
```

### 예시 초안 파일

`example-draft.md` 파일을 참고하세요.

---

## 출력 파일

| 파일명 | 내용 |
|--------|------|
| `[원본]_세부목표_정제.md` | 전체 연구목표 + 세부 개발목표 |
| `[원본]_연구계획서_초안.md` | 세부목표 + 연차별 연구내용 전체 |
| `[원본]_연차별연구내용.md` | 연차별 연구내용만 (`/annual-plan` 사용 시) |

---

## 플러그인 구조

```
research-plan-plugin/
├── .claude-plugin/
│   └── plugin.json          # 플러그인 매니페스트
├── agents/
│   └── research-plan-pro.md  # 핵심 서브에이전트
├── commands/
│   ├── research-plan.md     # /research-plan 슬래시 커맨드
│   └── annual-plan.md       # /annual-plan 슬래시 커맨드
├── example-draft.md         # 초안 예시 파일
└── README.md                # 이 파일
```

---

## 문의 / 커스터마이징

`agents/research-plan-pro.md`의 시스템 프롬프트를 수정하여 다음을 변경할 수 있습니다:
- 특정 부처/기관 형식에 맞춘 문체 및 구조
- 세부목표 개수 기본값
- 출력 파일명 규칙
- 연차별 구성 원칙
