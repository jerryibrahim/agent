# JIT Learning Framework

Apply the **Just-in-Time (JIT) Learning System** to any new technology.
Produce a structured, five-step learning report — one focused page per step —
grounded in Bloom's Taxonomy.

---

## Theoretical Foundation

### Just-in-Time (JIT) Learning

> When engineers fail to learn a new system, it is usually because they overwhelm
> their working memory by trying to memorize syntax rather than understanding the
> architecture.

Developers naturally default to **"Just-in-Case" learning** — reading the entire
documentation top-to-bottom just in case they need a detail later. This is highly
inefficient.

**JIT learning** dictates that you only hunt for the specific information required
to overcome your immediate roadblock.

### Bloom's Taxonomy

This educational framework proves you cannot analyze a system until you first
remember and understand it. You must move sequentially from lower-order thinking
(running the code) to higher-order thinking (evaluating the architecture).

### The Five-Step Grokking Script

| Step | Name                     | Bloom's Level | Key Question                           | Output                   |
| ---- | ------------------------ | ------------- | -------------------------------------- | ------------------------ |
| 1    | The JIT Filter           | Remember      | What's my minimum goal today?          | A hard learning boundary |
| 2    | The Macro Scan           | Understand    | What pain does this solve?             | One-sentence summary     |
| 3    | Trace the Happy Path     | Apply         | What goes in, what comes out?          | Lifecycle map            |
| 4    | Functional Decomposition | Analyze       | How does it work under the hood?       | Internal dependency map  |
| 5    | The ELI5 Translation     | Evaluate      | How do I explain this to a 5-year-old? | Solidified mental model  |

**Step 1 — The JIT Filter** (Remember): Before opening a single file, define your
exact goal. Ask: "What is the absolute minimum I need to learn today to get this
working?" Output: A hard boundary that stops you from falling into rabbit holes.

**Step 2 — The Macro Scan** (Understand): Read the README and ignore the code.
Identify the core value proposition. Ask: "What specific pain point is this
solving?" Output: The one-sentence summary of the technology's purpose.

**Step 3 — Trace the Happy Path** (Apply): Execute the quickstart guide to get a
successful output. Don't worry about how it works yet. Ask: "What are the minimum
inputs required, and what is the exact output?" Output: A mapped lifecycle of the
user experience.

**Step 4 — Functional Decomposition** (Analyze): Open the source code. Break the
system down into its 3–5 core components (e.g., routing, auth, state management).
Ask: "How is the Happy Path actually implemented under the hood?" Output: A
granular map of the internal dependencies.

**Step 5 — The ELI5 Translation** (Evaluate): Force yourself to explain the entire
system using a non-technical analogy. Ask: "How would I explain this to a
5-year-old?" Output: A solidified mental model that proves you truly grok the
concept.

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

Search the web aggressively. Do not guess at architecture — verify it.

---

## Output Format

Produce **five distinct pages** in a single `.docx` file. Each page maps to exactly
one step from the framework above.

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
