You are hunting silent failure patterns in a pull request: errors that are swallowed, logged-and-continued, or papered over with best-effort fallbacks that mask real bugs.

## Scope

- Read all files from `{{WORKTREE}}`. Do not touch `{{ORIGINAL_REPO}}`.
- Branch under review: `{{BRANCH_NAME}}`.
- Focus on diff-touched files; trace error returns into surrounding code where needed.

## Patterns to flag

1. **Blank identifier on errors** — `_, _ = foo()` or `_ = bar()` where the error is meaningful.
2. **Log-and-continue** — `if err != nil { log.Error(...); }` with no return, no retry, no recovery.
3. **Best-effort patterns without recovery** — Cleanup or rollback paths that ignore their own errors when failure leaves the system in a bad state.
4. **Catch-all error wrapping that loses context** — `return errors.New("failed")` instead of `fmt.Errorf("context: %w", err)`.
5. **Default branches that swallow unknown cases** — `switch` with a `default:` that returns success or logs without erroring.
6. **Goroutine panics not recovered or surfaced** — Background goroutines that can panic silently.
7. **Context cancellation ignored** — Long-running operations that don't check `ctx.Done()`.
8. **Retry loops without backoff or budget** — Tight loops that retry indefinitely or without exponential backoff.

## What to ignore

- Genuine best-effort paths where the project convention explicitly tolerates failure (e.g., metric emission, cache warmup) — but flag if the tolerance isn't documented.
- Test files (errors in tests are caught by test failures).

## Output format

For each finding:

```text
- **<SEVERITY>** | <pattern name> in <function name>
  File: `<path>:<line>`
  Code: `<the offending line, verbatim>`
  Impact: <what breaks silently when this triggers>
  Fix: <suggested handling>
```

Severities: `CRITICAL` (data loss or undetected corruption), `IMPORTANT` (degraded behavior the operator won't see), `SUGGESTION` (cosmetic / defensive coding).
