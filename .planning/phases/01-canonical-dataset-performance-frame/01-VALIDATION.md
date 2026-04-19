---
phase: 01
slug: canonical-dataset-performance-frame
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-04-19
---

# Phase 01 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | none — Wave 0 installs |
| **Quick run command** | `python -m pytest tests/test_canonical_dataset.py tests/test_performance_frame.py tests/test_phase1_notebook_contract.py -q` |
| **Full suite command** | `python -m pytest -q` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run the task-specific pytest file plus the phase quick command before a notebook-only handoff.
- **After every plan wave:** Run `python -m pytest -q`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | DATA-01 | — | All 10 country CSVs are discovered and tagged with country metadata. | unit | `python -m pytest tests/test_canonical_dataset.py -q` | ❌ W0 | ⬜ pending |
| 01-01-02 | 01 | 1 | DATA-02 | — | Row-level parquet regeneration preserves normalized dates, booleans, and raw-plus-helper text fields. | integration | `python -m pytest tests/test_canonical_dataset.py -q && python -m youtube_trends.canonical_dataset` | ❌ W0 | ⬜ pending |
| 01-02-01 | 02 | 2 | DATA-03 | — | Video-country snapshot uses first-trending anchors and computes `trend_days_in_country_proxy`. | unit | `python -m pytest tests/test_performance_frame.py -q` | ❌ W0 | ⬜ pending |
| 01-02-02 | 02 | 2 | DATA-03 | — | Notebook documents the proxy, association framing, and missing-duration limitation. | integration | `python -m pytest tests/test_performance_frame.py tests/test_phase1_notebook_contract.py -q && python -m youtube_trends.performance_frame` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_canonical_dataset.py` — stubs for DATA-01 and DATA-02 parsing and normalization checks
- [ ] `tests/test_performance_frame.py` — stubs for DATA-03 anchor-row and proxy logic
- [ ] `tests/test_phase1_notebook_contract.py` — notebook contract checks for proxy documentation and limitations
- [ ] `requirements.txt` — includes `pytest`, `pandas`, `pyarrow`, and `pandera`

---

## Manual-Only Verifications

All phase behaviors have automated verification.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
