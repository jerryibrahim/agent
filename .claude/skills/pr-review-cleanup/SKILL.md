---
name: pr-review-cleanup
description: >-
  Remove worktrees created by the pr-review skill. Lists candidate worktrees
  (those alongside the main repo with names matching <repo>-pr-*), removes
  the one specified by argument, or asks before removing each. Refuses to
  remove worktrees with uncommitted changes unless --force.
argument-hint: "[PR number, branch name, path, --all, or --force]"
---

# PR Review Cleanup

Removes worktrees created by the `pr-review` skill. The pr-review skill leaves its worktree in place so you can rebase, fix up, or push follow-up changes; this skill is the explicit teardown step when you are done.

## Steps

1. Capture the original repo root: `ORIGINAL_REPO=$(git rev-parse --show-toplevel)`. If we are currently inside a pr-review worktree (path matches `*-pr-*` next to the parent repo), resolve `$ORIGINAL_REPO` to the main worktree using `git worktree list --porcelain` and pick the entry whose path is *not* a `-pr-*` sibling.
2. List candidate worktrees: `git -C "$ORIGINAL_REPO" worktree list --porcelain`. Filter to entries whose path is `<dirname($ORIGINAL_REPO)>/<basename($ORIGINAL_REPO)>-pr-*`. Exclude the main worktree (`$ORIGINAL_REPO` itself).
3. For each candidate, gather:
   - Path
   - Branch (or `(detached)`)
   - Last commit (`git -C <path> log -1 --format='%h %s'`)
   - Dirty flag (`git -C <path> status --porcelain` — non-empty means dirty)
   - Unpushed commits (`git -C <path> log @{u}.. --oneline 2>/dev/null` if upstream is set)
4. Resolve the target from `$ARGUMENTS`:
   - `--all` — every candidate.
   - A bare number — the worktree whose path ends in `-pr-<number>`.
   - A path — must match a registered worktree.
   - A branch name — the worktree currently checked out to that branch.
   - Empty — present the candidate list with the per-worktree info from step 3 and ask which to remove.
   - The literal flag `--force` may appear in addition to one of the above; it relaxes the dirty/unpushed checks.
5. For each target:
   - If dirty and `--force` was not passed, refuse and report the dirty files.
   - If there are unpushed commits and `--force` was not passed, refuse and list the unpushed commits.
   - Otherwise, run `git -C "$ORIGINAL_REPO" worktree remove "<path>"` (add `--force` only when the user explicitly passed `--force`).
6. After all removals, run `git -C "$ORIGINAL_REPO" worktree prune`.
7. Print the resulting `git -C "$ORIGINAL_REPO" worktree list` so the user can confirm.

## Safety

- Never `rm -rf` a directory; always use `git worktree remove`.
- Never pass `--force` to `git worktree remove` unless the user explicitly passed `--force` to this skill.
- Do not touch the main worktree (`$ORIGINAL_REPO`) under any circumstances.
- If a `-pr-*` directory exists but is not registered as a worktree (e.g., stray from a prior failure), do not remove it — surface the path and let the user investigate.
- If the user's current shell is inside a worktree that is about to be removed, warn them and ask them to `cd "$ORIGINAL_REPO"` first.
