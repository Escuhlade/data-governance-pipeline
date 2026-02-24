# Changelog

All notable changes to this project will be documented in this file.

Format: `[version] — date — description`  
Types: `Added` `Changed` `Fixed` `Removed`

---

## [1.1.0] — 2026-02-24

### Added
- `docs/ROADMAP.md` — program roadmap across 3 phases with milestones and success criteria
- `docs/DECISION_LOG.md` — 6 architectural decisions with options considered and rationale
- `docs/RISK_REGISTER.md` — 6 identified risks with likelihood, impact, mitigation plans
- `docs/DATA_QUALITY_RULES.md` — formal governance documentation for all 6 DQ rules
- `docs/DATA_DICTIONARY.md` — full field definitions for all 36 columns in nyc311_clean
- `docs/ARCHITECTURE.md` — system design with Mermaid diagrams for pipeline flow and data lineage
- `docs/RUNBOOK.md` — operational guide with setup, run instructions, and troubleshooting
- `docs/CHANGELOG.md` — this file
- GitHub Issues backlog with 17 issues across 3 milestones
- GitHub Projects board with To Do / In Progress / Done columns
- README badges and capsule-render header

### Changed
- README updated with full program artifact table, DQ rules summary, and tech stack

---

## [1.0.0] — 2026-02-23

### Added
- Initial repository setup with full folder structure
- `pipeline/extract.py` — NYC 311 API ingestion with error handling and lineage logging
- `pipeline/transform.py` — cleaning, type fixes, and derived column generation
- `pipeline/dq_checks.py` — 6 DQ rules with PASS/FAIL/WARN severity tiers
- `pipeline/load.py` — SQLite persistence with lineage_log table
- `main.py` — full pipeline orchestration with CLI `--limit` argument
- `requirements.txt` — pandas, requests, python-dotenv
- `.gitignore` — Python and venv exclusions
- `.env.example` — environment variable template
- `reports/.gitkeep` — reports directory placeholder
- DQ report CSV export on every pipeline run

### Pipeline Results on First Run
- 5,000 rows extracted from NYC Open Data API in 1.90 seconds
- 44 raw columns → 36 clean columns after transform
- 6 DQ rules active — 1 FAIL, 2 WARN, 3 PASS
- 30 critical rows dropped, 4,970 clean rows loaded to SQLite
- Lineage tracking active on every run

---

## [Upcoming] — 1.2.0 — Target March 9, 2026

### Planned
- Docusaurus documentation site initialized
- All governance docs migrated to Docusaurus
- Mermaid diagrams rendered natively in docs site
- GitHub Actions workflow for automated deployment
- Site live at aaiyanvirji.github.io/data-governance-pipeline