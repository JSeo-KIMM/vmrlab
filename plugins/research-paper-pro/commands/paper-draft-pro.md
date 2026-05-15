---
name: paper-draft-pro
description: >
  Polish a Korean draft paper written casually into a refined academic Markdown.
  Takes a .md file written in conversational Korean, interprets [] bracketed
  authoring notes, preserves figures and Fig. numbers, converts marked passages
  into equations, and asks for target word count and whether an English
  translation version is also needed.
  Usage: /research-paper-pro:paper-draft-pro <draft.md>
  Example: /research-paper-pro:paper-draft-pro ./my_draft.md
---

$ARGUMENTS 를 확인합니다.

$ARGUMENTS 에 `.md` 파일 경로가 포함되어 있으면 그 경로를 @paper-drafter 에게 위임합니다.

파일 경로가 없으면 사용자에게 다음과 같이 질문합니다:

> Polishing 할 draft 파일 경로를 알려주세요.
>
> - 한국어로 대충 써 둔 `.md` 파일을 받아 학술 스타일로 다듬어 드립니다.
> - 본문 내 `[...]` 표기는 작업 지시로 해석합니다.
> - 작업 전에 **목표 단어 수**와 **영문 번역본 생성 여부**를 여쭤보겠습니다.
>
> 예: `/research-paper-pro:paper-draft-pro ./my_draft.md`

파일 경로가 확인되면 @paper-drafter 에게 위임합니다.
