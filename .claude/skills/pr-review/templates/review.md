# PR Review — {{BRANCH_NAME}}

**Ticket:** {{JIRA_TICKET}}
**Review type:** {{REVIEW_TYPE}}
**Verdict:** <Approve | Approve with comments | Request changes>

---

## Merge Blockers

These items **must be addressed before merge**. If the section reads
`None — no blockers.`, the PR can merge once any non-blocking findings the
author chooses to address are resolved or tracked.

<For each blocker, emit:>

- **<BLOCKER-N>** — <one-line summary>
  - File: `<path>:<line>`
  - Why this blocks: <one sentence on the concrete merge-time risk: data loss, security exploit, regression, build break, etc.>
  - Required fix: <specific change required>

<If empty: "None — no blockers.">

---

## Non-Blocking Findings

These do not block merge. The author may address them in this PR or track
them in a follow-up ticket. They are grouped by category for triage, not
by urgency.

### Security (non-blocking)

<Hardening suggestions and defense-in-depth items that are not exploitable as-is. Any exploitable issue belongs in Merge Blockers, not here.>

### Correctness and design

<Bugs, design issues, and convention violations that do not threaten production data or security.>

### Test coverage gaps

### Documentation issues

### Spelling and typos

### Process

<Jira traceability, commit hygiene, stale base, merge conflicts that did not rise to blocker level.>

### Suggestions

<Optional improvements.>

### Strengths

<What the PR does well — call these out so the author knows what to keep doing.>

---

## Verdict Rationale

<One paragraph. If there are blockers, name them explicitly and tie the verdict to that set. If there are no blockers, state that and note whether the author may want to address any non-blocking items inline vs. follow-up.>
