# Pass — Security

**Perimeter: SECURITY only.** Owner's own project; defensive review. Not code style, not product logic, not architecture, not prod-readiness — sibling passes cover those. Read-only. The stack + auth mechanism + secrets/crypto locations are provided by the orchestrator's context block.

Find real issues:

- **AuthZ**: IDOR / missing ownership checks — check EVERY route: does each verify the current user owns the resource? Report ALL confirmed gaps individually.
- **Auth tokens**: algorithm, expiry, secret handling (default/weak secret in config?), client-side storage (localStorage XSS exposure), refresh/revocation.
- **Secrets**: encryption-key management, defaults that "work", `.env` committed or live secrets on disk, hardcoded credentials (grep `password`/`secret`/`api_key`).
- **OAuth** (if any): state/CSRF, redirect URI validation, token storage at rest.
- **Injection**: raw SQL, subprocess with user-controlled input, SSRF via user-supplied URLs, path traversal on any file writes.
- **API hardening**: CORS wildcard + credentials, rate limiting on login/register, password policy, account enumeration, mass assignment, verbose error leakage.
- **Frontend**: XSS sinks (`dangerouslySetInnerHTML` / `v-html` / raw markdown of LLM or user content).

Also list what is done **RIGHT** (verified): authz that holds, crypto done well.

Output: follow the finding contract provided by the orchestrator. Ranked (critical/high/medium/low). For each: `file:line`, issue, concrete exploit scenario, short fix. **No generic advice without a code citation.** Verify any claimed ABSENCE by searching before asserting it. 10-25 findings.
