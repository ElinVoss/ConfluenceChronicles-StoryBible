#!/usr/bin/env python3
import os, json, subprocess, re, sys, argparse

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LEX_LINT = os.path.join(REPO_ROOT, "tools", "lint", "lexicon_lint.py")
KG_LINT = os.path.join(REPO_ROOT, "tools", "lint", "knowledge_gate_lint.py")
INDEX_PATH = os.path.join(REPO_ROOT, "ai", "index", "index.jsonl")

def run(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out,_ = p.communicate()
    return p.returncode, out

def changed_files(base, head):
    rc, out = run(["git", "diff", "--name-only", f"{base}...{head}"])
    paths = [l.strip() for l in out.splitlines() if l.strip()]
    md = [p for p in paths if p.endswith(('.md','.txt'))]
    if not md:
        for root, _, files in os.walk('docs'):
            for fn in files:
                if fn.endswith(('.md','.txt')):
                    md.append(os.path.join(root, fn))
    return sorted(set(md))

def infer_era(path):
    m = re.search(r"/novellas/(N\d{2})/", path.replace('\\','/'))
    if m: return m.group(1)
    return "N05"

def ensure_index():
    if not os.path.exists(INDEX_PATH):
        rc, out = run(["python", "ai/index/build_index.py"])
        print(out)

def review_files(files):
    ensure_index()
    report = []
    for path in files:
        era = infer_era(path)
        report.append(f"### {path} (Era: {era})")
        if os.path.exists(LEX_LINT):
            rc, out = run(["python", LEX_LINT, path])
            if rc != 0:
                report.append("**Lexicon drift found:**\n```")
                report.append(out.strip())
                report.append("```\n")
            else:
                report.append("Lexicon: clean.\n")
        else:
            report.append("Lexicon linter not found.\n")
        if os.path.exists(KG_LINT):
            rc2, out2 = run(["python", KG_LINT, "--era", era, path])
            if rc2 != 0:
                report.append("**Knowledge Gate violations:**\n```")
                report.append(out2.strip())
                report.append("```\n")
            else:
                report.append("Knowledge Gate: clean.\n")
        else:
            report.append("Knowledge Gate linter not found.\n")
    return "\n".join(report)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--out", default=os.environ.get("AI_REVIEW_OUT","ai_review_comment.md"))
    args = ap.parse_args()
    files = changed_files(args.base, args.head)
    header = "# AI Review — Story Bible Enforcer\n"
    body = header + f"\nFiles reviewed: {len(files)}\n\n" + review_files(files) + "\n"
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"Wrote review to {args.out}")
    print(body)

if __name__ == "__main__":
    main()
