#!/usr/bin/env python3
import os, re, json, argparse

def norm_ws(s):
    return re.sub(r"\s+", " ", s.strip())

def build_regex_from_term(term: str) -> str:
    parts = re.split(r"\s*[/,|]\s*", term.strip())
    patterns = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        esc = re.escape(p)
        esc = re.sub(r"\\\s+", r"\\s+", esc)
        if re.search(r"(hour|minute|week|month|year)$", p, re.I):
            base = re.escape(re.sub(r"(s)?$", "", p))
            esc = base + r"s?"
        patterns.append(rf"\\b{esc}\\b")
    if len(patterns) == 1:
        return patterns[0]
    return "(" + "|".join(patterns) + ")"

def parse_markdown_table(lines):
    rows = []
    header = None
    for ln in lines:
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if not cells or all(not c for c in cells):
            continue
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if all(re.match(r"^:?-{3,}:?$", c) for c in cells):
            continue
        while len(cells) < len(header):
            cells.append("")
        row = dict(zip(header, cells))
        rows.append(row)
    return rows

def parse_arrows(lines):
    rows = []
    rx = re.compile(r"^[\-\*]\s*([^#\n]+?)\s*(?:→|->)\s*([^#\n]+)$")
    for ln in lines:
        m = rx.search(ln.strip())
        if not m:
            continue
        src = norm_ws(m.group(1))
        dst = norm_ws(m.group(2))
        rows.append({"modern": src, "in-world": dst, "notes": "", "regex": ""})
    return rows

def main():
    ap = argparse.ArgumentParser(description="Extract lexicon substitution rules from Master Lexicon")
    ap.add_argument("--lexicon", default="docs/01-canon/master-lexicon.md")
    ap.add_argument("--out", default="tools/lint/lexicon_rules.json")
    args = ap.parse_args()

    if not os.path.isfile(args.lexicon):
        print("Lexicon file not found:", args.lexicon)
        return 2

    text = open(args.lexicon, "r", encoding="utf-8", errors="ignore").read()
    lines = text.splitlines()

    table_rows = parse_markdown_table(lines)
    arrow_rows = parse_arrows(lines)

    rows = []
    if table_rows:
        for r in table_rows:
            modern = r.get("modern") or r.get("modern terms") or r.get("source") or ""
            inworld = r.get("in-world") or r.get("in world") or r.get("target") or r.get("replacement") or ""
            regex = r.get("regex") or r.get("pattern") or ""
            notes = r.get("notes","")
            if modern and inworld:
                rows.append({"modern": modern, "in_world": inworld, "regex": regex, "notes": notes})
    if arrow_rows:
        for r in arrow_rows:
            rows.append({"modern": r["modern"], "in_world": r["in-world"], "regex": r.get("regex",""), "notes": r.get("notes","")})

    # Dedup by modern+regex (case-insensitive)
    dedup = {}
    for r in rows:
        key = (r["modern"].lower().strip(), r.get("regex","").strip())
        if key not in dedup:
            dedup[key] = r
    rows = list(dedup.values())

    if not rows:
        rows = [
            {"modern":"week/weeks","in_world":"anneal/anneals","regex":"","notes":""},
            {"modern":"month/months","in_world":"crucible/crucibles","regex":"","notes":""},
            {"modern":"year/years","in_world":"casting/castings","regex":"","notes":""},
            {"modern":"hour/hours","in_world":"tides/breaths (context)","regex":"","notes":""},
            {"modern":"minute/minutes","in_world":"breaths/strokes (context)","regex":"","notes":""},
        ]

    rules = []
    for r in rows:
        pattern = r.get("regex","").strip()
        if not pattern:
            pattern = build_regex_from_term(r["modern"])
        rules.append({
            "pattern": pattern,
            "suggest": r["in_world"],
            "source": r["modern"],
            "notes": r.get("notes","")
        })

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"rules": rules}, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(rules)} rules to {args.out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
