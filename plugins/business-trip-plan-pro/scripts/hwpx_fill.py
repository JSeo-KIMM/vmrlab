#!/usr/bin/env python3
"""HWPX 양식(국외출장 계획서)을 채우기 위한 ZIP-level 편집 도구.

HWPX는 ZIP + XML 구조이며, 본문은 `Contents/section0.xml`에 들어 있다.
이 스크립트는 HwpxDocument.open() 없이 XML을 문자열 단위로 안전하게 편집한다.

기능:
  dump         양식 내 모든 텍스트를 표/셀 좌표와 함께 출력 (치환 매핑 작성용)
  replace      {옛텍스트: 새텍스트} 매핑(JSON)을 일괄 치환
  expand-rows  표의 특정 행을 복제해 행 수를 늘림 (3년실적 표 등 평면 표용)
  set-cell     표의 특정 셀(행,열) 텍스트를 교체 (여러 줄 지원)
  build-schedule  출장일정 표를 JSON으로부터 7열 병합 표로 통째로 재구성
                  (셀 병합 rowspan/colspan — set-cell로는 불가능)
  insert-para  특정 텍스트를 가진 문단 뒤에 본문 문단을 삽입 (1번/4번 항목용)
  delete-para  특정 텍스트를 가진 문단을 삭제 (양식 기본 문구 제거용)
  format       서식 일괄 적용 — 번호 제목 볼드 / 줄간격 120% / 출장일정 표 속성
               / 모든 표 셀 가운데 정렬 (모든 채우기 작업이 끝난 뒤 마지막에 실행)

사용법:
  python hwpx_fill.py dump <hwpx>
  python hwpx_fill.py replace <src.hwpx> <dst.hwpx> <map.json>
  python hwpx_fill.py expand-rows <src.hwpx> <dst.hwpx> --table-id ID --row N --count K
  python hwpx_fill.py build-schedule <src.hwpx> <dst.hwpx> --table-id ID --data days.json
  python hwpx_fill.py set-cell <src.hwpx> <dst.hwpx> --table-id ID --row R --col C --text "내용"
  python hwpx_fill.py set-cell ... --text-file 내용.txt   (여러 줄은 파일로 전달 권장)
  python hwpx_fill.py insert-para <src.hwpx> <dst.hwpx> --anchor "1. 출장목적" --text-file 본문.txt
  python hwpx_fill.py format <src.hwpx> <dst.hwpx> --schedule-table-id ID

표 id와 행/열 좌표는 먼저 `dump`로 확인한다.
편집은 항상 src → dst로 새 파일을 만든다 (원본 양식 보존).
"""
import argparse
import json
import os
import re
import sys
import zipfile

# Windows 콘솔 기본 코드페이지(cp949)는 — 〜 등 일부 유니코드를 못 찍어
# 작업이 끝난 뒤 print에서 죽는다. 표준출력/에러를 UTF-8로 돌려 막는다.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SECTION = "Contents/section0.xml"
HEADER = "Contents/header.xml"

# 별지 제2호 6개 표준 항목 제목 (공백 제거 후 비교 — '2. 출장 일정' == '2.출장일정')
SECTION_HEADINGS = [
    "1. 출장목적",
    "2. 출장일정",
    "3. 최근 3년간 국외출장 실적",
    "4. 출장중 파악(수행)해야 할 내용",
    "5. 출장예산",
    "6. 연구관련 반출 예정 전산장비 및 자료 현황",
]


# ---------------------------------------------------------------- ZIP helpers
def _read_part(path, part):
    with zipfile.ZipFile(path) as z:
        return z.read(part).decode("utf-8")


def _read_section(path):
    return _read_part(path, SECTION)


def _write_parts(src, dst, parts):
    """src의 모든 파트를 복사하되 parts({파트명: 새 XML})만 교체해 dst로 저장."""
    tmp = dst + ".tmp"
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in parts:
                data = parts[item.filename].encode("utf-8")
            zout.writestr(item, data)
    if os.path.exists(dst):
        os.remove(dst)
    os.rename(tmp, dst)


def _write_section(src, dst, xml):
    """src의 모든 파트를 복사하되 section0.xml만 교체해 dst로 저장."""
    _write_parts(src, dst, {SECTION: xml})


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
    # <hp:t> 안에는 <hp:fwSpace/>(전각공백)·<hp:tab/> 같은 인라인 태그가 섞일 수 있다.
    # replace는 XML 문자열을 그대로 치환하므로, 그런 태그가 있으면 태그까지 포함한
    # 원본 문자열을 키로 써야 한다. 정리된 텍스트와 다르면 [replace 키]를 함께 보여준다.
    print("[본문 텍스트]   (정리된 텍스트 / 인라인 태그가 있으면 replace 키 별도 표기)")
    for raw in re.findall(r"<hp:t>(.*?)</hp:t>", xml, re.S):
        clean = re.sub(r"<[^>]+>", "", raw)
        if not clean.strip():
            continue
        if raw != clean:
            print(f"   {clean!r}   [replace 키: {raw!r}]")
        else:
            print(f"   {clean!r}")


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


# ------------------------------------------------------------ build-schedule
# 출장일정 표는 셀 병합이 필요해 set-cell로는 만들 수 없다 (set-cell은 평면 격자 전용).
# build-schedule는 양식의 출장일정 표를 통째로 7열 병합 표로 다시 만든다.
# 마크다운 초안의 HTML <table>(rowspan/colspan)과 같은 모양이 되도록,
# 동행 2인 이상인 행사일은 인원수만큼 그리드 행으로 나누고 날짜·장소 칸은 rowSpan으로 묶는다.
#
# HWPX(OWPML) 표 병합 규칙:
#  - <hp:tbl rowCnt colCnt>는 그리드(논리) 행/열 수.
#  - 병합으로 가려진 칸은 <hp:tc>를 아예 쓰지 않는다 (그 행의 <hp:tr>에서 생략).
#  - 각 <hp:tc>는 <hp:cellAddr>로 자기 그리드 좌표(colAddr,rowAddr)를 명시한다.
#  - 병합 셀은 <hp:cellSpan colSpan rowSpan>으로 차지 범위를 표시한다.

# 7열 폭(HWPUNIT). 합계는 양식 원래 표 폭(48464)과 같아야 한다.
#   0 월일  1 출발지  2 도착지  3 방문기관  4 업무수행내용  5 담당자  6 면담예정자
SCHED_COL_W = [4764, 5048, 5332, 10728, 11436, 2700, 8456]
SCHED_HEADER_H = 2680   # 머리글 행 높이
SCHED_ROW_H = 2800      # 데이터 그리드 행 1줄 높이 (한글이 내용에 맞게 다시 계산함)


def _sched_cell(col, row, colspan, rowspan, width, height, lines, header=False):
    """출장일정 표의 <hp:tc> 한 칸을 만든다. lines는 줄 목록(각 줄 = 한 문단)."""
    para_pr = "14" if header else "4"
    if not lines:
        lines = [""]
    paras = "".join(
        '<hp:p id="0" paraPrIDRef="%s" styleIDRef="0" pageBreak="0" '
        'columnBreak="0" merged="0"><hp:run charPrIDRef="8"><hp:t>%s</hp:t>'
        '</hp:run></hp:p>' % (para_pr, _esc(ln))
        for ln in lines)
    return (
        '<hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" '
        'dirty="0" borderFillIDRef="5"><hp:subList id="" '
        'textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" '
        'linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" '
        'hasTextRef="0" hasNumRef="0">%s</hp:subList>'
        '<hp:cellAddr colAddr="%d" rowAddr="%d"/>'
        '<hp:cellSpan colSpan="%d" rowSpan="%d"/>'
        '<hp:cellSz width="%d" height="%d"/>'
        '<hp:cellMargin left="141" right="141" top="141" bottom="141"/></hp:tc>'
        % (paras, col, row, colspan, rowspan, width, height))


def _lines(value):
    r"""JSON 값의 줄바꿈(\n)을 줄 목록으로. None/빈값은 ['-']."""
    if value is None or value == "":
        return ["-"]
    return str(value).split("\n")


def cmd_build_schedule(args):
    r"""출장일정 표를 JSON(days[])로부터 7열 병합 표로 통째로 다시 만든다.

    JSON 형식:
    {
      "days": [
        {"date":"7월 22일\n(수)","from":"부산","to":"싱가포르/\n싱가포르",
         "org":"-","meet":"-","work":"출국 및 싱가포르(출장지) 도착"},
        {"date":"7월 23일\n(목)","from":"-","to":"싱가포르/\n싱가포르",
         "org":"National\nUniversity of\nSingapore","meet":"-",
         "persons":[
            {"name":"서준호","work":"- ...\n- ..."},
            {"name":"심성보","work":"- ..."},
            {"name":"정덕기","work":"- ..."}
         ]}
      ]
    }
    - persons가 2명 이상이면 그 날은 인원수만큼 행으로 나뉘고 날짜·장소 칸은 rowSpan으로 묶임.
    - persons가 없거나 1명이면 한 행. 업무수행내용은 colSpan=2로 두 열을 합침(work 또는 persons[0].work).
    """
    with open(args.data, encoding="utf-8") as f:
        days = json.load(f)["days"]

    xml = _read_section(args.src)
    ts, te = _find_table(xml, args.table_id)
    tbl = xml[ts:te]
    open_m = re.match(r"<hp:tbl\b[^>]*>", tbl)
    open_tag = open_m.group(0)
    first_tr = tbl.index("<hp:tr>")
    prefix = tbl[open_m.end():first_tr]   # <hp:sz>/<hp:pos>/<hp:outMargin>/<hp:inMargin>

    W = SCHED_COL_W
    rows = []

    # ---- 머리글 행 (그리드 row 0) ----
    header = [
        _sched_cell(0, 0, 1, 1, W[0], SCHED_HEADER_H, ["월 일", "(요일)"], header=True),
        _sched_cell(1, 0, 1, 1, W[1], SCHED_HEADER_H, ["출발지"], header=True),
        _sched_cell(2, 0, 1, 1, W[2], SCHED_HEADER_H, ["도착지"], header=True),
        _sched_cell(3, 0, 1, 1, W[3], SCHED_HEADER_H, ["방문기관"], header=True),
        _sched_cell(4, 0, 2, 1, W[4] + W[5], SCHED_HEADER_H, ["업무수행내용"], header=True),
        _sched_cell(6, 0, 1, 1, W[6], SCHED_HEADER_H, ["면담예정자", "(직위포함)"], header=True),
    ]
    rows.append("<hp:tr>" + "".join(header) + "</hp:tr>")

    grow = 1   # 다음에 쓸 그리드 행 번호
    for day in days:
        date, dfrom = _lines(day.get("date")), _lines(day.get("from"))
        dto, org = _lines(day.get("to")), _lines(day.get("org"))
        meet = _lines(day.get("meet"))
        persons = day.get("persons") or []

        if len(persons) >= 2:
            # 행사일·동행 N인: N개 그리드 행, 날짜·장소·면담 칸은 rowSpan=N
            n = len(persons)
            h = SCHED_ROW_H * n
            first = [
                _sched_cell(0, grow, 1, n, W[0], h, date),
                _sched_cell(1, grow, 1, n, W[1], h, dfrom),
                _sched_cell(2, grow, 1, n, W[2], h, dto),
                _sched_cell(3, grow, 1, n, W[3], h, org),
                _sched_cell(4, grow, 1, 1, W[4], SCHED_ROW_H, _lines(persons[0].get("work"))),
                _sched_cell(5, grow, 1, 1, W[5], SCHED_ROW_H, _lines(persons[0].get("name"))),
                _sched_cell(6, grow, 1, n, W[6], h, meet),
            ]
            rows.append("<hp:tr>" + "".join(first) + "</hp:tr>")
            for k in range(1, n):
                # 가려진 칸(0~3,6)은 생략 — 업무수행내용·담당자 2칸만
                later = [
                    _sched_cell(4, grow + k, 1, 1, W[4], SCHED_ROW_H, _lines(persons[k].get("work"))),
                    _sched_cell(5, grow + k, 1, 1, W[5], SCHED_ROW_H, _lines(persons[k].get("name"))),
                ]
                rows.append("<hp:tr>" + "".join(later) + "</hp:tr>")
            grow += n
        else:
            # 이동일 또는 단독 행사일: 한 행, 업무수행내용은 colSpan=2
            work = day.get("work")
            if work is None and persons:
                work = persons[0].get("work")
            cells = [
                _sched_cell(0, grow, 1, 1, W[0], SCHED_ROW_H, date),
                _sched_cell(1, grow, 1, 1, W[1], SCHED_ROW_H, dfrom),
                _sched_cell(2, grow, 1, 1, W[2], SCHED_ROW_H, dto),
                _sched_cell(3, grow, 1, 1, W[3], SCHED_ROW_H, org),
                _sched_cell(4, grow, 2, 1, W[4] + W[5], SCHED_ROW_H, _lines(work)),
                _sched_cell(6, grow, 1, 1, W[6], SCHED_ROW_H, meet),
            ]
            rows.append("<hp:tr>" + "".join(cells) + "</hp:tr>")
            grow += 1

    total_rows = grow
    total_h = SCHED_HEADER_H + (total_rows - 1) * SCHED_ROW_H

    # 여는 태그의 rowCnt/colCnt 갱신
    new_tag = re.sub(r'\browCnt="\d+"', 'rowCnt="%d"' % total_rows, open_tag)
    new_tag = re.sub(r'\bcolCnt="\d+"', 'colCnt="7"', new_tag)
    # 표 전체 높이(<hp:sz height>) 갱신 — 폭은 그대로
    new_prefix = re.sub(r'(<hp:sz\b[^>]*\bheight=")\d+(")',
                        r"\g<1>%d\g<2>" % total_h, prefix, count=1)

    new_tbl = new_tag + new_prefix + "".join(rows) + "</hp:tbl>"
    _write_section(args.src, args.dst, xml[:ts] + new_tbl + xml[te:])
    print("[완료] 출장일정 표 %s 재구성: 7열 병합 표, %d행(머리글 포함) → %s"
          % (args.table_id, total_rows, args.dst))


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


# --------------------------------------------------------------- delete-para
def cmd_delete_para(args):
    """anchor 텍스트를 포함하는 <hp:p> 문단 하나를 통째로 삭제한다.

    양식에 미리 들어 있는 기본 문구(예: 첨부 기본 목록, 옛 출장기간 줄)를
    없앨 때 쓴다. anchor는 그 문단 안 텍스트의 일부이며 문서에서 유일해야 한다.
    유니코드 깨짐을 피하려면 --anchor-file로 파일에 담아 넘긴다.
    """
    if args.anchor_file:
        with open(args.anchor_file, encoding="utf-8") as f:
            anchor = f.read().strip("\n")
    else:
        anchor = args.anchor if args.anchor is not None else ""
    if not anchor:
        sys.exit("[오류] --anchor 또는 --anchor-file 로 삭제할 문단 텍스트를 지정하세요.")

    xml = _read_section(args.src)
    idx = xml.find(anchor)
    if idx == -1:
        sys.exit(f"[오류] 삭제할 문단 미발견: {anchor!r}. 'dump'로 본문 텍스트 확인.")
    ps = xml.rfind("<hp:p ", 0, idx)
    pe = xml.index("</hp:p>", idx) + len("</hp:p>")
    if ps == -1 or pe <= ps:
        sys.exit("[오류] 문단 경계 탐색 실패")
    _write_section(args.src, args.dst, xml[:ps] + xml[pe:])
    print(f"[완료] 문단 삭제: {anchor!r} → {args.dst}")


# ----------------------------------------------------------------- format
def _norm(text):
    """공백을 모두 제거해 제목 비교를 너그럽게 한다."""
    return re.sub(r"\s+", "", text)


def _bump_itemcnt(header, container):
    """<hh:charProperties itemCnt="N"> 등의 항목 수를 1 증가."""
    return re.sub(r'(<hh:%s itemCnt=")(\d+)(")' % container,
                  lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3),
                  header, count=1)


def _set_attr(tag, name, value):
    """여는 태그 문자열에서 속성을 교체하거나, 없으면 추가."""
    pat = r'\b' + re.escape(name) + r'="[^"]*"'
    if re.search(pat, tag):
        return re.sub(pat, '%s="%s"' % (name, value), tag, count=1)
    if tag.endswith("/>"):
        return tag[:-2] + ' %s="%s"/>' % (name, value)
    return tag[:-1] + ' %s="%s">' % (name, value)


def _para_text(p_xml):
    """문단 XML에서 순수 텍스트만 추출."""
    joined = "".join(re.findall(r"<hp:t>(.*?)</hp:t>", p_xml, re.S))
    return re.sub(r"<[^>]+>", "", joined)


def cmd_format(args):
    """채우기가 끝난 hwpx에 서식을 일괄 적용한다.

    1) 번호 붙은 표준 항목 제목(1.출장목적 ~ 6.…)을 볼드 처리
    2) 모든 문단의 줄간격을 지정값(기본 120%)으로 통일
    3) 출장일정 표: 글자처럼 취급 안 함 + 자리차지 배치 + 쪽 경계에서 나눔
    4) 모든 표 셀 안의 문단을 가운데 정렬

    제목 볼드와 셀 정렬은 header.xml의 글자/문단 모양을 새로 만들어
    원본 모양은 건드리지 않고 안전하게 적용한다.
    """
    section = _read_section(args.src)
    header = _read_part(args.src, HEADER)
    ls = args.line_spacing

    # ---- (2) 줄간격 모두 지정값(%)으로 통일 ----
    # paraPr 마다 <hp:case>/<hp:default> 두 곳에 lineSpacing이 들어 있어 모두 교체한다.
    header = re.sub(
        r'<hh:lineSpacing\b[^>]*/>',
        '<hh:lineSpacing type="PERCENT" value="%d" unit="HWPUNIT"/>' % ls,
        header)

    # ---- (1) 번호 제목 볼드 ----
    targets = {_norm(h) for h in SECTION_HEADINGS}

    heading_charprs = set()
    for m in re.finditer(r"<hp:p\b[^>]*>.*?</hp:p>", section, re.S):
        if _norm(_para_text(m.group(0))) in targets:
            heading_charprs.update(re.findall(r'charPrIDRef="(\d+)"', m.group(0)))

    bold_map = {}                       # 원본 charPr id -> 볼드 charPr id
    next_char_id = max((int(x) for x in re.findall(r'<hh:charPr id="(\d+)"', header)),
                       default=-1) + 1
    for cid in sorted(heading_charprs, key=int):
        cm = re.search(r'<hh:charPr id="%s".*?</hh:charPr>' % cid, header, re.S)
        if not cm:
            continue
        block = cm.group(0)
        if "<hh:bold" in block:         # 이미 볼드면 그대로 사용
            bold_map[cid] = cid
            continue
        clone = block.replace('id="%s"' % cid, 'id="%d"' % next_char_id, 1)
        clone = clone.replace("<hh:underline", "<hh:bold/><hh:underline", 1)
        header = header.replace("</hh:charProperties>", clone + "</hh:charProperties>", 1)
        header = _bump_itemcnt(header, "charProperties")
        bold_map[cid] = str(next_char_id)
        next_char_id += 1

    def _bold_heading(m):
        p = m.group(0)
        if _norm(_para_text(p)) not in targets:
            return p
        return re.sub(r'(<hp:run charPrIDRef=")(\d+)(")',
                      lambda r: r.group(1) + bold_map.get(r.group(2), r.group(2)) + r.group(3),
                      p)
    section = re.sub(r"<hp:p\b[^>]*>.*?</hp:p>", _bold_heading, section, flags=re.S)

    # ---- (3) 출장일정 표 속성 ----
    if args.schedule_table_id:
        ts, te = _find_table(section, args.schedule_table_id)
        tbl = section[ts:te]
        tm = re.match(r"<hp:tbl\b[^>]*>", tbl)
        tag = tm.group(0)
        tag = _set_attr(tag, "textWrap", "TOP_AND_BOTTOM")   # 본문과의 배치: 자리차지
        tag = _set_attr(tag, "pageBreak", "TABLE")           # 쪽 경계에서: 나눔
        tbl = tag + tbl[tm.end():]
        # <hp:pos treatAsChar="..."> → 0 (글자처럼 취급 안 함)
        if re.search(r'<hp:pos\b[^>]*\btreatAsChar="', tbl):
            tbl = re.sub(r'(<hp:pos\b[^>]*\btreatAsChar=")\d+(")', r"\g<1>0\g<2>", tbl, count=1)
        section = section[:ts] + tbl + section[te:]
        print(f"[적용] 출장일정 표({args.schedule_table_id}): 자리차지/나눔/글자취급해제")
    else:
        print("[안내] --schedule-table-id 미지정 — 출장일정 표 속성 변경 건너뜀", file=sys.stderr)

    # ---- (4) 모든 표 셀 내용 가운데 정렬 ----
    cell_paraprs = set()
    for tc in re.finditer(r"<hp:tc\b.*?</hp:tc>", section, re.S):
        cell_paraprs.update(re.findall(r'<hp:p\b[^>]*\bparaPrIDRef="(\d+)"', tc.group(0)))

    center_map = {}                     # 원본 paraPr id -> 가운데정렬 paraPr id
    next_para_id = max((int(x) for x in re.findall(r'<hh:paraPr id="(\d+)"', header)),
                       default=-1) + 1
    for pid in sorted(cell_paraprs, key=int):
        pm = re.search(r'<hh:paraPr id="%s".*?</hh:paraPr>' % pid, header, re.S)
        if not pm:
            continue
        block = pm.group(0)
        am = re.search(r'<hh:align horizontal="([^"]*)"', block)
        if am and am.group(1) == "CENTER":      # 이미 가운데면 그대로 사용
            center_map[pid] = pid
            continue
        clone = block.replace('id="%s"' % pid, 'id="%d"' % next_para_id, 1)
        clone = re.sub(r'(<hh:align horizontal=")[^"]*(")', r"\g<1>CENTER\g<2>", clone, count=1)
        header = header.replace("</hh:paraProperties>", clone + "</hh:paraProperties>", 1)
        header = _bump_itemcnt(header, "paraProperties")
        center_map[pid] = str(next_para_id)
        next_para_id += 1

    def _center_cell(m):
        return re.sub(r'(<hp:p\b[^>]*\bparaPrIDRef=")(\d+)(")',
                      lambda r: r.group(1) + center_map.get(r.group(2), r.group(2)) + r.group(3),
                      m.group(0))
    section = re.sub(r"<hp:tc\b.*?</hp:tc>", _center_cell, section, flags=re.S)

    _write_parts(args.src, args.dst, {SECTION: section, HEADER: header})
    print(f"[완료] 서식 적용 (제목 볼드 / 줄간격 {ls}% / 표 셀 가운데 정렬) → {args.dst}")


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

    p = sub.add_parser("build-schedule", help="출장일정 표를 7열 병합 표로 재구성")
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--table-id", required=True)
    p.add_argument("--data", required=True, help="days[] 구조의 JSON 파일")
    p.set_defaults(func=cmd_build_schedule)

    p = sub.add_parser("insert-para", help="문단 뒤에 본문 삽입")
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--anchor", required=True, help="삽입 기준이 되는 기존 문단의 텍스트")
    p.add_argument("--text", default=None)
    p.add_argument("--text-file", default=None, help="여러 줄 내용을 담은 텍스트 파일")
    p.set_defaults(func=cmd_insert_para)

    p = sub.add_parser("delete-para", help="anchor 텍스트를 가진 문단 삭제")
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--anchor", default=None, help="삭제할 문단 안 텍스트(유일해야 함)")
    p.add_argument("--anchor-file", default=None, help="삭제할 문단 텍스트를 담은 파일(유니코드 안전)")
    p.set_defaults(func=cmd_delete_para)

    p = sub.add_parser("format", help="서식 일괄 적용(제목 볼드/줄간격/표 속성/셀 정렬)")
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--schedule-table-id", default=None,
                   help="출장일정 표 id (dump로 확인). 지정 시 자리차지/나눔/글자취급해제 적용")
    p.add_argument("--line-spacing", type=int, default=120,
                   help="줄간격 백분율 (기본 120)")
    p.set_defaults(func=cmd_format)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
