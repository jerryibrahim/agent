You are reviewing a large diff for simplification opportunities. The PR adds more than 500 lines of non-test code — find duplication, over-abstraction, and unnecessary indirection.

## Scope

- Read all files from `{{WORKTREE}}`. Do not touch `{{ORIGINAL_REPO}}`.
- Branch under review: `{{BRANCH_NAME}}`.
- Only consider non-test files added or modified by this PR.
- **Read complete files, not just diff hunks.** Duplication and over-abstraction are only visible when you can see the whole shape — the helper plus all its callers, the interface plus all its implementations. Hunk-only reads miss the duplicate three pages down.

## What to look for

1. **Duplication** — Three or more near-identical blocks that could collapse into a helper or table-driven structure.
2. **Premature abstraction** — Interfaces, factories, or registries with one implementation and no foreseeable second one.
3. **Indirection without payoff** — Wrapper functions that only forward arguments; one-line methods that don't add invariants; types that exist only to be embedded once.
4. **Reinvented stdlib** — Custom slice/map utilities, custom error types where `errors.Is`/`As` would do, custom retry/backoff where a small helper exists.
5. **Dead branches** — Defensive checks for impossible states; fallback code paths that can never be reached given the call sites.
6. **Configuration sprawl** — New env vars or config fields with no consumer yet; flags whose only caller passes a constant.
7. **Layered try-catch / multi-layer error wrapping** — `fmt.Errorf("a: %w", fmt.Errorf("b: %w", err))` chains that add no information.

## What to ignore

- Code that looks verbose but encodes a real invariant or readability win.
- Patterns the project already uses consistently — flag deviation, not the convention itself.

## Output format

For each opportunity:

```text
- **SUGGESTION** | <simplification>
  Location: `<path>:<line-range>`
  Current: <one-line characterization of the current code>
  Proposed: <one-line sketch of the simpler form>
  Lines saved (estimate): <number>
```

End with a one-paragraph summary: total estimated lines that could be removed, and whether the diff is well-shaped or carries excess weight.
