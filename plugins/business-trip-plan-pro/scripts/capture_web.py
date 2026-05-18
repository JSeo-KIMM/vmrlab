#!/usr/bin/env python3
"""행사 홈페이지를 헤드리스 브라우저로 접속해 스크린샷 PNG로 저장한다.

국외출장 계획서 4번 항목에 들어갈 '행사 대표 이미지', '행사 일정 페이지'를
캡처할 때 사용한다.

설치:
    pip install playwright --break-system-packages
    python -m playwright install chromium

사용법:
    python capture_web.py <url> <output.png> [--full-page] [--selector CSS] [--width 1280] [--timeout 30]

예시:
    python capture_web.py https://example-conf.org out/행사홈페이지.png
    python capture_web.py https://example-conf.org/program out/행사일정.png --full-page

종료 코드:
    0  성공
    2  Playwright 미설치 / 브라우저 미설치 (호출 측은 이미지 URL 검색 등 대체 경로로 폴백)
    1  그 외 오류 (네트워크/타임아웃 등)
"""
import argparse
import os
import sys


def main():
    ap = argparse.ArgumentParser(description="웹 페이지 스크린샷 캡처")
    ap.add_argument("url", help="캡처할 페이지 URL")
    ap.add_argument("output", help="출력 PNG 경로")
    ap.add_argument("--full-page", action="store_true", help="페이지 전체를 캡처 (기본: 화면 1장)")
    ap.add_argument("--selector", default="", help="특정 요소만 캡처할 CSS 선택자")
    ap.add_argument("--width", type=int, default=1280, help="뷰포트 너비 (기본 1280)")
    ap.add_argument("--height", type=int, default=900, help="뷰포트 높이 (기본 900)")
    ap.add_argument("--timeout", type=int, default=30, help="로딩 타임아웃 초 (기본 30)")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[폴백필요] Playwright 미설치. 설치: pip install playwright --break-system-packages "
              "&& python -m playwright install chromium", file=sys.stderr)
        sys.exit(2)

    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)

    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch()
            except Exception as e:
                print(f"[폴백필요] Chromium 미설치/실행 불가: {e}\n"
                      "설치: python -m playwright install chromium", file=sys.stderr)
                sys.exit(2)
            page = browser.new_context(
                viewport={"width": args.width, "height": args.height}
            ).new_page()
            page.goto(args.url, timeout=args.timeout * 1000, wait_until="networkidle")
            if args.selector:
                el = page.query_selector(args.selector)
                if el is None:
                    print(f"[오류] 선택자 미발견: {args.selector}", file=sys.stderr)
                    browser.close()
                    sys.exit(1)
                el.screenshot(path=args.output)
            else:
                page.screenshot(path=args.output, full_page=args.full_page)
            browser.close()
    except SystemExit:
        raise
    except Exception as e:
        print(f"[오류] 캡처 실패: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[저장] {args.output}")


if __name__ == "__main__":
    main()
