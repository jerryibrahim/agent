# PR comment (copy-paste)

**Verdict: <Approve | Approve with comments | Request changes>.** <One- to three-sentence framing that names the PR's purpose and the headline outcome of the review. If supplemental to prior review rounds (Copilot, prior reviewers), say so here.>

**Ticket:** {{JIRA_TICKET}}

---

## Blocking — must fix before merge

<If no blockers, replace this entire section with: `None — no blockers.`>

<Otherwise, one sub-section per blocker. Length is driven by the bug's complexity, not by a cap. Each blocker carries enough context for the author to act on it without seeing the local analysis file.>

### <BLOCKER-N> — <one-line title naming the bug>

`<path/to/file.go:line-range>`:

<Optional: short code excerpt (3–10 lines) if the bug is in the literal code shape. Use a fenced block with the right language.>

<1–3 paragraphs explaining the bug. Cover: what the code intends, where it goes wrong, the concrete failure scenario (with realistic actor/data, not abstract "if X then Y"), and why the existing tests don't catch it. Include file:line refs throughout — every claim should be auditable.>

**Fix** — <If there is one obvious fix, describe it in 2–4 sentences with the code or SQL shape. If there are multiple defensible options, label them Option A / Option B with one-paragraph pros/cons each and a recommendation. Ship with a regression test where applicable — name the test by file and the invariant it pins.>

---

## Non-blocking findings

<Group by character, not by count. Use whichever subset of the headings below the PR actually needs. Each finding gets enough context for the author to act on it OR a follow-up Jira link that carries the full detail.>

### Worth addressing before merge

<Non-blocking items that are cheap and worth bundling into the same rebase. Two- to four-sentence write-ups with file:line and a concrete fix. Example phrasing: "At minimum X; ideally Y."  Save deep multi-option analyses for blockers or for follow-up tickets.>

### Important polish

<Operability / design / convention issues that should be addressed but can wait for a follow-up PR. One short paragraph each, file:line, and the fix shape.>

### Test coverage gaps

<Each gap: name, production file, the missing case (concrete scenario), and a one-line sketch of the test to add. Mention if a gap is "regression coverage that lands with blocker C-N" vs "post-merge follow-up."  >

### Documentation

<Doc nits, missing OpenAPI entries, runbook gaps. Same shape: file:line, what's wrong, fix.>

### Process

<Jira traceability, commit hygiene (squash recommendations with the rough commit groupings), stale base, test-plan boxes unchecked. Concrete and operational, not generic.>

### Suggestions

<Optional improvements — defense-in-depth comments, helper extractions for once-a-second-consumer-exists, naming improvements. One sentence each is fine here.>

### Follow-ups tracked elsewhere

<Reference Jira tickets that capture larger non-blocking scope: `- **[KCS-552](https://mirantis.jira.com/browse/KCS-552)** — consolidated post-merge polish: ...`. Use ticket references to keep the comment focused instead of inlining every detail.>

---

## Strengths

<Genuine callouts. Not optional padding — the example reviews always include this. The author should know what to keep doing. Avoid generic praise; cite specific patterns with file:line refs.>

- **<Pattern name>** — <one- to three-sentence explanation of why this pattern is well-shaped, with file:line where it appears>.
- ...

---

## Notes

- Strip reviewer-only material from this block: "What I verified," local verification commands, worktree paths, cross-PR coordination notes the author doesn't need.
- Never reference local-only paths (`out/PR/...`, worktree directories, `tasks/`). The author sees this block as a public PR comment.
- Length is driven by the PR. A clean Approve can be a few paragraphs of Strengths; a Request-changes on a complex PR can be very long if each blocker needs full context.
