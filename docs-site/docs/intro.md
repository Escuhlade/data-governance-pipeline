---
sidebar_position: 1
---

# Data Governance Pipeline

End-to-end ETL pipeline with embedded data quality validation framework built on the NYC 311 public dataset.

## What This Project Demonstrates

- **Pipeline Engineering** — modular ETL architecture with extract, transform, DQ validation, and load stages
- **Data Governance** — formal governance artifacts including DQ rules, data dictionary, lineage tracking, and metadata management
- **Program Management** — full TPM artifact suite including roadmap, risk register, decision log, gate checklists, and testing workbook
- **Documentation** — enterprise-grade documentation site with Mermaid system diagrams

## Quick Start
```bash
git clone https://github.com/Escuhlade/data-governance-pipeline.git
cd data-governance-pipeline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py --limit 5000
```

## Pipeline Results

| Metric | Value |
|--------|-------|
| Rows Extracted | 5,000 |
| Rows After DQ | 4,970 |
| Rows Dropped | 30 |
| DQ Rules Active | 6 |
| Pipeline Duration | 1.90 seconds |

## Project Status

| Phase | Status |
|-------|--------|
| Phase 1 — Pipeline Setup | ✅ Complete |
| Phase 2 — Governance Artifacts | ✅ Complete |
| Phase 3 — Docs Site & Deployment | 🔄 In Progress |
```

Save it. Now we need to add `sidebar_position` frontmatter to each of your docs so Docusaurus knows how to order them. Open each file and add this at the very top:

**ROADMAP.md** — add at top:
```
---
sidebar_position: 2
---
```

**DECISION_LOG.md:**
```
---
sidebar_position: 3
---
```

**RISK_REGISTER.md:**
```
---
sidebar_position: 4
---
```

**DATA_QUALITY_RULES.md:**
```
---
sidebar_position: 5
---
```

**DATA_DICTIONARY.md:**
```
---
sidebar_position: 6
---
```

**ARCHITECTURE.md:**
```
---
sidebar_position: 7
---
```

**RUNBOOK.md:**
```
---
sidebar_position: 8
---
```

**CHANGELOG.md:**
```
---
sidebar_position: 9
---
```

**GATE_CHECKLIST.md:**
```
---
sidebar_position: 10
---
```

**FUNCTIONAL_REQUIREMENTS.md:**
```
---
sidebar_position: 11
---
```

**TESTING_WORKBOOK.md:**
```
---
sidebar_position: 12
---