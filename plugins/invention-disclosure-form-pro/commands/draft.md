---
description: |
  새로운 발명 아이디어를 KIMM 직무발명 내용 설명서 양식에 맞춰 작성한다.
  부족한 정보는 사용자에게 질문하면서 채워가며, 필요시 도면/다이어그램용
  편집 가능한 pptx 파일을 함께 생성한다.

  사용법:
    /invention-disclosure-form-pro:draft <아이디어 텍스트 또는 파일경로>
    /invention-disclosure-form-pro:draft <아이디어> --no-figure
    /invention-disclosure-form-pro:draft <아이디어> --output=<경로>

  옵션:
    --no-figure   도면/다이어그램 생성을 건너뜀 (텍스트만 작성)
    --output=DIR  출력 폴더 지정 (기본: 입력 파일과 같은 폴더, 텍스트 입력시 현재 폴더)

  예시:
    /invention-disclosure-form-pro:draft ./아이디어.md
    /invention-disclosure-form-pro:draft "스튜어트 플랫폼 기반 마스터 장치..."
    /invention-disclosure-form-pro:draft ./idea.md --no-figure
---

# KIMM 직무발명 내용 설명서 작성 커맨드

## 실행 절차

### Step 1: 입력 파싱
`$ARGUMENTS`에서 다음을 추출한다:
- **아이디어 입력**: 파일 경로(`.md`, `.txt`)이면 Read로 읽고, 그렇지 않으면 텍스트 자체를 아이디어로 간주
- **옵션**: `--no-figure`, `--output=<경로>`

파일 경로로 보이는데 존재하지 않으면 사용자에게 확인 후 텍스트로 처리한다.

### Step 2: invention-drafter 에이전트 호출
`invention-drafter` 서브에이전트에게 아래를 전달한다:
- 아이디어 본문 (파일 내용 또는 텍스트)
- 입력 파일 경로 (있을 경우)
- 출력 폴더 경로 (--output 또는 입력 파일 폴더 또는 cwd)
- 도면 생성 여부 (--no-figure가 없으면 true)

### Step 3: 결과 안내
에이전트 완료 후:
1. 생성된 파일 목록 (`.md`, 필요시 `.pptx`)
2. 작성된 발명 명칭과 5번 항목(보호받고 싶은 권리) 요약
3. 추가 검토가 필요한 부분 안내 (예: 유사특허 조사가 비어있다면 명시)

## 에이전트 전달 프롬프트

다음 내용을 invention-drafter 에이전트에게 전달한다:

```
새로운 발명 아이디어를 KIMM 직무발명 내용 설명서 양식에 맞춰 작성해주세요.

[아이디어 본문]:
(파일 내용 또는 텍스트 전체)

[입력 파일]: $ARGUMENTS에서 파싱된 파일 경로 (없으면 N/A)
[출력 폴더]: 결정된 출력 폴더 경로
[도면 생성]: true | false

작업 절차:
1. 아이디어 분석 후 KIMM 양식 6개 항목 각각에 대해 정보 충분성을 점검
2. 부족한 항목이 있으면 AskUserQuestion으로 한 번에 최대 4개씩 질문하여 보완
3. 사용자 작성 스타일(~함체, 개조식)로 초안 작성
4. 필요한 도면이 있으면 캡션 정의 후 편집용 pptx 파일도 생성
5. 결과 파일 저장 후 경로 보고
```
