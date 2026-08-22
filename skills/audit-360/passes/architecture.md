# Pass — Architecture / Structure

**Perimeter: STRUCTURAL / DESIGN problems only** — the *shape* of the code, not its runtime defects (code pass), not product behavior (product pass), not security, not ops (prod-readiness pass). **Verified-or-nothing still holds**: every finding cites `file:line` and a concrete consequence — never a taste judgement. A structural finding must name the cost it imposes ("this shallow module forces every caller to reassemble X"), not just "this feels wrong".

Read-only. Use the **deep-module** vocabulary: a module is **deep** when a lot of behavior sits behind a small **interface**, **shallow** when its interface is nearly as complex as its implementation. Depth is leverage at the interface, not lines of code.

Trace how modules depend on each other, then look for:

- **Shallow modules / pass-throughs**: interfaces nearly as complex as the implementation behind them; wrappers that add an interface without hiding complexity. Apply the **deletion test** — if deleting the module makes complexity vanish (rather than reappear across N callers), it earned nothing.
- **God objects / god functions**: one unit doing many unrelated things; a function that owns too much of a flow.
- **Coupling & cohesion**: **shotgun surgery** (one logical change forces scattered edits across many files) and **divergent change** (one file edited for several unrelated reasons) — name the hotspots and quantify the spread.
- **Missing or leaky seams**: places where behavior can't be swapped or tested without editing in place; a hard dependency created *inside* (`new StripeGateway()`) where it should be accepted as a parameter; business logic reachable only through I/O.
- **Layering violations**: a lower layer reaching into a higher one; a boundary that's documented but not enforced.
- **Primitive obsession at scale**: a domain concept passed as bare primitives/strings across many call sites instead of its own type.
- **Testability-blocking structure**: units that can't be exercised through their interface because dependencies are hard-wired or side effects are unavoidable.

Do NOT report **speculative generality / over-engineering / dead flexibility** here if `/ponytail-audit` is part of this run — that's its territory. Report it only when ponytail is not in the run.

Also list what is done **RIGHT** (verified): genuinely deep modules, clean seams, well-placed boundaries — so a future refactor doesn't break them.

Read thoroughly: {KEY FILES from context}, plus the entry points and the most-depended-on modules.

Output: follow the finding contract provided by the orchestrator. Each finding: the module/seam, `file:line`, the structural problem, and the **concrete cost** it imposes (leverage lost for callers, locality lost for maintainers, tests blocked). **End with cross-cutting structural root causes** (e.g. "no seam between domain and persistence anywhere in the codebase"). 10-20 findings, structure only.
