# business-trip-plan-pro

KIMM(한국기계연구원) **국외출장 계획서**(별지 제2호 양식) 작성을 보조하는 Claude Code 플러그인.

출장유형(학회/전시회/연구과제)을 고른 뒤 작업 폴더의 필수 파일을 점검하고, 행사 홈페이지를
웹에서 조사하여 KIMM 표준 6개 항목으로 정리한다. 마크다운 초안을 먼저 만들고, 검토 후
별지 제2호 hwpx 양식을 채워 새 hwpx 파일을 생성한다. 행사·일정·항공인보이스 이미지는
PNG로 저장하고 양식에는 자리표시를 남긴다. 사용자의 `~함`체 개조식 문체를 따른다.

## 설치

`marketplace.json`에 등록되어 있으면:

```
/plugin install business-trip-plan-pro
```

## 사용법

```
/business-trip-plan-pro:draft
/business-trip-plan-pro:draft <행사명_또는_파일경로>
/business-trip-plan-pro:draft <입력> --output=<폴더>
/business-trip-plan-pro:draft <입력> --type=학회|전시회|연구과제
/business-trip-plan-pro:draft <입력> --md-only
```

### 예시

```
/business-trip-plan-pro:draft
/business-trip-plan-pro:draft "MICCAI 2025 학회 참석, 미국 보스턴"
/business-trip-plan-pro:draft ./trip_idea.md --type=학회
/business-trip-plan-pro:draft "CES 2026 참관" --type=전시회 --output=D:\trips\2026_CES
```

## 작업 폴더 준비

플러그인을 실행하기 전, 작업 폴더에 다음 파일을 둔다 (유형에 따라 다름).

| 파일 | 학회 | 전시회 | 연구과제 |
|---|:--:|:--:|:--:|
| 논문 파일 | 필수 | — | — |
| 연구과제관련 파일 | — | — | 필수 |
| 항공인보이스 파일 | 필수 | 필수 | 필수 |
| 내용참고 파일 (지급계정·계정명 포함) | 필수 | 필수 | 필수 |

- `[별지 제2호] 국외출장 계획서.hwpx`(양식)와 `[별표 제2-1호] 해외출장 여비 정액표.pdf`(여비표)는
  작업 폴더에 없으면 플러그인 `assets/`의 동봉본을 자동 사용한다.
- 필수 파일이 없으면 플러그인이 작성을 멈추고 어떤 파일이 필요한지 알려준다.

## 출력

- `국외출장계획서_<YYYY>_<신청자명>_<요약>.md` — 검토용 마크다운 초안 (6개 항목)
- `국외출장계획서_<YYYY>_<신청자명>_<요약>.hwpx` — 채워진 별지 제2호 양식
- `images/` — 행사 홈페이지·일정·항공인보이스 PNG 이미지

hwpx 양식의 이미지 자리에는 `[그림: images/파일명.png — 한글에서 이 위치에 삽입]` 안내가 남으며,
사용자가 한글에서 직접 이미지를 끼워넣는다. 예실대비표는 빈칸으로 두어 사용자가 수동 캡처한다.

## 작성되는 양식 구조 (별지 제2호 6개 항목)

1. 출장목적 — 행사개요 / (유형별) 발표논문·연구분야·과제 연관성 / 행사소개
2. 출장일정 — 출장기간 / 출장국 / 동행자 / 일자별 표
3. 최근 3년간 국외출장 실적
4. 출장중 파악(수행)해야 할 내용 — 행사 상세 + 연구 연관 단락 + 이미지 자리
5. 출장예산 — 지급계정 / 소요경비 표 (여비표·항공인보이스 기준)
6. 연구관련 반출 예정 전산장비 및 자료 현황 — 양식 기본값 유지 (수정 안 함)

## 동작 개요

1. **출장유형 확정** — 학회 / 전시회 / 연구과제
2. **필수 파일 점검** — 작업 폴더 스캔, 누락 시 사용자에게 요청
3. **행사 웹 조사** — 홈페이지·개요·일정 검색 (못 찾으면 URL 요청)
4. **인터뷰** — 동행자·실적·부가활동 등 누락 정보를 AskUserQuestion으로 보완
5. **마크다운 초안 작성** — 6개 항목, 사용자 검토
6. **이미지 PNG 저장** — 헤드리스 캡처(실패 시 이미지 검색 폴백), PDF→PNG 변환
7. **hwpx 양식 채우기** — 새 hwpx 생성

## 구성 파일

```
business-trip-plan-pro/
├── .claude-plugin/plugin.json
├── README.md
├── commands/
│   └── draft.md                          # /business-trip-plan-pro:draft 커맨드
├── agents/
│   └── business-trip-drafter.md          # 메인 작성 에이전트
├── skills/
│   └── business-trip-plan-pro/
│       ├── SKILL.md
│       └── references/
│           ├── form-structure.md         # 별지 제2호 6개 항목 구조
│           ├── interview-protocol.md     # 유형별 필수 파일 점검 + 질문 전략
│           ├── writing-style.md          # ~함체 문체 규칙
│           ├── event-research.md         # 행사 웹 조사 + 이미지 캡처
│           ├── schedule-template.md      # 출장일정 표 작성 패턴
│           ├── budget-calculator.md      # 등급지별 여비 산식
│           └── hwpx-output.md            # hwpx 양식 채우기 절차
├── scripts/
│   ├── hwpx_fill.py                      # hwpx dump/치환/행추가/셀설정/문단삽입/서식적용
│   ├── pdf_to_png.py                     # PDF(인보이스·논문) → PNG
│   └── capture_web.py                    # 행사 홈페이지 헤드리스 스크린샷
├── assets/
│   ├── [별지 제2호] 국외출장 계획서.hwpx   # 양식 폴백본
│   └── [별표 제2-1호] 해외출장 여비 정액표.pdf
└── examples/
    ├── example1-CARS2024-책임연구원.md
    └── example2-CARS2024-선임연구원.md
```

## 의존성

- Python 3, `PyMuPDF` (PDF→PNG): `pip install PyMuPDF --break-system-packages`
- (선택) `playwright` (웹 스크린샷): `pip install playwright --break-system-packages` 후
  `python -m playwright install chromium`. 미설치 시 이미지 URL 검색으로 폴백한다.

## 라이선스 / 작성자

- Author: Joonho Seo (https://github.com/JSeo-KIMM)
- 사내(KIMM) 국외출장 계획서 작성 보조용
