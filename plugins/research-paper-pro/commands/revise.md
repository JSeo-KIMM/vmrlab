---
name: revise
description: >
  Revise an academic paper based on a peer review file.
  Requires a review file (.md) and a paper file (.pdf or .md).
  Usage: /research-paper-pro:revise <review_file> <paper_file>
  Example: /research-paper-pro:revise ./review-detail.md ./my_paper.md
  Example: /research-paper-pro:revise ./review-simple.md ./my_paper.pdf
---

$ARGUMENTS 를 확인합니다.

$ARGUMENTS 에서 두 개의 파일 경로를 파악합니다:
- **리뷰 파일**: `review-simple.md` 또는 `review-detail.md` 등 리뷰가 담긴 `.md` 파일
- **논문 파일**: 수정 대상인 `.pdf` 또는 `.md` 파일

두 파일이 모두 있으면 @paper-reviser 에게 위임합니다.

파일이 하나만 있거나 없으면 사용자에게 다음과 같이 질문합니다:

> 논문 수정을 위해 두 개의 파일이 필요합니다:
>
> **1. 리뷰 파일** — `review-simple.md` 또는 `review-detail.md` (리뷰어 코멘트가 담긴 파일)
> **2. 논문 파일** — 수정할 원본 논문 (`.pdf` 또는 `.md`)
>
> 두 파일의 경로를 함께 알려주세요. (예: `./review-detail.md ./my_paper.md`)

파일 경로가 완성되면 @paper-reviser 에게 위임합니다.
