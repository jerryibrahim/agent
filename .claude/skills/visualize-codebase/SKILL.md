---
name: visualize-codebase
description: >-
  Generate interactive visual documentation for any codebase — SVG infographics
  descending from 50,000 ft to ground level, plus GSAP-animated sequence diagrams.
  Use when the user says "visualize this codebase", "generate architecture diagrams",
  "create visual docs", "show me how this system works visually", or "map this codebase".
argument-hint: "[phase] — optional: all (default), static, interactive, deep-dive"
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Agent
---

# Codebase Visualization Skill

Generate a suite of visual artifacts that explain a codebase from 50,000 ft down to
ground level. Zero external Python dependencies — all SVGs are built with pure Python
string construction, and the interactive walkthrough uses GSAP from CDN.

**Input**: `$ARGUMENTS` — an optional phase selector:

- `all` (default) — run all phases
- `static` — only generate SVG infographics
- `interactive` — only generate the GSAP animated walkthrough
- `deep-dive` — only produce the deep-understanding analysis

If no arguments are provided, run all phases.

---

## Phase 0: Explore the Codebase

Before generating anything, build a complete mental model. Use subagents in parallel
to gather:

1. **Structure**: read README, CLAUDE.md, `docs/` directory, top-level config files
2. **Entry points**: find `main.go`, `cmd/`, `index.ts`, `main.py`, etc.
3. **Architecture layers**: map directories to roles (handlers, services, models, store, etc.)
4. **Domain model**: identify core types/structs/classes and their relationships
5. **API surface**: find all route registrations, endpoints, or CLI commands
6. **State machines**: find any status/state enums and their transitions
7. **Database schema**: find migrations or schema definitions
8. **Key flows**: trace the primary use case end-to-end

Capture findings as internal notes before proceeding to generation.

---

## Phase 1: Static SVG Infographics

Generate 10-12 SVG files using the **data-driven template** at
`templates/generate_visuals.py` (relative to this skill file). The template contains
all helper functions and rendering logic — you only need to fill in the `DATA` dict
with project-specific content from Phase 0 exploration.

### How to use the template

1. Copy `templates/generate_visuals.py` to the project's visualization directory
   (e.g., `visualizations/<project>/generate_visuals.py`).
2. Replace the `DATA` dict (everything below the `#### PROJECT DATA ####` marker)
   with project-specific data. Each key (1-11) maps to one slide's data dict.
3. Do **NOT** modify anything above the marker — helpers and renderers are shared.

The template has **zero pip dependencies** — only Python stdlib.

### DATA dict structure

Each slide number maps to a data dict consumed by its renderer. The key fields for
each slide type are documented in the template's placeholder DATA. Key patterns:

- **Slide 1 (ELI5)**: `analogy_lines`, `cards` (name, metaphor, desc, color, path_hint)
- **Slide 2 (System Context)**: `boxes` (id, label, sub, x, y, w, h, color), `connections` (from_xy, to_xy, color, label)
- **Slide 3 (Architecture Layers)**: `layers` (label, description, color)
- **Slide 4 (Domain Model)**: `entities` (name, fields, x, y, w, h, color), `relationships` (from_xy, to_xy, label, color)
- **Slide 5 (Request Lifecycle)**: `steps` (label, description, color)
- **Slide 6 (Routing)**: `routes` (name, triggers, color), `detail_panels` (title, lines)
- **Slide 7 (State Machines)**: `machines` (name, color, states, transitions, outcomes, details)
- **Slide 8 (Database Schema)**: `tables` (name, fields, color, x, y, w, h), `artifacts` (optional)
- **Slide 9 (API Routes)**: `groups` (name, color, routes), `extra_section` (optional)
- **Slide 10 (Code Structure)**: `tree` (name, desc, color, indent), `stats` (optional)
- **Slide 11 (Config)**: `panels` (title, color, x, y, w, h, items), `conventions` (optional)

### Slide sequence (altitude descent)

| Slide | Altitude  | Content |
|-------|-----------|---------|
| 01 | 50,000 ft | ELI5 — real-world analogy (restaurant, post office, factory, etc.) explaining what the system does and why it exists |
| 02 | 30,000 ft | System context — all actors (user, API, workers, DB, external systems) and the protocols/transports between them |
| 03 | 20,000 ft | Architecture layers — the request flow through each layer with one-line descriptions |
| 04 | 15,000 ft | Domain model — entity relationship diagram showing core types and connections |
| 05 | 10,000 ft | Request lifecycle — step-by-step sequence for the primary use case |
| 06 | 5,000 ft  | Routing/dispatch — how requests get matched to implementations |
| 07 | 3,000 ft  | State machines — lifecycle states and transitions of primary domain objects |
| 08 | 1,000 ft  | Database schema — tables with columns, types, and key indexes |
| 09 | 500 ft    | API route map — every endpoint grouped by concern |
| 10 | 100 ft    | Code structure — every package/module with file counts and descriptions |
| 11 | Ground    | Key config and environment — env vars, feature flags, operational knobs |

### SVG styling rules

- Dark background: `#0f172a`
- Primary text: `#e2e8f0`
- Muted text: `#94a3b8`
- Accent gradients per slide (blues, purples, greens, etc.)
- Fonts: `'JetBrains Mono', 'Fira Code', monospace` for code, `system-ui, sans-serif` for prose
- All text must be XML-escaped via `xml.sax.saxutils.escape()`
- Standard dimensions: 1200×900 for most slides, taller if content requires it

### After generating

Run the script:

```bash
python3 visualizations/generate_visuals.py
```

Validate all SVGs parse as valid XML:

```bash
for f in visualizations/slide_*.svg; do
  xmllint --noout "$f" 2>&1 && echo "OK: $(basename $f)" || echo "BROKEN: $(basename $f)"
done
```

Fix any broken SVGs (usually unescaped `&` characters) and re-run.

### Slideshow viewer

Write `visualizations/index.html` using the canonical template at `templates/index.html`
(relative to this skill file). Read the template, copy its full HTML/CSS/JS structure, then
only modify:

- Replace `{{PROJECT_NAME}}` with the actual project name.
- Replace the placeholder `SLIDES` array with the actual slides generated by the Python script.
- Add or remove slide entries to match the generated SVG files.

**Do not change** the CSS, class names, DOM structure, toolbar layout, or sidebar styling.
The template enforces these rules:

- Dark theme (`#0f172a` background)
- **Navigation controls in a top-left toolbar** (Prev/Next buttons + slide counter) — never at center, bottom, or top-right
- Thumbnail sidebar on the left for quick jumping
- SVGs embedded via `<img>` tags, scaled to fit viewport
- Keyboard shortcuts (arrow keys)

---

## Phase 2: Interactive Animated Walkthroughs

Write `visualizations/interactive.html` — a single HTML file with GSAP animations.
Only external dependency: GSAP from CDN.

### Canonical template

**You MUST use the template at `templates/interactive.html` (relative to this skill file)
as the exact starting point.** Read the template, copy its full HTML/CSS/JS structure, then
only modify the following:

- Replace `{{PROJECT_NAME}}` with the actual project name.
- Replace the placeholder `SCENARIOS` array with real scenarios derived from Phase 0 exploration.
- Adjust actor `x`/`y` positions to fit the specific project's architecture.

**Do not change** the CSS, class names, DOM structure, bottom bar layout, tab styling,
control placement, or any other structural element. The template is the single source of
truth for the interactive page layout.

### Template design rules (for reference)

These rules are already encoded in the template — listed here for clarity:

- **Top bar**: project title (left) + horizontally scrollable scenario tabs. Tabs are rounded-corner rectangles (`border-radius: 6px`) with a colored outline for the active tab and `var(--border)` for inactive tabs.
- **Center**: SVG canvas with actor boxes + right-side State Inspector panel (280px).
- **Bottom bar** (all controls aligned left):

  - **Row 1**: Narration box — step title (15px, bold) + detail (13px, muted).
  - **Row 2**: Play/Pause toggle, Prev, Next, progress text (`N / M`), progress dots.
  - **Row 3**: Speed buttons + keyboard shortcut hints.

- **Play/Pause is a single toggle button.** Play shows &#9654; icon, Pause shows &#9724; icon with `.active` class (blue background). Never show both simultaneously.
- **Speed toggle is always buttons** — a horizontal group (0.5x, 1x, 1.5x, 2x, 3x) with active state highlighted.
- **Progress dots** have `gap: 6px`, each dot `12px × 12px` (spacing ≈ dot size).

### Scenario data structure

Each scenario in the `SCENARIOS` array must follow this shape:

```javascript
{
  id: "scenario-id",
  label: "Human-readable label",
  color: "#3b82f6",
  actors: [
    { id: "actor-id", label: "Actor Name", sub: "subtitle", x: 100, y: 200, color: "#3b82f6" }
  ],
  steps: [
    {
      from: "actor-a",
      to: "actor-b",
      label: "POST /v1/resource",
      narration: "Short title for this step",
      detail: "Detailed explanation of what happens in this step...",
      state: { status: "running", step: "1/5", data: "..." }
    }
  ]
}
```

### Scenarios to include

Identify all major use cases from the codebase exploration:

- **Happy path**: the primary CRUD or workflow operation end-to-end
- **Error/recovery path**: what happens when something fails
- **Human-in-the-loop**: any approval, review, or manual intervention flows
- **Advanced routing**: if the system has dispatch, routing, or selection logic
- **Real-world domain scenarios**: derived from docs and domain-specific behavior

Each scenario should have 8-15 steps with realistic data in the `detail` and `state` fields.

---

## Phase 3: Deep-Dive Analysis (optional)

If the user requested `deep-dive` or `all`, produce both:

1. A markdown report at `visualizations/deep-dive.md`
2. A styled HTML version at `visualizations/deep-dive.html` using the canonical template at
   `templates/deep-dive.html` (relative to this skill file)

For the HTML version, read the template and copy its full HTML/CSS structure. Only modify:

- Replace `{{PROJECT_NAME}}` with the actual project name.
- Replace placeholder content with real analysis derived from Phase 0 exploration.
- Add or remove `<h3>` sections as needed to cover all findings.

**Do not change** the CSS, class names, top bar breadcrumb structure, or content container
styling. The template enforces the dark theme (`#0f172a` background, `#e2e8f0` text), sticky
top bar with navigation breadcrumbs, and consistent typography.

Both files should cover:

### Design Decisions

For each non-obvious pattern in the codebase, explain:
- What the pattern is and where it appears
- What problem it solves
- What would break if it were removed
- What alternatives exist and why they weren't chosen

### Invariants

List all system invariants (things that must always be true):
- State machine constraints
- Database constraints and indexes
- Concurrency guarantees
- Idempotency requirements
- Error handling contracts

### Failure Modes

For each critical flow, enumerate:
- What can fail at each step
- How the system currently handles it
- Whether the handling is correct
- What happens if the mitigation itself fails

---

## Phase 4: Validate and Deliver

1. Open the generated artifacts and verify they render:

   ```bash
   open visualizations/index.html
   open visualizations/interactive.html
   open visualizations/deep-dive.html
   ```

2. Run through the completeness checklist:
   - [ ] ELI5 covers the "what" and "why" without jargon
   - [ ] System context shows all external actors and protocols
   - [ ] Architecture layers match actual code structure
   - [ ] Domain model covers all core entities
   - [ ] Every primary use case has an animated walkthrough
   - [ ] State machines match actual code transitions
   - [ ] API routes match actual router registrations
   - [ ] Code structure slide accounts for all packages

3. Report to the user what was generated and where.

---

## Guardrails

- **No pip installs.** The Python SVG generator uses only stdlib. No `pillow`, no `google-genai`, no SVG libraries.
- **Single CDN dependency.** Only GSAP is loaded externally, for the interactive HTML.
- **Read before drawing.** Every diagram must be grounded in actual code you've read — never guess at architecture.
- **Escape all text.** Every string rendered in SVG must go through `xml.sax.saxutils.escape()`.
- **Validate XML.** Run `xmllint` on every generated SVG before declaring success.
- **Accurate over pretty.** If you can't determine something from the code, omit it rather than fabricate it.
