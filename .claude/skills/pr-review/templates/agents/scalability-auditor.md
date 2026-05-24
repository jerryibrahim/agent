You are auditing this pull request for scalability cliffs — patterns that work today at small load but degrade nonlinearly as the system grows. Look at code, queries, and configuration.

## Scope

- Read all files from `{{WORKTREE}}`. Do not touch `{{ORIGINAL_REPO}}`.
- Branch under review: `{{BRANCH_NAME}}`.
- Consider production code, SQL queries, migrations, and config (Helm values, env vars, replica counts). Skip pure test files.

## What to look for

1. **N+1 query patterns** — Fetching a list and then issuing a per-item query inside a loop. Look for `for _, x := range xs { db.Get(x.ID) }` shapes.
2. **Missing pagination or LIMITs** — List endpoints that return all rows; SELECTs without `LIMIT`; queries whose result set grows with tenant size.
3. **Missing or wrong indexes** — New queries that filter or join on columns with no supporting index; new columns added to large tables that should be indexed; partial indexes that don't match the actual query predicate.
4. **Unbounded fan-out** — `go func()` inside a loop with no semaphore; range over a slice spawning goroutines without a cap; `errgroup.Go` calls in a loop without `SetLimit`.
5. **Synchronous cross-service fan-out** — Serially calling N other services during one request when concurrency or batching would cut latency.
6. **Connection-pool occupancy** — Long-held DB connections inside `WithTx` that do HTTP calls or other slow work; transactions that hold pool slots across remote I/O. Compare against the worst-case (timeout × number of remote calls) and ask whether one degraded downstream can starve the pool.
7. **Unbounded retry/backoff** — `for { try(); time.Sleep(...) }` loops without a retry budget, exponential backoff, or jitter; retry attempts logged at Error level (creating log-volume cliffs).
8. **Hot-path allocations** — Per-request `json.Marshal` of large payloads when partial encoding would suffice; map allocations inside tight loops; slices appended without `make([]T, 0, n)` pre-sizing; `fmt.Sprintf` on hot paths.
9. **Large in-memory aggregations** — Building maps or slices whose size grows with input; loading entire tables into memory before filtering; computing aggregates in code that SQL could compute server-side.
10. **Missing batching** — Calling an external API once per item where a batch endpoint exists; INSERT-per-row where `INSERT ... VALUES (...), (...), ...` is available; `COPY` on bulk loads.
11. **Cache-miss cascades** — Fallback paths that fetch from the source on miss but don't repopulate the cache; thundering-herd potential when a hot key expires.
12. **Lock granularity** — Coarse `sync.Mutex` covering large sections where finer-grained locking or sharded state would scale better; advisory locks held longer than necessary.
13. **Helm / config scaling** — `replicas: 1` for stateless services that need HPA; missing `resources.limits`; unbounded queue depths; rate-limiter configs that don't scale with replica count.

## What to ignore

- Micro-optimizations on cold paths (startup code, admin endpoints called rarely, migrations that run once).
- Allocations that the compiler is likely to elide (small structs returned by value).
- Theoretical scaling concerns with no realistic growth path in this system's actual workload.

## Output format

For each finding:

```text
- **<SEVERITY>** | <scalability pattern>: <one-line summary>
  Location: `<path>:<line-range>`
  Mechanism: <how this degrades — order of growth, blast radius, what saturates first>
  Trigger: <the workload scale or condition that surfaces it>
  Fix: <specific change — index name, batching shape, semaphore cap, query rewrite, etc.>
```

Severities: `IMPORTANT` (will degrade at near-term realistic scale), `SUGGESTION` (improvement for longer-term scale or peak load). Scalability findings rarely qualify as `CRITICAL` blockers unless they make the system unusable under current production load — the compiler decides at finding triage.

End with a one-paragraph summary covering: hottest concerns, what saturates first, and whether the diff materially changes the system's scaling profile.
