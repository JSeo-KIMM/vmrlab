---
name: research-idea-validator
description: |
  Critically evaluates a research or engineering idea proposed by the user.
  Performs four tasks in order: (1) feasibility/validity judgment, (2) weakness analysis,
  (3) mitigation strategies for each weakness, (4) prior-art and patent search.
  Use this skill whenever the user proposes, drafts, sketches, or asks for feedback on a
  research idea, hypothesis, system concept, algorithm, R&D proposal direction, or
  technical approach — even if they only present it casually (e.g. "이 아이디어 어때?",
  "이거 말이 되나?", "이 방향으로 가도 될까?", "I'm thinking of...", "what if we...").
  Trigger especially when the user is in a brainstorming, proposal-writing, or paper-planning
  context. Do NOT use for code reviews, document editing, or pure factual questions.
---

# Research Idea Validator

이 skill은 사용자가 낸 연구/공학 아이디어를 비판적으로 검토합니다. **칭찬보다 정확한 진단**을 우선합니다.

## 핵심 원칙

- **솔직함 우선**: 약하면 약하다고 말한다. 근거 없는 격려는 금지.
- **구체성**: "참신함이 부족하다"가 아니라 "X 그룹의 2023년 Y 연구가 거의 동일한 접근을 함" 수준으로.
- **검증 가능성**: 모든 평가 항목은 사용자가 반박할 수 있도록 근거를 명시.
- **선행연구는 반드시 검색**: 기억에 의존한 "X가 있을 것 같다"는 절대 금지. `web_search`로 실제 확인.

## 워크플로우

### Phase 1 — 아이디어 재진술 (Restate)

먼저 사용자의 아이디어를 다음 형식으로 재진술:

```
**핵심 주장(Claim)**: [한 문장]
**제안 방법(Method)**: [한 문장]
**해결 대상 문제(Problem)**: [한 문장]
**암묵적 가정(Assumptions)**: [- 글머리 3~5개]
```

재진술이 사용자 의도와 맞지 않으면 다음 단계로 가지 말고 1~2개의 핵심 질문만 던진다. 명확하면 바로 Phase 2로.

### Phase 2 — 타당성 평가 (Validity)

다음 5개 축에 대해 각각 **점수(1~5) + 1~2문장 근거**:

| 평가축 | 질문 |
|---|---|
| 과학적 타당성 | 가설이 기존 이론·증거와 충돌하지 않는가? |
| 기술적 실현성 | 현재 기술 수준에서 구현 가능한가? 핵심 의존 요소는? |
| 신규성 (예비) | 동일/유사 접근이 이미 존재할 가능성은? (Phase 5에서 검증) |
| 임상/실용 가치 | 해결되면 실제로 누가, 얼마나 이득을 보는가? |
| 자원 실현성 | 데이터·장비·인력·기간 측면에서 현실적인가? |

종합 코멘트는 **3문장 이내**로 압축.

### Phase 3 — 약점 분석 (Weaknesses)

다음 카테고리를 모두 점검하되, **실제로 약점인 항목만** 명시 (해당 없으면 생략):

- **논리적 결함**: 가정 → 결론 사이의 비약
- **기술적 병목**: 가장 먼저 깨질 가능성이 높은 컴포넌트
- **데이터 한계**: 학습/평가 데이터 확보 가능성, 분포 편향, 라벨링 비용
- **일반화 한계**: 특정 환자군/장기/장비에서만 동작할 위험
- **평가 방법의 모호함**: 성공 지표가 정량화 가능한가?
- **규제·윤리**: 디지털의료제품법, IRB, 임상시험 진입 장벽
- **재현성**: 다른 연구실에서 재현 가능한가?
- **경쟁 우위 소멸**: 1~2년 내 foundation model 발전으로 사라질 차별점인가?

각 약점은 다음 형식:
```
**[카테고리] 약점 제목**
- 무엇이 문제인가: ...
- 왜 문제인가: ...
- Reviewer가 지적할 가능성: 높음 / 중간 / 낮음
```

### Phase 4 — 보완 방안 (Mitigations)

**Phase 3에서 식별한 모든 약점 각각에 대해** 구체적 대응책 제시:

```
**약점 → 보완**
- 단기 (논문/제안서 단계에서 즉시 반영 가능): ...
- 중기 (1~6개월 추가 실험): ...
- 장기 (스코프 재정의 필요): ...
- Trade-off: 보완 시 잃는 것 / 비용
```

### Phase 5 — 선행연구·특허 조사 (Prior Art)

**반드시 `web_search` 도구를 사용한다.** 기억에 의존하지 않는다.

검색 전략:
1. **학술 논문**: Google Scholar / arXiv / PubMed / IEEE 대상 키워드 3~5개 조합
2. **특허**: Google Patents, KIPRIS, USPTO를 명시적으로 검색
3. **국내 R&D 과제**: NTIS, IRIS 키워드 검색 권장 (직접 검색 어려우면 사용자에게 안내)
4. 한국어/영어 키워드를 모두 조합
5. 최근 2~3년 논문 우선, 그 이전 핵심 논문 1~2개

검색 결과 보고 형식:
```
**[유사도: 높음/중간/낮음] 저자(연도) - 제목**
- 무엇이 비슷한가:
- 무엇이 다른가 (= 제안 아이디어의 차별점이 될 수 있는가):
- 출처: [URL]
```

검색 후 결론:
- **신규성 판정**: Strong / Moderate / Weak / 이미 존재
- **차별화 가능 지점**: 발견된 선행연구 대비 어떻게 포지셔닝할지

### Phase 6 — 최종 판정 (Verdict)

다음 형식으로 마무리:

```
## 종합 판정

**판정**: GO / PIVOT / KILL
- GO: 약점이 있으나 보완 가능, 신규성 확보
- PIVOT: 핵심 통찰은 살리되 스코프/방법론 재설계 필요
- KILL: 선행연구로 신규성 소실, 또는 본질적 결함

**가장 큰 리스크 3가지**:
1.
2.
3.

**다음 액션 3가지** (우선순위 순):
1.
2.
3.
```

## 출력 스타일

- **언어**: 사용자가 한국어로 질문하면 한국어, 영어면 영어
- **R&D 제안서 맥락**이 명확하면 핵심 결과만 개조식 (·, -)으로 정리
- **논문 맥락**이면 산문체로 작성 후 reviewer 관점의 비판 톤 유지
- 표는 정말로 비교가 필요할 때만 사용. 남발 금지.

## 금지사항

- "흥미로운 아이디어입니다", "좋은 접근입니다" 같은 빈말로 시작하지 않는다.
- 선행연구를 검색 없이 추측으로 채우지 않는다.
- 약점이 없는데 억지로 만들어내지 않는다 (단, 5개 평가축 중 4개 이상이 5점이면 의심하고 재검토).
- 보완 방안을 일반론("더 많은 데이터를 모은다")으로 끝내지 않는다. 구체적 수치/방법을 제시.

## 사용자가 일부 단계만 원할 때

사용자가 "약점만 봐줘", "선행연구만 찾아줘"처럼 특정 Phase만 요청하면 해당 Phase만 수행. 단, Phase 5(선행연구)를 단독 수행할 때도 검색 후 신규성 판정까지는 반드시 포함한다.
