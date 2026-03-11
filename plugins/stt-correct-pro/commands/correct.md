---
name: correct
description: |
  STT(음성→텍스트) 변환 결과물의 오탈자, 맥락 단어, 군더더기를 교정합니다.
  원문의 어투와 의미를 보존하면서 읽기 쉽게 다듬습니다.

  사용법:
    /stt-correct-pro:correct <파일경로>

  예시:
    /stt-correct-pro:correct ./회의록.md
    /stt-correct-pro:correct ./interview.txt
---

`$ARGUMENTS`에서 파일 경로를 파싱합니다.

- 파일 경로가 없으면 사용자에게 교정할 파일 경로를 요청
- 파일이 존재하지 않으면 오류 메시지를 출력하고 종료
- 지원 형식: `.md`, `.txt`

파일을 읽은 뒤 `stt-correct-pro` 스킬의 교정 절차(1단계~4단계)를 그대로 따라 교정을 수행합니다.
교정된 텍스트로 원본 파일을 덮어쓰고, 완료를 안내합니다.
