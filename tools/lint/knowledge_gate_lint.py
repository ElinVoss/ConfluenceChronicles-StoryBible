#!/usr/bin/env python3

import sys, os, re, argparse

BANS = {
    "N01": re.compile(r"\b(resonance|principle|veins?|Hollowing|Confluence|suppression|factions?|god-?vessels?)\b", re.I),
    "N02": re.compile(r"\b(four principles|Hollowing|dual-?principle|Confluence|suppression|god-?vessels?)\b", re.I),
    "N03": re.compile(r"\b(four principles|Hollowing|dual-?principle|Confluence|suppression|god-?vessels?)\b", re.I),
    "N04": re.compile(r"\b(Confluence|suppression|god-?vessels?)\b", re.I),
    "N05": None,
}

def scan_file(path, era):
    rx = BANS.get(era)
    if not rx:
        return []
    try:
        txt = open(path, "r", encoding="utf-8", errors="ignore").read()
    except:
        return []
    hits = []
    for m in rx.finditer(txt):
        start = max(0, m.start()-40)
        end = min(len(txt), m.end()+40)
        ctx = txt[start:end].replace("\n"," ")
        hits.append((m.group(0), ctx))
    return hits

def main():
    ap = argparse.ArgumentParser(description="Knowledge Gate linter")
    ap.add_argument("--era", required=True, choices=["N01","N02","N03","N04","N05","N06","N07","N08","N09","N10","N11","N12","N13","N14","N15","N16","N17","N18","N19","N20","N21","N22","N23","N24","N25","N26","N27","N28","N29","N30"])
    ap.add_argument("paths", nargs="+")
    args = ap.parse_args()

    files = []
    for p in args.paths:
        if os.path.isdir(p):
            for root, _, fs in os.walk(p):
                for fn in fs:
                    if fn.lower().endswith((".md",".markdown",".txt")):
                        files.append(os.path.join(root, fn))
        else:
            files.append(p)

    any_hits = False
    for f in sorted(files):
        hits = scan_file(f, args.era)
        for term, ctx in hits:
            any_hits = True
            print(f"[GATE {args.era}] {f}: term '{term}' not allowed")
            print(f"  ...{ctx}...")
    if any_hits:
        print(f"\nKnowledge Gate {args.era} violations found.")
        sys.exit(1)
    else:
        print(f"Knowledge Gate {args.era}: clean.")
        sys.exit(0)

if __name__ == "__main__":
    main()
