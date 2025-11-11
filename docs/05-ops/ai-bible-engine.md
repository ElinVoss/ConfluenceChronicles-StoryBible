# Confluence Chronicles – AI Story-Bible Engine (Operator Manual)

## Purpose

This repository serves as the **global canonical bible** for the Confluence Chronicles saga, containing the master lexicon, magic system rules, character definitions, and plot structures that govern all 30 novellas across 6 turnings.

The **AI Story-Bible Engine** is a specialized AI worker designed to transform high-level novella briefs into comprehensive, novella-specific story bibles. It operates as a lore department assistant that:

- **Consumes** a structured novella brief (YAML format) defining the scope, themes, and requirements for a single novella
- **Respects** all global canon rules, temporal constraints, and knowledge gates
- **Produces** a complete novella-specific story bible with character arcs, location details, magic system applications, and chapter-by-chapter beats

The engine ensures consistency across the saga while allowing each novella to explore unique themes, locations, and character development within the established framework.

---

## Golden Rules

The AI Bible Engine operates under strict constraints to maintain saga integrity:

### 1. Canon is Law

Global canon **always** overrides local creative impulses. The engine must:

- Reference `docs/01-canon/master-lexicon.md` for all terminology
- Respect the Soulpulse Resonance System production canon
- Honor knowledge gates defined in `knowledge-gates-and-scene-ladder-N01-N05.md`
- Never contradict established character histories, world geography, or temporal mechanics
- Flag any conflicts between the novella brief and canon, proposing resolutions that preserve canon

### 2. Cost and Consequences are Mandatory

Every use of power, magic, or extraordinary ability **must** show explicit on-page cost. The engine must:

- Include physiological costs (vein-burn, calcification, isolation, vitality drain)
- Track psychological costs (echo stacking, identity erosion, moral compromise)
- Document systemic costs (environmental damage, lattice dust contamination, societal impact)
- Ensure costs escalate appropriately across the novella's arc
- Never allow "free" workings or consequence-free power usage

### 3. Era Purity

Knowledge, technology, and faction development must respect temporal boundaries. The engine must:

- Prevent future Turnings from leaking backward (no N15 tech appearing in N03)
- Respect the knowledge ceiling for each novella's era (see knowledge gates documentation)
- Ensure character awareness matches their position in the timeline
- Avoid anachronistic terminology (e.g., no "Confluence" terminology in N01-N03)
- Maintain consistent technological and magical development progression

### 4. No Meta Layer

Story materials must remain **in-world** and immersive. The engine must:

- Never reference AI, prompts, repositories, or the generation process in output
- Avoid "guilty" meta-commentary about the writing process
- Write as if documenting an actual world, not constructing a narrative
- Keep all technical/operational notes in designated metadata sections, not in story content

---

## Inputs

The AI Bible Engine requires a **NOVELLA BRIEF** as its primary input. This structured YAML document contains:

### Required Fields

- **novella_id**: Unique identifier (e.g., "N01", "N17")
- **working_title**: The novella's title or working title
- **era**: Which Turning the novella belongs to (e.g., "Turning_1", "Turning_4")
- **target_length_words**: Expected word count (typically 40,000-50,000)

### Thematic Fields

- **tone_pillars**: 2-4 core tonal qualities (e.g., "forge-punk grit", "glass-punk fragility")
- **primary_theme**: The central thematic question or tension
- **secondary_themes**: Supporting thematic threads

### Constraint Fields

- **required_characters**: Characters who must appear or be referenced
- **forbidden_elements**: Explicit constraints (e.g., "No Confluence scenes in first three chapters")
- **must_hit_beats**: Non-negotiable story beats that must occur

### Optional Fields

- **preferred_locations**: Specific locations to feature
- **magic_focus**: Which aspects of the Soulpulse system to emphasize
- **faction_involvement**: Which factions should be prominent
- **continuity_hooks**: Connections to other novellas

The brief template is available at `docs/05-ops/novella-brief.template.yaml`.

---

## Required Output Structure

The AI Bible Engine must produce a complete novella-specific story bible with the following file structure:

```
products/<novella-id>-story-bible/
├── 00-brief/
│   └── novella-brief.yaml          # Copy of the input brief
├── 01-canon-overrides/
│   └── canon-deltas.md             # Any novella-specific canon clarifications
├── 02-characters/
│   ├── core-cast.md                # POV and major characters
│   └── supporting-cast.md          # Secondary and minor characters
├── 03-world/
│   ├── key-locations.md            # Featured locations with sensory details
│   └── factions.md                 # Relevant factions and their roles
├── 04-magic/
│   └── local-limits-and-edges.md   # Soulpulse applications, costs, and boundaries
├── 05-plot/
│   ├── act-beats.md                # High-level three-act structure
│   └── chapter-beats.md            # Chapter-by-chapter breakdown
└── README.md                       # Overview and usage notes
```

### File Content Requirements

#### 00-brief/novella-brief.yaml
- Exact copy of the input brief for reference

#### 01-canon-overrides/canon-deltas.md
- Document any novella-specific interpretations or clarifications
- Flag any tensions with global canon and how they're resolved
- Should be minimal; most content should align with existing canon

#### 02-characters/core-cast.md
For each core character, include:
- **Role**: Their function in this novella's story
- **Arc**: Concrete emotional/psychological journey with beginning and end states
- **Relationships**: Key dynamics with other characters
- **Costs**: What they sacrifice or suffer across the novella
- **Voice notes**: Distinctive speech patterns, internal monologue style

#### 02-characters/supporting-cast.md
For secondary characters:
- **Function**: Why they exist in the story
- **Distinctiveness**: What makes them memorable
- **Connection to core cast**: How they affect main characters

#### 03-world/key-locations.md
For each featured location:
- **Sensory profile**: Sights, sounds, smells, textures
- **Cultural significance**: What this place means to characters
- **Dramatic potential**: What kinds of scenes work here
- **Canon alignment**: References to global world documentation

#### 03-world/factions.md
For relevant factions:
- **Presence in this novella**: How they appear or influence events
- **Representative characters**: Who embodies this faction
- **Conflict vectors**: How they create pressure or opportunity

#### 04-magic/local-limits-and-edges.md
- **Featured workings**: Specific Soulpulse applications in this novella
- **Cost tracking**: How costs accumulate for each character
- **Failure modes**: What happens when workings go wrong
- **Knowledge ceiling**: What characters know vs. don't know about the system
- **Sensory FX**: How workings look, sound, and feel in this era

#### 05-plot/act-beats.md
Three-act structure with:
- **Act I (Setup)**: Inciting incident, character introductions, world establishment
- **Act II (Escalation)**: Rising pressure, complications, midpoint reversal
- **Act III (Resolution)**: Climax, consequences, new equilibrium
- Each act should include emotional beats, not just plot events

#### 05-plot/chapter-beats.md
For each chapter (typically 12-15 chapters):
- **Chapter number and working title**
- **POV character** (if applicable)
- **Scene summary**: 2-4 sentences on what happens
- **Emotional beat**: What the character feels/learns
- **Cost/consequence**: Any magic costs or fallout
- **Hook**: How it propels to the next chapter

---

## Working Method

The AI Bible Engine follows this systematic process:

### Step 1: Restate the Brief
- Parse and internalize the novella brief
- Identify the core dramatic question
- Note all constraints and requirements
- Clarify any ambiguities (flag for human review if needed)

### Step 2: Align with Canon
- Cross-reference against master lexicon
- Check knowledge gates for era-appropriate information
- Verify character continuity if characters appear in multiple novellas
- Flag any conflicts between brief and canon
- Propose resolutions that preserve canon integrity

### Step 3: Design Arcs
- Develop concrete character arcs with clear beginning/end states
- Ensure arcs are **specific**, not vague (e.g., "learns to trust" → "trusts Jhace enough to reveal her Hollowing symptoms")
- Create pressure sources that force character growth
- Design cost escalation that mirrors emotional escalation
- Identify key decision points where characters reveal themselves

### Step 4: Generate All Files
- Produce complete content for each file in the output structure
- Use specific, concrete details (not placeholders or "TBD")
- Maintain consistent voice and terminology throughout
- Include cross-references between files where relevant
- Ensure chapter beats add up to the target word count

### Step 5: Self-Audit
Before finalizing, verify:

**Canon Consistency**
- [ ] All terminology matches master lexicon
- [ ] Knowledge gates respected for this era
- [ ] Character continuity maintained
- [ ] No anachronistic elements

**Cost Visibility**
- [ ] Every working has explicit cost
- [ ] Costs escalate appropriately
- [ ] Consequences are on-page, not implied
- [ ] Cost tracking is consistent across files

**Character Depth**
- [ ] Arcs are concrete and specific
- [ ] Characters make active choices
- [ ] Relationships have texture and conflict
- [ ] Voice distinctions are clear

**Structural Integrity**
- [ ] Three-act structure is balanced
- [ ] Chapter beats flow logically
- [ ] Pacing varies appropriately
- [ ] Climax delivers on setup

**Completeness**
- [ ] All required files generated
- [ ] No placeholder content
- [ ] Cross-references are accurate
- [ ] README provides clear overview

---

## Usage Notes

### For Human Operators

This document defines the **conceptual contract** for the AI Bible Engine. When generating a novella bible:

1. Prepare a novella brief using the template at `docs/05-ops/novella-brief.template.yaml`
2. Provide the brief to the AI along with this contract document
3. Review the generated output for canon compliance and quality
4. Iterate as needed, providing specific feedback
5. Once approved, commit the novella bible to `products/<novella-id>-story-bible/`

### For AI Agents

If you are an AI agent executing this contract:

- Treat this document as your primary instruction set
- Prioritize canon compliance over creative novelty
- Be specific and concrete in all outputs
- Self-audit before declaring completion
- Flag ambiguities or conflicts for human review rather than making assumptions

### Integration with Existing Workflow

The AI Bible Engine complements existing tools:

- **Linters** (`tools/lint/`) can validate generated content for lexicon compliance
- **Scene templates** (`docs/05-ops/scene-templates/`) can be used when drafting from chapter beats
- **Knowledge gates** documentation ensures era-appropriate content
- **Ops decks** (`docs/05-ops/ops-decks/`) provide additional per-novella operational guidance

---

## Maintenance

This document is **living documentation**. Update it when:

- Global canon rules change or expand
- New output file types are needed
- Working method improvements are discovered
- Integration with new tools is required

All changes should be committed with clear explanations and versioned appropriately.

---

**Version**: 1.0  
**Last Updated**: 2025-11-11  
**Maintained By**: Story Bible Operations Team
