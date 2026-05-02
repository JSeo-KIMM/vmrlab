---
description: |
  연구·공학 아이디어를 6단계(재진술→타당성→약점→보완→선행연구→판정)로 비판적으로 검토합니다.
  WebSearch로 선행연구와 특허를 실제 조회하며, 칭찬 대신 정확한 진단을 우선합니다.

  사용법:
    /idea-gen-pro:develop <아이디어 텍스트>
    /idea-gen-pro:develop <초안_파일경로>
    /idea-gen-pro:develop <아이디어> --phases=3,5     # 일부 단계만 수행

  예시:
    /idea-gen-pro:develop "초음파 영상 자가검진을 위한 멀티모달 LLM ..."
    /idea-gen-pro:develop ./idea_draft.md
    /idea-gen-pro:develop ./idea_draft.md --phases=5  # 선행연구만
---

# 아이디어 검토 커맨드

## Step 1: 입력 파싱

`$ARGUMENTS`에서 다음을 파싱한다.

- 위치 인자: 아이디어 본문 또는 파일 경로 (`.md`, `.txt`)
- `--phases=` 옵션: 수행할 Phase 번호 목록 (콤마 구분, 예 `1,2,3`). 미지정 시 1~6 전체.

파일 경로면 Read로 내용을 로드하고, 그 외에는 인자 본문을 그대로 사용한다.
입력이 비어 있으면 검토할 아이디어 또는 파일을 요청하고 종료한다.

## Step 2: 스킬 실행

`idea-develop-pro` 스킬을 호출하여 다음을 수행한다.

- Phase 1 재진술 → Phase 2 타당성 → Phase 3 약점 → Phase 4 보완 → Phase 5 선행연구 → Phase 6 판정
- `--phases=` 지정 시 해당 Phase만 수행. 단, Phase 5를 단독 수행해도 신규성 판정까지 포함한다.
- Phase 5는 반드시 WebSearch로 실제 검색 (기억 의존 금지).

## Step 3: 결과 출력

- 출력은 대화창에 직접 작성 (파일로 저장하지 않음, 사용자가 요청 시 별도 저장).
- 한국어 입력은 한국어로, 영어 입력은 영어로 응답.
- R&D 제안서 맥락이면 개조식, 논문 맥락이면 산문체.
