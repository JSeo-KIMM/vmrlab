---
name: invention-disclosure-form-pro
description: |
  KIMM(한국기계연구원) 직무발명 내용 설명서 양식에 맞춰 발명 아이디어를
  정형화된 문서로 변환하는 스킬. 6개 표준 항목(명칭/배경/종래기술/상세설명/
  권리/추가자료) 구조를 따르고, 사용자의 ~함체 개조식 문체로 작성한다.
  부족한 정보가 있으면 사용자에게 질문하면서 보완하고, 도면이 필요하면
  편집 가능한 pptx 파일을 동일 폴더에 함께 만든다.

  다음 키워드/맥락에서 자동 사용:
  - "직무발명", "발명 신고서", "직무발명 내용 설명서", "KIMM 양식"
  - "이 아이디어 특허로 정리해줘", "직무발명 작성"
  - 발명 아이디어를 정형화된 문서로 변환하는 모든 요청
---

# Invention Disclosure Form Pro (KIMM 직무발명 내용 설명서)

## 핵심 원칙

- **사용자 스타일 충실**: ~함/~음 종결, 하이픈 불릿, 개조식. examples 폴더의 4개 사례와 톤이 다르면 안 됨.
- **양식 보존**: KIMM 6개 항목의 번호와 순서는 절대 변경하지 않음.
- **추측 금지**: 본문에 없는 사실(출원번호, 저자, 수치)을 만들어내지 않음.
- **부족분 질문**: 누락된 항목은 사용자에게 한 번에 최대 4개씩 묶어 질문.
- **도면 일관성**: 본문에 `<그림 N. 캡션>`을 삽입하면 pptx에도 같은 슬라이드가 있어야 함.

## 워크플로우

### Step 1: 아이디어 분석
- 입력 텍스트에서 핵심 발상, 적용 도메인, 차별점, 구성 요소 묘사를 추출
- 항목별로 `[충분]/[부족]/[빈]` 라벨링

### Step 2: 부족 정보 보완
- `references/interview-protocol.md`에 따라 AskUserQuestion으로 인터뷰
- 한 라운드 = 최대 4개 질문, 최대 2~3 라운드

### Step 3: 초안 작성
- `references/form-structure.md` — 항목별 템플릿
- `references/writing-style.md` — 문체 규칙
- examples 폴더 — 톤 참조

### Step 4: 도면 생성 (옵션)
- 본문에 `<그림 N. 캡션>` 마커 삽입
- `references/figure-generation.md`에 따라 python-pptx로 편집 가능한 pptx 작성
- 각 슬라이드 = 캡션 1개 + 기본 도형 placeholder

### Step 5: 파일 저장
- 본문: `직무발명_<요약명>_<YYYYMMDD>.md`
- 도면: `직무발명_<요약명>_<YYYYMMDD>_도면.pptx`

## 참고 파일

- `references/form-structure.md` — KIMM 양식 6개 항목 구조
- `references/writing-style.md` — 사용자 고유 문체 규칙
- `references/interview-protocol.md` — 누락 정보 질문 전략
- `references/figure-generation.md` — pptx 도면 파일 생성 방법
- `references/example-titles.md` — 발명 명칭 작명 가이드
- `../../../examples/` (플러그인 루트) — 4개 실제 사례

## 금지사항

- "흥미로운 아이디어입니다" 같은 빈말로 시작하지 않음
- 추측에 의존한 유사특허/문헌 기재 금지 (반드시 사용자 입력 또는 WebSearch 결과)
- "~합니다", "~이다" 같은 정중체 또는 평서체 사용 금지 (~함체 통일)
- 양식 항목 번호(1~6) 변경 금지
- 본문 도면 마커와 pptx 슬라이드 캡션 불일치 금지
