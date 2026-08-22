# Pass — SaaS / Prod-Readiness

**Perimeter: OPERATIONAL / BUSINESS readiness only** — what is missing or wrong to run this as a paid multi-tenant product. Not code style, not classic vulns (security pass), not product logic, not architecture — sibling passes cover those. Read-only.

Check concretely (cite files, and **verify ABSENCE by searching before claiming it**):

- **Multi-tenancy**: per-user quotas/limits, fairness on shared workers/queues, one tenant starving others.
- **Billing**: plans/subscriptions/metering; is the per-user cost of expensive operations (LLM, external APIs) tracked at all? Does any code path silently spend the **OPERATOR's** credentials on behalf of users?
- **Identity lifecycle**: email verification, password reset, transactional email, account deletion, session model fit for consumers.
- **Ops**: structured logging, metrics/tracing/error reporting, health/readiness probes that actually check dependencies, graceful shutdown, DB pooling, migration strategy on deploy (vs `create_all`), backup/restore story.
- **Deployment**: prod Dockerfile/manifests vs dev-only, CI/CD, secrets management, per-env config, proxy/timeout assumptions vs long-running requests.
- **Scalability**: in-process ML models per replica, local-disk storage vs object storage, single points of failure (one Redis, one worker), work done inside HTTP requests that belongs in a queue.
- **Legal**: third-party ToS exposure (scraping vs official APIs), GDPR (export/delete), ToS/privacy pages, OAuth-provider verification requirements.
- **Product ops**: admin/support tooling, runtime feature flags, per-tenant config.

Output: follow the finding contract provided by the orchestrator. Return 15-25 gaps, **tiered**: Tier 1 launch blockers / Tier 2 will break in operation / Tier 3 legal & product ops. For each: evidence (file, or "absent — verified by searching X") and why it blocks a launch.
