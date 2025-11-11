# Novella-Specific Story Bibles

This directory contains **generated story bibles** for individual novellas in the Confluence Chronicles saga. Each novella-specific bible is produced by the AI Story-Bible Engine from a structured novella brief.

## Purpose

While the main repository contains **global canon** that applies across all 30 novellas, each novella needs its own focused story bible that:

- Translates global canon into novella-specific applications
- Develops character arcs for that particular story
- Details locations, factions, and magic usage relevant to that novella
- Provides chapter-by-chapter beats for drafting
- Tracks costs and consequences specific to that narrative

These generated bibles serve as **drafting guides** for writers, ensuring consistency with canon while providing concrete creative direction.

---

## Directory Structure

Each novella-specific story bible lives in its own subdirectory:

```
products/
├── N01-story-bible/
├── N02-story-bible/
├── N03-story-bible/
...
├── N29-story-bible/
└── N30-story-bible/
```

### Standard Bible Structure

Each `<novella-id>-story-bible/` directory contains:

```
<novella-id>-story-bible/
├── 00-brief/
│   └── novella-brief.yaml          # Copy of the input brief
├── 01-canon-overrides/
│   └── canon-deltas.md             # Novella-specific canon clarifications
├── 02-characters/
│   ├── core-cast.md                # POV and major characters
│   └── supporting-cast.md          # Secondary and minor characters
├── 03-world/
│   ├── key-locations.md            # Featured locations with sensory details
│   └── factions.md                 # Relevant factions and their roles
├── 04-magic/
│   └── local-limits-and-edges.md   # Soulpulse applications, costs, boundaries
├── 05-plot/
│   ├── act-beats.md                # High-level three-act structure
│   └── chapter-beats.md            # Chapter-by-chapter breakdown
└── README.md                       # Overview and usage notes for this bible
```

---

## Usage Workflow

### Step 1: Create a Novella Brief

Copy the template and fill it out:

```bash
cp docs/05-ops/novella-brief.template.yaml docs/05-ops/N01-brief.yaml
```

Edit `docs/05-ops/N01-brief.yaml` with:
- Novella ID, title, era, target word count
- Tone pillars and themes
- Required characters and constraints
- Must-hit story beats

Refer to `docs/05-ops/novella-brief.schema.yaml` for field documentation.

### Step 2: Generate the Story Bible

**Option A: Using Manus or another AI agent**

Provide the agent with:
1. The system prompt: `prompts/ai-bible-engine-system.txt`
2. Relevant canon files from `docs/01-canon/` (master lexicon, knowledge gates, magic system)
3. Your completed novella brief: `docs/05-ops/N01-brief.yaml`

The agent will generate all files according to the structure above.

**Option B: Using the Python script**

```bash
python tools/forge_bible.py --novella-brief docs/05-ops/N01-brief.yaml
```

This will:
- Read the brief and system prompt
- Call an LLM with canon context
- Parse the output into the proper file structure
- Write files to `products/N01-story-bible/`

### Step 3: Review and Refine

Generated bibles should be reviewed for:
- **Canon compliance**: Run `make lint` to check lexicon and knowledge gate adherence
- **Character arc specificity**: Are arcs concrete enough to execute?
- **Cost tracking**: Is every working's cost visible and tracked?
- **Structural integrity**: Do chapter beats flow logically and add up to target word count?

Iterate as needed, providing specific feedback to the AI or manually editing files.

### Step 4: Use for Drafting

Once approved, the story bible serves as the **primary reference** during drafting:
- `05-plot/chapter-beats.md` provides the roadmap
- `02-characters/core-cast.md` ensures character consistency
- `04-magic/local-limits-and-edges.md` tracks costs and limits
- `03-world/key-locations.md` provides sensory details

Combine with scene templates from `docs/05-ops/scene-templates/` for structured drafting.

---

## Relationship to Global Canon

**Global canon always takes precedence.** If a generated bible conflicts with:

- `docs/01-canon/master-lexicon.md`
- `docs/01-canon/soulpulse-resonance-system-production-canon.md`
- `docs/01-canon/knowledge-gates-and-scene-ladder-N01-N05.md`
- Character definitions in `docs/03-characters/`
- Turning structure in `docs/04-plot/turnings/`

...then the global canon is correct and the generated bible must be revised.

The `01-canon-overrides/canon-deltas.md` file in each bible should document any novella-specific interpretations or clarifications, but these must not contradict global rules.

---

## Maintenance and Versioning

Generated bibles are **living documents** during development:

- Initial generation provides the foundation
- Revisions incorporate feedback and discoveries
- Final version is locked when drafting begins
- Post-draft updates may occur based on editorial needs

When updating a bible:
1. Document changes in the bible's README.md
2. Ensure changes don't break continuity with adjacent novellas
3. Update continuity tracking in `docs/04-plot/meta/` if needed
4. Re-run linters to verify compliance

---

## Integration with Existing Tools

Generated bibles work alongside existing repository tools:

### Linters (`tools/lint/`)
- `lexicon_lint.py`: Validates terminology against master lexicon
- `knowledge_gate_lint.py`: Ensures era-appropriate content

Run linters on generated content:
```bash
make lint
python tools/lint/knowledge_gate_lint.py --era N01 products/N01-story-bible/
```

### Scene Templates (`docs/05-ops/scene-templates/`)
Use `scene-ladder-template.md` when drafting from chapter beats, ensuring proper Te'Oga time formatting and cost tracking.

### Ops Decks (`docs/05-ops/ops-decks/`)
For novellas N16-N30, ops decks provide additional operational guidance that complements generated bibles.

---

## Troubleshooting

**Problem**: Generated bible conflicts with canon

**Solution**: Review `01-canon-overrides/canon-deltas.md` in the bible. If conflict is real, regenerate with explicit canon constraints in the brief's `forbidden_elements` field.

---

**Problem**: Character arcs feel vague or generic

**Solution**: Revise the brief's `must_hit_beats` to be more specific. Regenerate or manually edit `02-characters/core-cast.md` with concrete begin/end states.

---

**Problem**: Chapter beats don't add up to target word count

**Solution**: Adjust `target_length_words` in brief or modify chapter count in `05-plot/chapter-beats.md`. Typical chapters are 800-1,300 words.

---

**Problem**: Magic costs aren't tracked consistently

**Solution**: Check `04-magic/local-limits-and-edges.md` for cost definitions. Ensure each chapter beat in `05-plot/chapter-beats.md` notes costs when workings occur.

---

**Problem**: Linter flags anachronistic terminology

**Solution**: Review knowledge gates for the novella's era. Regenerate with stricter `forbidden_elements` in the brief, or manually edit to use era-appropriate terms.

---

## Contributing

When adding new bibles to this directory:

1. Follow the standard structure above
2. Include a README.md in each bible directory explaining its specific focus
3. Commit with clear messages: `feat: add N01 story bible`
4. Update this README if you discover new patterns or best practices

---

## Example: N01 Story Bible

For reference, here's what a complete N01 bible might contain:

**00-brief/novella-brief.yaml**  
The input brief defining N01's scope, themes, and constraints.

**01-canon-overrides/canon-deltas.md**  
Notes that N01 is pre-terminology era; magic feels instinctive and miraculous.

**02-characters/core-cast.md**  
Jhace Torrins: Arc from "brute-force problem solver" to "recognizing limits"; vein-burn begins at ~2.5cm by end.  
Tiffani Merrow: Arc from "precision as control" to "perfection as prison"; calcification seeds appear.

**02-characters/supporting-cast.md**  
Mobel Kress: Early isolation symptoms; foreshadows N05 transformation.  
Venn Eries: Philosophical voice; vitality drain begins subtly.

**03-world/key-locations.md**  
Coreven—Underface: Industrial forge district, heat-grid hum, metal-on-stone percussion.  
Tiffani's glassworks: Crystalline precision, controlled temperature, fragile beauty.

**03-world/factions.md**  
Pre-factional era: Informal clusters forming around different approaches (structural vs. continuity vs. purity).

**04-magic/local-limits-and-edges.md**  
Instinctive workings: healing (warmth, golden glow), shaping (precision, crystalline clarity).  
Costs: vein-burn (Jhace), calcification (Tiffani), isolation (Mobel), vitality drain (Venn).  
Failure modes: pain, exhaustion, tremor, cascade.

**05-plot/act-beats.md**  
Act I: Scaffold incident, Jhace's vein-burn begins, Tiffani's precision work shows costs.  
Act II: Failed working reveals Confluence danger, Mobel's isolation worsens, factions begin forming.  
Act III: Climactic choice, costs become permanent, new equilibrium with visible consequences.

**05-plot/chapter-beats.md**
15 chapters, each 800-1,300 words, alternating Jhace/Tiffani POV, with specific scene summaries, emotional beats, and cost tracking.

---

**Version**: 1.0  
**Last Updated**: 2025-11-11  
**Maintained By**: Story Bible Operations Team
