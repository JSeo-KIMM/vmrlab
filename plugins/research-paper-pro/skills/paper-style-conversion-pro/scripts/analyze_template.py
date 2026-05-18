#!/usr/bin/env python3
"""Analyze a .docx paper template and report its formatting.

The report tells you (Claude) exactly which named styles, margins, fonts,
and table styles the template defines, so you can map a draft's headings
and body text onto the *template's own* styles instead of guessing.

Usage:
    python analyze_template.py <template.docx> [--json report.json]

A human-readable summary is printed to stdout. With --json, a
machine-readable report is also written for build_paper.py / your reference.

Requires: python-docx  (pip install python-docx)
"""
import sys
import json
import argparse

# Windows consoles often default to cp949/cp1252; template text may contain
# em-dashes, Korean style names, etc. Force UTF-8 so printing never crashes.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

try:
    from docx import Document
    from docx.oxml.ns import qn
except ImportError:
    sys.exit("python-docx is required:  pip install python-docx")


def cm(emu):
    return None if emu is None else round(emu / 360000, 2)


def pt(length):
    return None if length is None else round(length / 12700, 1)


def analyze(path):
    doc = Document(path)
    report = {
        "template": path,
        "sections": [],
        "paragraph_styles": [],
        "character_styles": [],
        "table_styles": [],
        "default_font": None,
        "outline": [],
    }

    # Default document font
    try:
        nf = doc.styles["Normal"].font
        report["default_font"] = {"name": nf.name, "size_pt": pt(nf.size)}
    except Exception:
        pass

    # Page setup (margins, size, orientation, columns)
    for sec in doc.sections:
        cols = sec._sectPr.find(qn("w:cols"))
        col_num, col_space = 1, None
        if cols is not None:
            col_num = int(cols.get(qn("w:num"), "1"))
            sp = cols.get(qn("w:space"))
            col_space = round(int(sp) / 567, 2) if sp else None  # twips -> cm
        report["sections"].append({
            "page_width_cm": cm(sec.page_width),
            "page_height_cm": cm(sec.page_height),
            "margin_top_cm": cm(sec.top_margin),
            "margin_bottom_cm": cm(sec.bottom_margin),
            "margin_left_cm": cm(sec.left_margin),
            "margin_right_cm": cm(sec.right_margin),
            "header_distance_cm": cm(sec.header_distance),
            "footer_distance_cm": cm(sec.footer_distance),
            "orientation": str(sec.orientation),
            "columns": col_num,
            "column_spacing_cm": col_space,
        })

    # Styles
    for style in doc.styles:
        try:
            stype = str(style.type)
        except Exception:
            continue
        if "PARAGRAPH" in stype:
            font = style.font
            pf = style.paragraph_format
            report["paragraph_styles"].append({
                "name": style.name,
                "base_style": style.base_style.name if style.base_style else None,
                "font_name": font.name,
                "font_size_pt": pt(font.size),
                "bold": font.bold,
                "italic": font.italic,
                "alignment": str(pf.alignment) if pf.alignment else None,
                "line_spacing": pf.line_spacing,
                "space_before_pt": pt(pf.space_before),
                "space_after_pt": pt(pf.space_after),
            })
        elif "CHARACTER" in stype:
            report["character_styles"].append(style.name)
        elif "TABLE" in stype:
            report["table_styles"].append(style.name)

    # Body outline so you can see what placeholder content exists
    for i, para in enumerate(doc.paragraphs[:120]):
        text = para.text.strip()
        if not text and not (para.style and para.style.name):
            continue
        report["outline"].append({
            "index": i,
            "style": para.style.name if para.style else None,
            "text_preview": text[:100],
        })

    return report


def print_report(r):
    print("=" * 64)
    print(f"TEMPLATE: {r['template']}")
    print("=" * 64)

    if r["default_font"]:
        print(f"\n[Default font]  {r['default_font']['name']}  "
              f"{r['default_font']['size_pt']} pt")

    print("\n[Page setup]")
    for i, s in enumerate(r["sections"]):
        print(f"  section {i}: {s['page_width_cm']} x {s['page_height_cm']} cm "
              f"({s['orientation']})  ->  {s['columns']} column(s)"
              + (f", spacing {s['column_spacing_cm']} cm" if s['column_spacing_cm'] else ""))
        print(f"    margins  T {s['margin_top_cm']} / B {s['margin_bottom_cm']} "
              f"/ L {s['margin_left_cm']} / R {s['margin_right_cm']} cm")

    print(f"\n[Paragraph styles]  ({len(r['paragraph_styles'])})")
    for s in r["paragraph_styles"]:
        bits = []
        if s["font_name"]:
            bits.append(s["font_name"])
        if s["font_size_pt"]:
            bits.append(f"{s['font_size_pt']}pt")
        if s["bold"]:
            bits.append("bold")
        if s["alignment"]:
            bits.append(s["alignment"].split()[0].lower())
        if s["line_spacing"]:
            bits.append(f"ls={s['line_spacing']}")
        print(f"  - {s['name']:<28} {'  '.join(bits)}")

    if r["table_styles"]:
        print(f"\n[Table styles]  {', '.join(r['table_styles'])}")
    if r["character_styles"]:
        print(f"\n[Character styles]  {', '.join(r['character_styles'])}")

    print(f"\n[Body outline]  (first {len(r['outline'])} blocks)")
    for o in r["outline"]:
        print(f"  {o['index']:>3}  [{o['style']}]  {o['text_preview']}")
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template")
    ap.add_argument("--json", help="also write a JSON report to this path")
    args = ap.parse_args()

    report = analyze(args.template)
    print_report(report)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"JSON report written: {args.json}")


if __name__ == "__main__":
    main()
