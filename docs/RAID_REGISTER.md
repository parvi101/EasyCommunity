# EasyCommunity RAID Register

**Established:** 2026-08-12  
**Baseline:** v0.1.1 / `f1a02aed`  
**Owner:** Easy Council

| ID | Type | Description | Impact | Likelihood | Severity | Owner | Mitigation / Action | Status | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| R-001 | Risk | Health/data freshness can be reported as Live without validating freshness or data integrity | Users/admins may trust stale or incomplete information | High | High | Engineering + QA | Implement truthful service/data state, cache-safe offline handling, automated stale/recovery tests | Open | GitHub #6 |
| R-002 | Risk | Mandatory test-plan coverage is materially incomplete | Defects can escape while validation still appears green | High | High | QA | Build RTM-to-test coverage and gate releases on requirement coverage | Open | GitHub #7 |
| I-001 | Issue | Expired notices remain visible and can retain Verified presentation | Misleading community information | High | High | Engineering | Enforce effective dates and stale/expired presentation | Open | GitHub #2 |
| I-002 | Issue | LIKE wildcard characters are not escaped in listing search | Incorrect search results | Medium | Low | Engineering | Escape `%` and `_` and add tests | Open | GitHub #3 |
| I-003 | Issue | Decision request text is unbounded | Storage growth / basic DoS surface | Medium | Low | Engineering | Add server-side request limits | Open | GitHub #4 |
| I-004 | Issue | Backend supports `Modified` status without equivalent admin UI action | Inconsistent workflow/state reachability | Low | Low | Product + Engineering | Align backend state model and UI workflow | Open | GitHub #5 |
| A-001 | Assumption | v0.1.1 remains a controlled local MVP, not public production | Production controls may remain deferred only while this assumption holds | Medium | Medium | Product | Revalidate before any public/venue/cloud deployment | Active | BUILD_SCOPE_AND_LIMITATIONS.md |
| A-002 | Assumption | Seeded local notices/events are demonstration data | Demo data must never be interpreted as current live civic intelligence | High | High | Product + QA | Clearly mark demo fixtures and validate freshness semantics | Active | config/seed_data.json |
| D-001 | Dependency | Production identity, authorization and tenant isolation | Required before public production | High | High | Security + Architecture | Implement and independently test before production | Open | BUILD_SCOPE_AND_LIMITATIONS.md |
| D-002 | Dependency | Backup/recovery and formal migration/rollback capability | Required for resilient production operations | High | High | Architecture + Operations | Define RPO/RTO, backup restore test, migration/rollback evidence | Open | BUILD_SCOPE_AND_LIMITATIONS.md |

## Governance Rules
- Every Council audit updates this register.
- GitHub defects are the system of record for actionable defects; RAID references the issue rather than duplicating technical detail.
- High/Critical unresolved truthfulness, security, privacy, resilience, or data-integrity findings are release vetoes.
- Closing an item requires evidence, regression results, and an updated traceability record.
