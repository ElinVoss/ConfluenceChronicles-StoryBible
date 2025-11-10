#!/usr/bin/env python3
import sys, re, os, argparse, json

DEFAULT_RULES = [
    {"pattern": r"\\bweeks?\\b", "suggest": "anneal/anneals"},
    {"pattern": r"\\bmonths?\\b", "suggest": "crucible/crucibles"},
    {"pattern": r"\\byears?\\b", "suggest": "casting/castings"},
    {"pattern": r"\\bhours?\\b", "suggest": "tides/breaths (context)"},
    {"pattern": r"\\bminutes?\\b", "suggest": "breaths/strokes (context)"},
    {"pattern": r"\\bradio|broadcast|airwaves\\b", "suggest": "bell-line/crier/signal board"},
    {"pattern": r"\\bphone|call|text\\b", "suggest": "runner/bellman/notice slate"},
    {"pattern": r"\\belectric(ity|al)?|power\\s+grid\\b", "suggest": "heat-grid/pressure-lines"},
    {"pattern": r"\\bpolice|cops\\b", "suggest": "guard cohort/Bureau agents"},
    {"pattern": r"\\bhospital|ER\\b", "suggest": "clinic hall/recovery ward/quench-hall"},
    {"pattern": r"\\bGPS|map\\s+app\\b", "suggest": "route slate/surveyor’s marks"},
]

FILE_OFF_TOKEN = "<!-- LEXICON_LINT:OFF -->"
REGION_START = "<!-- LEXICON_LINT:START-IGNORE -->"
REGION_END = "<!-- LEXICON_LINT:END-IGNORE -->"

def load_rules():
    path = os.path.join(os.path.dirname(__file__), "lexicon_rules.json")
    try:
        data = json.load(open(path, "r", encoding="utf-8"))
        rules = data.get("rules", [])
        if rules:
            return rules
    except Exception:
        pass
    return DEFAULT_RULES

def strip_ignored_regions(text: str) -> str:
    # Remove regions between START-IGNORE and END-IGNORE
    out = []
    ignore = False
    for line in text.splitlines(keepends=True):
        if REGION_START in line:
            ignore = True
            continue
        if REGION_END in line:
            ignore = False
            continue
        if not ignore:
            out.append(line)
    return "".join(out)

def scan_file(path, rules):
    hits = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception:
        return hits
    # file-level OFF
    if FILE_OFF_TOKEN in text:
        return hits
    # region-level ignore
    text = strip_ignored_regions(text)
    for r in rules:
        rx = re.compile(r.get("pattern"), re.I)
        for m in rx.finditer(text):
            start = max(0, m.start()-40)
            end = min(len(text), m.end()+40)
            ctx = text[start:end].replace("\\n"," ")
            hits.append((path, m.group(0), r.get("suggest",""), ctx))
    return hits

def main():
    ap = argparse.ArgumentParser(description="Lexicon linter; loads rules from lexicon_rules.json if present")
    ap.add_argument("paths", nargs="+")
    args = ap.parse_args()
    rules = load_rules()
    files = []
    for p in args.paths:
        if os.path.isdir(p):
            for root, _, fs in os.walk(p):
                for fn in fs:
                    if fn.lower().endswith((".md", ".txt", ".markdown")):
                        files.append(os.path.join(root, fn))
        else:
            files.append(p)
    any_hits = False
    for fpath in sorted(files):
        for path, term, repl, ctx in scan_file(fpath, rules):
            any_hits = True
            print(f"[LEXICON] {path}: '{term}' -> suggested '{repl}'")
            print(f"  ...{ctx}...")
    if any_hits:
        print("\nLexicon linter found drift. Please replace terms.")
        sys.exit(1)
    else:
        print("Lexicon linter: clean.")
        sys.exit(0)

if __name__ == "__main__":
    main()
