---
name: svgtopptx
description: |
  SVG 다이어그램을 편집 가능한 PPTX(PowerPoint)로 변환합니다.
  SVG의 도형, 텍스트, 화살표가 파워포인트 네이티브 개체로 변환되어 개별 편집 가능합니다.

  사용법:
    /svgtopptx-pro:svgtopptx [입력_경로] [출력_경로.pptx]

  예시:
    /svgtopptx-pro:svgtopptx ./images/
    /svgtopptx-pro:svgtopptx ./diagram.svg
    /svgtopptx-pro:svgtopptx ./images/ ./result.pptx
---

`$ARGUMENTS`에서 입력 경로와 (선택) 출력 경로를 파싱합니다.

- 입력 경로가 없으면 **현재 작업 폴더**의 `*.svg` 파일을 자동 탐색
- SVG 파일이 없으면 오류 메시지를 출력하고 종료

`svgtopptx-pro` 스킬의 절차를 따라 변환을 수행합니다:

1. 변환 스크립트를 탐색한다: Glob `**/svgtopptx-pro/scripts/svg_to_pptx.py`
2. 의존성을 확인한다: `pip show python-pptx lxml`
3. 스크립트를 실행한다: `python svg_to_pptx.py <입력> [출력]`
4. 결과를 보고한다: 출력 파일 경로, 슬라이드 수, 도형 수
