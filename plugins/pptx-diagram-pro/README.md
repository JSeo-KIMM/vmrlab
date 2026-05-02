# pptx-diagram-pro

연구 내용·프로세스·아이디어를 정부/공공기관 톤의 PPTX 다이어그램으로 변환하는 플러그인.

## 주요 기능

- **두 가지 입력**: 자연어 프롬프트 / 구조화 YAML·JSON
- **두 가지 렌더 모드**:
  - `native` — python-pptx 도형(편집 가능) — 기본
  - `image` — Gemini로 다이어그램 이미지 렌더링 후 PPTX 삽입
- **두 가지 다이어그램 유형**:
  - 프로세스/플로우차트 (start·process·decision·end + 화살표)
  - 시스템 아키텍처 (블록·연결·계층)
- **정부/공공기관 톤**: 차분한 4-mood 팔레트 + 한글 친화 타이포

## 사용법

대화 또는 슬래시 커맨드.

```
이 강화학습 학습 루프를 PPTX 다이어그램으로 그려줘
/pptx-diagram-pro:diagram "학습 루프: 환경 → 에이전트 → 보상 → 환경"
/pptx-diagram-pro:diagram ./architecture.yaml --mode=native --out=./out.pptx
/pptx-diagram-pro:diagram ./flow.md --mode=image
```

## 의존성

- Python 3.9+
- `pip install python-pptx` (필수)
- Gemini API 키 (`GEMINI_API_KEY` 환경변수, image 모드만)
