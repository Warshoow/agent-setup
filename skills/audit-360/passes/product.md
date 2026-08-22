# Pass — Product / Feature Logic

**Perimeter: PRODUCT / FEATURE LOGIC only** — flaws in how features *behave*, not code style, not security, not architecture, not prod-readiness. This is the highest-value, least-standard pass: it reads the **flows end-to-end** (not files one by one) and hunts the gaps between intended and actual behavior.

Read-only. First read the product docs: {DOCS from context}. Known tracked issues (do NOT re-report): {KNOWN_ISSUES from context}.

Trace the actual flows end-to-end and look for:

- **State-machine holes**: every status enum — is every documented transition actually written somewhere? (grep each enum value for WRITES, not just reads). What happens on partial failure, retry, crash mid-flow, cancel, double-submit, two concurrent runs of the same flow?
- **Data consistency**: re-run behavior (duplicates? stale derived data? orphans?), deletes (cascades vs orphans), re-import/dedup, cache invalidation after mutations (check frontend query-invalidation against every mutation).
- **Failure economics**: what happens when an external dependency (API key, quota, network) fails mid-batch — is prior work lost, double-billed, stranded?
- **UX-logic mismatches**: are displayed counts/filters/labels computed from the same data the server uses, or from a capped/sorted page? Progress that lies.
- **Edge inputs**: empty collection, item with no content, huge collection, item shared across parents, falsy-but-valid params (`0`, `""`, `[]`).

Output: follow the finding contract provided by the orchestrator. Ranked. For each: the flow, `file:line` refs, concrete scenario, user impact. **End with cross-cutting root causes** shared by several findings. 10-20 findings, confirmed-by-code only.
