---
description: |
  연구·프로세스·아이디어를 정부 톤 PPTX 다이어그램으로 만듭니다.
  플로우차트와 시스템 아키텍처 두 유형, native(편집 가능 도형) / image(Gemini 이미지) 두 모드를 지원합니다.

  사용법:
    /pptx-diagram-pro:diagram <자연어 또는 파일 경로>
    /pptx-diagram-pro:diagram <입력> --mode=native|image
    /pptx-diagram-pro:diagram <입력> --type=flowchart|architecture
    /pptx-diagram-pro:diagram <입력> --mood=technical-report|clarity|tech-focus|growth
    /pptx-diagram-pro:diagram <입력> --out=<경로.pptx>

  예시:
    /pptx-diagram-pro:diagram "강화학습 학습 루프: 환경→관측→에이전트→행동→보상→환경"
    /pptx-diagram-pro:diagram ./architecture.yaml --mode=native --type=architecture
    /pptx-diagram-pro:diagram ./flow_idea.md --mode=image --mood=tech-focus
---

# 다이어그램 생성 커맨드

## Step 1: 입력 파싱

`$ARGUMENTS`에서 다음을 파싱한다.

- 위치 인자: 자연어 본문 또는 파일 경로(`.md`, `.txt`, `.json`, `.yaml`, `.yml`)
- 옵션: `--mode=` (native|image, 기본 native), `--type=` (flowchart|architecture, 미지정 시 추론),
  `--mood=` (technical-report|clarity|tech-focus|growth, 기본 technical-report), `--out=` (출력 PPTX 경로)

입력이 비어 있으면 사용자에게 다이어그램으로 만들 내용을 요청하고 종료한다.

## Step 2: 스킬 실행

`pptx-diagram-pro` 스킬의 5단계 워크플로우를 그대로 수행한다.

1. 모드·유형 확정 (옵션이 있으면 그대로, 없으면 입력 분석 후 추론)
2. IR(JSON) 작성 — 자연어면 `references/prompt-extraction.md` 4단계 적용, 구조화 파일이면 직접 매핑
3. IR 5개 체크리스트 검증
4. 렌더 스크립트 실행 (`render_native.py` 또는 `render_image.py`)
5. 출력 경로·슬라이드 수·모드·유형 보고

## Step 3: 결과 안내

- `--out=` 미지정 시: 입력 파일과 같은 디렉토리에 `<원본이름>.pptx`로 저장 (자연어 입력은 현재 작업 디렉토리에 `diagram.pptx`)
- IR JSON은 `<원본이름>.ir.json`으로 함께 저장하여 사용자가 수정 후 재렌더 가능하도록 한다
- image 모드 시 `GEMINI_API_KEY` 환경변수 확인. 없으면 즉시 안내 후 종료
