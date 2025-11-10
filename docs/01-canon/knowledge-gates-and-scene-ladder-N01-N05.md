# N01–N05 Knowledge Gates & Scene Ladder — v1.0

**Purpose:** Hard-stop canon for what characters/world know at each novella (N01–N05), plus drop-in scene templates and lint filters. This prevents anachronistic knowledge, keeps costs visible, and standardizes sensory FX.

## 1) Knowledge Boundary Matrix (Writer-Facing)

| Novella | What Characters Know (Ceiling) | What Characters Do **Not** Know (Redline) |
|---|---|---|
| **N01 — “Grip That Holds”** | Magic is real post-Piercing; instinctive, miraculous, unpredictable. Distinct abilities observed (healing, shaping). Costs exist (pain, exhaustion, burns/tremor). No system. | Any formal terms: **Resonance, Principles, Veins, Hollowing, Confluence, Echo Stacking, Suppression, Factions-by-principle, God-vessels**. |
| **N02 — “Light Cracks Through”** | Three **affinities** emerging (Structural, Continuity, Purity). Frequency matching concept. Failure modes named: **vein-snap, cascade, sympathetic overload**. Costs tracked (vein-burn, calcification, isolation). Faction fracture begins. | No **fourth principle** formalization. No named **Hollowing** (use “burnout/overload”). No dual-principle reveal. No **Confluence**, no suppression tech, no god-vessel concept, no full vein-theory. |
| **N03 — “Alloy Folded Wrong”** | Three factions fully formed; Releasers distinct (fourth **group** emerging). Weaponization of abilities. Lattice dust hazard. Shadow grid networks. Political crisis. | No formal **Four Principles** framework. No named **Hollowing**. No dual-principle. No **Confluence**, suppression tech, god-vessels, or systematic vein theory. |
| **N04 — “Shatter From Heat”** | **Hollowing** identified as **terminal**. **Dual-principle** possible (Tiffani: Form+Wholeness). Four principles **theorized** (not fully formalized). Strict safe-use limits codified. ~90% heat-grid restored. God-vessels **approaching** (unrecognized). | No formal “Four Principles” doctrine. No **Confluence**. No suppression devices. No knowledge of imminent transformations. No complete vein-network theory. |
| **N05 — “Steal Breaks Open”** | **Four Principles formalized. Confluence exists (Jhace only).** Suppression tech exists and fails catastrophically. **Four god-vessel transformations complete** (Xilcore, Leesa, Blemo, Seeri). Vein network understood post-catastrophe. World remade, Era shift. | None of the above should be withheld; this is the **culmination** of discovery for Books 1–5. |

> **Room Rule:** If a draft line violates the Redline column for its novella, flag it `// KNOWLEDGE REDLINE: N0X` during review.

## 2) Health & Cost Clocks (Anchor Values)

**Jhace — Vein-burn (cm, forearm disc):**
- **N01:** present (scaffold incident); unmeasured baseline.
- **N02:** ~2.5 cm; tremor established.
- **N03:** ~3.0 cm; steady spread.
- **N04:** ~3.5 cm; near-Hollowing recovery; partial self-heal learned.
- **N05:** ~4.0 cm; multi-cost stacking begins post-Confluence.

**Tiffani — Calcification (hands):**
- **N01:** stiffness seeds.
- **N02:** noticeable stiffness; pain on fine work.
- **N03:** stiffness + pain sustained; range reduced.
- **N04:** **range notably reduced**; dual-principle worsens; blue-silver discoloration.
- **N05:** **severe** by death; barrier feat pre-Confluence.

**Mobel — Purity Isolation:**
- **N01:** early numbness trend.
- **N02:** isolation + swelling.
- **N03:** severe isolation; sensitivity extreme.
- **N04:** near-transformation affect; body failing.
- **N05:** transforms → **Blemo**.

**Venn/Eries — Entropy Vitality Drain:**
- **N01–N02:** early fatigue.
- **N03:** visibly older; constant fatigue.
- **N04:** weakness + philosophy peak (near-transformation).
- **N05:** transforms → **Seeri**.

> Use these as continuity anchors in beat sheets; deviations require an on-page explanation.

## 3) Sensory FX Ladder (Per Novella)

**Colors, sounds, and tactile cues are permitted only as discovered in-era.**

- **N01:**
  - *Warmth-type (Jhace):* soft golden warmth; gentle hum; connection pull.
  - *Precision-type (Tiffani):* cool crystalline clarity; high chime; sharpened edges.
  - Avoid faction labels; avoid “resonance,” “frequency,” or principle names.

- **N02:**
  - Introduce **frequency matching** language and the three affinity identities.
  - Allow failure-mode terms (**vein-snap, cascade, sympathetic overload**).

- **N03:**
  - Weaponization FX allowed (barriers, prisons, decay auras) with **cost beats**.
  - Lattice dust: glows on use; corrosive residue.

- **N04:**
  - Add **Hollowing** nomenclature and caution rituals; dual-principle visuals (blue-silver + copper-gold overlay).

- **N05:**
  - Full palette active: four glows concurrently during **Confluence**, world-scale PF ripples, suppression-field failure visuals, god-vessel ascensions.

## 4) Scene Header & Ladder Template (Drop-In)

**Header (Te’Oga standard):**
`Striketide • Ember Anneal • Final Temper • Casting 431 — Coreven—Underface`
`4/5/7/431 — Coreven—Underface`

**Scene Ladder Fields (fill per scene):**
- **Era Gate:** N01 / N02 / N03 / N04 / N05
- **Knowledge Ceiling:** (auto-filled from §1)
- **Principle Usage:** None / Form / Wholeness / Purity / Entropy / Dual / Confluence
- **Breath Budget:** Micro (2–3) / Standard (4–8) / Grand (9–12+)
- **Cost Beats:** Physio / Psycho / Systemic (Vein-burn stage: __ )
- **Failure Safeguards:** Breaker? Choir? Damp window?
- **Forbidden Flags:** (terms/tech restricted by era)
- **Continuity Pins:** Jhace burn size; Tiffani mobility; Mobel isolation; Venn vitality.
- **Aftermath FX:** echo, dust glow, environmental ringdown.

> Paste this block atop every new scene card; the knowledge gate becomes muscle memory.

## 5) Era Lint Pack (Regex & Review Notes)

**N01:**
- Ban: `resonance|principle|veins?|Hollowing|Confluence|suppression|faction(s)?|god-?vessel(s)?`
- Replace **“magic/miracle/gift”** for system terms.

**N02:**
- Allow: `resonance`, `frequency matching`, and failure-mode terms.
- Ban: `four principles|Hollowing|dual-?principle|Confluence|suppression|god-?vessel(s)?`

**N03:**
- Allow faction names; allow weaponization terms.
- Ban: `four principles` (as a formal doctrine), `Hollowing` (as a named medical), `dual-?principle`, `Confluence`, `suppression`, `god-?vessel(s)?`.

**N04:**
- Allow: `Hollowing`, dual-principle visuals.
- Ban: explicit **Confluence**, `suppression`, foreknowledge of god-transformation, complete vein-network theory.

**N05:**
- All terms unlocked; ensure **order-of-revelation** is dramatized on page.

> Use editor search with case-insensitive regex during copyedits.

## 6) Ops Cards (One-Pagers per Novella)

**N01 Ops Card**
- **Allowed FX:** instinctive healing/shaping; small-scale feats; costs.
- **No-Go:** systemic language, predictions, world-theory.
- **Key Beats:** Bram’s death; burn scar; tremor.

**N02 Ops Card**
- **Allowed FX:** three-affinity talk; failure-mode naming; faction fracture.
- **No-Go:** fourth principle formalization, named Hollowing, dual-principle.

**N03 Ops Card**
- **Allowed FX:** faction warfare; Releasers as distinct; dust-as-weapon.
- **No-Go:** system formalism; dual-principle; Confluence.

**N04 Ops Card**
- **Allowed FX:** Hollowing; dual-principle; safety rules; 90% grid.
- **No-Go:** suppression tech; god-transformation foreknowledge; full vein theory.

**N05 Ops Card**
- **Allowed FX:** everything: Four Principles formalized; Confluence (Jhace); suppression catastrophe; four ascensions; world reset.

## 7) QA Checklist (Per Chapter)
- Does any line leak knowledge from a later novella? Strike or mask.
- Are **costs** visible for every use? Physio/Psycho/Systemic logged.
- Are sensory cues era-appropriate?
- Do health clocks increment correctly?
- Are faction labels used only after their first on-page availability?
- Are suppression/god terms introduced only in N05?

### Change Log
- v1.0 — Initial gates, clocks, templates, and lint pack consolidated for the room.
