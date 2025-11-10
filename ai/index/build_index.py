#!/usr/bin/env python3
import os, json, re, argparse, glob, hashlib

def read_text(path):
    try:
        return open(path, "r", encoding="utf-8", errors="ignore").read()
    except:
        return ""

def chunk_text(text, max_chars=1800, overlap=200):
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + max_chars)
        cut = text.rfind("\n\n", start, end)
        if cut == -1 or cut <= start + 200:
            cut = end
        chunks.append(text[start:cut])
        start = max(cut - overlap, cut)
    return [c for c in chunks if c.strip()]

def path_tags(path):
    tags = []
    p = path.replace("\\", "/")
    m = re.search(r"/novellas/(N\d{2})", p)
    if m: tags.append(m.group(1))
    if "/01-canon/" in p: tags.append("canon")
    if "/05-ops/" in p: tags.append("ops")
    return tags

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", nargs="+", default=["docs/01-canon","docs/04-plot/novellas","docs/05-ops"])
    ap.add_argument("--out", default="ai/index/index.jsonl")
    ap.add_argument("--max-chars", type=int, default=1800)
    ap.add_argument("--overlap", type=int, default=200)
    args = ap.parse_args()

    records = []
    for root in args.roots:
        for path in glob.glob(os.path.join(root, "**", "*.*"), recursive=True):
            if not path.lower().endswith((".md",".txt")): continue
            if not os.path.isfile(path): continue
            txt = read_text(path)
            for i, ch in enumerate(chunk_text(txt, args.max_chars, args.overlap)):
                rid = hashlib.md5(f"{path}:{i}".encode()).hexdigest()
                rec = {"id":rid, "path":path.replace("\\","/"), "chunk_id":i, "text":ch, "tags":path_tags(path)}
                records.append(rec)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False)+"\n")
    print(f"Wrote {len(records)} chunks to {args.out}")

if __name__ == "__main__":
    main()
