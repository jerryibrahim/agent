# Agent

A collection of Claude Code custom skills and commands for structured thinking, adversarial review, and accelerated learning.

## Skills

### Adversarial Review

Three-pass **Advocate / Critic / Judge** debate for reviewing code, designs, or documents. Each pass uses a different cognitive frame to surface issues that single-perspective review would miss.

- **Advocate** — Steelmans the artifact (Dennett's Rapoport Rules)
- **Critic** — Finds real problems with evidence (Analysis of Competing Hypotheses)
- **Judge** — Resolves tensions and delivers a verdict (Dialectical synthesis)

### Red Team

Adversarial failure analysis that assumes the target will break and finds how. Works through five attack vectors: input boundaries, state/concurrency, failure cascades, security, and operational concerns. Includes the **10th Man Rule** — if the system looks sound, argue the opposite.

### Steelman

Constructs the strongest possible counter-argument to a position, then evaluates both sides. Implements Rapoport's Rules: demonstrate understanding of a position before earning the right to critique it.

### JIT Learning

Applies the Just-in-Time Learning framework to rapidly understand any new technology. Produces a structured five-page report grounded in Bloom's Taxonomy, progressing from a hard JIT boundary through functional decomposition to an ELI5 mental model.

### Visualize Codebase

Generates interactive visual documentation for any codebase — SVG infographics descending from 50,000 ft to ground level, plus GSAP-animated sequence diagrams. Zero external Python dependencies; all SVGs are built with pure Python string construction. Produces:

- **Static SVGs** — 10-12 slides covering ELI5, system context, architecture layers, domain model, request lifecycle, routing, state machines, database schema, API routes, code structure, and config
- **Interactive walkthrough** — GSAP-animated sequence diagrams for major use cases
- **Deep-dive analysis** — design decisions, invariants, and failure mode documentation

### Visualize Index

Builds or rebuilds an `index.html` gallery inside `visualizations/`, stitching together all project folders into a dark-themed 3-column grid with links to each project's Overview, Interactive, and Deep Dive pages.

### Propose

Deep-analyzes a topic and proposes 2-4 implementation options with pros, cons, effort, and risk. Useful for evaluating approaches before committing to an implementation strategy.

### Commit

Automates git commits with a user-provided summary as the first line and an auto-generated bullet-point body summarizing key changes. Stages files individually (never `git add .`) and skips secrets and `.vscode/`.

## Slash Commands

| Command               | Description                     |
| --------------------- | ------------------------------- |
| `/debate:review`      | Run an adversarial review       |
| `/debate:red-team`    | Run a red team analysis         |
| `/debate:steelman`    | Build a counter-argument        |
| `/visualize-codebase` | Generate visual codebase docs   |
| `/visualize-index`    | Build the visualization gallery |
| `/propose`            | Propose implementation options  |
| `/commit`             | Create a structured git commit  |

## /visualize-codebase Example

An example of the **Visualize Codebase** skill run on this repo. These files live in the `docs/` directory and are served via GitHub Pages:

- [Overview](https://jerryibrahim.github.io/agent/) — slideshow of SVG infographics from 50,000 ft to ground level
- [Interactive Walkthrough](https://jerryibrahim.github.io/agent/interactive.html) — GSAP-animated sequence diagrams of key flows
- [Deep Dive](https://jerryibrahim.github.io/agent/deep-dive.html) — design decisions, invariants, and failure mode analysis

## Installation

Copy or symlink the `.claude/` directory into your project root. Claude Code will automatically pick up the skills and commands.

```text
your-project/
├── .claude/
│   └── skills/
│       ├── commit/
│       ├── debate/
│       ├── jit-learning/
│       ├── propose/
│       ├── visualize-codebase/
│       └── visualize-index/
```

## Release Notes

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for the full changelog.

## License

Apache License 2.0 — see [LICENSE.md](LICENSE.md) for details.
