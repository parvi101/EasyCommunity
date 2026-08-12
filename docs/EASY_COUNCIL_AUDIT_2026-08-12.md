# EasyCommunity Easy Council Audit — 2026-08-12

**Scope:** v0.1.1 controlled MVP  
**Baseline commit:** `f1a02aedacbd9ec46062222ac84c9ae4b2a084cc`  
**Objective:** Apply the Project Phoenix / ParkEasy governance model without changing working functionality during the audit phase.

## Follow-up Audit Result — 2026-08-12 09:10 IST
The protected `main` baseline is unchanged from the initial Council audit. No application-code remediation has been merged, so defects #2–#7 remain open. The follow-up audit added one evidence-backed configuration/release defect, #9, for non-reproducible dependency resolution. No duplicate issues were created and no application code was changed.

## Council Verdict
**Pilot/UAT:** CONDITIONAL PASS  
**Public production:** NO-GO  
**Reason:** Existing controlled-MVP production gates remain open. High-severity truthful-status defect #6 remains unresolved, freshness defect #2 remains unresolved, mandatory test evidence is incomplete (#7), and release dependency resolution is not reproducible (#9).

## Defect Register
| Issue | Severity | Finding | Gate |
|---|---|---|---|
| #2 | Medium | Expired notices are not filtered/badged and may remain presented as Verified | Truthfulness / Freshness |
| #3 | Low | `%` and `_` are interpreted as SQL LIKE wildcards in listing search | Functional correctness |
| #4 | Low | Decision request reason has no server-side length limit | Security / Input validation |
| #5 | Low | `Modified` decision exists in backend but not admin UI | Workflow consistency |
| #6 | High | Health/data_state is unconditionally Live and can be misleading with stale/missing/offline cached data | Truthful status / Resilience |
| #7 | Medium | Mandatory test-plan groups are not represented by the four-test automated suite | Quality evidence / RTM |
| #9 | Medium | Runtime dependencies are lower-bound only and re-resolved at install time, so the validated executable environment can drift | Configuration integrity / Release reproducibility |

## Gate Assessment
| Gate | Status | Notes |
|---|---|---|
| Baseline integrity | PASS | `main` remains at `f1a02aed`; governance work isolated from application behavior |
| Core smoke evidence | PASS WITH LIMITS | Historical validation shows 4 automated tests and smoke evidence; no new remediation build exists |
| Requirements traceability | PARTIAL | Requirements register exists but test traceability is incomplete (#7) |
| Truthful live/stale state | FAIL | #2 and #6 remain open |
| Invalid/boundary input | FAIL/PARTIAL | #3 and #4 remain open; documented test group not fully covered |
| Decision/audit workflow | PARTIAL | Basic decision/audit path exists; #5 creates state-model mismatch and production identity remains pending |
| Security/privacy | NOT PRODUCTION READY | Security baseline explicitly excludes production authentication, TLS, rate limiting, formal penetration testing and related controls |
| Accessibility | NOT FORMALLY PASSED | Formal WCAG 2.2 AA, screen-reader and representative-user validation remain open |
| Resilience/recovery | NOT PASSED | Backup/recovery/migration evidence remains open; cached-health truthfulness risk exists (#6) |
| Configuration integrity | FAIL/PARTIAL | Source hashes exist, but dependency versions are not locked (#9) |
| Auditability | PARTIAL | Decision records and audit rows exist, but production actor identity/authorization is a documented future gate |
| Native mobile | NOT INCLUDED | Current controlled MVP is PWA only |
| Cost/operability | PARTIAL | Lightweight local architecture; no production observability/SLA evidence yet |
| Human impact | PARTIAL | Trusted-information positioning is positive, but stale/incorrect presentation can create real-world inconvenience |

## Evidence Consistency Review
- `docs/ARCHITECTURE.md` states that health states distinguish live and stale information, but current code does not substantiate that claim; #6 remains the controlling defect.
- `docs/ACCESSIBILITY.md` calls for clear live/stale labels; current freshness behavior is not sufficient because #2/#6 remain open.
- `docs/TEST_PLAN.md` defines broader mandatory coverage than the four automated tests currently provide; #7 remains the controlling evidence gap.
- `BUILD_MANIFEST.json` protects source-file integrity, but it does not lock the runtime dependency graph; #9 covers this separate reproducibility gap.
- `docs/SECURITY_PRIVACY.md` correctly states that production identity, TLS, rate limiting, secure sessions, formal testing and incident response remain future gates. This was not duplicated as a defect because the limitation is explicitly declared for the controlled MVP.

## Mandatory Remediation Sequence
1. Fix #6 truthful health/data-state behavior and cache/offline semantics.
2. Fix #2 notice expiry/freshness behavior.
3. Expand automated coverage and RTM for #7.
4. Establish reproducible release dependencies for #9 and record the validated versions.
5. Fix #3, #4 and #5 with focused regression tests.
6. Re-run syntax, API, negative, boundary, freshness, offline/recovery, PWA, install/reinstall and workflow regression.
7. Update validation report, release notes, requirements traceability, RAID and lessons learned.
8. Council re-vote on UAT/release readiness.

## Change Protection Rule
No existing working behavior is to be removed or rewritten solely to satisfy a defect. Each remediation must preserve unrelated working paths, carry focused tests, and be followed by regression evidence.
