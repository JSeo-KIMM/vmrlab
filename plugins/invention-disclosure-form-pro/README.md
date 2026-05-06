# invention-disclosure-form-pro

KIMM(한국기계연구원) **직무발명 내용 설명서** 작성을 보조하는 Claude Code 플러그인.

발명 아이디어 텍스트 또는 마크다운 파일을 입력하면, 사용자의 기존 작성 스타일(`~함`체, 개조식)을 그대로 따라 KIMM 양식의 6개 표준 항목으로 정리해 준다. 부족한 정보가 있으면 사용자에게 직접 질문하면서 보완하고, 도면이 필요한 경우 편집 가능한 `.pptx` 파일을 같은 폴더에 함께 생성한다.

## 설치

`marketplace.json`에 본 플러그인이 등록되어 있다면 `/plugin install invention-disclosure-form-pro` 로 설치한다.

## 사용법

```
/invention-disclosure-form-pro:draft <아이디어 텍스트 또는 파일경로>
/invention-disclosure-form-pro:draft <아이디어> --no-figure
/invention-disclosure-form-pro:draft <아이디어> --output=<폴더경로>
```

### 예시

```
# 마크다운 파일을 입력
/invention-disclosure-form-pro:draft ./아이디어_초음파혈관검출.md

# 짧은 텍스트로 시작
/invention-disclosure-form-pro:draft "스튜어트 플랫폼 기반 마스터 장치를 ANN으로 정기구학 해석..."

# 도면 생성 건너뛰기
/invention-disclosure-form-pro:draft ./idea.md --no-figure
```

## 출력

- `직무발명_<요약명>_<YYYYMMDD>.md` — 6개 항목으로 정리된 직무발명 내용 설명서 본문
- `직무발명_<요약명>_<YYYYMMDD>_도면.pptx` — (필요시) 캡션과 기본 도형 placeholder가 배치된 편집 가능 PPT

## 작성되는 양식 구조

KIMM 표준 양식 6개 항목:

1. 발명(고안)의 명칭
2. 발명(고안)의 배경
   - (1) 유사특허 또는 출원
   - (2) 배경문헌 또는 관련특허
   - (3) 발명(고안)과 관련된 본 연구원의 전출원
3. 종래기술의 설명과 그것의 문제점
4. 본 발명의 상세한 설명 (목적/구성/효과)
5. 보호받고 싶은 권리
6. 추가자료

## 인터뷰 모드

플러그인은 입력된 아이디어가 6개 항목을 채우기에 부족하다고 판단하면 **AskUserQuestion** 도구로 한 번에 최대 4개씩 질문을 묶어 진행한다. 한 라운드가 끝나면 정보가 충분한지 재평가하고, 최대 2~3 라운드까지만 묻고 작성에 진입한다.

질문 예시:
- 적용 도메인 (의료/산업/소프트웨어)
- 유사특허 보유 여부
- 본 연구원 전출원 여부
- 도면 필요 종류

## 도면 생성

도면이 필요한 경우 본문에 `<그림 N. 캡션>` 마커를 삽입하고, 동일 캡션을 가진 슬라이드들을 가진 `.pptx` 파일을 출력 폴더에 생성한다. 슬라이드는 다음과 같이 구성됨:

- 제목: `그림 N. 캡션`
- 가이드 노트: 어떤 시각화가 적합한지 안내문
- 도형 placeholder: 발명 유형에 맞춰 적층(stack) / 흐름도(flowchart) / 시스템 블록 등을 기본 배치

PowerPoint 또는 한컴오피스에서 열어 자유롭게 도형을 추가/수정/이동할 수 있다.

## 구성 파일

```
invention-disclosure-form-pro/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── commands/
│   └── draft.md                              # /invention-disclosure-form-pro:draft 커맨드
├── agents/
│   └── invention-drafter.md                  # 메인 작성 에이전트
├── skills/
│   └── invention-disclosure-form-pro/
│       ├── SKILL.md                          # 메인 스킬
│       └── references/
│           ├── form-structure.md             # 양식 6개 항목 구조
│           ├── writing-style.md              # ~함체 등 문체 규칙
│           ├── interview-protocol.md         # 인터뷰 질문 전략
│           ├── figure-generation.md          # pptx 도면 생성 가이드
│           └── example-titles.md             # 발명 명칭 작명 가이드
└── examples/
    ├── example1-bending-sensor.md            # 비접촉식 휨 센서
    ├── example2-marker.md                    # 방사선/적외선 동시 마커
    ├── example3-doppler.md                   # 도플러 혈관 검출
    └── example4-stewart-platform.md          # ANN 기반 스튜어트 플랫폼
```

## 라이선스 / 작성자

- Author: Joonho
- 사내(KIMM) 직무발명 작성 보조용
