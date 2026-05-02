# Architecture Guide — 시스템 아키텍처 작성

`type: "architecture"` 다이어그램 작성 시 본 가이드를 따른다.

## kind → 도형 매핑

| kind | 도형 | 의미 |
|---|---|---|
| `service` | 라운드 사각형 (반경 0.15") | 일반 서비스/모듈/API |
| `database` | 원통형 (상단·하단 타원 + 직사각) | RDBMS, NoSQL, 스토리지 |
| `queue` | 평행사변형 양단 직선 | 메시지 큐, 스트림 (Kafka 등) |
| `model` | 6각형 또는 라운드 사각형(굵은 테두리) | AI/ML 모델 추론 |
| `user` | 사람 아이콘 (원 + 사다리꼴) | 최종 사용자, 운영자 |
| `external` | 점선 외곽 라운드 사각형 | 외부 시스템·디바이스 |
| `note` | 직각 사각형(좌상단 접힘) | 메모, 설명 라벨 |

## 레이아웃 휴리스틱

- **계층 구조**가 명확하면 `direction: "TB"`, 위에서 아래로 사용자 → 프론트 → 백 → 데이터 순으로 행 배치.
- **데이터 흐름**이 핵심이면 `direction: "LR"`, 좌→우.
- **그룹**(`groups[]`)으로 계층/서브넷/zone을 묶는다. 예: `엣지 단`, `서버 단`, `데이터 단`.
- 격자는 `rows × cols ≤ 4 × 4`를 권장. 그 이상이면 슬라이드 분할.

## 그룹 활용

```json
"groups": [
  { "id": "g_edge",   "label": "엣지 단", "row": 0, "col": 0, "rowspan": 3, "colspan": 1 },
  { "id": "g_server", "label": "서버 단", "row": 0, "col": 1, "rowspan": 3, "colspan": 2 },
  { "id": "g_data",   "label": "데이터 단", "row": 0, "col": 3, "rowspan": 3, "colspan": 1 }
]
```

각 노드의 `group` 필드에 그룹 id를 지정해 시각적으로 묶는다.

## 자주 쓰는 패턴

### 3-tier 클라이언트-서버-DB
```
[user] ─→ [frontend] ─→ [backend service] ─→ [database]
```
1행 4열 또는 4행 1열 (LR/TB).

### 마이크로서비스 + 큐
```
[gateway] ─→ [service A] ─→ [queue] ─→ [service B] ─→ [DB]
                  │
                  └─→ [model inference]
```
2행 5열 격자, model에 `accent: true`.

### 엣지 + 클라우드
```
[엣지 단]                  [서버 단]                 [데이터 단]
[user]                                                     
  │                                                        
[device] ──→ [api] ──→ [model] ──→ [queue] ──→ [DB]
```
groups 3개로 zone 구분.

## 라벨 작성 규칙

- 서비스명은 대문자/약어 그대로 (REST API, gRPC, GPU Worker).
- 노드 라벨은 명사구. 동사형 금지. "데이터 적재" → "ETL 파이프라인".
- 한 노드 최대 2줄, 줄당 8~12자.

## 외부 시스템 표기

- 외부 API/디바이스는 `kind: "external"`로 점선 외곽선 적용.
- 클라우드 서비스(AWS/GCP/Azure)는 `external` + 서비스명 그대로 (예: "S3", "BigQuery").
