Analyze all open PRs and recommend a merge sequence that minimizes conflicts.

## Steps

### 1. Gather open PRs

```bash
gh pr list --state open --json number,title,headRefName,author,isDraft,createdAt,updatedAt,additions,deletions,changedFiles \
  --jq '.[] | select(.isDraft == false)'
```

Exclude draft PRs. Present a summary table:

| PR | Author | Title | Size (+/-) | Files |
|----|--------|-------|------------|-------|

### 2. Collect changed files per PR

For each non-draft PR, run:

```bash
gh pr diff <number> --name-only
```

Store the file list per PR for overlap analysis.

### 3. Identify file overlaps

Build an overlap matrix:
- For each pair of PRs, find files that appear in both diffs.
- Group overlapping PRs into clusters (e.g., "IAM contention", "config loader chain").
- Flag high-risk overlaps: shared types, `main.go`, `go.mod`, `docker-compose.yml`, Helm values, middleware, routes.

Present overlaps as:

```text
**<cluster name>:** #X, #Y, #Z all touch <files>
```

### 4. Detect dependency chains

Look for PRs that form a sequence:
- Same author, same package, incremental adoption pattern (e.g., shared config across services).
- PR descriptions or branch names referencing other PRs ("stacks on #X", "depends on #Y").
- File overlap where one PR creates a package and others consume it.

### 5. Stale-base regression check

For each open PR, check whether its diff would **revert** changes from recently merged PRs:

1. Get the last 10 merged PRs: `gh pr list --state merged -L 10 --json number,title,mergedAt`
2. For each open PR, compare its version of shared files against main:
   - For each file the PR touches, check if main's version has lines the PR's version removes
   - Focus on high-risk files: `secret-auth.yaml`, `values.yaml`, `values-kind.yaml`, `docker-compose.yml`, `go.mod`, shared types
3. If the PR's diff removes lines that were added by a recently merged PR, flag it:

```text
**REGRESSION WARNING:** PR #X removes lines from `<file>` that were added by recently merged PR #Y (<title>).
  - Line(s) at risk: <description of what would be lost>
  - Cause: PR #X was branched before PR #Y merged (stale base)
  - Fix: rebase PR #X onto current main
```

This catches the class of bug where a stale-base PR silently reverts another PR's additions during merge — the exact issue that caused `SSH_KEY_ENCRYPTION_KEY` to be dropped when PR #186 merged over PR #154's addition.

### 6. Recommend merge sequence

Organize PRs into waves:

```text
Wave 1 — Independent, no overlaps
  #N  description (reason: no file overlap with any other PR)

Wave 2 — <theme> (merge in order)
  #N  description (reason: depends on prior)
  #M  description (reason: ...)

Wave 3 — ...
```

**Sequencing rules:**
- PRs with zero file overlap go in Wave 1 (can merge in parallel).
- Dependency chains are ordered within the same wave.
- PRs touching the same service go after the foundational PR for that service lands.
- Cross-service PRs (touching 3+ services) go later to avoid broad conflicts.
- Large PRs (30+ files) go last unless they are foundational.
- Dependabot/CI-only PRs go in Wave 1.

**For each wave, explain:**
- Why these PRs are grouped together.
- What order within the wave matters (if any).
- What would conflict if merged out of order.

### 7. Save analysis

Write the analysis to `out/pr-analysis.md` with a timestamp at the top.

## Output format

```markdown
# PR Merge Sequence Analysis

**Date:** YYYY-MM-DD
**Open PRs:** N (M non-draft)

## Summary Table

| PR | Author | Title | Files | Overlaps with |
|----|--------|-------|-------|---------------|

## File Overlap Clusters

**<cluster>:** ...

## Recommended Merge Sequence

### Wave 1 — Independent
...

### Wave 2 — <theme>
...

## Stale-Base Regression Warnings

**REGRESSION WARNING:** PR #X removes lines from `<file>` that were added by recently merged PR #Y.
  - Line(s) at risk: ...
  - Cause: stale base
  - Fix: rebase onto main

## Risks

- <specific conflict risks if sequence is not followed>
```
