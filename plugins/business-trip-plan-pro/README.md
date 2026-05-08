# business-trip-plan-pro

KIMM(한국기계연구원) **국외출장 계획서**(별지 2 양식) 작성을 보조하는 Claude Code 플러그인.

장소·날짜·행사명 같은 출장 핵심 정보를 입력(또는 인터뷰로 수집)하면, 사용자의 기존 작성 스타일(`~함`체, 개조식, 하이픈 불릿)을 그대로 따라 KIMM 별지 2 양식의 6개 표준 항목으로 정리해 준다. 부족한 정보가 있으면 사용자에게 직접 질문하면서 보완하고, 동행자 정보가 있으면 일정 표를 자동 분배한다.

## 설치

`marketplace.json`에 본 플러그인이 등록되어 있다면 다음으로 설치한다.

```
/plugin install business-trip-plan-pro
```

## 사용법

```
/business-trip-plan-pro:draft
/business-trip-plan-pro:draft <간단한_설명_또는_파일경로>
/business-trip-plan-pro:draft <입력> --output=<폴더>
/business-trip-plan-pro:draft <입력> --no-budget
/business-trip-plan-pro:draft <입력> --reference=<참고파일.md>
```

### 예시

```
# 인자 없이 시작 (모든 정보를 인터뷰로 수집)
/business-trip-plan-pro:draft

# 짧은 텍스트로 시작
/business-trip-plan-pro:draft "MICCAI 2025 학회 참석, 미국 시카고, 9월 22-28일"

# 마크다운 파일을 입력
/business-trip-plan-pro:draft ./trip_idea_MICCAI2025.md

# 출력 폴더 지정
/business-trip-plan-pro:draft ./idea.md --output=D:\trips\2025_MICCAI

# 예산 없이 텍스트만 작성 (예산은 후속 입력)
/business-trip-plan-pro:draft "ICRA 2025, 영국 런던, 5월 19-23일" --no-budget
```

## 출력

- `국외출장계획서_<YYYY>_<신청자명>_<요약>.md`
  - 별지 2 양식 헤더 + 신청자 표
  - 6개 표준 항목 본문
  - 첨부 placeholder

마크다운 파일에는 그림/첨부 위치만 `<그림. ...>`, `<첨부. ...>` 마커로 표기되어 있고, 사용자가 hwpx로 변환할 때 실제 이미지를 직접 붙여 넣는다.

## 작성되는 양식 구조

KIMM 별지 2 양식 6개 항목:

1. 출장목적 (학회개요 / 발표논문개요 / 학회소개)
2. 출장일정 (출장기간 / 출장국 / 동행자 / 일자별 표)
3. 최근 3년간 국외출장 실적
4. 출장중 파악(수행)해야 할 내용 (동행자별 세부역할 + 활동별 ○ 블록)
5. 출장예산 (지급계정 / 소요경비 표 / 등급지·환율)
6. 연구관련 반출 예정 전산장비 및 자료 현황

## 인터뷰 모드

플러그인은 입력된 출장 개요가 6개 항목을 채우기에 부족하다고 판단하면 **AskUserQuestion** 도구로 한 번에 최대 4개씩 질문을 묶어 진행한다. 보통 2~3 라운드 안에 모든 정보가 수집된다.

### 라운드 1 — 출장 핵심 4종
- 행사명/학회명
- 출장지(도시, 국가, 방문기관)
- 출장기간(출국일~귀국일)
- 신청자 정보(소속/직급/성명)

### 라운드 2 — 출장 부가정보
- 동행자(직급/성명, 없으면 "단독 출장")
- 발표 논문(제목/저자/발표시간, 없으면 생략)
- 지급계정(과제번호+과제명)
- 부가 활동(이사회 참석, 차년도 학회 홍보 등)

### 라운드 3 — 예산/실적/반출
- 등급지(가/나/다, 모르면 자동 추론)
- 왕복교통비 실제값
- 환율 (없으면 작성 시점 환율 자동 사용)
- 최근 3년 출장 실적
- 반출 장비 여부

## 자동 계산 기능

### 일정 표 자동 생성
출장기간(예: `2025-09-22 ~ 2025-09-28`)을 입력하면:
- 출국일: 인천 → 출장지
- 행사일: 출장지 → 방문기관(학회 참석/발표)
- 귀국 항공 탑승일: 출장지 → 인천
- 인천 도착일: - → 인천

요일은 자동으로 한글로 표기되며, 동행자가 있으면 한 행 안에 동행자별 활동을 자동 분배한다.

### 예산 자동 환산
등급지(가/나/다) + 직급(책임/선임/연구원) + 일수 + 환율을 받아 일비/식비/숙박비를 원화로 자동 환산. 왕복교통비는 항공권 인보이스 실제값을 사용자가 입력.

## 구성 파일

```
business-trip-plan-pro/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── commands/
│   └── draft.md                           # /business-trip-plan-pro:draft 커맨드
├── agents/
│   └── business-trip-drafter.md           # 메인 작성 에이전트
├── skills/
│   └── business-trip-plan-pro/
│       ├── SKILL.md                       # 메인 스킬
│       └── references/
│           ├── form-structure.md          # 양식 6개 항목 구조
│           ├── writing-style.md           # ~함체 등 문체 규칙
│           ├── interview-protocol.md      # 부족 정보 질문 전략
│           ├── budget-calculator.md       # 등급지별 일비/식비/숙박비 산식
│           └── schedule-template.md       # 출장일정 표 작성 패턴
└── examples/
    ├── example1-CARS2024-책임연구원.md    # 책임연구원 + 발표 + 부가활동 사례
    └── example2-CARS2024-선임연구원.md    # 선임연구원 + 동행 + 3년 실적 사례
```

## 라이선스 / 작성자

- Author: Joonho Seo (https://github.com/JSeo-KIMM)
- 사내(KIMM) 국외출장 계획서 작성 보조용
