---
name: debate
description: >-
  Structured adversarial analysis toolkit with three modes: review (Advocate/Critic/Judge),
  red-team (attack-oriented failure analysis), and steelman (strongest counter-argument).
  Use when the user says "debate", "review this", "red team this", "break this",
  "argue against this", "steelman the opposite", or wants rigorous adversarial analysis.
argument-hint: "<mode> <target> — modes: review, red-team, steelman"
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git log *), Bash(git show *), Agent
---

# Debate — Adversarial Analysis Toolkit

A structured adversarial analysis system with three modes, each using a different
cognitive frame to surface issues that single-perspective analysis misses.

**Input**: `$ARGUMENTS` — expects `<mode> <target>` where:

- **`review`** — Three-pass Advocate/Critic/Judge review
- **`red-team`** — Attack-oriented failure analysis
- **`steelman`** — Strongest counter-argument construction

If no mode is specified, ask the user which mode they want. If the input is ambiguous,
default to `review` for code/diffs and `steelman` for decisions/positions.

`<target>` is a file path, directory, git diff range, or description.

---

## Mode Dispatch

Parse the first word of `$ARGUMENTS` to determine the mode:

1. If it matches `review`, `red-team`/`redteam`, or `steelman` → use that mode, pass the rest as target
2. If it doesn't match any mode → treat the entire argument as the target and ask which mode to use

Once you have the mode, **read the corresponding reference file** before proceeding:

- `review` → read `references/review.md`, then follow its three-pass methodology
- `red-team` → read `references/red-team.md`, then follow its attack methodology
- `steelman` → read `references/steelman.md`, then follow its three-step methodology

---

## Shared Principles

All three modes share these rules:

- **Read everything first.** Read all target files completely before producing any analysis. Never speculate about code you have not opened.
- **Evidence or remove.** Every finding must cite a specific `file:line`. No abstract claims.
- **State facts, not suggestions.** Instead of "you might want to consider..." write "Line 47 accepts unbounded input. A 10MB payload crashes the parser."
- **Scope to what was asked.** Analyze what the user submitted. Flag adjacent concerns only if directly relevant.
- **Do not implement fixes.** Report findings and recommend fixes, but do not write code.
