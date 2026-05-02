# Release Notes

## v1.2.0 — 2026-05-02

### New Skills

- **PR Analysis** skill — surveys all open PRs, builds a file-overlap matrix, and recommends a merge sequence that minimizes conflicts
- **PR Review** skill — full PR review workflow that creates an isolated git worktree for the PR branch, runs four parallel review agents (general code, silent-failure hunter, test analyzer, security), checks for stale base and merge conflicts, and saves the review to `out/PR/<n>_PR.md` for copy-paste into GitHub
- **PR Review Cleanup** skill — removes pr-review worktrees by PR number, branch, path, or `--all`; refuses to remove worktrees with uncommitted changes or unpushed commits unless `--force`
- Slash commands added: `/pr-analysis`, `/pr-review`, `/pr-review-cleanup`

---

## v1.1.0 — 2026-03-14

### New Skills

- **Visualize Codebase** skill — generates interactive visual documentation: 10-12 SVG infographics (50,000 ft to ground level), GSAP-animated sequence diagrams, and deep-dive analysis with design decisions, invariants, and failure modes
- **Visualize Index** skill — builds a dark-themed gallery page stitching all visualization projects into a 3-column grid with Overview, Interactive, and Deep Dive links
- **Propose** skill — deep-analyzes a topic and proposes 2-4 implementation options with pros, cons, effort, and risk assessment

### Changes

- Consolidated debate sub-skills (adversarial-review, red-team, steelman) under a single `debate/` skill directory
- Added slash commands for all skills: `/visualize-codebase`, `/visualize-index`, `/propose`, `/commit`

---

## v1.0.0 — 2026-03-06

### Initial Release

- **Adversarial Review** skill — three-pass Advocate/Critic/Judge structured debate
- **Red Team** skill — adversarial failure analysis with five attack vectors and the 10th Man Rule
- **Steelman** skill — strongest counter-argument construction using Rapoport's Rules
- **JIT Learning** skill — five-step learning framework grounded in Bloom's Taxonomy
- Slash commands: `/debate:review`, `/debate:red-team`, `/debate:steelman`
