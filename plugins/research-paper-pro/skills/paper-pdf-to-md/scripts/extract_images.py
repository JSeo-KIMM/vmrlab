#!/usr/bin/env python3
"""
extract_images.py
PDF 페이지를 고해상도로 렌더링한 후 이미지 영역을 캡처하여 JPG로 저장합니다.
(raw 이미지 추출 방식은 투명도 처리 문제로 검은 배경이 생기므로, 렌더링 캡처 방식 사용)

사용법:
    python extract_images.py <PDF_PATH> <OUTPUT_DIR> [DPI]

    DPI: 렌더링 해상도 (기본값 200, 높을수록 선명하지만 느림)

출력:
    <OUTPUT_DIR>/figure-001.jpg
    <OUTPUT_DIR>/figure-002.jpg
    ...
    추출된 이미지 정보가 stdout에 출력됩니다.
"""

import sys
import os
import json

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF가 설치되지 않았습니다. 다음 명령으로 설치하세요:")
    print("  pip install pymupdf")
    sys.exit(1)


def extract_images_by_render(pdf_path: str, output_dir: str, dpi: int = 200) -> list[dict]:
    """
    PDF 페이지를 렌더링한 후 이미지 영역을 잘라 JPG로 저장합니다.
    투명도(alpha) 문제 없이 원본 그대로 캡처됩니다.
    """
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    extracted = []
    image_counter = 1
    scale = dpi / 72.0  # PDF 기본 72dpi 기준 배율

    matrix = fitz.Matrix(scale, scale)

    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)

        if not image_list:
            continue

        for img_info in image_list:
            xref = img_info[0]

            # 페이지 내 이미지의 바운딩 박스 (PDF 좌표계, 포인트 단위)
            rects = page.get_image_rects(xref)
            if not rects:
                continue

            for rect in rects:
                w_pt = rect.width
                h_pt = rect.height

                if w_pt < 10 or h_pt < 10:
                    # 너무 작은 영역(아이콘 등)은 건너뜀
                    continue

                # PDF 좌표계 rect를 clip으로 지정하여 해당 영역만 렌더링
                sub_pm = page.get_pixmap(matrix=matrix, clip=rect, colorspace=fitz.csRGB)

                w_px = sub_pm.width
                h_px = sub_pm.height
                is_small = w_px < 100 or h_px < 100

                filename = f"figure-{image_counter:03d}.jpg"
                filepath = os.path.join(output_dir, filename)
                sub_pm.save(filepath, jpg_quality=95)

                extracted.append({
                    "filename": filename,
                    "filepath": filepath,
                    "page": page_num + 1,
                    "width": w_px,
                    "height": h_px,
                    "is_small": is_small,
                })
                image_counter += 1

    doc.close()
    return extracted


def main():
    if len(sys.argv) < 3:
        print("사용법: python extract_images.py <PDF_PATH> <OUTPUT_DIR> [DPI]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 200

    if not os.path.exists(pdf_path):
        print(f"오류: PDF 파일을 찾을 수 없습니다: {pdf_path}")
        sys.exit(1)

    print(f"PDF 렌더링 방식으로 이미지 캡처 중: {pdf_path} (DPI={dpi})")
    extracted = extract_images_by_render(pdf_path, output_dir, dpi)

    print(f"\n총 {len(extracted)}개 이미지 캡처 완료:")
    for img in extracted:
        flag = " [소형]" if img["is_small"] else ""
        note = f" ({img['note']})" if "note" in img else ""
        print(f"  - {img['filename']} (p.{img['page']}, {img['width']}x{img['height']}px){flag}{note}")

    # JSON으로 결과 저장
    result_path = os.path.join(output_dir, "_extraction_result.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(extracted, f, ensure_ascii=False, indent=2)

    print(f"\n추출 결과 저장됨: {result_path}")


if __name__ == "__main__":
    main()
