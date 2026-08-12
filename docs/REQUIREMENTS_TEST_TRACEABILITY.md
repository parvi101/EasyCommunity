# EasyCommunity Requirements-to-Test Traceability

Baseline remediation: 2026-08-12

| Test-plan group | Automated evidence | Status |
|---|---|---|
| Health and startup | `test_health_fresh_and_stale`, `test_health_unavailable_when_core_data_missing` | Covered |
| Core end-to-end journey | listings/search, notices/events, recommendations and PWA endpoint tests | Covered for controlled MVP APIs |
| Recommendation decision lifecycle | Modified/valid decision + audit and invalid-decision tests | Covered |
| Duplicate and invalid input handling | invalid decision, query length and request-size boundary tests; no create endpoint exists in current MVP so duplicate-create testing is N/A | Covered / N/A |
| Data consistency and audit creation | recommendation decision/audit test; health unavailable when core listings are missing | Covered |
| PWA manifest and service worker presence | PWA asset test | Covered |
| Handedness setting persistence | Implementation remains in `static/common.js`; browser persistence requires browser/UAT validation | Manual/UAT |
| Stale/live status behaviour | fresh, stale, unavailable and no-cached-API service-worker contract tests | Covered |
| Notice/event freshness | expired notice/event filtering plus legacy undated-event timing classification | Covered |
| Security/privacy hardening | Production authentication, authorisation, TLS, tenant isolation, penetration testing and incident response | Production gate - open |
| Accessibility hardening | Formal WCAG 2.2 AA, screen-reader and representative-user testing | Production gate - open |
| Backup/migration/rollback | Existing-schema event-column migration is exercised by startup logic; formal production backup/rollback remains required | Partial / production gate |
| Reproducible install | `requirements.lock.txt` + installer uses locked release dependencies | Covered for controlled release install |

## Release evidence rule
A passing automated test count must not be presented as proof that manual or production-only gates have passed. Release reports must show this traceability status alongside test results.
