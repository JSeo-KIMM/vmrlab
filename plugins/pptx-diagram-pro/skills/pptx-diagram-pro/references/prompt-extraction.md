# Prompt Extraction Guide — 자연어 → IR 변환

자연어 프롬프트(예: "강화학습 학습 루프 다이어그램 그려줘. 환경·에이전트·보상·관측이 들어가게")를
[`ir-spec.md`](ir-spec.md)의 IR JSON으로 변환하는 절차.

## 4단계 추출

### 1. 다이어그램 유형 판정 (type)

키워드로 분류한다.

- **flowchart 신호**: "프로세스", "단계", "흐름", "파이프라인", "워크플로우", "절차", "루프", "→", 시간/순서 표현 ("먼저", "다음", "마지막")
- **architecture 신호**: "구성", "아키텍처", "시스템", "모듈", "서비스", "DB", "큐", "API", "프론트엔드/백엔드", "엣지/클라우드"

둘 다 가능하면 사용자에게 1회 짧게 확인. 명확하면 바로 진행한다.

### 2. 노드 추출 (nodes)

- 명사구·고유명사·약어를 후보로 뽑는다.
- 같은 개체의 다른 표현은 하나로 통합 (예: "DB", "데이터베이스", "결과 저장소" → 1개 노드).
- `kind` 결정:
  - flowchart: 시작 동사("시작", "입력") → `start`. 판단/조건 → `decision`. 종결("저장", "출력", "보고") → `end`. 입출력 매개체 → `io`. 그 외 → `process`.
  - architecture: "DB·저장소" → `database`, "큐·스트림" → `queue`, "모델·추론" → `model`, "사용자·운영자" → `user`, "외부 시스템·API·디바이스" → `external`, 그 외 → `service`.
- 핵심 차별화 노드 1~3개에 `accent: true`.

### 3. 엣지 추출 (edges)

- 동사·전치사·기호로 관계를 잡는다: "→", "전달", "호출", "→", "응답", "피드백".
- 방향이 명시되지 않으면 "원인 → 결과" 또는 "데이터 출발 → 도착" 휴리스틱.
- 피드백·옵션 경로는 `style: "dashed"`.
- 엣지 라벨은 동사형 짧게 ("호출", "응답", "feedback"). 6자 이내 권장.

### 4. 격자 좌표 추정 (layout + row/col)

- flowchart: 단계 수가 N이면 `rows: 1, cols: N`(분기 없음) 또는 `rows: 분기수+1, cols: 단계수`.
- architecture: 계층 수 = rows, zone 수 = cols. 사용자→프론트→백→데이터를 위→아래(TB) 또는 좌→우(LR).
- 항상 `node.row + rowspan ≤ rows`, `node.col + colspan ≤ cols`.
- `direction`은 시간/순차 흐름 → `LR`, 계층 → `TB`.

## 검증 후 출력

추출이 끝나면 [`ir-spec.md`](ir-spec.md)의 검증 체크리스트 5개 항목을 확인한 뒤 JSON을 출력한다.
사용자에게 IR을 보여주고 수정 의견을 1회 받는다 (자명하면 생략하고 바로 렌더).

## 모호할 때 질문 1~2개만

다음 경우에만 사용자에게 질문(과도한 질문 금지):

- type이 flowchart/architecture 중 어느 쪽인지 모를 때
- 노드 5개 이상 추출되고 그 중 같은 개체 의심이 강한 경우 (병합 의도 확인)

그 외는 추정으로 진행하고 결과를 보여준 뒤 사용자가 수정 요청 시 반영한다.

## 입력 예시 → IR 변환

**입력**: "초음파 자가검진 시스템 그려줘. 환자가 휴대 프로브로 모바일 앱 통해 REST API 호출하면, VLM 추론하고 메시지 큐 거쳐서 결과 DB에 저장."

**판정**:
- type → architecture (구성/모듈 키워드)
- 노드 7개: user(환자), external(휴대 프로브), service(모바일 앱), service(REST API), model(VLM, accent), queue(메시지 큐), database(결과 DB)
- 엣지 6개 (직선 흐름)
- groups 2개: 엣지 단(user/probe/app), 서버 단(api/model/queue/db)
- 격자 3행 3열, direction TB

이 결과를 IR JSON으로 만들어 [`ir-spec.md`](ir-spec.md)의 architecture 예시와 동일한 형식으로 출력.
