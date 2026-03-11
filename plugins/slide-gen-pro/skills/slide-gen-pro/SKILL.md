---
name: slide-gen-pro
description: "정부 스타일 이미지 슬라이드 생성기. 입력 문서를 기반으로 정부/공공기관 발표용 4K 이미지 슬라이드를 생성한다. 구조화 모드(4-block 파이프라인)와 자유 모드(자유 형식 프롬프트) 중 선택 가능. 박사급 연구자·정부 관계자 대상의 공식 발표 자료를 만들 때 사용한다. '정부 슬라이드', '공식 발표자료', '연구 발표 슬라이드', 'gov 테마 슬라이드', '정부 스타일 PPT 이미지', '슬라이드 만들어줘' 등의 요청 시 반드시 이 스킬을 사용할 것."
---

# 정부 스타일 이미지 슬라이드 생성기

입력 문서(연구 보고서, 정책 문서, 기술 보고서 등)를 기반으로 정부/공공기관 발표용 4K 이미지 슬라이드를 생성한다.

---

## 0단계: 모드 선택 (시작 시 반드시 확인)

스킬 실행 시 **가장 먼저** 사용자에게 다음을 질문한다:

> **프롬프트 생성 방식을 선택해주세요:**
>
> **A. 자유 모드** (권장) — 자유 형식 프롬프트로 Gemini에게 직접 전달. 디자인 자유도가 높고 시각적 완성도가 좋습니다.
>
> **B. 구조화 모드** — visual-generator 4-block 파이프라인(content-organizer → content-reviewer → prompt-designer → prompt-validator → renderer-agent)을 거칩니다. 중간 산출물과 품질 검증 보고서가 포함됩니다.

사용자가 명시적으로 선택하지 않으면 **자유 모드(A)**를 기본값으로 사용한다.

---

## 공통 사항

### 핵심 원칙
- **고급 문체**: 개조식 명사구, 4자 한자어, 서술어 최소화
- **정돈된 형식**: 플랫 인포그래픽, 직각 박스, 번호 매김, 격자 배치
- **화려함 지양**: 과도한 그라데이션, 글래스모피즘 금지
- **한글 전용**: 한영 병기 금지 (고유 약어 AI, IoT 등만 허용)

### 사전 준비
1. 사용자로부터 입력 문서를 받는다
2. 출력 디렉토리를 설정한다 (기본: 입력 문서와 동일 경로의 `slides/` 하위 폴더)
3. GEMINI_API_KEY 환경변수 확인 — 없으면 `.env` 파일에서 로드하거나 사용자에게 안내

### 렌더링 스크립트
`generate_slide_images.py`를 사용하여 프롬프트를 4K PNG 이미지로 변환한다.
- 스크립트 탐색 순서: Glob(`**/visual-generator/skills/slide-renderer/scripts/generate_slide_images.py`) → 확장 Glob(`**/generate_slide_images.py`)
- 스크립트를 찾지 못하면 자체 코드 작성 금지 — 사용자에게 경로 확인 요청

### 에러 처리
- API 타임아웃: 5초 대기 후 재시도 (최대 3회)
- 이미지 데이터 없음: 5초 대기 후 재시도 (최대 3회)
- GEMINI_API_KEY 미설정: 즉시 중단, 사용자 안내

---

## A. 자유 모드

입력 문서를 분석하여 자유 형식 프롬프트를 직접 작성하고, Gemini API로 이미지를 생성한다.
디자인 자유도가 높아 시각적 완성도와 시인성이 우수하다.

### 실행 절차

```
입력 문서
  │
  ▼
[1단계] 문서 분석 + 슬라이드 구성 결정
  │
  ▼
[2단계] 슬라이드별 자유 형식 프롬프트 작성
  │
  ▼
[3단계] generate_slide_images.py로 이미지 렌더링
  │
  ▼
[4단계] 최종 검증
```

### 1단계: 문서 분석

입력 문서를 읽고 다음을 결정한다:

- **슬라이드 수**: 문서 분량에 따라 5~9장 (섹션당 1~2장 기준)
- **슬라이드 구성**: 표지 → 현황/배경 → 본론(기술/전략/구성) → 성과/효과 → 향후 계획/종합
- **색상 팔레트**: 정부 스타일에 적합한 4색 (주조색, 보조색, 강조색, 배경색)
- **무드 선택 기준**:
  - 기술/연구 보고서 → 네이비 + 틸 계열
  - 정책/제도 → 차콜 + 앰버 계열
  - 디지털/AI → 블루 + 시안 계열
  - 환경/성장 → 그린 계열

### 2단계: 프롬프트 작성

각 슬라이드마다 다음 구조의 자유 형식 프롬프트를 작성한다:

```markdown
■ 이미지 유형
PPT 슬라이드 스타일의 인포그래픽. 정부 국가연구개발 과제 발표자료 수준의
전문적 도식. 가로형(16:9 비율), 고해상도, 벡터 그래픽 스타일.

■ 색상 팔레트 (4색 제한)
1. 주조색: #1E3A5F (진한 네이비) — 제목, 핵심 박스
2. 보조색: #4A90A4 (청록색) — 연결선, 보조 요소
3. 강조색: #E07B39 (오렌지) — 핵심 수치, 하이라이트
4. 배경색: #F5F7FA (라이트 그레이) — 전체 배경

■ 전체 레이아웃 구성
[ASCII 도식으로 레이아웃 설명]
┌─────────────────────────────┐
│ [상단 타이틀 바]              │
├─────────────────────────────┤
│                             │
│   [중앙 내용 영역]            │
│                             │
├─────────────────────────────┤
│ [하단 요약/출처]              │
└─────────────────────────────┘

■ 반드시 포함할 텍스트 (한글)
- "슬라이드 제목"
- "핵심 내용 1"
- "핵심 내용 2"
- "수치 데이터 (출처, 연도)"

■ 그래픽 요소
- 아이콘: [구체적 설명]
- 연결선: [흐름 설명]
- 차트/표: [필요 시]

■ 스타일 지침
- 모든 텍스트 한글 렌더링, 깔끔하고 선명하게
- 정부 공식 문서 수준의 격식
- 직각 박스, 명확한 테두리, 정돈된 격자
- No watermarks, no blurry text, no placeholder brackets
```

**프롬프트 작성 시 핵심 규칙**:
- ASCII 레이아웃 도식을 포함하여 Gemini가 공간 배치를 이해하도록 한다
- 렌더링할 텍스트를 "반드시 포함할 텍스트"에 명시적으로 나열한다
- `[Image 1]`, `[사진]` 같은 플레이스홀더 사용 금지 — Gemini가 그대로 텍스트로 렌더링한다
- 수치 데이터에는 출처를 병기한다: "시장 규모 5조원 (과기부, 2025)"
- 한영 병기 금지: "연구 (Research)" → "연구"

### 3단계: 이미지 렌더링

프롬프트 파일들을 `prompts/` 폴더에 저장하고 `generate_slide_images.py`로 렌더링한다.

### 4단계: 최종 검증

렌더링 완료 후 아래 검증을 수행한다 (공통 검증 절차 참조).

### 디렉토리 구조

```
[출력 디렉토리]/
├── prompts/
│   ├── 01_표지.md
│   ├── 02_현황.md
│   ├── ...
│   └── 0N_종합.md
├── images/
│   ├── 01_표지.png
│   ├── 02_현황.png
│   └── ...
└── verification_report.md
```

---

## B. 구조화 모드

visual-generator 에이전트 파이프라인을 gov 테마 기본값으로 오케스트레이션한다.
중간 산출물과 품질 검증 보고서가 포함되어 프로세스 추적이 가능하다.

### 실행 절차

```
입력 문서
  │
  ▼
[1단계] content-organizer ─── concepts.md, slide_plan.md, theme_recommendation.md
  │
  ▼
[2단계] content-reviewer ──── review_result.md (PASS/REJECT)
  │
  ▼
[3단계] prompt-designer ───── 4-block 프롬프트 파일들 (01_*.md, 02_*.md, ...)
  │
  ▼
[4단계] prompt-validator ──── 프롬프트 품질 검증
  │
  ▼
[5단계] renderer-agent ────── PNG 이미지 파일들 (4K 3840×2160)
  │
  ▼
[6단계] 최종 검증 ──────────── verification_report.md (PASS/FAIL)
```

### 1단계: 콘텐츠 분석 (content-organizer)

content-organizer 에이전트를 호출하되, 다음 기본값을 적용한다:

- **theme**: `gov`
- **mood**: 문서 성격에 따라 자동 선택 (기본값: `technical-report`)
  - 기술/연구 보고서 → `technical-report`
  - 정책 설명/제도 정의 → `clarity`
  - 디지털/AI 전략 → `tech-focus`
  - 성장/발전 전략 → `growth`
  - 성과 발표 → `presentation`
- **슬라이드 수**: 3~7장 (문서 분량에 따라 자동 결정)
- **레이아웃 우선순위**: Org-Network > Swimlane > Horizontal Timeline > Structure
  - Mind Map, Bento Grid는 비격식적이므로 사용하지 않는다

**출력 파일**:
- `concepts.md` — 슬라이드별 핵심 개념 (3~7개)
- `slide_plan.md` — 슬라이드 구성 계획
- `theme_recommendation.md` — 테마/무드/레이아웃 선택 근거

### 2단계: 콘텐츠 검토 (content-reviewer)

content-reviewer 에이전트를 호출하여 1단계 결과를 검증한다.

**검증 기준** (5점 만점, 각 항목 3.5점 이상 필요):
- 개념 추출 정확성 (원문 충실도, 시각화 적합도)
- 테마 선택 적절성 (내용 부합, 대상 적합)
- 레이아웃 선택 적절성 (정보 용량, 시각 균형)
- 구성 텍스트 검출 (메타데이터/플레이스홀더 혼입 여부)

**REJECT 시**: 피드백을 반영하여 1단계를 재실행한다 (최대 2회 재시도).

### 3단계: 프롬프트 생성 (prompt-designer)

prompt-designer 에이전트를 호출하여 4-block Gemini 프롬프트를 생성한다.

**gov 테마 강제 적용 사항**:
- INSTRUCTION의 Rendering Style에 gov 렌더링 7차원 반드시 포함 (서피스, 배경, 코너/엣지, 연결선, 시각 장식, 공간 구성, 시각 메타포)
- CONTENT는 번호 목록 텍스트만 — 메타라벨, 테이블, 역할 분류명 금지
- Content Placement에서 CONTENT 실제 텍스트를 작은따옴표로 직접 인용
- 최대 텍스트 요소 수: 25개
- 프롬프트당 100줄 이상

**출력 파일**: `01_layout_name.md`, `02_layout_name.md`, ... + `prompt_index.md`

### 4단계: 프롬프트 검증 (prompt-validator)

prompt-validator 에이전트를 호출하여 3단계 프롬프트의 품질을 검증한다.

**검증 항목**:
- 4-block 구조 완전성 (INSTRUCTION, CONFIGURATION, CONTENT, FORBIDDEN)
- 금지 패턴 미포함 (pt/px 단위, 한영 병기, 이미지 플레이스홀더, 메타라벨 등)
- gov 렌더링 스타일 준수 (직각, 플랫 인포그래픽, 번호 매김)
- 텍스트 밀도 25개 이내

### 5단계: 이미지 렌더링 (renderer-agent)

renderer-agent를 호출하여 검증 통과한 프롬프트를 4K PNG 이미지로 렌더링한다.

### 6단계: 최종 검증

렌더링 완료 후 아래 검증을 수행한다 (공통 검증 절차 참조).

### 디렉토리 구조

```
[출력 디렉토리]/
├── concepts.md              ← 1단계 출력
├── slide_plan.md            ← 1단계 출력
├── theme_recommendation.md  ← 1단계 출력
├── review_result.md         ← 2단계 출력
├── prompts/                 ← 3~4단계 출력
│   ├── 01_org_network.md
│   ├── 02_swimlane.md
│   ├── ...
│   └── prompt_index.md
├── images/                  ← 5단계 출력
│   ├── 01_org_network.png
│   ├── 02_swimlane.png
│   └── ...
├── generation_report.md     ← 5단계 렌더링 리포트
└── verification_report.md   ← 6단계 최종 검증 보고서
```

---

## 공통 검증 절차

모든 이미지 렌더링이 완료된 후, 모드에 관계없이 아래 검증을 수행하고 `verification_report.md`를 생성한다. 이 단계를 건너뛰면 안 된다.

### 검증 체크리스트

#### A. 생성 완결성 검증

| 항목 | 검증 방법 | PASS 기준 |
|------|-----------|-----------|
| 슬라이드 수 일치 | 프롬프트 파일 수 vs 생성 이미지 수 비교 | 모든 프롬프트에 대응하는 이미지 존재 |
| 파일 무결성 | 각 PNG 파일의 크기 > 0 바이트 확인 | 0바이트 파일 없음 |
| 해상도 확인 | Pillow로 각 이미지 크기 확인 | 16:9 비율 |

**검증 스크립트** (인라인 실행):
```python
from PIL import Image
import os, glob

def verify_completeness(prompts_dir, output_dir):
    prompts = sorted(glob.glob(os.path.join(prompts_dir, "*.md")))
    images = sorted(glob.glob(os.path.join(output_dir, "*.png")))
    prompts = [p for p in prompts if "prompt_index" not in os.path.basename(p)]

    results = {
        "total_prompts": len(prompts),
        "total_images": len(images),
        "missing": [],
        "zero_byte": [],
        "wrong_resolution": []
    }

    for img_path in images:
        if os.path.getsize(img_path) == 0:
            results["zero_byte"].append(os.path.basename(img_path))
        else:
            img = Image.open(img_path)
            w, h = img.size
            ratio = round(w / h, 2)
            if ratio != 1.78 and (w, h) != (3840, 2160):
                results["wrong_resolution"].append(f"{os.path.basename(img_path)}: {w}x{h}")

    if len(images) < len(prompts):
        results["missing"] = [
            os.path.basename(p) for p in prompts
            if not any(os.path.basename(p).replace(".md", "") in os.path.basename(i) for i in images)
        ]

    return results
```

#### B. 프롬프트 품질 검증

| 금지 패턴 | 심각도 |
|-----------|--------|
| 이미지 플레이스홀더 (`[Image N]`, `[사진]`, `[아이콘]`) | CRITICAL |
| 한영 병기 (`연구 (Research)`, `목표 / Goal`) | CRITICAL |
| 깨진 텍스트, 의미 없는 문자열 | CRITICAL |

#### C. 슬라이드 간 서사 흐름 검증

- 슬라이드 제목들을 순서대로 나열하여 논리적 흐름이 있는지 확인
- 첫 슬라이드가 전체 개요/비전을 제시하는지 확인
- 마지막 슬라이드가 성과 요약/결론/향후 계획인지 확인
- 중간 슬라이드들이 논리적 순서(현황→문제→해결→성과 등)를 따르는지 확인

### 검증 보고서 형식

```markdown
# 슬라이드 생성 검증 보고서

## 생성 일시
YYYY-MM-DD HH:MM

## 생성 모드
자유 모드 / 구조화 모드

## 입력 문서
[입력 문서 파일명]

## A. 생성 완결성
- 프롬프트 수: N개
- 생성 이미지 수: N개
- 누락: 없음 / [누락 파일 목록]
- 0바이트 파일: 없음 / [파일 목록]
- 해상도 이상: 없음 / [파일 목록]
- **판정: PASS / FAIL**

## B. 프롬프트 품질
- CRITICAL 위반: N건
- **판정: PASS / FAIL**

## C. 서사 흐름
- 슬라이드 순서: [제목 나열]
- 흐름 평가: [논리적 / 재배치 필요]
- **판정: PASS / FAIL**

## 종합 판정
**PASS / FAIL**
- FAIL 사유: [있는 경우 기술]
- 권고 사항: [있는 경우 기술]
```

### FAIL 시 처리

- **A 영역 FAIL** (누락/0바이트): 해당 프롬프트만 재렌더링
- **B 영역 FAIL**: 해당 프롬프트 수정 → 재렌더링
- **C 영역 FAIL**: 슬라이드 순서 재구성 → 전체 재실행
- 재검증은 최대 2회까지 허용. 2회 후에도 FAIL이면 사용자에게 보고서와 함께 판단을 요청한다.

---

## 사용 예시

**Example 1 (자유 모드):**
입력: "이 연구 보고서를 발표용 슬라이드로 만들어줘" + 연구보고서.md
→ 모드 선택 질문 → 사용자: "A" → 7장의 자유 형식 4K PNG 이미지 + verification_report.md

**Example 2 (구조화 모드):**
입력: "디지털 전환 슬라이드 만들어줘, 중간 산출물도 필요해" + 추진현황.md
→ 모드 선택 질문 → 사용자: "B" → 5장의 4-block 기반 이미지 + 중간 산출물 + verification_report.md

**Example 3 (기본값 = 자유 모드):**
입력: "이거 슬라이드로 만들어줘" + AI전략.md
→ 모드 선택 질문 → 사용자: 무응답/엔터 → 자유 모드로 진행
