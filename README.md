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
    novellas/
    meta/
  05-ops/
tools/
  lint/
  templates/
  forge_bible.py
prompts/
products/
.github/
  ISSUE_TEMPLATE/
  workflows/
```
- **Canon**: rules you can't break.  
- **World/Characters**: reference.  
- **Plot**: turning/novella outlines and meta-analysis.  
- **Ops**: templates, checklists, lint packs, and AI Bible Engine contract.  
- **Tools**: custom linters, generators, and bible forge script.  
- **Prompts**: system prompts for AI agents.  
- **Products**: generated novella-specific story bibles.

## House Rules (must-read)
- Use **Te’Oga time units** in prose and docs (tide/anneal/crucible/casting).  
- **Costs are mandatory** on-page for every working (vein-burn/echo/identity tax).  
- **Knowledge gates**: don’t leak N05 terms into N01–N04 drafts.
- **Confluence** is terminal for mortals; gods cannot Confluence.

## AI Story-Bible Engine

This repository includes an **AI Story-Bible Engine** that generates novella-specific story bibles from structured briefs.

### What It Does

- Transforms high-level novella briefs (YAML) into comprehensive drafting guides
- Ensures canon compliance and knowledge gate adherence
- Generates character arcs, location details, magic system applications, and chapter beats
- Outputs to `products/<novella-id>-story-bible/` with standardized structure

### Quick Workflow

1. **Create a brief**: Copy `docs/05-ops/novella-brief.template.yaml` to `docs/05-ops/N0X-brief.yaml` and fill it out
2. **Generate the bible**: Either:
   - Use an AI agent (like Manus) with `prompts/ai-bible-engine-system.txt` + the brief + canon files
   - Or run: `python tools/forge_bible.py --novella-brief docs/05-ops/N0X-brief.yaml`
3. **Review and refine**: Check canon compliance, character arc specificity, and cost tracking
4. **Use for drafting**: Generated bibles provide chapter-by-chapter roadmaps and reference materials

### Key Files

- **Contract**: `docs/05-ops/ai-bible-engine.md` — human-readable operator manual
- **System Prompt**: `prompts/ai-bible-engine-system.txt` — machine-facing instructions for LLMs
- **Brief Schema**: `docs/05-ops/novella-brief.schema.yaml` — field documentation
- **Brief Template**: `docs/05-ops/novella-brief.template.yaml` — N01 exemplar
- **Forge Script**: `tools/forge_bible.py` — automated generation via OpenAI API
- **Products Directory**: `products/README.md` — detailed usage and structure guide

### Requirements for Script

- Python 3.10+
- `pip3 install openai pyyaml`
- Environment variable: `OPENAI_API_KEY`

## Local Linting
- Python 3.10+ recommended.
- `make lint` runs `tools/lint/lexicon_lint.py` and `tools/lint/knowledge_gate_lint.py`.
- Or call linters directly:
  - `python tools/lint/lexicon_lint.py docs`
  - `python tools/lint/knowledge_gate_lint.py --era N03 docs/04-plot/turnings/Turning1-N01-05.md`

## Licensing
By default this repo is **private / all rights reserved**. Update `LICENSE` if you switch.
