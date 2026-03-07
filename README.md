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

## Slash Commands

| Command            | Description               |
| ------------------ | ------------------------- |
| `/debate:review`   | Run an adversarial review |
| `/debate:red-team` | Run a red team analysis   |
| `/debate:steelman` | Build a counter-argument  |

## Installation

Copy or symlink the `claude/` directory into your project root. Claude Code will automatically pick up the skills and commands.

```text
your-project/
├── claude/
│   ├── commands/
│   │   └── debate/
│   │       ├── review.md
│   │       ├── red-team.md
│   │       └── steelman.md
│   └── skills/
│       ├── adversarial-review/
│       ├── red-team/
│       ├── steelman/
│       └── jit-learning/
```

## Release Notes

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for the full changelog.

## License

Apache License 2.0 — see [LICENSE.md](LICENSE.md) for details.
