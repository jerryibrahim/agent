---
name: visualize-index
description: >-
  Build or rebuild a root-level index.html that stitches together all visualization
  folders into a dark-themed gallery with 3-column grid, aligned rows, and 3 links
  per card (Overview, Interactive, Deep Dive). Sorts projects alphabetically.
  Use when the user says "build the index", "rebuild the index", "update the
  visualization index", or "visualize-index".
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Agent
---

# Visualize Index Skill

Generate (or regenerate) a root-level `index.html` that serves as a gallery landing
page for all codebase visualization folders in the current directory. This skill is
idempotent — running it again after adding new folders simply replaces `index.html`
with an updated version.

## Templates

This skill uses reference templates in `templates/` relative to this SKILL.md file:

- **`templates/index.html`** — Full page skeleton with CSS. Placeholders:
  `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{CARDS}}`
- **`templates/card.html`** — Single card snippet. Placeholders:
  `{{FOLDER}}`, `{{DISPLAY_NAME}}`, `{{DESCRIPTION}}`, `{{TAGS}}`, `{{LINKS}}`
- **`templates/README.md`** — Markdown gallery page. Placeholders:
  `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{TABLE_ROWS}}`
- **`templates/readme-row.md`** — Single table row snippet. Placeholders:
  `{{DISPLAY_NAME}}`, `{{DESCRIPTION}}`, `{{TAGS}}`, `{{SLIDE_COUNT}}`, `{{LINKS}}`

Read all templates before generating output. Replace placeholders with extracted
metadata — do not modify the CSS or HTML structure in HTML templates, and do not
alter the table format in README templates.

---

## Step 1: Discover Visualization Folders

Scan the current working directory for subdirectories that contain visualization
output. A valid visualization folder must contain **at least** `slide_01_eli5.svg`
and `index.html`.

```bash
# Find all visualization folders
for d in */; do
  [ -f "$d/slide_01_eli5.svg" ] && [ -f "$d/index.html" ] && echo "$d"
done
```

Sort the discovered folders **alphabetically** (case-insensitive).

---

## Step 2: Extract Metadata from Each Folder

For each discovered folder, gather:

### Display Name

Read the `<title>` tag from the folder's `index.html`. Strip the suffix
" Codebase Visualization" if present. Fall back to the folder name with first
letter capitalized.

### Description

Read `deep-dive.md` (if it exists). Extract a concise 1-2 sentence summary by:

1. Reading the first `## Design Decisions` section
2. Reading the first `### 1.` subsection's **"Problem it solves"** line
3. Synthesizing a brief description that captures the project's purpose and key
   architectural patterns

If `deep-dive.md` doesn't exist, read the title slide SVG (`slide_01_eli5.svg`)
for context and write a short description.

Keep descriptions under 180 characters. They should answer: "What does this
component do and what makes its architecture interesting?"

### Language Tags

Detect primary languages by checking:

- `*.go` references in deep-dive.md or generate_visuals.py → tag: `Go`
- `*.ts` / `*.tsx` / TypeScript references → tag: `TypeScript`
- `*.py` / Python references (as primary language, not the generator script) → tag: `Python`
- `*.rs` / Rust references → tag: `Rust`

Use the corresponding CSS class from the template: `lang-go`, `lang-ts`, `lang-py`,
`lang-rs`.

### Category Tags

Extract 1-2 category keywords from the deep-dive content. Examples:
`Controllers`, `CRDs`, `Observability`, `PostgreSQL`, `Workflows`, `AI`,
`Next.js`, `React`, `Ironic`, `Hardware`.

### Slide Count

Count `slide_*.svg` files in the folder.

### Link Availability

Check which files exist:

- `index.html` → Overview link (always present)
- `interactive.html` → Interactive link
- `deep-dive.html` → Deep Dive link

If `deep-dive.md` exists but `deep-dive.html` does not, generate the HTML version
(see Step 3).

---

## Step 3: Generate Missing deep-dive.html Files

For any folder that has `deep-dive.md` but no `deep-dive.html`, convert the
markdown to a styled HTML page. Use this approach:

- Dark theme matching the rest of the site (`#0f172a` background)
- Sticky breadcrumb nav: All Projects / {Component} / Deep Dive
- Proper rendering of headings, paragraphs, bold, code, lists, tables
- Same CSS variables and fonts as the main index

Write a Python conversion script if more than one file needs converting, or
write the HTML directly for a single file.

---

## Step 4: Generate index.html

1. Read `templates/index.html` and `templates/card.html` from this skill's directory.
2. For each discovered folder (sorted alphabetically by display name), populate a
   copy of the card template:
   - `{{FOLDER}}` — folder name (no trailing slash)
   - `{{DISPLAY_NAME}}` — extracted display name
   - `{{DESCRIPTION}}` — extracted description
   - `{{TAGS}}` — one `<span class="tag ...">` per language/category/slide-count tag,
     each indented 8 spaces
   - `{{LINKS}}` — one `<a href="...">` per available link (Overview, Interactive,
     Deep Dive), each indented 6 spaces
3. Join all populated cards and substitute into the index template:
   - `{{PROJECT_NAME}}` — detected project name (see Header rules below)
   - `{{PROJECT_DESCRIPTION}}` — detected project description
   - `{{CARDS}}` — concatenated card HTML

### Header — Project Name

Detect the project name from the common prefix of folder names, or from the
repository name, or from context the user provides.

- If a name is found, set `{{PROJECT_NAME}}` to
  `<span>{name}</span> Codebase Visualizations`
- If no name can be inferred, use `Codebase <span>Visualizations</span>`

Set `{{PROJECT_DESCRIPTION}}` to a sentence describing the gallery, e.g.:
"Interactive architecture diagrams and deep-dive documentation for every
component in the {name} platform."

If no name, use: "Interactive architecture diagrams and deep-dive documentation."

---

## Step 4b: Generate README.md

Using the **same metadata** extracted in Steps 1-2 (and the same project name /
description from Step 4):

1. Read `templates/README.md` and `templates/readme-row.md` from this skill's
   directory.
2. For each discovered folder (same alphabetical order as Step 4), populate a copy
   of the row template:
   - `{{DISPLAY_NAME}}` — extracted display name
   - `{{DESCRIPTION}}` — extracted description
   - `{{TAGS}}` — comma-separated list of language and category tags (e.g.
     `Go, Controllers, CRDs`)
   - `{{LINKS}}` — markdown links to available files, separated by ` · ` (e.g.
     `[Overview](folder/index.html) · [Interactive](folder/interactive.html) · [Deep Dive](folder/deep-dive.html)`)
3. Join all populated rows and substitute into the README template:
   - `{{PROJECT_NAME}}` — plain text project name (no HTML `<span>` tags)
   - `{{PROJECT_DESCRIPTION}}` — same description, plain text
   - `{{TABLE_ROWS}}` — concatenated row lines

---

## Step 5: Validate

1. Verify the generated `index.html` is well-formed HTML
2. Verify the generated `README.md` has a valid markdown table (header + separator
   + one row per project)
3. Verify all linked files exist (`index.html`, `interactive.html`, `deep-dive.html`
   in each folder)
4. Report a summary: how many projects were indexed, any missing files

---

## Guardrails

- **Use the templates verbatim** — read all templates (`index.html`, `card.html`,
  `README.md`, `readme-row.md`), replace only the `{{PLACEHOLDER}}` tokens; never
  alter the CSS, HTML structure, or table format
- **Card preview + body are wrapped in an `<a class="card-link">` linking to the
  Overview page** — the card-links row stays outside the wrapper so individual
  links remain independently clickable
- **Grid uses `repeat(3, 1fr)`** — enforced by the index template; never change
  to `auto-fill` or `auto-fit`
- **Sort alphabetically** — always, no exceptions
- **Idempotent** — running this skill twice produces the same output (assuming
  no new folders were added)
- **No external dependencies** — the index.html is a single self-contained file
  with inline CSS only
- **Read before writing** — always read existing files to extract metadata; never
  guess at descriptions or tags
