# Agent Deep-Dive Analysis

## Design Decisions

### 1. Skill-Per-Directory Architecture

**What it is**: Each skill is a self-contained directory with a `SKILL.md` frontmatter file, optional `references/` subdirectory for methodology docs, and optional `templates/` for output generation.

**Where it appears**: `.claude/skills/debate/`, `.claude/skills/jit-learning/`, `.claude/skills/visualize-codebase/`, etc.

**What problem it solves**: Skills can be installed, updated, or removed independently. A user can copy just `debate/` without pulling in visualization templates. Claude Code auto-discovers skills from the directory structure.

**What would break without it**: All skill logic would live in a single monolithic instruction file. Updates to one skill would risk regressions in others. Users couldn't selectively install skills.

**Alternatives**: A single `SKILLS.md` file with all skills concatenated was the original approach. It was abandoned because (a) context window bloat on every invocation and (b) no way to selectively distribute individual skills via `make copy-claude-skill SKILL=X`.

### 2. Template-Driven Generation with Structural Fidelity

**What it is**: All generated HTML files must match a canonical template skeleton exactly. Only project-specific content (data arrays, text) may differ. CSS, DOM structure, class names, and navigation placeholders must be verbatim copies.

**Where it appears**: `visualize-codebase/templates/index.html`, `interactive.html`, `deep-dive.html`. Phase 4 validation explicitly diffs structural skeletons.

**What problem it solves**: Prevents CSS/DOM drift across regenerations. When the `visualize-index` skill injects shared navigation via `<!-- nav:inject -->`, it can rely on the placeholder being in the exact right position. Ensures visual consistency across all projects in a gallery.

**What would break without it**: Each regeneration could introduce subtle layout differences. The gallery navigation injection would fail if the comment placeholder was missing or moved. Cross-project styling would diverge.

**Alternatives**: Using a templating engine (Jinja2, Handlebars) was considered but rejected because it would add a dependency. The current approach keeps templates as plain HTML files that Claude copies and fills in.

### 3. Data-Driven Python SVG Generator

**What it is**: A single Python script (`generate_visuals.py`, ~800 lines) with two sections: (1) shared helper functions and renderers that never change, and (2) a `DATA` dict that gets replaced with project-specific content.

**Where it appears**: `visualize-codebase/templates/generate_visuals.py`

**What problem it solves**: Zero pip dependencies. Deterministic SVG output. The LLM only needs to fill in a data structure, not write rendering code. All XML escaping is handled by the shared helpers.

**What would break without it**: Each visualization would require hand-crafted SVG strings with ad-hoc escaping, leading to XML parsing failures from unescaped `&` characters. Output would be inconsistent across projects.

**Alternatives**: SVG libraries (svgwrite, drawSvg) add pip dependencies. D3.js-based generation requires Node.js. Browser-rendered SVG (via headless Chrome) adds infrastructure complexity. The stdlib-only approach is the simplest that works.

### 4. Three-Pass Adversarial Review (Advocate/Critic/Judge)

**What it is**: The debate review skill enforces three distinct analytical passes with different objectives. The Advocate steelmans first (Rapoport Rules), the Critic challenges assumptions (ACH methodology), and the Judge synthesizes a verdict.

**Where it appears**: `.claude/skills/debate/SKILL.md` and `references/review.md`

**What problem it solves**: Prevents the common failure mode of jumping straight to criticism without understanding. Forces the reviewer to demonstrate comprehension before challenging. The Judge pass prevents both false positives (Critic overreach) and false negatives (Advocate bias).

**What would break without it**: Single-pass reviews tend to be either too generous (missing real issues) or too harsh (nitpicking without context). The three-pass structure produces balanced, actionable findings.

**Alternatives**: Single-pass review (standard code review), two-pass (pro/con only), or unstructured adversarial analysis. The three-pass approach was chosen because it maps to established intelligence analysis tradecraft (ACH) and philosophical methodology (Hegelian dialectic).

### 5. Permission Model: Deny-by-Default with Explicit Allow List

**What it is**: `settings.json` explicitly lists every Bash command pattern that Claude is allowed to run, plus a deny list for destructive operations.

**Where it appears**: `.claude/settings.json`

**What problem it solves**: Prevents accidental destructive operations like `rm -rf`, `git push`, or `helm install`. The allow list ensures only read-only and generation commands run without user confirmation.

**What would break without it**: Claude could accidentally push code, delete files, or modify cluster state. The deny list for `git push` is especially important because skills like `/commit` stage and commit but should never push without explicit user approval.

**Alternatives**: Relying on Claude's built-in safety checks alone, or using a broader allow list. The explicit approach was chosen because the cost of a false positive (blocking a safe command) is low, while the cost of a false negative (running a destructive command) is high.

---

## Invariants

### Skill Structure Constraints

- **Every skill must have a SKILL.md**: Claude Code discovers skills by the presence of this file. Without it, the skill directory is invisible.
- **SKILL.md frontmatter must include `name` and `description`**: The description field contains trigger patterns that Claude Code uses for intent matching.
- **Allowed tools must be explicitly listed**: If a skill needs Bash access, the SKILL.md must declare it. This prevents skills from silently escalating their tool usage.

### Template Fidelity Constraints

- **`<!-- nav:inject -->` must appear immediately after `<body>`**: The `visualize-index` skill replaces this comment with a `<script>` tag. If it's missing or moved, navigation injection fails silently.
- **CSS must be single-line compact format**: The template validation in Phase 4 compares CSS blocks. Multi-line or reformatted CSS would fail structural conformance checks.
- **Generated HTML must be standalone**: No build step, no npm install, no server. Open the file in a browser and it works.

### SVG Generation Constraints

- **All text must be XML-escaped**: Every string passed to SVG renderers goes through `xml.sax.saxutils.escape()`. Unescaped `&`, `<`, or `>` characters produce invalid XML that xmllint rejects.
- **Output files must validate with xmllint**: Phase 4 runs `xmllint --noout` on every generated SVG. A broken SVG is a bug, not a warning.
- **Dark theme colors are fixed**: Background `#0f172a`, primary text `#e2e8f0`, muted text `#94a3b8`. Changing these would break visual consistency across the gallery.

### Methodology Constraints

- **Debate review must complete all three passes**: Skipping the Advocate pass means the Critic lacks context. Skipping the Judge pass means no verdict synthesis.
- **Red team must apply the 10th Man Rule**: Even if all 5 attack vectors find no issues, the methodology requires constructing at least one plausible failure scenario.
- **JIT Learning must produce exactly 5 pages**: One page per Bloom's Taxonomy step. This constraint ensures comprehensive coverage and prevents shallow analysis.

### Idempotency

- **SVG generation is idempotent**: Running the Python script twice with the same DATA dict produces identical output.
- **Gallery index rebuild is idempotent**: Running `/visualize-index` twice produces the same gallery (assuming no new projects were added).
- **Navigation injection is idempotent**: Replacing `<!-- nav:inject -->` with a script tag, then running again, does not duplicate the script tag (the comment is consumed).

---

## Failure Modes

### Codebase Visualization Flow

| Step | What Can Fail | Current Handling | Correctness |
|------|---------------|-----------------|-------------|
| Phase 0: Explore | Subagents return incomplete findings | Multiple subagents with overlapping scope; manual review | Partial |
| Phase 1: SVG gen | Unescaped XML characters | `escape()` + xmllint validation | Correct |
| Phase 1: SVG gen | Missing DATA keys | KeyError traceback; slide not generated | Partial |
| Phase 2: Interactive | GSAP CDN unavailable | No fallback; static layout still renders | Partial |
| Phase 4: Validate | xmllint not installed | Command fails; user sees error | Correct |
| Gallery index | Missing slide_01_eli5.svg | Folder excluded from discovery | Correct |

### Debate Review Flow

| Step | What Can Fail | Current Handling | Correctness |
|------|---------------|-----------------|-------------|
| Mode parsing | Unrecognized mode | Defaults to review | Correct |
| Pass 1: Advocate | LLM doesn't steelman effectively | Rapoport Rules structure | Partial |
| Pass 2: Critic | False positive findings | Judge rejects overreach | Correct |
| Evidence matrix | Non-diagnostic evidence | ACH rates diagnostic value | Correct |

### Cascading Failures

- **If settings.json is corrupted**: Claude Code falls back to default permissions. All Bash commands require manual approval. Skills still work but every command prompts.
- **If a template file is deleted**: The corresponding skill fails at generation time. Other skills are unaffected (skill isolation).
- **If CLAUDE.md is removed**: Claude Code loses operational guidelines but skills still function. Commit format, task management, and verification practices degrade to defaults.

---

## Architecture Strengths

1. **Zero external dependencies**: No pip install, no npm install, no Docker required. Python uses only stdlib. HTML uses a single CDN script (GSAP).
2. **Skill isolation**: Each skill is a self-contained directory. Adding, removing, or updating one skill cannot break another.
3. **Template-driven idempotent generation**: Output is deterministic given the same input data. Templates enforce visual consistency.
4. **Methodology grounding**: Skills are grounded in established frameworks: ACH (intelligence analysis), Rapoport Rules (philosophy), Bloom's Taxonomy (cognitive science), Hegelian dialectic.
5. **Progressive disclosure**: The 11-slide altitude descent means any audience can engage at their level.

## Architecture Risks

1. **LLM fidelity to methodology**: Skills describe detailed methodologies, but the LLM may not follow them precisely on every invocation.
2. **Template rigidity vs. customization**: Strict conformance means any visual customization requires modifying the canonical template.
3. **Single-CDN dependency for interactivity**: If the GSAP CDN is unavailable, interactive walkthroughs lose all animation.
4. **No automated testing**: Validation relies on xmllint and manual checks. No test suite exists.
