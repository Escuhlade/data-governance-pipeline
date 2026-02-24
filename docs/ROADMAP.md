# Roadmap

## Program Overview

**Project:** Data Governance Pipeline — NYC 311 Service Requests  
**Owner:** Aaiyan Virji  
**Start Date:** February 23, 2026  
**Target Completion:** March 9, 2026  

---

## Phase 1 — Pipeline Setup ✅
**Status:** Complete  
**Completed:** February 23, 2026  

### Milestones
| Milestone | Status | Completed |
|-----------|--------|-----------|
| Repository setup and folder structure | ✅ Done | Feb 23, 2026 |
| extract.py — NYC 311 API ingestion | ✅ Done | Feb 23, 2026 |
| transform.py — cleaning and type fixes | ✅ Done | Feb 23, 2026 |
| dq_checks.py — DQ validation framework | ✅ Done | Feb 23, 2026 |
| load.py — SQLite persistence | ✅ Done | Feb 23, 2026 |
| main.py — full pipeline orchestration | ✅ Done | Feb 23, 2026 |

### Success Criteria
- Pipeline runs end to end in a single command
- 5,000 rows extracted, transformed, validated, and loaded in under 5 seconds
- DQ report exported to reports/ on every run
- All Phase 1 GitHub Issues closed

### Results
- 5,000 rows processed in 1.90 seconds
- 6 DQ rules active — 1 FAIL, 2 WARN, 3 PASS on first run
- 30 critical rows dropped, 4,970 clean rows loaded to SQLite
- Lineage tracking active on every pipeline run

---

## Phase 2 — Governance Artifacts 🔄
**Status:** In Progress  
**Target Completion:** March 2, 2026  

### Milestones
| Milestone | Status | Target |
|-----------|--------|--------|
| ROADMAP.md | 🔄 In Progress | Mar 2, 2026 |
| DECISION_LOG.md | ⬜ Not Started | Mar 2, 2026 |
| RISK_REGISTER.md | ⬜ Not Started | Mar 2, 2026 |
| DATA_QUALITY_RULES.md | ⬜ Not Started | Mar 2, 2026 |
| DATA_DICTIONARY.md | ⬜ Not Started | Mar 2, 2026 |
| ARCHITECTURE.md | ⬜ Not Started | Mar 2, 2026 |
| RUNBOOK.md | ⬜ Not Started | Mar 2, 2026 |
| CHANGELOG.md | ⬜ Not Started | Mar 2, 2026 |

### Success Criteria
- All 8 governance artifacts complete and committed
- Each artifact follows enterprise documentation standards
- All Phase 2 GitHub Issues closed

---

## Phase 3 — Docs Site & Deployment ⬜
**Status:** Not Started  
**Target Completion:** March 9, 2026  

### Milestones
| Milestone | Status | Target |
|-----------|--------|--------|
| Docusaurus project initialized | ⬜ Not Started | Mar 9, 2026 |
| All docs migrated to Docusaurus | ⬜ Not Started | Mar 9, 2026 |
| Mermaid diagrams integrated | ⬜ Not Started | Mar 9, 2026 |
| GitHub Actions workflow configured | ⬜ Not Started | Mar 9, 2026 |
| Site live on GitHub Pages | ⬜ Not Started | Mar 9, 2026 |

### Success Criteria
- Docusaurus site live at aaiyanvirji.github.io/data-governance-pipeline
- All docs render correctly with Mermaid diagrams
- Auto-deploys on every push to main
- All Phase 3 GitHub Issues closed

---

## Overall Progress

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1 — Pipeline Setup | ✅ Complete | 6/6 milestones |
| Phase 2 — Governance Artifacts | 🔄 In Progress | 1/8 milestones |
| Phase 3 — Docs Site & Deployment | ⬜ Not Started | 0/5 milestones |