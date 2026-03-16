---
name: jit-learning
description: >
  Apply the JIT (Just-in-Time) Learning framework to rapidly grok any new technology,
  codebase, library, API, platform, or system. Use this skill whenever the user asks
  you to "learn", "research", "understand", "grok", "explore", or "figure out" a new
  technology — including GitHub repos, documentation sites, SDKs, frameworks, and
  platforms. Also trigger when the user says things like "help me understand X",
  "what is X and how does it work", "I need to learn X", "walk me through X", or
  "research X for me". This skill produces a structured five-page learning report
  grounded in Bloom's Taxonomy, progressing from a hard JIT boundary through a mental
  model analogy. Always use this skill instead of ad-hoc research when the deliverable
  is comprehensive understanding of an unfamiliar system.
---

# JIT Learning Framework

This skill applies the **Just-in-Time (JIT) Learning System** to any new technology.
It produces a structured, five-step learning report — one focused page per step —
grounded in Bloom's Taxonomy.

**Before proceeding, read the full framework:**
→ `references/jit-learning-system.md`

---

## When to Use This Skill

Trigger on any of these patterns:

- "Research X for me" / "learn X" / "grok X" / "help me understand X"
- A GitHub repo URL, docs site, or package name with an open-ended research request
- "Walk me through how X works"
- A technology is mentioned the user is clearly unfamiliar with and needs a primer on

---

## What to Research

Before writing anything, gather source material. For each target system, fetch:

1. **The homepage or README** — for the value proposition and pain points
2. **The architecture / how-it-works page** — for internal components
3. **The quickstart or getting-started guide** — for the happy path
4. **The concepts or reference page** — for decomposition vocabulary
5. **Any examples** — to ground the analogy in concrete behavior

Use `web_fetch` and `web_search` aggressively. Do not guess at architecture — verify it.

---

## Output Format

Produce **five distinct sections** in a single `.md` file.
Each section maps to exactly one step from the framework.

Read `references/jit-learning-system.md` for the exact definition of each step.
The five pages are:

### Page 1 — Step 1: The JIT Filter
- State the single learning goal (the "minimum I need today")
- List what is **in scope** (5–7 bullet points)
- List what is **explicitly deferred / out of scope** (5–7 bullet points)
- Include a side-by-side: "Without JIT" vs "With JIT" outcome

### Page 2 — Step 2: The Macro Scan
- Identify the pain points the system solves (split into layers if applicable)
- Deliver the **one-sentence summary** in a highlighted callout box
- Note the target audiences
- Include any edition/tier comparison if relevant

### Page 3 — Step 3: Trace the Happy Path
- Map the full developer lifecycle as a table: Phase | Action | Input | Output
- Identify the **universal input format** (the primitive that flows through the system)
- Describe the end-to-end request/response lifecycle in prose

### Page 4 — Step 4: Functional Decomposition
- Identify **3–5 core components** in a table: Component | Role | Key Details
- Produce an **internal pipeline diagram** (ASCII art in a callout box)
- Call out 3–4 critical design decisions and why they matter

### Page 5 — Step 5: The ELI5 Translation
- Choose a vivid non-technical analogy (e.g., a hospital, a city, a restaurant kitchen)
- Map every core concept to the analogy in a table: Concept | Analogy | Why It Maps
- Write the **one-paragraph mental model** in a highlighted callout box
- End with 4–5 "Proof of Grokking" questions the reader can now answer

---

## Document Design

- Use a distinct accent color per page header (vary: navy, blue, teal, purple, green, orange)
- Each page starts with a large step label, title, and subtitle
- Use callout boxes (shaded tables) for key outputs: one-sentence summary, pipeline diagram, mental model
- Use comparison tables wherever two options, phases, or tiers exist
- End each page with a horizontal rule and a bold one-sentence **Output** summary

---

## Quality Bar

A successful output means:

- A reader with zero prior knowledge of the system can explain it to a colleague after reading
- The JIT boundary is explicit — someone could verify what was and wasn't researched
- The Happy Path lifecycle could be implemented from Page 3 alone
- The ELI5 analogy maps cleanly with no broken metaphors
- The pipeline diagram on Page 4 matches the actual architecture (not inferred)
