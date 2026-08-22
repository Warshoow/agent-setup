# Pass — Code Quality

**Perimeter: CODE QUALITY / CORRECTNESS defects only.** Not security, not product logic, not architecture/structure, not prod-readiness — sibling passes cover those. If `/ponytail-audit` is being run alongside this audit, **over-engineering and dead code are its territory — do not report them here**. God-functions, significant duplication, and structural coupling belong to the **architecture** pass — flag structure there, not here.

Read-only. Do NOT modify anything. The stack + code map are provided by the orchestrator's context block.

Find CODE QUALITY problems only. Look for:

- **Real bugs**: race conditions, incorrect async usage (blocking calls in async routes, sync IO in the event loop), broken error handling, resource leaks (sessions/files/subprocesses), exception swallowing.
- **Data-access defects**: N+1 queries, unbounded queries (no pagination/limit), loading huge lists into memory, missing indexes vs actual query patterns.
- **Fragile runtime patterns**: mutable global state, thread-safety, ORM sessions shared across threads/tasks, missing transactions around multi-step writes.
- **Frontend**: broken hook deps, state races, missing fetch error handling.
- **Config/build**: unpinned deps, dead heavyweight deps, dev artifacts committed.
- **Dead code** — only if `/ponytail-audit` is NOT part of this run.

Read thoroughly: {KEY FILES from context}.

Output: follow the finding contract provided by the orchestrator. Ranked (high/medium/low). For each: severity, `file:line`, one-sentence defect, concrete failure scenario. **Only verified findings.** 10-20 findings max, skip naming/style nitpicks.
