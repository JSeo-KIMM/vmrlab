---
description: |
  KIMM 국외출장 계획서(별지 2) 양식에 맞춘 출장계획서 초안을 작성한다.
  장소, 출장기간, 행사명 등 핵심 정보를 사용자에게 묻고, 6개 표준 항목
  (출장목적/출장일정/최근3년실적/파악수행내용/출장예산/반출장비)으로
  정리한다.

  사용법:
    /business-trip-plan-pro:draft
    /business-trip-plan-pro:draft <간단한_설명_또는_파일경로>
    /business-trip-plan-pro:draft <입력> --output=<폴더>
    /business-trip-plan-pro:draft <입력> --no-budget

  옵션:
    --output=DIR  출력 폴더 지정 (기본: 입력 파일 폴더 또는 cwd)
    --no-budget   5번 출장예산 항목을 비워두고 초안만 작성
    --reference=PATH  스타일 참고용 기존 출장계획서 파일 경로

  예시:
    /business-trip-plan-pro:draft
    /business-trip-plan-pro:draft "MICCAI 2025 학회 참석, 미국 시카고, 9월"
    /business-trip-plan-pro:draft ./trip_idea.md
    /business-trip-plan-pro:draft ./idea.md --output=D:\trips\2025_MICCAI
---

# KIMM 국외출장 계획서 작성 커맨드

## 실행 절차

### Step 1: 입력 파싱
`$ARGUMENTS`에서 다음을 추출한다:
- **출장 개요 입력**: 파일 경로(`.md`, `.txt`)이면 Read로 읽고, 그렇지 않으면 텍스트 자체를 출장 아이디어로 간주. 인자가 비어 있으면 처음부터 인터뷰로 진행.
- **옵션**: `--output=<경로>`, `--no-budget`, `--reference=<참고파일경로>`

파일 경로로 보이는데 존재하지 않으면 사용자에게 확인 후 텍스트로 처리한다.

### Step 2: business-trip-drafter 에이전트 호출
`business-trip-drafter` 서브에이전트에게 아래를 전달한다:
- 출장 개요 본문 (파일 내용 또는 텍스트, 빈 값일 수 있음)
- 입력 파일 경로 (있을 경우)
- 출력 폴더 경로 (--output 또는 입력 파일 폴더 또는 cwd)
- 예산 작성 여부 (--no-budget이 없으면 true)
- 참고 양식 경로 (--reference 지정 시)

### Step 3: 결과 안내
에이전트 완료 후:
1. 생성된 파일 절대경로 (`.md`)
2. 출장 핵심 요약 (행사명, 출장지, 출장기간, 동행자, 합계 예산)
3. 사용자가 후속 보완해야 할 항목 (예: "예실대비표/항공 인보이스 첨부", "최근 3년간 출장실적 확인 필요")

## 에이전트 전달 프롬프트

다음 내용을 business-trip-drafter 에이전트에게 전달한다:

```
새로운 KIMM 국외출장 계획서를 양식에 맞춰 작성해주세요.

[출장 개요 본문]:
(파일 내용 또는 텍스트 전체. 비어있을 수 있음)

[입력 파일]: $ARGUMENTS에서 파싱된 파일 경로 (없으면 N/A)
[출력 폴더]: 결정된 출력 폴더 경로
[예산 작성]: true | false
[참고 양식]: --reference 지정 경로 (없으면 플러그인 examples/ 사용)

작업 절차:
1. 출장 개요 분석 → 핵심 6개 항목별 정보 충분성 점검
2. 핵심 누락 정보(장소/기간/행사명/신청자/동행자/지급계정 등)는 AskUserQuestion으로 한 번에 최대 4개씩 질문
3. 사용자 작성 스타일(~함체, 개조식, 하이픈 불릿)로 초안 작성
4. 출장일정 표와 예산 산식은 사용자가 입력한 등급지/일수에 따라 자동 계산
5. 결과 파일 저장 후 경로 보고
```
