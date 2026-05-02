---
name: pptx-diagram-pro
description: >
  연구 내용·프로세스·아이디어를 정부/공공기관 톤의 PPTX 다이어그램으로 변환하는 스킬.
  자연어 프롬프트(예: "강화학습 학습 루프 그려줘", "이 시스템 아키텍처 PPTX로 만들어줘") 또는
  구조화된 YAML/JSON 입력을 받아 (1) 프로세스/플로우차트와 (2) 시스템 아키텍처 두 유형의
  다이어그램을 생성한다. 두 가지 렌더 모드를 지원한다 — native(python-pptx 도형으로 편집 가능,
  기본값)와 image(Gemini로 다이어그램 이미지 렌더링 후 슬라이드 삽입). "다이어그램 그려줘",
  "PPTX 다이어그램", "플로우차트", "시스템 구성도", "아키텍처 그림", "프로세스 그림", "발표용 도식",
  "정부 스타일 다이어그램" 등의 요청 시 자동으로 사용한다.
---

# pptx-diagram-pro

연구 내용·프로세스·아이디어를 정부 톤 PPTX 다이어그램으로 만든다. 자연어든 구조화 입력이든
중간 표현(IR JSON)으로 수렴한 뒤 결정론적 스크립트가 PPTX를 생성한다.

## 워크플로우

```
사용자 입력
   │
   ▼
[1] 모드·유형 확정 (native|image, flowchart|architecture)
   │
   ▼
[2] IR(JSON) 작성  ← references/ir-spec.md
   │   • 자연어 입력은 references/prompt-extraction.md 4단계 적용
   │   • 구조화 입력은 IR로 직접 매핑
   ▼
[3] IR 검증 (5개 체크리스트)
   │
   ▼
[4] 렌더 스크립트 실행
   │   • native → scripts/render_native.py
   │   • image  → scripts/render_image.py (GEMINI_API_KEY 필요)
   ▼
[5] PPTX 출력 + 사용자에게 경로 보고
```

## 1단계 — 모드와 유형 확정

진입 시 두 가지를 결정한다.

- **모드**: `native`(기본, 편집 가능한 도형) / `image`(Gemini 이미지)
- **유형**: `flowchart`(프로세스/단계) / `architecture`(시스템 구성)

사용자가 명시했으면 그대로. 모호하면 1회 짧게 확인한다.
- "프로세스/단계/흐름/파이프라인" → flowchart
- "구성/아키텍처/모듈/서비스/DB/큐" → architecture

## 2단계 — IR 작성

IR(중간 표현, JSON)은 [`references/ir-spec.md`](references/ir-spec.md)에 정의된 스키마를 따른다.
핵심 필드: `type`, `title`, `nodes[]`, `edges[]`, `layout{rows, cols, direction}`, `style{mood}`.

각 노드는 격자 좌표(`row`, `col`)를 명시한다(자동 레이아웃 의존 금지).
`kind`별 도형 매핑·레이아웃 휴리스틱은 유형별 가이드를 본다.

- 플로우차트 → [`references/flowchart-guide.md`](references/flowchart-guide.md)
- 아키텍처 → [`references/architecture-guide.md`](references/architecture-guide.md)
- 색·폰트·사이즈 → [`references/gov-style.md`](references/gov-style.md)

자연어 입력에서 IR을 추출할 때는 [`references/prompt-extraction.md`](references/prompt-extraction.md)의
4단계(유형 판정 → 노드 추출 → 엣지 추출 → 격자 좌표 추정)를 그대로 적용한다.

## 3단계 — IR 검증

렌더 직전 다음 5개를 확인한다(스크립트에도 동일 검증이 들어있음).

1. `type`이 flowchart 또는 architecture
2. `nodes`가 비어있지 않음
3. 모든 `edges[].from`/`to`가 `nodes[].id`에 존재
4. 격자 좌표 충돌 없음(같은 셀에 두 노드 금지)
5. `accent: true` 노드 ≤ 3

## 4단계 — 렌더 실행

IR을 임시 파일에 저장한 뒤 스크립트를 실행한다.

### Native 모드

```bash
python plugins/pptx-diagram-pro/skills/pptx-diagram-pro/scripts/render_native.py \
  <ir.json> --output <out.pptx>
```

의존성: `pip install python-pptx lxml` (lxml은 python-pptx 설치 시 함께 설치됨).
편집 가능한 도형이 생성되어 PPT에서 위치·색·텍스트를 자유롭게 수정할 수 있다.

### Image 모드

```bash
python plugins/pptx-diagram-pro/skills/pptx-diagram-pro/scripts/render_image.py \
  <ir.json> --output <out.pptx>
```

의존성: `pip install python-pptx google-genai` + `GEMINI_API_KEY` 환경변수.
스크립트가 IR을 기반으로 Gemini용 4-block 프롬프트를 자동 구성하고 4K 이미지 1장을 생성해
풀블리드 슬라이드로 삽입한다. 결과 이미지는 편집 불가하므로 발표 직전 시각 품질이 우선일 때 사용.

스크립트 탐색 우선순위(상대 경로가 작동하지 않는 환경에서):
- Glob `**/pptx-diagram-pro/skills/pptx-diagram-pro/scripts/render_*.py`
- 그래도 없으면 사용자에게 경로 확인 요청. **자체 코드 작성으로 우회 금지**.

## 5단계 — 출력 보고

출력 PPTX 경로·슬라이드 수·렌더 모드·다이어그램 유형을 한 줄로 보고한다.
필요 시 사용자에게 IR 수정 요청을 받아 재실행한다.

## 입력 포맷

자연어 외에 사용자가 IR을 직접 줄 수도 있다.

- `.json` 파일 — 그대로 IR로 사용
- `.yaml`/`.yml` 파일 — Python `pyyaml`로 로드 후 임시 JSON으로 변환
- `.md` 파일 — 프론트매터에 IR JSON이 들어있거나 본문이 자연어면 추출 후 IR로 변환

## 사용하지 않을 때

- 슬라이드 덱 **전체**(여러 장의 발표 자료) — 본 스킬은 다이어그램 1장 슬라이드만 생성한다
- 텍스트 위주 문서
- 이미지 한 장만 필요 (PPTX 불필요) → `render_image.py --png-only`

## 참조 파일

- [`references/ir-spec.md`](references/ir-spec.md) — IR JSON 스키마, 검증 규칙, 예시 2종
- [`references/flowchart-guide.md`](references/flowchart-guide.md) — 플로우차트 도형 매핑·레이아웃·패턴
- [`references/architecture-guide.md`](references/architecture-guide.md) — 아키텍처 도형 매핑·그룹 활용·패턴
- [`references/gov-style.md`](references/gov-style.md) — 정부 톤 색·폰트·사이즈·금지사항
- [`references/prompt-extraction.md`](references/prompt-extraction.md) — 자연어 → IR 4단계 추출 절차
