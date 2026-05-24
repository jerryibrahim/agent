---
name: pr-review
description: >-
  Full PR review workflow. Creates an isolated git worktree for the PR
  branch, runs parallel review agents (code, security, tests, errors),
  checks for stale base and merge conflicts, and saves the review to
  out/PR/ in the original repo. The worktree is left in place so you can
  rebase or push follow-up fixes; clean up with /pr-review-cleanup when done.
argument-hint: "<PR number or branch name>"
---

# PR Review

Orchestrates a multi-agent PR review in an isolated worktree, compiles the
findings into a full review file, and emits a GitHub-ready PR comment.

## Templates

All content templates live in `templates/` (relative to this skill file):

- `templates/agents/*.md` — one prompt per review agent. Each agent reads its
  template, substitutes placeholders, and is dispatched in parallel.
- `templates/review.md` — full review skeleton saved locally.
- `templates/concise-feedback.md` — the GitHub PR comment. Length is driven
  by the PR's complexity, not a fixed cap; "concise" means stripped of
  reviewer-only material (verification trace, local commands), not short.
  It is the author's only source of truth — the saved analysis file is
  local and cannot be referenced.
- `templates/footer.txt` — worktree footer printed to chat (not saved).

Placeholders used across templates: `{{WORKTREE}}`, `{{ORIGINAL_REPO}}`,
`{{BRANCH_NAME}}`, `{{PR_NUMBER}}`, `{{JIRA_TICKET}}`, `{{REVIEW_TYPE}}`.

---

## Phase 1: Scope Detection

**If `$ARGUMENTS` is a PR number or branch name**, prepare an isolated worktree
so the user's current working tree is never disturbed:

1. Capture the original repo root: `ORIGINAL_REPO=$(git rev-parse --show-toplevel)`.
   The review file will be written here, not in the worktree.
2. Resolve the target branch:
   - PR number: `gh pr view <number> --json headRefName --jq '.headRefName'`
   - Branch name: use `$ARGUMENTS` directly
3. Choose a worktree path:
   `WORKTREE="$(dirname "$ORIGINAL_REPO")/$(basename "$ORIGINAL_REPO")-pr-<n>"`
   (or `-<branch-slug>` for the branch case). Prefer the PR number.
4. Check whether the path already exists:
   - If it is a registered worktree (`git worktree list --porcelain`), ask
     whether to reuse or remove and recreate.
   - If it is a stray directory, ask before removing.
5. Check whether the target branch is already checked out elsewhere
   (`git worktree list --porcelain | grep "branch refs/heads/<branch>"`). If
   so, surface that path and stop — do not create a duplicate.
6. Fetch and create the worktree:
   - `git -C "$ORIGINAL_REPO" fetch origin`
   - `git -C "$ORIGINAL_REPO" worktree add --detach "$WORKTREE"`
   - From inside `$WORKTREE`, run `gh pr checkout <number>` (PR case) or
     `git checkout <branch>` (branch case).
7. Run all subsequent steps with `-C "$WORKTREE"` or after `cd "$WORKTREE"`.
   Do **not** mutate the original working tree.

**If no `$ARGUMENTS`**, use the current branch in the current working tree.
No worktree is created; `$ORIGINAL_REPO` and `$WORKTREE` both refer to the
current repo root.

### Determine review type

1. Check `git diff --cached` and `git diff` for staged/unstaged changes.
2. If there are uncommitted changes → **pre-commit review** of those changes.
3. If the working tree is clean → **pre-merge review** of `git log main..HEAD`.
4. If no changes anywhere, report that there is nothing to review and stop.

---

## Phase 2: Gather Context

### Jira ticket traceability

Look for project ticket prefixes (KCS-*, DEVINT-*, or similar UPPERCASE-number
patterns) in:

1. Branch name (e.g., `feat/KCS-64`)
2. Commit messages: `git log main..HEAD --oneline`
3. PR title (if a PR exists): `gh pr view --json title`

Capture into `{{JIRA_TICKET}}`. If none found, set `{{JIRA_TICKET}}` to
`None found` and add a finding to the PROCESS section:

> **PROCESS: No Jira ticket reference found.** Branch name, commit messages,
> and PR title do not contain a ticket reference (expected pattern: KCS-*,
> DEVINT-*, or similar). Link the relevant ticket for traceability.

### PR conversation

When a PR exists, read existing comments to avoid re-raising resolved issues:

1. `gh pr view <number> --json comments --jq '.comments[].body'`
2. `gh api repos/{owner}/{repo}/pulls/<number>/comments`

Look for prior review feedback already addressed in follow-up commits, linked
Jira tickets in comments, author responses explaining design decisions, and
acknowledged follow-up items.

### Stale base detection

Before reviewing content, check whether the branch includes unrelated changes
from a stale base:

1. Run `git show <sha> --stat` for each commit on the branch.
2. Compare against `git diff main..HEAD --stat`. If the full diff includes
   files not in any commit, the branch has base divergence.
3. If CI workflow files (`.github/`), `go.mod`/`go.sum`, or unrelated service
   files appear in the diff but not in the commits, add a PROCESS finding:

> **PROCESS: Stale base branch.** The diff includes files not modified by any
> commit on this branch (likely divergence from main). Rebase onto current
> main before review.

Only review files that appear in the actual commits, not the full diff.

### Stale-base regression check

After detecting stale base files, check whether the PR's version of shared
files would silently revert changes from recently merged PRs:

1. `gh pr list --state merged -L 10 --json number,title,mergedAt`
2. For each file the PR modifies that was also modified by a recently merged
   PR, compare what the merged PR added vs. what the current PR's version
   contains.
3. Focus on high-risk files: `secret-auth.yaml`, `values.yaml`,
   `values-kind.yaml`, `values-secrets-sample.yaml`, `docker-compose.yml`,
   `go.mod`, `config.go`, `main.go`.
4. If the PR would remove lines added by a recently merged PR, flag as:

> **REGRESSION WARNING:** This PR's version of `<file>` is missing lines added
> by recently merged PR #Y (`<title>`). If merged as-is, those additions will
> be silently reverted. Cause: this branch was created before PR #Y merged
> (stale base). Fix: rebase onto current main.

### Merge conflict check (pre-merge only)

1. `git merge-tree main <branch>` — check for textual conflicts.
2. If clean, note whether a semantic conflict is likely — check if the branch
   modifies files also recently changed on main (shared types, function
   signatures, Helm values).
3. If the branch touches `main.go`, config types, or shared packages, flag
   for post-merge build verification.

---

## Phase 3: Structural Surface Checks

These are file-system / contract-level checks the reviewer runs directly,
not via subagents. Each can produce blocking or non-blocking findings that
flow into Phase 5 finding-triage alongside the agent results.

### 3a. OpenAPI contract drift

Trigger: the diff modifies handler files, route-registration calls
(`routes.go`, `routes_test.go`, `Method("...")`, `HandleFunc("...")`,
`mux.Handle("...")`), or any code that registers HTTP endpoints.

Only run if the repo has an OpenAPI bundle. Detect by checking for any of:
`api/contract/`, `api/openapi.yaml`, `openapi.yaml`, `swagger.yaml`,
`api/**/openapi.yaml`.

1. List route additions and changes from the diff. `routes_test.go` is often
   the cleanest source — each entry pins method + path.
2. For each new route, grep the OpenAPI bundle for a matching `path` entry
   and matching method (`get`, `post`, `delete`, etc.).
3. For each modified route (method change, path-param rename, new query
   param), check the OpenAPI entry reflects the change.
4. For removed routes, check the OpenAPI bundle no longer references them.

If a new **public** route has no OpenAPI entry, flag as a blocker candidate.
The project standard is "spec changes ship with implementation" — a new
endpoint without spec is a contract regression (see PR #311 C3 as the
canonical precedent). Internal-only routes (admin, debug) may be exempt
depending on project convention; check `CLAUDE.md` or `api/contract/README`.

Required fix: new path file under `api/contract/paths/...`, path entry in
`api/contract/openapi.yaml`, and bundle regeneration. Cite a sibling path
file as a shape reference.

### 3b. Helm sample-values sync

Trigger: the diff modifies any `deploy/helm/**/values.yaml` keys — added,
removed, renamed, or restructured.

Only run if the repo has Helm charts. Detect via `deploy/helm/` or
`charts/`.

1. List every `values-*.yaml` file in the repo:

   ```bash
   find deploy/helm -name 'values-*.yaml' -type f
   ```

   Typical names: `values-secrets-sample.yaml`, `values-secret-kind.yaml`,
   `values-kind.yaml`, `values-secrets-dev*.yaml`, `values-prod.yaml`.

2. For each **removed or renamed** key, grep all sample files for the old
   key path. Any sample file still using the old path is a finding.

3. For each **new** key that requires operator configuration (not just an
   internal default), check that at least one sample file demonstrates
   canonical usage with the right indentation context.

4. If a key was renamed without a deprecation shim, flag whether existing
   `values-*.yaml` overlays in the repo OR in known operator-managed paths
   (the user may keep these under `~/k/k8/...` per their workflow) would
   break on next `helm upgrade`. PR #316 I1 is the canonical precedent —
   the rename worked at the chart level but broke every cluster's overlay.

Common severity calls:
- Rename with no shim + sample still uses old key → blocker if `helm
  upgrade` would fail; otherwise "worth addressing before merge."
- New required key with no sample → "worth addressing before merge."
- Renamed key with deprecation shim in `_helpers.tpl` → non-blocking; note
  the migration window.

### 3c. DB migration numbering

Trigger: the diff adds a file under `migrations/`, `db/migrations/`, or
`services/*/db/migrations/`.

1. List migration files on the branch grouped by service:

   ```bash
   git -C "$WORKTREE" diff main..HEAD --name-only -- '**/migrations/*.sql'
   ```

2. List migration numbers currently on `main` for the same service:

   ```bash
   git -C "$WORKTREE" ls-tree -r --name-only main -- '<service>/migrations/' \
     | sort
   ```

3. Check recently merged PRs for migration adds: `gh pr list --state merged
   -L 20 --json number,title,files`. Each migration `NNNNNN_name.up.sql`
   has a numeric prefix.

4. Flag:
   - **Number collision** — the PR adds `000009_foo.up.sql` and a
     recently merged PR (or another open PR) also added `000009_*.up.sql`.
     This is a hard blocker; one of the two must be renumbered before
     merge.
   - **Gap in numbering** — the PR adds `000011_*.up.sql` but `000010_*`
     doesn't exist. Sometimes intentional (matching another branch);
     usually a typo. Flag as PROCESS.
   - **Out-of-order rename** — the PR renames an existing migration. This
     is a blocker on any production system that has already applied the
     old name; rename is only safe pre-release.
   - **Missing `down.sql`** — if the convention requires paired
     up/down files, flag the missing partner.

The migration-numbering check is the highest-value low-effort guard against
silently merging two PRs that both try to claim the same number — the
collision usually fails CI but only after merge. Catching it pre-merge
avoids the cleanup PR.

---

## Phase 4: Dispatch Review Agents

For each agent, read its prompt template from `templates/agents/`, substitute
`{{WORKTREE}}` and `{{BRANCH_NAME}}`, and dispatch in parallel.

**Always launch (5 agents):**

| Agent | Template |
|-------|----------|
| General reviewer | `templates/agents/general-reviewer.md` |
| Silent failure hunter | `templates/agents/silent-failure-hunter.md` |
| Test analyzer | `templates/agents/test-analyzer.md` |
| Security reviewer | `templates/agents/security-reviewer.md` |
| Scalability auditor | `templates/agents/scalability-auditor.md` |

**Conditionally launch:**

| Agent | Condition | Template |
|-------|-----------|----------|
| Type design analyzer | Diff introduces new struct, interface, or type alias | `templates/agents/type-design-analyzer.md` |
| Code simplifier | Diff adds more than 500 lines of non-test code | `templates/agents/code-simplifier.md` |

**Pre-commit reviews** use the same agent set but each agent should focus on
the staged/unstaged diff rather than the full branch diff.

All agents must read files from `{{WORKTREE}}` only. The template's scope
section enforces this — do not edit it out when substituting placeholders.

---

## Phase 5: Finding Triage

Before compiling the review, deep-analyze every finding one-by-one. This
phase compares each candidate finding against the rest of the codebase and
either drops it or upgrades it with a concrete recommended fix. The
input is the union of agent findings (Phase 4) and structural-check
findings (Phase 3). The output is a triaged set ready for the compile.

This is the load-bearing quality step. Agents produce many candidate
findings — some are noise (already the project's convention), some are
duplicates of each other, some are correct but lack a fix. Skipping this
phase produces reviews that flag things the author has to push back on.

### Procedure for each finding

1. **Read the referenced code.** Open the file at the cited line and read
   enough surrounding context to understand the function's role and the
   data flow into the cited line. If the agent only quoted a snippet, you
   may be missing context the agent didn't see.
2. **Compare to codebase patterns.** Look for sister implementations:
   - Other handlers / services / queries that do the same kind of thing.
   - The pattern used in the most-recently-merged code that touches this
     area (often the canonical shape).
   - Any `CLAUDE.md`, package-level doc, or `README` that codifies a
     convention.
   - Existing tests that pin the expected behavior — if the codebase
     already tests the "correct" shape and the diff matches it, the
     finding is likely noise.
3. **Decide drop or keep:**
   - **Drop** if the flagged pattern matches the established convention
     elsewhere in the codebase; another finding already covers it; the
     agent misread the code (e.g., flagged a `_` ignored error that is
     actually intentional and documented); there's a project-level
     exception that supersedes the generic rule.
   - **Keep** if codebase evidence confirms the issue; the surrounding
     code shows the failure mode is reachable; no countervailing
     convention exists.
4. **Attach a recommended fix to every kept finding.** "Add error
   handling" is not a fix — name the specific change:
   - The exact code or SQL diff (often 3–10 lines).
   - Multiple options (Option A / Option B) with one-paragraph pros/cons
     each when more than one shape is defensible.
   - The regression test that should accompany the fix, named by file and
     by the invariant it pins.
5. **Re-classify severity if the triage reveals new information.** If a
   `CRITICAL` agent finding turns out to be a project convention, drop
   it. If a `SUGGESTION` finding turns out to be a real bug after reading
   the surrounding code, promote it.

### Deduplication

Multiple agents often flag the same underlying issue from different angles
(e.g., silent-failure-hunter sees a swallowed error; security-reviewer
sees the same error path as an information-leak vector). Merge these into
a single finding that captures both angles. Triage output should have
zero duplicates by file:line.

### Recording the triage

Triage produces a working list per finding with one of:
- `DROPPED — <reason>` (these do not appear in the final review).
- `KEPT — <recommended-fix-summary>` (these flow into Phase 6).

Keep this working list in your scratch space; it does not appear in the
saved review or the GitHub comment.

---

## Phase 6: Compile Full Review

Read `templates/review.md` and substitute `{{BRANCH_NAME}}`, `{{JIRA_TICKET}}`,
`{{REVIEW_TYPE}}` (`pre-commit` or `pre-merge`).

### Step 6a — Select merge blockers

The `Merge Blockers` section at the top of the review is the **load-bearing
output of the entire review**. It is a small, explicit set the author must
address before merge. Everything else is non-blocking — it can be fixed in
this PR or tracked in a follow-up ticket.

**Blocker status is a reviewer decision, not a function of severity tag or
finding count.** A `CRITICAL` from an agent is a strong candidate but not
automatic. The reviewer (you, compiling the review) decides.

Default candidates for blocker status:

- Exploitable security issues (auth bypass, secret leak, injection with a
  realistic vector).
- Data-loss or data-corruption risks (lost writes, broken migrations,
  unguarded destructive operations).
- Regressions of recently merged PRs (caught by the stale-base regression
  check).
- Merge conflicts or build breaks that would land broken code on main.
- Authorization gaps on mutating endpoints.

Not blockers by default — even at high severity:

- Hardening suggestions and defense-in-depth where an existing layer
  mitigates the issue.
- Missing test coverage (track in a follow-up unless the missing case is a
  guaranteed production failure).
- Documentation, spelling, naming, and design suggestions.
- Style or convention deviations.

For each blocker, the entry must include: one-line summary, `file:line`,
**why this blocks** (the concrete merge-time risk in one sentence), and the
required fix.

### Step 6b — Place everything else

Non-blocking findings go into `Non-Blocking Findings`, grouped by category
(Security, Correctness and design, Test coverage gaps, Documentation issues,
Spelling and typos, Process, Suggestions, Strengths). The grouping is for
triage convenience — it carries no implication of urgency. A long list of
non-blocking findings does not change the verdict.

Routing from agents to non-blocking categories:

- Security-reviewer non-blockers → `Security (non-blocking)`.
- Silent-failure non-blockers → `Correctness and design`.
- Test-analyzer findings → `Test coverage gaps`.
- General-reviewer findings: documentation → `Documentation issues`;
  spelling → `Spelling and typos`; everything else → `Correctness and design`
  or `Suggestions` depending on impact.
- Type-design and code-simplifier findings → `Suggestions` unless promoted
  to blocker.
- Stale-base, Jira, merge-conflict, commit-hygiene findings → `Process`
  (or `Merge Blockers` if they would land broken code).

Every finding includes: one-line description, `file:line` where applicable,
and a suggested fix.

### Step 6c — Verdict

The verdict is mechanical from the blockers section:

- **Request changes** — at least one item in `Merge Blockers`.
- **Approve with comments** — `Merge Blockers` is empty AND there are
  non-blocking findings worth the author's attention.
- **Approve** — `Merge Blockers` is empty AND no non-blocking findings, or
  only `Strengths`.

The verdict goes both in the header (`**Verdict:**`) and into
`Verdict Rationale`, where you name the specific blockers (or state that
there are none) and tie the verdict to that set.

### Save

1. Determine the PR number:
   - From `$ARGUMENTS` if a PR number was provided.
   - Otherwise from `gh pr view --json number` on the current branch.
   - If no PR exists, use the branch slug as the filename.
2. Write to `$ORIGINAL_REPO/out/PR/{{PR_NUMBER}}_PR.md` (create `out/PR/` if
   needed). Always write to `$ORIGINAL_REPO`, never the worktree.
3. The file is formatted for direct paste into a GitHub PR comment — no
   preamble, no chat footer.

---

## Phase 7: GitHub PR Comment

After the full review is saved, generate the copy-paste PR comment using
`templates/concise-feedback.md`. The block mirrors the blocker-first
structure of the full review and is **the author's only source of truth** —
the saved analysis file is on the reviewer's machine and cannot be referenced.

### Content rules

1. **Lead with the verdict** in bold followed by a one- to three-sentence
   framing of the PR and outcome. Same verdict computed in Phase 6c.
2. **Blocking section is the centerpiece.** List every blocker, with enough
   context for the author to act on it without seeing the local analysis
   file. Each blocker gets: a named header, file:line refs, the bug
   explained (intent → mechanism → failure scenario → why existing tests
   miss it), and a concrete fix (Option A/B with tradeoffs when applicable).
   If there are no blockers, the section reads `None — no blockers.`
3. **Non-blocking findings get real context, not a count.** The author
   cannot see the full review file — every non-blocker that should be acted
   on needs a named header, file:line, what's wrong, and a fix path. Group
   by character (`Worth addressing before merge`, `Important polish`,
   `Test coverage gaps`, `Documentation`, `Process`, `Suggestions`,
   `Follow-ups tracked elsewhere`), not by count.
4. **Use Jira ticket references to control length.** When a cluster of
   non-blocking items is being tracked in a follow-up Jira ticket, link the
   ticket and give a one-paragraph summary in the comment rather than
   inlining each item's full detail. Ticket references must be real — do
   not invent IDs.
5. **Strengths section is required, not optional.** The example reviews
   always include genuine pattern-level callouts. Cite specific patterns
   with file:line refs. Avoid generic praise.
6. **Length follows the PR.** A clean Approve can be a few paragraphs of
   Strengths plus a Process line. A Request-changes on a complex PR can be
   200+ lines if each blocker needs SQL excerpts, code, scenarios, and
   multi-option fixes. Do not impose a finding cap or length cap.
7. **Verdict is mechanical from the blocker set.** `Request changes` iff
   the Blocking section is non-empty. A long list of non-blockers does not
   downgrade the verdict.

### What to strip from the comment

The concise block is the author's view. Cut anything that's only useful to
the reviewer at compile time:

- `What I verified` reviewer-trace notes.
- Local verification commands that reference the worktree path
  (`cd /Users/.../repo-pr-N`).
- Cross-PR coordination notes ("the sibling PR #312 ships X — that's the
  precedent here") **unless** the author needs the precedent to make a fix
  decision.
- Anything referencing `out/PR/...`, `tasks/`, or worktree directories.

### GitHub-bound output rules

The block is intended for paste into a public PR comment. It must **never**
reference local-only paths. Inline anything the author needs to see.

### Output

Substitute `{{JIRA_TICKET}}` and emit the comment in **two places**:

1. Printed to chat inside a fenced ` ```markdown ` block so the user can
   copy it directly into the GitHub PR comment.
2. Appended to the saved review file under a `---` separator and the
   heading `## PR comment (copy-paste)`.

---

## Phase 8: Worktree Footer (chat only)

Read `templates/footer.txt`, substitute `{{WORKTREE}}`, `{{ORIGINAL_REPO}}`,
`{{BRANCH_NAME}}`, `{{PR_NUMBER}}`, and print to chat. This footer is for
the chat session only — it must **not** be written into the saved review
file or the concise GitHub block.

Do not auto-remove the worktree. The user often rebases, fixes up, or
force-pushes from inside it.

---

## Phase 9: Suggested Verification

After delivering the review, suggest commands the reviewer can run locally:

- `make build-workspace` — verify compilation
- `make vet-workspace` — static analysis
- `make test-workspace` — unit tests
- `make run SERVICE=<service> TARGET=docker-test-e2e` — e2e tests for affected services

---

## Guardrails

- **No emoji** in any output.
- **No GitHub comments without explicit user approval.** Generate the
  concise block, but do not post it.
- **No local paths in GitHub-bound output.** The concise block is paste-ready
  for a public PR comment; it must never reference `out/PR/...` or any other
  local file.
- **Blocker discipline.** Merge blockers are a deliberate, named set chosen
  by the reviewer — not a function of severity tags or finding count. A PR
  with 30 non-blocking findings and 0 blockers still merges; non-blocking
  items belong in a follow-up ticket. See Phase 6a for blocker criteria.
- **Template fidelity.** Agent prompts must be substituted, not paraphrased.
  Read the template, replace placeholders, dispatch verbatim.
- **Read before flagging.** Every finding must be grounded in a file you
  (or a subagent) actually read. Do not flag from guessed structure.
- **Worktree isolation.** All agents and review steps operate on
  `$WORKTREE`. The original repo is read-only except for writing the final
  review file to `$ORIGINAL_REPO/out/PR/`.
- **One command per Bash call.** Prefer separate Bash invocations over
  chained `cmd1 && cmd2` shells, especially during Phase 1 (worktree
  setup) and Phase 6 (writing the review file). Each step's output should
  be visible before the next runs, so the user can intervene if something
  looks wrong. Reserve `&&` for genuinely atomic dependencies
  (`mkdir foo && cd foo`); pipelines inside one logical operation
  (`grep -r foo | wc -l`) are fine.
