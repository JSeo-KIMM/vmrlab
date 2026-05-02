# IR Spec — Diagram 중간 표현 (intermediate representation)

자연어 프롬프트든 구조화 YAML이든 모두 본 IR(JSON)로 수렴한 뒤 렌더링한다.

## 최상위 구조

```json
{
  "type": "flowchart" | "architecture",
  "title": "다이어그램 제목 (슬라이드 상단 표기)",
  "subtitle": "선택, 부제 (없으면 생략)",
  "nodes": [ ... ],
  "edges": [ ... ],
  "groups": [ ... ],
  "layout": {
    "rows": <int>,
    "cols": <int>,
    "direction": "LR" | "TB"
  },
  "style": {
    "preset": "gov",
    "mood": "technical-report" | "clarity" | "tech-focus" | "growth"
  }
}
```

`type`·`title`·`nodes`·`edges`·`layout`은 필수. 나머지는 선택.

## Node

```json
{
  "id": "n1",
  "label": "표시 텍스트 (한글, 줄바꿈은 \\n)",
  "kind": "start" | "process" | "decision" | "end" | "io"
        | "service" | "database" | "queue" | "user" | "external" | "model" | "note",
  "row": <int>,
  "col": <int>,
  "rowspan": <int, default 1>,
  "colspan": <int, default 1>,
  "group": "g1" | null,
  "accent": false
}
```

- `id` — 고유. 영문/숫자/`_`만 사용.
- `kind` — 도형 결정. flowchart는 `start`·`process`·`decision`·`end`·`io`, architecture는 `service`·`database`·`queue`·`user`·`external`·`model`·`note` 사용.
- `row`/`col` — 0-base 격자 좌표(0,0이 좌상단). 자동 레이아웃 대신 명시적 좌표를 사용한다.
- `rowspan`/`colspan` — 큰 블록(컨테이너)에 사용.
- `group` — 같은 그룹은 박스로 묶음(서브넷·계층 등). `groups`에서 정의.
- `accent: true` — 강조색 적용(전체에서 1~3개만).

## Edge

```json
{
  "from": "n1",
  "to": "n2",
  "label": "선택, 화살표 위 표기",
  "style": "solid" | "dashed" | "dotted",
  "arrow": "single" | "double" | "none",
  "bend": "auto" | "horizontal" | "vertical"
}
```

`style`·`arrow`·`bend` 미지정 시 각각 `solid`·`single`·`auto`.

## Group (선택)

```json
{
  "id": "g1",
  "label": "그룹 제목 (예: 데이터 계층)",
  "row": <int>,
  "col": <int>,
  "rowspan": <int>,
  "colspan": <int>
}
```

그룹은 회색 배경 라운드 사각형으로 그려지며 `label`은 좌상단에 작게 표기.

## Layout 규칙

- `rows`·`cols`는 전체 격자 크기. 모든 `node.row + rowspan ≤ rows`, `node.col + colspan ≤ cols`을 만족해야 한다.
- `direction`은 화살표 자동 굴절 시 우선축. `LR`(좌→우)이 기본.
- 격자는 슬라이드 본문 영역(13.333" × 7.5" 중 상단 타이틀 1" 제외, 좌우 0.6" 마진)을 균등 분할한다.

## 검증 체크리스트

렌더 직전 다음을 확인한다.

- 모든 `edges[i].from`, `edges[i].to`가 `nodes[].id`에 존재.
- 노드 격자 좌표가 겹치지 않음(같은 셀에 두 노드 금지).
- `accent: true` 노드 개수 ≤ 3.
- `kind`가 `type`에 부합(flowchart에 `database` 같은 architecture 도형 금지).
- `layout.rows ≤ 6`, `layout.cols ≤ 7` (가독성 보장).

## 최소 예시 — flowchart

```json
{
  "type": "flowchart",
  "title": "강화학습 학습 루프",
  "layout": { "rows": 1, "cols": 5, "direction": "LR" },
  "style": { "preset": "gov", "mood": "tech-focus" },
  "nodes": [
    { "id": "env",   "label": "환경",      "kind": "start",   "row": 0, "col": 0 },
    { "id": "obs",   "label": "관측",      "kind": "io",      "row": 0, "col": 1 },
    { "id": "agent", "label": "에이전트",  "kind": "process", "row": 0, "col": 2, "accent": true },
    { "id": "act",   "label": "행동",      "kind": "io",      "row": 0, "col": 3 },
    { "id": "rew",   "label": "보상",      "kind": "end",     "row": 0, "col": 4 }
  ],
  "edges": [
    { "from": "env",   "to": "obs" },
    { "from": "obs",   "to": "agent" },
    { "from": "agent", "to": "act" },
    { "from": "act",   "to": "rew" },
    { "from": "rew",   "to": "env", "label": "feedback", "style": "dashed" }
  ]
}
```

## 최소 예시 — architecture

```json
{
  "type": "architecture",
  "title": "초음파 자가검진 시스템 구성",
  "layout": { "rows": 3, "cols": 3, "direction": "TB" },
  "style": { "preset": "gov", "mood": "technical-report" },
  "groups": [
    { "id": "g_edge",   "label": "엣지 단",    "row": 0, "col": 0, "rowspan": 3, "colspan": 1 },
    { "id": "g_server", "label": "서버 단",    "row": 0, "col": 1, "rowspan": 3, "colspan": 2 }
  ],
  "nodes": [
    { "id": "user",  "label": "환자",         "kind": "user",     "row": 0, "col": 0 },
    { "id": "probe", "label": "휴대 프로브",   "kind": "external", "row": 1, "col": 0 },
    { "id": "app",   "label": "모바일 앱",     "kind": "service",  "row": 2, "col": 0 },
    { "id": "api",   "label": "REST API",     "kind": "service",  "row": 0, "col": 1, "colspan": 2 },
    { "id": "model", "label": "VLM 추론",     "kind": "model",    "row": 1, "col": 1, "accent": true },
    { "id": "queue", "label": "메시지 큐",     "kind": "queue",    "row": 1, "col": 2 },
    { "id": "db",    "label": "결과 DB",      "kind": "database", "row": 2, "col": 1, "colspan": 2 }
  ],
  "edges": [
    { "from": "user",  "to": "app" },
    { "from": "probe", "to": "app" },
    { "from": "app",   "to": "api" },
    { "from": "api",   "to": "model" },
    { "from": "model", "to": "queue" },
    { "from": "queue", "to": "db" }
  ]
}
```
