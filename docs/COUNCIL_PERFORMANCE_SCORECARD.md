# EasyCommunity Council Performance Scorecard

**Purpose:** Measure whether the Easy Council is finding important problems early, producing reliable evidence, and improving the product without breaking working functionality.

| Metric | Definition | Target | Current 2026-08-12 |
|---|---|---|---|
| Requirement coverage | Requirements mapped to verified test/evidence | 100% for release scope | Needs improvement — #7 |
| Defect escape prevention | High/Critical defects found before production | 100% | PASS — production remains blocked |
| Truthfulness gate effectiveness | Misleading status/freshness claims detected and vetoed | 100% | PASS — #2/#6 identified and veto retained |
| Duplicate-defect control | Existing issues reused instead of re-logged | 100% | PASS — #2–#7 preserved; #9 is distinct |
| Regression protection | Fixes include focused + broad regression evidence | 100% | Pending remediation cycle; no fixes merged yet |
| Evidence quality | Release claims supported by reproducible evidence | 100% | PARTIAL — #7 and #9 |
| Working-function protection | Unrelated working behavior preserved | 100% | PASS — audit changes remain governance-only |
| RAID currency | Active material risks/issues/assumptions/dependencies represented | 100% | PASS — follow-up register updated |
| Security/privacy gate | Production release blocked until mandatory controls pass | 100% | PASS — NO-GO retained |
| Accessibility gate | Formal production accessibility evidence present | 100% | Pending / production gate open |
| Resilience/recovery gate | Recovery, rollback and truthful degraded-state evidence | 100% | FAIL/Pending — #6 and open recovery dependency |
| Configuration integrity | Validated release environment is reproducible | 100% | FAIL/PARTIAL — #9 |
| Council action closure quality | Closed defects have fix + test + regression + traceability evidence | 100% | Not yet measurable — no audited fixes closed |

## Follow-up Council Performance Assessment
**Detection/governance performance:** STRONG WITH EVIDENCE GAPS. The Council has correctly kept production blocked, preserved existing issues instead of duplicating them, protected the stable application baseline during governance work, and identified an additional configuration-integrity gap (#9). However, overall assurance remains constrained by incomplete requirement-to-test evidence (#7), unresolved truthful-status behavior (#6), and the absence of a completed remediation/closure cycle from which regression and closure quality can be measured.

A numeric Council score is intentionally **not** claimed yet. The scoring model includes regression and closure-quality dimensions that cannot be measured honestly until at least one remediation cycle completes. This prevents a misleading high score based only on defect discovery.

## Scoring Model
Each completed audit cycle is scored out of 100:
- Requirements and traceability: 15
- Functional correctness and regression: 20
- Truthfulness/data integrity: 15
- Security/privacy: 10
- Accessibility/human impact: 10
- Resilience/recovery: 10
- Evidence/release governance: 10
- RAID/decision hygiene: 5
- Cost/operability: 5

A score does **not** override veto gates. Any unresolved Critical defect, or High defect affecting security, privacy, truthful status, data integrity, or safe recovery, can block release regardless of total score.

## Anti-Gaming Rules
- Test count alone is not a quality metric; requirement and risk coverage matter.
- A PASS without reproducible evidence scores zero for that evidence item.
- Reopening a falsely closed defect reduces closure-quality score.
- Finding defects early is positive; hiding or downgrading them to improve the score is prohibited.
- Do not publish a numeric Council score when material scoring dimensions have no evidence yet; mark them unmeasured instead.
