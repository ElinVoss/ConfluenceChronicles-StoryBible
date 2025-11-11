# N01 Story Bible: "The Grip That Holds"

## Overview

This is the novella-specific story bible for **N01: "The Grip That Holds"**, the opening novella of the Confluence Chronicles saga. This bible translates global canon into N01-specific applications and provides a complete roadmap for drafting.

---

## Quick Reference

**Novella ID:** N01
**Working Title:** "The Grip That Holds"
**Era:** Turning 1 (Post-Piercing, pre-factional, pre-systematic magic understanding)
**Target Length:** 45,000 words (15 chapters × ~3,000 words)
**POV Structure:** Dual POV alternating (Jhace Torrins and Tiffani Merrow)

**Primary Theme:** The cost of holding what should be let go
**Secondary Themes:**
- Flawed perfection as a trap
- Confluence as terminal, not a toy (foreshadowed)
- The violence of transformation

---

## What's Inside

### 00-brief/
- **novella-brief.yaml**: The input brief defining scope, themes, constraints, and must-hit beats

### 01-canon-overrides/
- **canon-deltas.md**: N01-specific canon clarifications; knowledge gates; forbidden terminology; how to handle foreshadowing vs. anachronism

### 02-characters/
- **core-cast.md**: Deep dives on POV and major characters (Jhace, Tiffani, Mobel, Venn, Chloen) with concrete arcs, costs, voice notes
- **supporting-cast.md**: Secondary characters with functions and memorable traits

### 03-world/
- **key-locations.md**: Sensory profiles and dramatic potential for featured locations (Underface, Glassworks, Lattice Yards, Council District)
- **factions.md**: Pre-factional era dynamics; informal clusters; philosophical positions; proto-factions emerging

### 04-magic/
- **local-limits-and-edges.md**: N01 magic scope (instinctive, unpredictable); costs and tracking; failure modes; sensory FX; knowledge ceiling; writer guidelines

### 05-plot/
- **act-beats.md**: Three-act structure with thematic focus, story functions, emotional arcs
- **chapter-beats.md**: Chapter-by-chapter roadmap with POV, scene summaries, emotional beats, costs, hooks

---

## How to Use This Bible

### For Drafting

1. **Start with chapter-beats.md**: Use as your primary roadmap; each chapter has scene summary, emotional beat, cost tracking, and hook
2. **Reference core-cast.md**: Ensure character voices and arcs stay consistent
3. **Check local-limits-and-edges.md**: Every magic use must show cost; use cost tracking table
4. **Use key-locations.md**: Pull sensory details for each scene location
5. **Verify canon-deltas.md**: Stay within N01 knowledge gates; avoid forbidden terminology

### For Revision

1. **Run linters**: `python tools/lint/lexicon_lint.py products/N01-story-bible/`
2. **Check knowledge gates**: `python tools/lint/knowledge_gate_lint.py --era N01 products/N01-story-bible/`
3. **Audit cost progression**: Use cost tracking table in local-limits-and-edges.md
4. **Verify character arcs**: Do Jhace and Tiffani reach specified end states?
5. **Check word count**: Target 45,000 words total; 3,000 per chapter

### For Continuity

**Cost Anchors (by end of N01):**
- Jhace: Vein-burn ~2.5 cm (left forearm); left hand tremor (permanent)
- Tiffani: Significant joint stiffness (hands); pain constant but managed
- Mobel: Extreme isolation; sensory sensitivity (foreshadows N05)
- Venn: Visibly aged; vitality drain (foreshadows N05)

**Relationship States:**
- Jhace and Tiffani: Together; relationship solidified through shared vulnerability
- Mobel: Isolated; barely reachable
- Chloen: Versatile; questions unanswered (foreshadows N04 dual-principle)

---

## Key Canon Constraints

### Forbidden Terminology (N01 Redline)

DO NOT USE in N01:
- Resonance (technical term)
- Four Principles or named principles (Form, Wholeness, Purity, Entropy)
- Veins or vein network (anatomical)
- Hollowing (medical diagnosis)
- Confluence (multi-principle ability)
- Echo stacking
- Suppression devices
- Faction names (capitalized, formal)
- God-vessel transformations

### Safe Language

USE INSTEAD:
- Magic, gift, ability, power
- Warmth/coolness, tingling, pulling (sensory)
- Instinctive, miraculous, unpredictable
- Exhaustion, pain, burns, tremors, stiffness
- "Healers" and "builders" (informal, lowercase descriptive)

---

## Tone Pillars

1. **Forge-punk grit**: Industrial, physical, metal-on-stone percussion; heat-grid hum; scaffold networks
2. **Glass-punk fragility**: Precision, crystalline beauty; geometric patterns; brittleness beneath perfection
3. **Intimate scale with cosmic stakes**: Personal stories with world-changing implications; focus on individuals, not armies

---

## Character Voice Cheat Sheet

**Jhace (POV):**
- Blunt, physical, action-oriented
- Short sentences during stress; longer reflections in quiet
- Craft metaphors (forge, scaffold, marry-point)
- Emotional undercurrent beneath practical surface

**Tiffani (POV):**
- Elegant prose with punched profanity
- Controlled until breaking point
- Geometric and architectural metaphors
- Sharp, analytical, self-critical internal monologue

**Mobel:**
- Sparse, halting; struggles to articulate
- Preservation metaphors ("keeping intact," "preventing decay")

**Venn:**
- Measured, thoughtful; rhetorical questions
- Patient and kind; philosophical metaphors

**Chloen:**
- Enthusiastic, questioning; speaks quickly
- Sensory language; optimism tempered by experience

---

## Cost Tracking Table

| Character | Cost Type | Ch 1-3 | Ch 4-6 | Ch 7-9 | Ch 10-12 | Ch 13-15 |
|-----------|-----------|--------|--------|--------|----------|----------|
| **Jhace** | Vein-burn | Baseline | 1.5cm appears | 2.0cm | 2.5cm | 2.5cm (stable) |
| **Jhace** | Tremor | None | None | Begins | Worsens | Permanent |
| **Tiffani** | Stiffness | None | Begins | Noticeable | Significant | Severe |
| **Tiffani** | Pain | None | Occasional | During work | Constant | Constant |
| **Mobel** | Isolation | Subtle | Avoids crowds | Rarely socializes | Hermit-like | Barely present |
| **Venn** | Vitality | Subtle fatigue | Looking older | Visibly aged | Exhausted | Exhausted but present |

---

## Must-Hit Beats Checklist

✓ **Inciting:** Jhace loses something he cannot brute-force reclaim (scaffold incident, vein-burn begins) — Ch 3
✓ **Early:** Tiffani's precision work shows first signs of calcification cost — Ch 4
✓ **Midpoint:** First glimpse of Confluence's true cost through a failed working — Ch 6-7 (Soress's cascade)
✓ **Act II:** Mobel's isolation symptoms become undeniable — Ch 8-11
✓ **Climax:** A choice where survival costs more than surrender — Ch 12-13
✓ **Resolution:** New equilibrium established, but costs are permanent and visible — Ch 14-15

---

## Continuity Hooks to N02

By end of N01, seeds are planted for N02 developments:

- **Three affinities emerging**: Healers (warmth-type), builders (precision-type), preservers (isolation-type) observed but not formalized
- **Cost patterns established**: Vein-burn (Jhace), calcification (Tiffani), isolation (Mobel), vitality drain (Venn)
- **Chloen's versatility**: Questions about dual-ability users remain unanswered (foreshadows N04 dual-principle)
- **Community fracture**: Philosophical divisions will formalize into factions in N02
- **Soress's cautionary example**: Demonstrates need for safe-use guidelines (N02 develops these)

---

## Production Status

**Status:** Generated 2025-11-11
**Ready for Drafting:** Yes
**Linting:** Pending (run after draft)
**Canon Compliance:** Verified against Master Lexicon, Knowledge Gates v1.0, N01 Soulpulse Scope

---

## Change Log

**v1.0 (2025-11-11):** Initial generation from N01 brief; all files complete; ready for drafting

---

## Questions or Issues?

If you encounter conflicts, ambiguities, or questions while drafting:

1. Check global canon first (docs/01-canon/)
2. Consult canon-deltas.md for N01-specific clarifications
3. Reference knowledge gates to verify era-appropriate content
4. If still unclear, document question and flag for ops review

**Global canon always overrides novella-specific content.**

---

**Maintained by:** Story Bible Operations Team
**Contact:** See main repository README for contributor info
