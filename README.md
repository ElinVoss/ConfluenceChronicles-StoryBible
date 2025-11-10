# Confluence Chronicles — Story Bible (Production Repo)

This is the **production-grade story bible** for the Confluence Chronicles. It’s organized for teams: writers’ room, editors, showrunners, and ops.  
All canon, ops templates, and outlines live here. Tooling enforces **lexicon**, **knowledge gates**, and **cost visibility**.

## Quick Start
- Browse `/docs` first.
- See `/docs/01-canon/` for **Master Lexicon**, **Magic System Production Canon**, and **N01–N05 Knowledge Gates & Scene Ladder**.
- Use `make lint` (or run the Python scripts in `tools/lint/`) to check lexicon and era redlines.
- Open `.github/workflows/ci.yml` for the CI that runs the custom linters in PRs.

## Structure
```
docs/
  00-overview/
  01-canon/
  02-world/
  03-characters/
  04-plot/
    turnings/
    meta/
  05-ops/
tools/
  lint/
  templates/
.github/
  ISSUE_TEMPLATE/
  workflows/
```
- **Canon**: rules you can’t break.  
- **World/Characters**: reference.  
- **Plot**: turning/novella outlines and meta-analysis.  
- **Ops**: templates, checklists, and lint packs.  
- **Tools**: custom linters, generators.

## House Rules (must-read)
- Use **Te’Oga time units** in prose and docs (tide/anneal/crucible/casting).  
- **Costs are mandatory** on-page for every working (vein-burn/echo/identity tax).  
- **Knowledge gates**: don’t leak N05 terms into N01–N04 drafts.
- **Confluence** is terminal for mortals; gods cannot Confluence.

## Local Linting
- Python 3.10+ recommended.
- `make lint` runs `tools/lint/lexicon_lint.py` and `tools/lint/knowledge_gate_lint.py`.
- Or call linters directly:
  - `python tools/lint/lexicon_lint.py docs`
  - `python tools/lint/knowledge_gate_lint.py --era N03 docs/04-plot/turnings/Turning1-N01-05.md`

## Licensing
By default this repo is **private / all rights reserved**. Update `LICENSE` if you switch.
