# 도면/다이어그램 생성 가이드

본문에서 그림이 필요한 지점을 식별하고, 사용자가 직접 편집 가능한 pptx 파일을 생성하는 방법.

## 도면이 필요한 신호

다음 중 하나라도 해당하면 그림 1장 이상 추천:
- 4번 구성에서 컴포넌트가 4개 이상 (시스템 구성도)
- 알고리즘이 단계 4개 이상 (흐름도)
- 물리적 적층 구조 또는 단면 묘사 (단면 모식도)
- 좌표계, 자유도, 회전축 등 방향 정보 (좌표축 다이어그램)
- 실험 결과나 비교 데이터 (그래프 자리)

## 도면 캡션 규칙

본문 삽입 형식:
```
<그림 N. 캡션 텍스트>
```

또는 사용자 기존 패턴:
```
<그림 1. 마커 제작에 필요한 재료 및 제작 방식 모식도>
<그림 2, 마커의 측면 구조>
<그림 3, 제작된 마커의 앞, 뒷면 (좌) 및 ...(우, 상)>
```

쉼표/마침표 혼용은 사용자 작성 습관 — 그대로 유지.

캡션은 본문 어느 위치에든 삽입할 수 있으나 보통 4번 구성 항목 내부 또는 6번 추가자료에 모음.

## pptx 파일 생성

### 도구 선택

`python-pptx` 라이브러리를 사용하여 편집 가능한 pptx 생성. 설치:

```bash
python -m pip install python-pptx
```

이미 환경에 있을 가능성이 높지만 import 실패 시 설치.

### 기본 스크립트 템플릿

각 그림 = 슬라이드 1장. 슬라이드에는:
1. 제목 영역 = 캡션 (예: "그림 1. 마커 제작 모식도")
2. 본문 영역 = 가이드 텍스트 (어떤 시각화가 필요한지 안내)
3. 기본 도형 placeholder (사용자가 이동/리사이즈/색 변경 가능)

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)   # 16:9
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]  # 빈 슬라이드

figures = [
    {
        "no": 1,
        "caption": "마커 제작에 필요한 재료 및 제작 방식 모식도",
        "guide": "동판 + 적외선 반사마커 + 투명 플라스틱판의 적층 순서를 좌→우 흐름으로 표현",
        "type": "stack_diagram"   # stack_diagram | flowchart | system_block | exploded_view
    },
    # ...
]

for fig in figures:
    slide = prs.slides.add_slide(blank_layout)

    # 제목
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.6))
    title.text_frame.text = f"그림 {fig['no']}. {fig['caption']}"
    title.text_frame.paragraphs[0].runs[0].font.size = Pt(20)
    title.text_frame.paragraphs[0].runs[0].font.bold = True

    # 가이드 노트 (작은 회색 텍스트)
    guide = slide.shapes.add_textbox(Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5))
    guide.text_frame.text = f"[가이드] {fig['guide']}"
    p = guide.text_frame.paragraphs[0]
    p.runs[0].font.size = Pt(11)
    p.runs[0].font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    p.runs[0].font.italic = True

    # 도형 placeholder (캔버스)
    canvas = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.5), Inches(1.7), Inches(12.3), Inches(5.5)
    )
    canvas.fill.solid()
    canvas.fill.fore_color.rgb = RGBColor(0xF5, 0xF5, 0xF5)
    canvas.line.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)
    canvas.text_frame.text = "이 영역에 도형을 자유롭게 배치하세요"
    canvas.text_frame.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
    canvas.text_frame.paragraphs[0].alignment = 2  # center

    # 도형 타입에 따른 기본 placeholder 추가
    if fig["type"] == "flowchart":
        for i, step in enumerate(["입력", "처리1", "처리2", "출력"]):
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(1 + 3*i), Inches(3.5), Inches(2), Inches(1)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = RGBColor(0xDB, 0xEA, 0xFD)
            box.text_frame.text = step

    elif fig["type"] == "stack_diagram":
        for i, layer in enumerate(["층 1", "층 2", "층 3", "층 4"]):
            box = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(5), Inches(2.5 + 0.7*i), Inches(3.5), Inches(0.6)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = RGBColor(0xE8, 0xF1, 0xFA)
            box.text_frame.text = layer

    elif fig["type"] == "system_block":
        for i, comp in enumerate(["컴포넌트 A", "컴포넌트 B", "컴포넌트 C"]):
            box = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(2 + 4*i), Inches(4), Inches(2.5), Inches(1.2)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = RGBColor(0xFF, 0xF4, 0xCC)
            box.text_frame.text = comp

prs.save(r"<출력경로>")
```

### 도형 타입 가이드

| 발명 유형 | 권장 도형 타입 |
|---|---|
| 적층 구조 (마커, 센서 패키지) | `stack_diagram` |
| 처리 단계 (알고리즘) | `flowchart` |
| 모듈 구성 (시스템) | `system_block` |
| 분해도 (메카닉) | `exploded_view` (수동 배치 권장) |
| 좌표축/자유도 | 화살표 도형(MSO_SHAPE.UP_DOWN_ARROW 등) 조합 |

### 슬라이드 마스터 톤

- 16:9 비율 (13.333 × 7.5 inches)
- 배경 흰색
- 제목 폰트 20pt, 본문 14pt 기본
- 색상은 옅은 파스텔(연파랑 #DBEAFD, 연노랑 #FFF4CC) — 흑백 인쇄 시에도 가독 유지

## 실행 절차

1. 본문 작성 중 그림 캡션 마커가 결정되면 리스트로 수집:
   ```
   figures = [
     {"no": 1, "caption": "...", "guide": "...", "type": "..."},
     ...
   ]
   ```
2. 출력 폴더에 `직무발명_<요약명>_<YYYYMMDD>_도면.pptx` 경로 결정
3. python-pptx 스크립트를 임시 파일로 작성 후 `python <스크립트>`로 실행
4. 실행 성공 확인 후 임시 스크립트는 삭제 가능 (원하면 출력 폴더에 `_도면생성.py`로 함께 보존)

## 사용자 안내 메시지

pptx 생성 후 사용자에게 다음과 같이 안내:

```
도면 파일이 생성되었습니다: <경로>

각 슬라이드에는 캡션과 기본 도형 placeholder가 배치되어 있습니다.
PowerPoint 또는 한컴오피스에서 열어 도형을 자유롭게 수정/추가하실 수 있습니다.
완성된 그림을 캡처하여 직무발명 내용 설명서 6번 항목에 첨부하시면 됩니다.
```

## 주의사항

- python-pptx 미설치 시 사용자에게 안내 후 생성 시도. 실패하면 캡션 목록만 텍스트 파일로 저장하고 사용자가 직접 PPT 작업 가능하도록 안내.
- 본문 캡션 번호와 pptx 슬라이드 순서는 반드시 일치.
- 그림이 1장도 필요 없다고 판단되면 pptx 생성을 건너뛰고, 6번 추가자료에 "없음"으로 마무리.
