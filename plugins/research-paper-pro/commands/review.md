---
name: review
description: >
  Perform a peer review on an academic paper in simple or detail mode.
  Optionally specify mode and file path as arguments.
  Usage: /research-paper-pro:review [simple|detail] <file_path>
  Example: /research-paper-pro:review simple ./my_paper.pdf
  Example: /research-paper-pro:review detail ./my_paper.pdf
  If no mode is specified, the user will be asked to choose.
---

$ARGUMENTS 를 확인합니다.

$ARGUMENTS 에 "simple" 또는 "detail" 키워드가 포함되어 있으면
해당 모드와 파일 경로를 그대로 @paper-reviewer 에게 위임합니다.

포함되어 있지 않으면 먼저 사용자에게 다음과 같이 질문합니다:

> 리뷰 모드를 선택해 주세요:
>
> **1. Simple** — 가장 중요한 지적사항 5개 이내, 간결한 요약
> **2. Detail** — 전체 체크리스트(A/B/C/D) 기반 10~20개 항목, 상세 분석
>
> 모드 선택 후 파일 경로도 함께 알려주세요. (예: `simple ./my_paper.pdf`)

선택이 완료되면 **모드명과 파일 경로**를 함께 @paper-reviewer 에게 위임합니다.
