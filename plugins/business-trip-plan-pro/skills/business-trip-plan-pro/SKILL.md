---
name: business-trip-plan-pro
description: |
  KIMM(한국기계연구원) 국외출장 계획서(별지 제2호) 양식에 맞춰 출장 정보를
  정형화된 hwpx 문서로 변환하는 스킬. 출장유형(학회/전시회/연구과제)을
  확정하고 작업 폴더의 필수 파일을 점검한 뒤, 행사 홈페이지를 웹에서 조사하여
  6개 표준 항목으로 정리한다. 마크다운 초안을 먼저 만들고 검토 후 별지 제2호
  hwpx 양식을 채운다. 행사·일정·인보이스 이미지는 PNG로 저장하고 양식에는
  자리표시를 남긴다. 사용자의 ~함체 개조식 문체로 작성한다.

  다음 키워드/맥락에서 자동 사용:
  - "국외출장 계획서", "출장계획서", "별지 제2호", "별지 2 양식"
  - "학회 출장 계획서", "전시회 출장 계획서", "연구과제 출장 계획서"
  - 행사명/장소/날짜를 가진 출장 정보를 KIMM 양식 문서로 변환하는 모든 요청
---

# Business Trip Plan Pro (KIMM 국외출장 계획서, 별지 제2호)

KIMM 연구원의 국외출장 계획서를 별지 제2호 hwpx 양식으로 작성하는 스킬.

## 핵심 원칙

- **유형 우선**: 출장유형(학회/전시회/연구과제)에 따라 1번 항목과 필수 파일이 달라짐. 가장 먼저 확정.
- **필수 파일 점검**: 작업 폴더에 유형별 필수 파일이 있는지 확인하고, 없으면 작성을 멈추고 사용자에게 요청.
- **양식 보존**: 별지 제2호 6개 항목의 번호·순서·헤더를 절대 변경하지 않음. 6번 반출 항목은 손대지 않음.
- **추측 금지**: 자료에 없는 사실(항공편명, 호텔명, 지급계정 번호, 논문 저자)을 만들어내지 않음.
- **사용자 스타일 충실**: `~함`/`~음` 종결, 하이픈 불릿, 개조식. examples 폴더의 2개 사례와 톤이 같아야 함.
- **계산 정확성**: 여비 단가는 여비표(별표 제2-1호)와 `references/budget-calculator.md`를 그대로 사용.
- **이미지는 PNG + 자리표시**: 행사·일정·인보이스 이미지는 PNG로 저장하고, hwpx 양식에는 라벨이 붙은 자리만 남김.

## 신청자 기본값

별도 지정이 없으면: 소속 **로봇응용연구실** / 직급 **책임연구원** / 성명 **서준호**.

## 워크플로우

### Step 1: 출장유형 확정
- `학회 / 전시회 / 연구과제` 중 하나를 확정 (미지정 시 질문)

### Step 2: 필수 파일 점검
- `references/interview-protocol.md`의 유형별 필수 파일 표를 보고 작업 폴더를 Glob 스캔
- 공통: 항공인보이스 파일, 내용참고 파일 / 학회: + 논문 파일 / 연구과제: + 연구과제관련 파일
- 양식 hwpx·여비표 pdf는 작업 폴더에 없으면 플러그인 `assets/` 동봉본 사용
- 내용참고 파일에 지급계정·계정명이 없으면 보완 요청
- 누락 파일이 있으면 작성 중단 → 사용자 요청 → 확보 후 진행

### Step 3: 행사 웹 조사
- `references/event-research.md`에 따라 행사 홈페이지·개요·일정 조사

### Step 4: 부족 정보 인터뷰
- `references/interview-protocol.md`에 따라 AskUserQuestion (라운드당 최대 4개, 최대 2~3 라운드)

### Step 5: 마크다운 초안 작성
- `references/form-structure.md` — 6개 항목 템플릿
- `references/writing-style.md` — 문체 규칙
- `references/schedule-template.md` — 일자별 일정 표 (셀 병합 HTML `<table>`)
- `references/budget-calculator.md` — 여비 산식
- examples 폴더 — 톤 참조
- 작성 후 사용자 검토

### Step 6: 이미지 PNG 저장
- `references/event-research.md`에 따라 `scripts/capture_web.py`(웹), `scripts/pdf_to_png.py`(인보이스/논문)로 `images/` 하위에 저장

### Step 7: hwpx 양식 채우기
- `references/hwpx-output.md`에 따라 `scripts/hwpx_fill.py`로 별지 제2호 양식을 채워 새 hwpx 생성

## 참고 파일

- `references/form-structure.md` — 별지 제2호 6개 항목 구조와 작성 규칙
- `references/interview-protocol.md` — 출장유형별 필수 파일 점검 + 질문 전략
- `references/writing-style.md` — 사용자 고유 문체 규칙
- `references/event-research.md` — 행사 웹 조사 + 이미지 캡처 방법
- `references/schedule-template.md` — 출장일정 표 작성 패턴
- `references/budget-calculator.md` — 등급지별 일비/식비/숙박비 산식
- `references/hwpx-output.md` — hwpx 양식 채우기 + 이미지 자리표시
- `scripts/hwpx_fill.py` — hwpx 양식 dump/치환/행추가/셀설정 + 출장일정 7열 병합 표 생성(build-schedule) 도구
- `scripts/pdf_to_png.py` — PDF(항공인보이스/논문) → PNG 렌더링
- `scripts/capture_web.py` — 행사 홈페이지 헤드리스 스크린샷
- `assets/` — 별지 제2호 양식 hwpx, 해외출장 여비 정액표 pdf (작업 폴더에 없을 때 폴백)
- `../../examples/` — 2개 실제 사례(서준호/심성보 CARS 2024)

## 금지사항

- "흥미로운 출장이네요" 같은 빈말로 시작하지 않음
- 추측에 의존한 항공편/호텔/일정/저자 기재 금지 (사용자 입력·자료·WebSearch 결과만)
- `~합니다`, `~이다` 같은 정중체·평서체 금지 (`~함`체 통일)
- 양식 항목 번호(1~6)·헤더 변경 금지
- 6번 반출 항목 수정 금지
- 여비 단가 임의 변경 금지 — 여비표/`budget-calculator.md` 그대로
- 필수 파일이 없는데 작성 강행 금지
