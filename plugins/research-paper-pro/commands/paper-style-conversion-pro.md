---
name: paper-style-conversion-pro
description: >
  Convert a draft Markdown paper into a finished .docx that matches a
  journal/conference template. Reads a draft .md and a template .docx/.doc,
  analyzes the template's styles, margins, fonts, heading hierarchy and table
  styles, then refills it with the draft's title, authors, body, equations
  (as native Word equations), figures, tables and references. Preserves the
  draft's content; logs any content-level change to a separate file.
  Usage: /research-paper-pro:paper-style-conversion-pro <draft.md> <template.docx>
  Example: /research-paper-pro:paper-style-conversion-pro ./my_draft.md ./journal_form.docx
---

$ARGUMENTS 를 확인합니다.

$ARGUMENTS 에 draft `.md` 파일 경로와 양식 `.docx`(또는 `.doc`) 파일 경로가
모두 포함되어 있으면, 두 경로를 @paper-style-converter 에게 위임합니다.

두 경로 중 하나라도 없으면 사용자에게 질문합니다:

> 논문 양식 변환에는 두 파일이 필요합니다.
>
> 1. **draft 원고** (`.md`) — 논문 내용
> 2. **양식 파일** (`.docx` 또는 `.doc`) — 저널/학회 제출 양식
>
> 두 경로를 알려주세요. 양식 파일의 폰트·여백·줄간격·제목 스타일을 분석해
> draft 내용을 그 양식에 맞춰 채운 `.docx`를 만들어 드립니다.
>
> 예: `/research-paper-pro:paper-style-conversion-pro ./my_draft.md ./journal_form.docx`

두 경로가 확인되면 @paper-style-converter 에게 위임합니다.
