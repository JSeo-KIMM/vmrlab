#!/usr/bin/env python3
"""PDF의 각 페이지를 PNG 이미지로 렌더링한다.

국외출장 계획서의 첨부(항공 인보이스, 논문 첫 페이지 등)를 이미지로 만들 때 사용한다.
PyMuPDF(fitz)를 사용하며 poppler 등 외부 바이너리가 필요 없다.

설치:
    pip install PyMuPDF --break-system-packages

사용법:
    python pdf_to_png.py <input.pdf> <output_prefix> [--dpi 200] [--pages 1-2]

예시:
    python pdf_to_png.py "서준호님 항공인보이스.pdf" out/항공인보이스 --dpi 200
    -> out/항공인보이스_p1.png, out/항공인보이스_p2.png ...
"""
import argparse
import os
import sys


def parse_pages(spec, total):
    """'1-3', '2', '1,3' 형태를 0-기반 인덱스 리스트로 변환."""
    if not spec:
        return list(range(total))
    idx = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            idx.extend(range(int(a) - 1, int(b)))
        else:
            idx.append(int(part) - 1)
    return [i for i in idx if 0 <= i < total]


def main():
    ap = argparse.ArgumentParser(description="PDF 페이지를 PNG로 렌더링")
    ap.add_argument("pdf", help="입력 PDF 경로")
    ap.add_argument("prefix", help="출력 PNG 경로 접두사 (예: out/항공인보이스)")
    ap.add_argument("--dpi", type=int, default=200, help="렌더링 해상도 (기본 200)")
    ap.add_argument("--pages", default="", help="페이지 범위 (예: '1-2', '1,3'). 생략 시 전체")
    args = ap.parse_args()

    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("[오류] PyMuPDF 미설치. 'pip install PyMuPDF --break-system-packages' 실행 후 재시도.")

    if not os.path.exists(args.pdf):
        sys.exit(f"[오류] PDF 파일 없음: {args.pdf}")

    out_dir = os.path.dirname(os.path.abspath(args.prefix))
    os.makedirs(out_dir, exist_ok=True)

    doc = fitz.open(args.pdf)
    pages = parse_pages(args.pages, doc.page_count)
    zoom = args.dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    written = []
    for i in pages:
        pix = doc.load_page(i).get_pixmap(matrix=matrix)
        out_path = f"{args.prefix}_p{i + 1}.png"
        pix.save(out_path)
        written.append(out_path)
        print(f"[저장] {out_path}  ({pix.width}x{pix.height})")

    doc.close()
    if not written:
        sys.exit("[오류] 출력된 페이지 없음 — --pages 범위 확인")
    print(f"[완료] {len(written)}개 PNG 생성")


if __name__ == "__main__":
    main()
