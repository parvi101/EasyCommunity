# EasyCommunity Remediation Validation — 2026-08-12

Remediation branch: `fix/easycommunity-audit-defects-2026-08-12`
Baseline: `main` at `f1a02aed`

## Validation executed
- `python -m py_compile app.py` — PASS
- `node --check static/community.js` — PASS
- `node --check static/community_admin.js` — PASS
- `node --check static/sw.js` — PASS
- `pytest -q` — **11 passed**

## Defect coverage
- #2: expired notices and dated events are filtered; legacy undated events are explicitly marked `timing-unverified` rather than presented as current.
- #3: SQL LIKE wildcard characters `%` and `_` are escaped for literal search.
- #4: request/query size boundaries are enforced server-side.
- #5: `Modified` is exposed in the admin workflow.
- #6: service status and data freshness are separated; stale/unavailable data is reported truthfully; API responses are not served from the PWA cache.
- #7: automated regression coverage expanded from 4 to 11 tests and requirements-to-test traceability added; manual/production-only gates remain explicitly separate.
- #9: release dependencies are locked and the Windows installer consumes the lock rather than resolving open-ended versions and upgrading pip each run.

## Protection of working functionality
The existing product workflows, routes, listing data, recommendation decisions, audit creation, PWA installation assets, and single-hand preference implementation were retained. Schema change for event timing is additive and includes migration of existing databases.

## Gates intentionally still open
This remediation does **not** claim public-production readiness. Production identity/authorisation, HTTPS/secrets hardening, formal security testing, WCAG 2.2 AA representative-user validation, production backup/rollback, deployment architecture and related production gates remain open.
