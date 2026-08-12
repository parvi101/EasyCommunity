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
| R-004 | Risk | Independent Antigravity UAT evidence is not bound to the governed EasyCommunity build/commit and may describe a different static prototype | **Open / High / Independent Challenge VETO for UAT #11-#19** | GitHub #20; Antigravity #11-#19; current `main` source-layout reconciliation |
| I-001 | Issue | Expired notices/events not handled truthfully | Closed | GitHub #2 |
| I-002 | Issue | SQL LIKE wildcard search defect | Closed | GitHub #3 |
| I-003 | Issue | Unbounded decision request text | Closed | GitHub #4 |
| I-004 | Issue | `Modified` backend/UI mismatch | Closed | GitHub #5 |
| I-005 | Issue | Antigravity UAT issues #11-#19 require exact artifact provenance and replay against the governed Flask controlled-MVP baseline before they can drive remediation/release decisions | Open | GitHub #20 |
| A-001 | Assumption | EasyCommunity remains a controlled MVP until production gates are passed | Active | BUILD_SCOPE_AND_LIMITATIONS.md |
| A-002 | Assumption | Seeded notices/events are demonstration/reference fixtures, not live civic intelligence | Active | config/seed_data.json |
| D-001 | Dependency | Production identity, authorisation and tenant isolation | Open | BUILD_SCOPE_AND_LIMITATIONS.md |
| D-002 | Dependency | Production backup/recovery and formal migration/rollback | Open | BUILD_SCOPE_AND_LIMITATIONS.md |
| D-003 | Dependency | Formal WCAG 2.2 AA and representative-user validation | Open | ACCESSIBILITY.md |
| D-004 | Dependency | HTTPS, secrets hardening, formal security testing and incident response | Open | SECURITY_PRIVACY.md |
| D-005 | Dependency | Production deployment architecture, observability and SLA evidence | Open | BUILD_SCOPE_AND_LIMITATIONS.md |
| D-006 | Dependency | Candidate-bound independent UAT evidence with exact version/path/hash or Git commit provenance | Open | GitHub #20 |

## Remediation Closure — 2026-08-12
- PR #10 merged to `main` as `d0d08ff59f4c63bee62c2104d364597bacafe207`.
- Python syntax PASS.
- JavaScript syntax PASS.
- Automated regression **11/11 PASS**.
- Defects #2–#7 and #9 closed as completed.
- Controlled MVP/Pilot/UAT was assessed as **PASS WITH SAFEGUARDS** for that governed candidate.
- Public production remains **NO-GO** until the open production dependencies above are evidenced and passed.

## Antigravity Independent-UAT Reconciliation — 2026-08-12
- Antigravity subsequently created issues #11–#19.
- Those issues cite a root-level static `index.html` / `app.js` implementation and identifiers/content not found in the current governed Flask `main` baseline.
- GitHub #20 therefore records a **High release-assurance provenance defect**.
- Issues #11–#19 are preserved as evidence but are **quarantined from release/remediation decisions** until the exact tested artifact is identified and each scenario is replayed against the intended governed candidate.
- This does **not** erase the earlier controlled-MVP validation result for `d0d08ff...`; it means the later Antigravity run cannot independently confirm or overturn that result because its tested baseline is currently unproven.
- Public production remains NO-GO regardless, because production identity/security, accessibility, backup/recovery, deployment and operational-readiness dependencies remain open.

## Governance Rules
- Every Council audit updates this register.
- GitHub issues remain the technical system of record; RAID references rather than duplicates defect detail.
- Closed risks/issues must be reopened if regression evidence demonstrates recurrence.
- High/Critical security, privacy, truthful-status, data-integrity or recovery failures can veto release regardless of score.
- Independent/local UAT must record the exact candidate version plus package/hash, filesystem path or Git commit before its findings can drive release remediation or closure.
- Do not change or remove previously working functionality based on evidence from an unbound prototype or local artifact.
