---
description: |
  구어체 연구제안서 초안 마크다운을 A4 3장 분량의 정부 제출 형식(개조식, 7개 대제목)으로 변환합니다.

  사용법:
    /proposal <초안_파일경로>
    /proposal <초안_파일경로> --out=<출력경로>

  예시:
    /proposal ./prompt_v2.md
    /proposal ./draft.md --out=./proposal_final.md
---

# 3장 연구제안서 작성 커맨드

## Step 1: 입력 파싱
`$ARGUMENTS`에서 파일 경로와 `--out=` 옵션을 파싱한다. 파일이 없으면 오류 출력 후 종료.

## Step 2: 스킬 실행
`3page-proposal-pro` 스킬을 호출하여 다음을 수행한다.
- 초안 읽기 및 빈 구간(`[...]`, `...`, TBD) 식별
- 필요 시 WebSearch로 정량 수치·출처·동향 보강
- `references/writing-rules.md`, `section-guide.md`, `templates.md` 규칙 적용
- `references/checklist.md` 전 항목 점검
- 개조식 A4 3장 제안서 생성

## Step 3: 저장
- `--out=` 미지정 시: 입력과 동일 디렉토리에 `<원본이름>_v<n>.md` 저장
- 지정 시: 해당 경로에 저장

## Step 4: 결과 안내
1. 생성 파일 경로
2. 섹션별 분량 추정(글자 수)
3. `[출처 확인 필요]` 또는 추가 검토가 필요한 항목 리스트
