---
name: pr-review
description: >-
  Full PR review workflow. Checks out the PR branch from a clean main,
  runs parallel review agents (code, security, tests, errors), checks for
  stale base and merge conflicts, and saves the review to out/PR/ for
  copy-paste into GitHub.
argument-hint: "<PR number or branch name>"
---

# Code Review

## Focus Areas

1. **Documentation correctness** — Do comments, ER diagrams, DATABASE_SCHEMA.md, and OpenAPI specs match the actual code?
2. **Domain correctness** — State machine transitions, validation logic, cross-service contracts
3. **Silent error swallowing** — Catch blocks that log-and-continue, blank identifiers on errors, best-effort patterns without recovery
4. **Test coverage** — Are all behavioral paths tested? Edge cases, error paths, race conditions
5. **Design** — Separation of concerns, interface design, type safety across boundaries
6. **Logging standards** — Structured slog usage, no global logger, appropriate levels, no leaked secrets
7. **Cross-boundary access** — No cross-DB queries, services communicate only via HTTP
8. **Security** — Authorization checks on all mutating endpoints, no auth bypass paths, no internal details leaked in error responses, secrets not logged or exposed
9. **Spelling and typos** — Check variable names, string literals, comments, error messages, log messages, and documentation for misspellings, typos, and grammatical errors

## Jira Ticket Traceability

Check that a Jira ticket is referenced. Look for patterns matching known project prefixes (KCS-*, DEVINT-*, or similar UPPERCASE-number patterns):

1. Check the branch name (e.g., `feat/KCS-64`, `fix/DEVINT-123`)
2. Check commit messages on the branch (`git log main..HEAD --oneline`)
3. Check the PR title if a PR exists (`gh pr view --json title`)

If no Jira ticket is found in any of these locations, flag it as:

> **PROCESS: No Jira ticket reference found.** Branch name, commit messages, and PR title do not contain a ticket reference (expected pattern: KCS-*, DEVINT-*, or similar). Link the relevant ticket for traceability.

If a ticket is found, note it in the review header (e.g., "Ticket: KCS-64").

## Scope Detection

Determine what to review based on current state:

**If `$ARGUMENTS` is a PR number or branch name**, prepare a clean checkout:

1. Stash any uncommitted changes if the working tree is dirty (`git stash --include-untracked`)
2. Switch to main and pull latest (`git checkout main && git pull --all`)
3. Checkout the target:
   - PR number: `gh pr checkout <number>`
   - Branch name: `git fetch origin <branch> && git checkout <branch>`
4. Note if a stash was created so the user can restore it after the review

**If no `$ARGUMENTS`**, use the current branch as-is.

### Gather PR Context

When reviewing a PR (not a pre-commit review), read existing PR comments and review threads for context:

1. `gh pr view <number> --json comments --jq '.comments[].body'` — PR conversation comments
2. `gh api repos/{owner}/{repo}/pulls/<number>/comments` — inline review comments
3. Check for:
   - Prior review feedback that may already be addressed in follow-up commits
   - Linked Jira tickets referenced in comments (e.g., KCS-163) — include these in the review output
   - Author responses explaining design decisions — factor these into the review
   - Follow-up items the author has acknowledged — reference them rather than re-raising

Then determine the review type:

1. Check `git diff --cached` (staged changes) and `git diff` (unstaged changes)
2. If there are staged or unstaged changes, review those — this is a **pre-commit review**
3. If the working tree is clean, check `git log main..HEAD` for branch commits — this is a **pre-merge review** of the full branch diff
4. If no changes anywhere, report that there is nothing to review

### Stale Base Detection

Before reviewing content, check whether the branch includes unrelated changes from a stale base:

1. Run `git show <sha> --stat` for each commit on the branch to identify what the **actual commits** touch
2. Compare against `git diff main..HEAD --stat` — if the full diff includes files not in any commit, the branch has base divergence
3. If CI workflow files (`.github/`), `go.mod`/`go.sum`, or unrelated service files appear in the diff but not in the commits, flag it:

> **PROCESS: Stale base branch.** The diff includes files not modified by any commit on this branch (likely divergence from main). Rebase onto current main before review.

Only review files that appear in the actual commits, not the full diff.

### Stale-Base Regression Check

After detecting stale base files, check whether the PR's version of shared files would **silently revert** changes from recently merged PRs:

1. Get the last 10 merged PRs: `gh pr list --state merged -L 10 --json number,title,mergedAt`
2. For each file the PR modifies that was also modified by a recently merged PR, compare:
   - What the merged PR added to main
   - Whether the current PR's version of that file is missing those additions
3. Focus on high-risk files: `secret-auth.yaml`, `values.yaml`, `values-kind.yaml`, `values-secrets-sample.yaml`, `docker-compose.yml`, `go.mod`, `config.go`, `main.go`
4. If the PR would remove lines added by a recently merged PR, flag it as:

> **REGRESSION WARNING:** This PR's version of `<file>` is missing lines added by recently merged PR #Y (`<title>`). If merged as-is, those additions will be silently reverted. Cause: this branch was created before PR #Y merged (stale base). Fix: rebase onto current main.

This catches the class of bug where a PR with a stale base silently overwrites another PR's additions — e.g., PR #186 reverting PR #154's `SSH_KEY_ENCRYPTION_KEY` addition from `secret-auth.yaml` because the branch predated that merge.

## Pre-Commit Review

Focus on the specific files being changed. Run targeted checks:

- Read every changed file fully before reviewing (do not review code you have not read)
- Check that new code follows patterns already established in the same file/package
- Verify error handling is consistent with surrounding code
- Flag any TODOs, commented-out code, or debug prints that should not be committed
- Verify test files are updated if behavioral code changed
- Check for secrets, credentials, or sensitive data in the diff
- Scan all string literals, comments, error messages, and log messages for spelling mistakes and typos

## Pre-Merge Review (Full PR)

### Merge Conflict Check

Test whether the branch merges cleanly with main and compiles:

1. Run `git merge-tree main <branch>` to check for textual conflicts
2. If clean, note whether a semantic conflict is likely — check if the branch modifies files that were also recently changed on main (e.g., shared types, function signatures, Helm values)
3. If the branch touches `main.go`, config types, or shared packages, flag for post-merge build verification

### Review Agents

Always launch these 4 agents in parallel:

- **General code reviewer** — domain correctness, design, logging, cross-boundary, spelling
- **Silent failure hunter** — error handling, swallowed errors, inappropriate fallbacks
- **Test analyzer** — coverage gaps, missing edge cases, mock quality
- **Security reviewer** — authorization checks on all endpoints (especially mutating: POST, PATCH, DELETE), authentication bypass paths, error response leakage, secrets in logs or config

Conditionally launch these 2 additional agents:

- **Type design analyzer** — launch if the diff introduces new struct types, interfaces, or type aliases
- **Code simplifier** — launch if the diff adds more than 500 new lines of non-test code

Compile all agent findings into a single report.

### Suggested Verification

After the code review, suggest commands the reviewer can run locally:

- `make build-workspace` — verify compilation
- `make vet-workspace` — static analysis
- `make test-workspace` — unit tests
- `make run SERVICE=<service> TARGET=docker-test-e2e` — e2e tests for affected services

## Output Format

Organize findings as:

- **CRITICAL** — Must fix before merge. Security issues, data loss risks, authorization bypasses.
- **IMPORTANT** — Should fix before merge. Correctness issues, missing error handling.
- **SECURITY** — Authorization, authentication, secrets exposure, error leakage.
- **TEST COVERAGE GAPS**
- **DOCUMENTATION ISSUES**
- **SPELLING / TYPOS**
- **PROCESS** — Jira traceability, commit hygiene, stale base, merge conflicts
- **SUGGESTIONS**
- **STRENGTHS**

Every finding must have: category, description, file:line reference (where applicable).

### Review Verdict

Conclude with one of:

- **Approve** — No critical or important issues. Minor suggestions only.
- **Approve with comments** — No blockers, but important suggestions the author should consider.
- **Request changes** — Critical or important issues that must be addressed before merge. List the specific items that block approval.

Do not use emoji in the output.
Do not post review comments to GitHub without explicit user approval.

### Save Review

After presenting the review to the user and incorporating any feedback or edits:

1. Determine the PR number:
   - From `$ARGUMENTS` if a PR number was provided
   - Otherwise from `gh pr view --json number` on the current branch
   - If no PR exists, use the branch name as the filename
2. Write the final review to `out/PR/<PR_number>_PR.md` (create `out/PR/` if needed)
3. The file should contain the complete review formatted for direct copy-paste into a GitHub PR comment — no extra preamble or instructions, just the review content
