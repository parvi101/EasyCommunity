# EasyCommunity Council Performance Scorecard

**Purpose:** Measure whether the Easy Council is finding important problems early, producing reliable evidence, and improving the product without breaking working functionality.

| Metric | Definition | Target | Current 2026-08-12 |
|---|---|---|---|
| Requirement coverage | Requirements mapped to verified test/evidence | 100% for release scope | Needs improvement |
| Defect escape prevention | High/Critical defects found before production | 100% | PASS — production remains blocked |
| Truthfulness gate effectiveness | Misleading status/freshness claims detected and vetoed | 100% | PASS — #2/#6 identified |
| Duplicate-defect control | Existing issues reused instead of re-logged | 100% | PASS — #2–#5 preserved |
| Regression protection | Fixes include focused + broad regression evidence | 100% | Pending remediation cycle |
| Evidence quality | Release claims supported by reproducible evidence | 100% | PARTIAL — #7 |
| Working-function protection | Unrelated working behavior preserved | 100% | PASS in audit phase; no app code changed |
| RAID currency | Active material risks/issues/assumptions/dependencies represented | 100% | PASS — initial register established |
| Security/privacy gate | Production release blocked until mandatory controls pass | 100% | PASS — NO-GO retained |
| Accessibility gate | Formal production accessibility evidence present | 100% | Pending / production gate open |
| Resilience/recovery gate | Recovery, rollback and truthful degraded-state evidence | 100% | FAIL/Pending |
| Council action closure quality | Closed defects have fix + test + regression + traceability evidence | 100% | To be measured after fixes |

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
