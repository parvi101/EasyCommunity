# EasyCommunity RAID Register

**Established:** 2026-08-12  
**Original baseline:** v0.1.1 / `f1a02aed`  
**Remediated main:** `d0d08ff59f4c63bee62c2104d364597bacafe207`  
**Owner:** Easy Council

| ID | Type | Description | Status | Evidence |
|---|---|---|---|---|
| R-001 | Risk | Misleading health/data freshness state | Closed / mitigated | GitHub #6, PR #10, regression evidence |
| R-002 | Risk | Mandatory test-plan coverage incomplete | Closed / mitigated | GitHub #7, RTM, 11/11 regression |
| R-003 | Risk | Runtime dependency drift | Closed / mitigated | GitHub #9, `requirements.lock.txt` |
| I-001 | Issue | Expired notices/events not handled truthfully | Closed | GitHub #2 |
| I-002 | Issue | SQL LIKE wildcard search defect | Closed | GitHub #3 |
| I-003 | Issue | Unbounded decision request text | Closed | GitHub #4 |
| I-004 | Issue | `Modified` backend/UI mismatch | Closed | GitHub #5 |
| A-001 | Assumption | EasyCommunity remains a controlled MVP until production gates are passed | Active | BUILD_SCOPE_AND_LIMITATIONS.md |
| A-002 | Assumption | Seeded notices/events are demonstration/reference fixtures, not live civic intelligence | Active | config/seed_data.json |
| D-001 | Dependency | Production identity, authorisation and tenant isolation | Open | BUILD_SCOPE_AND_LIMITATIONS.md |
| D-002 | Dependency | Production backup/recovery and formal migration/rollback | Open | BUILD_SCOPE_AND_LIMITATIONS.md |
| D-003 | Dependency | Formal WCAG 2.2 AA and representative-user validation | Open | ACCESSIBILITY.md |
| D-004 | Dependency | HTTPS, secrets hardening, formal security testing and incident response | Open | SECURITY_PRIVACY.md |
| D-005 | Dependency | Production deployment architecture, observability and SLA evidence | Open | BUILD_SCOPE_AND_LIMITATIONS.md |

## Remediation Closure — 2026-08-12
- PR #10 merged to `main` as `d0d08ff59f4c63bee62c2104d364597bacafe207`.
- Python syntax PASS.
- JavaScript syntax PASS.
- Automated regression **11/11 PASS**.
- Defects #2–#7 and #9 closed as completed.
- Controlled MVP/Pilot/UAT is PASS WITH SAFEGUARDS.
- Public production remains NO-GO until the open production dependencies above are evidenced and passed.

## Governance Rules
- Every Council audit updates this register.
- GitHub issues remain the technical system of record; RAID references rather than duplicates defect detail.
- Closed risks/issues must be reopened if regression evidence demonstrates recurrence.
- High/Critical security, privacy, truthful-status, data-integrity or recovery failures can veto release regardless of score.
