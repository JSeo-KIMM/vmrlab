---
name: svgtopptx-pro
description: >
  SVG 다이어그램/슬라이드 파일을 편집 가능한 PPTX(PowerPoint)로 변환하는 스킬.
  SVG 내의 rect, text, circle, line, polygon, path 요소를 파워포인트 네이티브 도형(사각형, 텍스트박스, 원, 연결선, 화살표 등)으로 변환하여
  모든 요소를 개별 편집할 수 있게 한다.
  'SVG를 PPTX로', 'SVG 변환', 'SVG를 파워포인트로', 'svg to pptx', '다이어그램을 편집 가능하게',
  'SVG 슬라이드 변환' 등의 요청이 들어오면 이 스킬을 사용할 것.
---

# SVG → 편집 가능 PPTX 변환기

SVG 파일의 도형·텍스트·화살표 등을 PowerPoint 네이티브 개체로 변환한다.
변환 후 모든 요소를 PowerPoint에서 개별 선택·수정·이동할 수 있다.

---

## 지원 SVG 요소

| SVG 요소 | PPTX 변환 결과 |
|----------|---------------|
| `<rect>` | 둥근사각형 (fill, stroke, 모서리 반경 반영) |
| `<text>` | 텍스트박스 (폰트 크기, 굵기, 색상, 정렬 반영) |
| `<circle>` | 타원 (fill, stroke, 점선 반영) |
| `<line>` | 연결선 (색상, 두께, 점선, 화살표 반영) |
| `<polygon>` | 삼각형 도형 (화살촉 등) |
| `<path>` | 선분 연결 (M/L/Q/C 경로를 직선으로 근사) |
| `<g>` | 재귀적으로 내부 요소 처리 |

---

## 사용 절차

### 1단계: 입력 확인

사용자로부터 변환할 SVG 파일 또는 SVG가 들어있는 폴더 경로를 받는다.

- 경로가 지정되지 않으면 **현재 작업 폴더**의 `*.svg` 파일을 자동 탐색한다
- 파일이 없으면 사용자에게 경로를 재확인한다

### 2단계: 스크립트 탐색

변환 스크립트를 다음 순서로 찾는다:

1. Glob: `**/svgtopptx-pro/scripts/svg_to_pptx.py`
2. Glob: `**/svg_to_pptx.py`
3. 찾지 못하면 사용자에게 안내 후 중단

### 3단계: 의존성 확인

스크립트 실행 전 필요한 Python 패키지를 확인한다:

```bash
pip show python-pptx lxml 2>/dev/null || pip install python-pptx lxml
```

### 4단계: 변환 실행

```bash
python svg_to_pptx.py <입력_경로> [출력_경로.pptx]
```

**입력 경로 규칙:**
- 폴더 → 폴더 내 모든 `*.svg`를 슬라이드 1장씩으로 변환 (기본 출력: `<폴더>/output.pptx`)
- 단일 SVG → 해당 파일만 변환 (기본 출력: `<파일명>.pptx`)

**출력 경로:**
- 사용자가 명시하면 해당 경로 사용
- 명시하지 않으면 기본 규칙 적용

### 5단계: 결과 보고

변환 완료 후 다음을 보고한다:

- 출력 파일 경로
- 슬라이드 수
- 각 슬라이드의 도형 수

---

## 변환 상세

### 좌표 매핑
- SVG `viewBox`를 기준으로 16:9 와이드스크린(13.333" × 7.5") 슬라이드에 비례 축소
- 종횡비 유지, 중앙 정렬

### 텍스트 처리
- `text-anchor` → PowerPoint 정렬 (start=왼쪽, middle=가운데, end=오른쪽)
- `font-size` (px) → pt 변환 (×0.75 비율)
- 기본 폰트: 맑은 고딕 (Malgun Gothic)
- `font-weight` 500 이상 → 굵게

### 색상 처리
- `#RRGGBB`, `rgb(r,g,b)`, `rgba(r,g,b,a)` 모두 지원
- `fill="none"` → 배경 투명
- `stroke="none"` → 테두리 없음

### 화살표
- `marker-end="url(#arrow)"` → 연결선 끝에 삼각형 화살촉

### 점선
- `stroke-dasharray` → PowerPoint DASH 스타일

---

## 제한사항

- **그라데이션/패턴**: SVG gradient, pattern fill은 무시된다 (단색으로 대체)
- **필터/효과**: SVG filter (drop-shadow, blur 등)는 반영되지 않는다
- **클리핑**: clipPath는 무시된다
- **복잡한 path**: 베지에 곡선(Q, C)은 끝점 직선 연결로 근사된다
- **텍스트 래핑**: SVG에서 여러 줄 텍스트는 개별 `<text>` 요소로 존재해야 한다
- **이미지 임베드**: `<image>` 요소는 현재 지원하지 않는다

---

## 주의사항

- **편집 목적**: 이 변환의 핵심은 "편집 가능성"이다. 시각적 완벽 재현보다 개별 도형 편집이 우선이다.
- **폰트**: 시스템에 맑은 고딕이 없으면 PowerPoint가 대체 폰트를 사용한다.
- **파일 덮어쓰기**: 출력 경로에 기존 파일이 있으면 덮어쓴다.
