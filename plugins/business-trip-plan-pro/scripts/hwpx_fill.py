#!/usr/bin/env python3
"""HWPX 양식(국외출장 계획서)을 채우기 위한 ZIP-level 편집 도구.

HWPX는 ZIP + XML 구조이며, 본문은 `Contents/section0.xml`에 들어 있다.
이 스크립트는 HwpxDocument.open() 없이 XML을 문자열 단위로 안전하게 편집한다.

기능:
  dump         양식 내 모든 텍스트를 표/셀 좌표와 함께 출력 (치환 매핑 작성용)
  replace      {옛텍스트: 새텍스트} 매핑(JSON)을 일괄 치환
  expand-rows  표의 특정 행을 복제해 행 수를 늘림 (출장일정/3년실적 표용)
  set-cell     표의 특정 셀(행,열) 텍스트를 교체 (여러 줄 지원)
  insert-para  특정 텍스트를 가진 문단 뒤에 본문 문단을 삽입 (1번/4번 항목용)

사용법:
  python hwpx_fill.py dump <hwpx>
  python hwpx_fill.py replace <src.hwpx> <dst.hwpx> <map.json>
  python hwpx_fill.py expand-rows <src.hwpx> <dst.hwpx> --table-id ID --row N --count K
  python hwpx_fill.py set-cell <src.hwpx> <dst.hwpx> --table-id ID --row R --col C --text "내용"
  python hwpx_fill.py set-cell ... --text-file 내용.txt   (여러 줄은 파일로 전달 권장)
  python hwpx_fill.py insert-para <src.hwpx> <dst.hwpx> --anchor "1. 출장목적" --text-file 본문.txt

표 id와 행/열 좌표는 먼저 `dump`로 확인한다.
편집은 항상 src → dst로 새 파일을 만든다 (원본 양식 보존).
"""
import argparse
import json
import os
import re
import sys
import zipfile

SECTION = "Contents/section0.xml"


# ---------------------------------------------------------------- ZIP helpers
def _read_section(path):
    with zipfile.ZipFile(path) as z:
        return z.read(SECTION).decode("utf-8")


def _write_section(src, dst, xml):
    """src의 모든 파트를 복사하되 section0.xml만 교체해 dst로 저장."""
    tmp = dst + ".tmp"
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == SECTION:
                data = xml.encode("utf-8")
            zout.writestr(item, data)
    if os.path.exists(dst):
        os.remove(dst)
    os.rename(tmp, dst)


def _esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------- table parse
def _find_table(xml, table_id):
    """table_id를 가진 <hp:tbl>...</hp:tbl> 블록의 (start, end)를 반환."""
    m = re.search(r'<hp:tbl\b[^>]*\bid="%s"' % re.escape(table_id), xml)
    if not m:
        sys.exit(f"[오류] 표 id={table_id} 없음. 'dump'로 표 id를 먼저 확인하세요.")
    start = m.start()
    end = xml.index("</hp:tbl>", start) + len("</hp:tbl>")
    return start, end


def _rows(tbl_xml):
    """표 블록 안의 <hp:tr>...</hp:tr> 블록 (start,end) 리스트."""
    out = []
    for m in re.finditer(r"<hp:tr>", tbl_xml):
        s = m.start()
        e = tbl_xml.index("</hp:tr>", s) + len("</hp:tr>")
        out.append((s, e))
    return out


# ---------------------------------------------------------------------- dump
def cmd_dump(args):
    xml = _read_section(args.hwpx)
    print(f"# {args.hwpx}\n")
    for tm in re.finditer(r'<hp:tbl\b[^>]*>', xml):
        tid = re.search(r'\bid="(\d+)"', tm.group(0))
        rc = re.search(r'\browCnt="(\d+)"', tm.group(0))
        cc = re.search(r'\bcolCnt="(\d+)"', tm.group(0))
        ts = tm.start()
        te = xml.index("</hp:tbl>", ts) + len("</hp:tbl>")
        print(f"[표] id={tid.group(1) if tid else '?'}  "
              f"rowCnt={rc.group(1) if rc else '?'} colCnt={cc.group(1) if cc else '?'}")
        for tcm in re.finditer(r"<hp:tc\b.*?</hp:tc>", xml[ts:te], re.S):
            tc = tcm.group(0)
            addr = re.search(r'<hp:cellAddr colAddr="(\d+)" rowAddr="(\d+)"/>', tc)
            txt = " / ".join(re.sub(r"<[^>]+>", "", t)
                             for t in re.findall(r"<hp:t>(.*?)</hp:t>", tc, re.S))
            if addr:
                print(f"   ({addr.group(2)},{addr.group(1)})  {txt!r}")
        print()
    # 표 밖 본문 텍스트
    print("[본문 텍스트]")
    for t in re.findall(r"<hp:t>(.*?)</hp:t>", xml, re.S):
        t = re.sub(r"<[^>]+>", "", t)
        if t.strip():
            print(f"   {t!r}")


# ------------------------------------------------------------------- replace
def cmd_replace(args):
    xml = _read_section(args.src)
    with open(args.mapfile, encoding="utf-8") as f:
        mapping = json.load(f)
    n = 0
    for old, new in mapping.items():
        cnt = xml.count(old)
        if cnt == 0:
            print(f"[경고] 미발견: {old!r}", file=sys.stderr)
        xml = xml.replace(old, new)
        n += cnt
    _write_section(args.src, args.dst, xml)
    print(f"[완료] {n}건 치환 → {args.dst}")


# --------------------------------------------------------------- expand-rows
def cmd_expand_rows(args):
    xml = _read_section(args.src)
    ts, te = _find_table(xml, args.table_id)
    tbl = xml[ts:te]
    rows = _rows(tbl)
    if args.row >= len(rows):
        sys.exit(f"[오류] row 인덱스 {args.row} 범위 초과 (행 수 {len(rows)})")
    rs, re_ = rows[args.row]
    template_row = tbl[rs:re_]

    # 복제 행 생성: rowAddr를 순차 증가
    base_row = args.row
    clones = []
    for k in range(1, args.count + 1):
        new_addr = base_row + k
        clone = re.sub(r'(<hp:cellAddr colAddr="\d+" rowAddr=")\d+(")',
                       r"\g<1>%d\g<2>" % new_addr, template_row)
        clones.append(clone)

    # 템플릿 행 뒤에 삽입하면서, 그 아래 기존 행들의 rowAddr도 밀어준다
    after = tbl[re_:]
    shifted = re.sub(
        r'<hp:cellAddr colAddr="(\d+)" rowAddr="(\d+)"/>',
        lambda m: '<hp:cellAddr colAddr="%s" rowAddr="%d"/>'
                  % (m.group(1), int(m.group(2)) + args.count),
        after)
    new_tbl = tbl[:re_] + "".join(clones) + shifted

    # rowCnt 갱신
    new_tbl = re.sub(r'(<hp:tbl\b[^>]*\browCnt=")(\d+)(")',
                     lambda m: m.group(1) + str(int(m.group(2)) + args.count) + m.group(3),
                     new_tbl, count=1)

    _write_section(args.src, args.dst, xml[:ts] + new_tbl + xml[te:])
    print(f"[완료] 표 {args.table_id}: row {args.row} 기준 {args.count}행 추가 → {args.dst}")


# ---------------------------------------------------------------- set-cell
def cmd_set_cell(args):
    if args.text_file:
        with open(args.text_file, encoding="utf-8") as f:
            text = f.read().rstrip("\n")
    else:
        text = args.text if args.text is not None else ""

    xml = _read_section(args.src)
    ts, te = _find_table(xml, args.table_id)
    tbl = xml[ts:te]

    target = '<hp:cellAddr colAddr="%d" rowAddr="%d"/>' % (args.col, args.row)
    if target not in tbl:
        sys.exit(f"[오류] 셀 (row={args.row}, col={args.col}) 없음. 'dump'로 좌표 확인.")

    # 대상 <hp:tc> 블록을 찾는다
    tcs = list(re.finditer(r"<hp:tc\b.*?</hp:tc>", tbl, re.S))
    tc_block = None
    for m in tcs:
        if target in m.group(0):
            tc_block = m
            break
    if tc_block is None:
        sys.exit("[오류] 셀 블록 탐색 실패")
    tc = tc_block.group(0)

    # 셀의 첫 문단/런에서 서식 ID를 물려받는다
    pm = re.search(r'<hp:p\b[^>]*paraPrIDRef="(\d+)"[^>]*styleIDRef="(\d+)"', tc)
    para_pr = pm.group(1) if pm else "0"
    style = pm.group(2) if pm else "0"
    cm = re.search(r'charPrIDRef="(\d+)"', tc)
    char_pr = cm.group(1) if cm else "0"

    lines = text.split("\n") if text else [""]
    paras = "".join(
        '<hp:p id="0" paraPrIDRef="%s" styleIDRef="%s" pageBreak="0" columnBreak="0" merged="0">'
        '<hp:run charPrIDRef="%s"><hp:t>%s</hp:t></hp:run></hp:p>'
        % (para_pr, style, char_pr, _esc(ln))
        for ln in lines)

    # <hp:subList ...> ... </hp:subList> 내부를 새 문단으로 교체
    new_tc = re.sub(r"(<hp:subList\b[^>]*>).*?(</hp:subList>)",
                    lambda m: m.group(1) + paras + m.group(2),
                    tc, count=1, flags=re.S)
    new_tbl = tbl[:tc_block.start()] + new_tc + tbl[tc_block.end():]
    _write_section(args.src, args.dst, xml[:ts] + new_tbl + xml[te:])
    print(f"[완료] 표 {args.table_id} 셀 ({args.row},{args.col}) 설정 → {args.dst}")


# --------------------------------------------------------------- insert-para
def cmd_insert_para(args):
    if args.text_file:
        with open(args.text_file, encoding="utf-8") as f:
            text = f.read().rstrip("\n")
    else:
        text = args.text if args.text is not None else ""

    xml = _read_section(args.src)
    idx = xml.find(args.anchor)
    if idx == -1:
        sys.exit(f"[오류] 기준 텍스트 미발견: {args.anchor!r}. 'dump'로 본문 텍스트 확인.")
    ps = xml.rfind("<hp:p ", 0, idx)
    pe = xml.index("</hp:p>", idx) + len("</hp:p>")
    anchor_p = xml[ps:pe]

    pm = re.search(r'paraPrIDRef="(\d+)"[^>]*styleIDRef="(\d+)"', anchor_p)
    para_pr = pm.group(1) if pm else "0"
    style = pm.group(2) if pm else "0"
    cm = re.search(r'charPrIDRef="(\d+)"', anchor_p)
    char_pr = cm.group(1) if cm else "0"

    lines = text.split("\n") if text else [""]
    paras = "".join(
        '<hp:p id="0" paraPrIDRef="%s" styleIDRef="%s" pageBreak="0" columnBreak="0" merged="0">'
        '<hp:run charPrIDRef="%s"><hp:t>%s</hp:t></hp:run></hp:p>'
        % (para_pr, style, char_pr, _esc(ln))
        for ln in lines)

    _write_section(args.src, args.dst, xml[:pe] + paras + xml[pe:])
    print(f"[완료] {args.anchor!r} 뒤에 {len(lines)}개 문단 삽입 → {args.dst}")


# ----------------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description="HWPX 양식 채우기 도구")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("dump", help="양식 텍스트/표 좌표 출력")
    p.add_argument("hwpx")
    p.set_defaults(func=cmd_dump)

    p = sub.add_parser("replace", help="JSON 매핑 일괄 치환")
    p.add_argument("src"); p.add_argument("dst"); p.add_argument("mapfile")
    p.set_defaults(func=cmd_replace)

    p = sub.add_parser("expand-rows", help="표 행 복제")
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--table-id", required=True)
    p.add_argument("--row", type=int, required=True, help="복제할 기준 행 인덱스(0-기반)")
    p.add_argument("--count", type=int, required=True, help="추가할 행 수")
    p.set_defaults(func=cmd_expand_rows)

    p = sub.add_parser("set-cell", help="셀 텍스트 설정")
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--table-id", required=True)
    p.add_argument("--row", type=int, required=True)
    p.add_argument("--col", type=int, required=True)
    p.add_argument("--text", default=None)
    p.add_argument("--text-file", default=None, help="여러 줄 내용을 담은 텍스트 파일")
    p.set_defaults(func=cmd_set_cell)

    p = sub.add_parser("insert-para", help="문단 뒤에 본문 삽입")
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--anchor", required=True, help="삽입 기준이 되는 기존 문단의 텍스트")
    p.add_argument("--text", default=None)
    p.add_argument("--text-file", default=None, help="여러 줄 내용을 담은 텍스트 파일")
    p.set_defaults(func=cmd_insert_para)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
