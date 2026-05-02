# slide-gen-pro

정부/공공기관 스타일 이미지 슬라이드 생성 플러그인.

입력 문서(연구 보고서, 정책 문서, 기술 보고서)를 기반으로 4K 발표용 이미지 슬라이드를 생성하고 PPTX 프레젠테이션으로 변환한다.

## Skills

- **slide-gen-pro** — 자유 모드(자유 형식 프롬프트) 또는 구조화 모드(4-block 파이프라인) 선택 가능

## 출력

- `images/` — 4K PNG 슬라이드 이미지 (3840×2160)
- `presentation.pptx` — PNG 이미지가 풀블리드 삽입된 PPTX 프레젠테이션
- `verification_report.md` — 생성 검증 보고서

## 사용법

```
입력 문서(.md)를 준비하고 "슬라이드 만들어줘"라고 요청
```

## 요구사항

- GEMINI_API_KEY 환경변수
- visual-generator 플러그인 (generate_slide_images.py)
- `pip install python-pptx` (PPTX 변환용)
