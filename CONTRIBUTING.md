# Contributing

- Keep **canon** authoritative. If your change affects rules (magic, lexicon, time units), edit `/docs/01-canon/` and reference changes in your PR.
- Respect **Knowledge Gates** (N01–N05). Don’t leak later-era terms into early drafts.
- Show **costs** on-page for every working.
- Use the **Scene Ladder Template** in `/docs/05-ops/scene-templates/` for new scenes.
- PRs must pass CI linters and include a brief **Impact on Canon** note.


## Quick Start for Contributors

**Branching & PRs**
- Create a feature branch: `git switch -c Nxx-chYY-scope`
- Commit focused changes; open a PR using the provided template. CI and the AI Review bot will respond.

**Make Lint Contract (must pass locally before PR)**
```bash
# 1) Sync lexicon rules from the Master Lexicon
python tools/lint/lexicon_sync.py

# 2) Run the full linter suite
make lint
```
- The **Lexicon Linter** enforces in-world terminology from `docs/01-canon/master-lexicon.md`.
- The **Knowledge Gate Linter** prevents era leaks. Era is inferred from the path:
  - `docs/04-plot/novellas/N09/...` ⇒ `--era N09`

**Regex Column for Precision**
- How to write precise patterns (boundaries, alternatives, whitespace, examples):
  See `docs/01-canon/master-lexicon.md#how-to-extend-the-regex-column-for-linter-precision`.

**Temporary Exemptions (only when documenting)**
- File-wide: add `<!-- LEXICON_LINT:OFF -->` at the top.
- Region-only: wrap content between
  `<!-- LEXICON_LINT:START-IGNORE -->` and `<!-- LEXICON_LINT:END-IGNORE -->`.

**Local Requirements**
- Python 3.11+, no external dependencies required.
- Optional: GitHub CLI (`gh`) for repo bootstrap and managing secrets.

**What CI Does**
- Builds the RAG index (`ai/index/build_index.py`).
- Syncs lexicon rules, runs linters.
- Posts an AI Review comment on your PR with violations and citations.
