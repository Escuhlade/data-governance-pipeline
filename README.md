<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=0f6fff&height=200&section=header&text=Data%20Governance%20Pipeline&fontSize=36&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=End-to-end%20ETL%20with%20embedded%20DQ%20validation%20framework&descAlignY=55&descColor=ffffff)

![Pipeline Status](https://img.shields.io/badge/pipeline-passing-brightgreen)
![Phase](https://img.shields.io/badge/phase-2%20of%203-blue)
![Python](https://img.shields.io/badge/python-3.11.5-blue)

📚 **[View Full Documentation →](https://aaiyanvirji.github.io/data-governance-pipeline)**

</div>

---

## Overview

End-to-end data governance pipeline with embedded DQ validation framework — ETL, lineage tracking, and governance artifacts for the NYC 311 public dataset.

## Quick Start
```bash
# Clone the repo
git clone https://github.com/Escuhlade/data-governance-pipeline.git
cd data-governance-pipeline

# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python main.py --limit 5000
```

## Pipeline Architecture
```
NYC 311 API → extract.py → transform.py → dq_checks.py → SQLite → DQ Report
```

## Program Artifacts

| Artifact | Description |
|----------|-------------|
| [ROADMAP.md](docs/ROADMAP.md) | Phases, milestones, delivery timeline |
| [RISK_REGISTER.md](docs/RISK_REGISTER.md) | Identified risks and mitigations |
| [DECISION_LOG.md](docs/DECISION_LOG.md) | Key tradeoffs and decisions made |
| [DATA_QUALITY_RULES.md](docs/DATA_QUALITY_RULES.md) | Governance framework documentation |
| [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) | Field definitions and metadata |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design and component breakdown |
| [RUNBOOK.md](docs/RUNBOOK.md) | Operational guide and troubleshooting |
| [CHANGELOG.md](docs/CHANGELOG.md) | Version history |

## DQ Rules Summary

| Rule ID | Rule | Critical | Status |
|---------|------|----------|--------|
| DQ-001 | Descriptor Not Null | ✅ Yes | Active |
| DQ-002 | Zip Code Format | ⚠️ No | Active |
| DQ-003 | Coordinate Completeness | ✅ Yes | Active |
| DQ-004 | Open/Closed Flag Consistency | ✅ Yes | Active |
| DQ-005 | Unique Key Integrity | ✅ Yes | Active |
| DQ-006 | Resolution Description Consistency | ⚠️ No | Active |

## Tech Stack

- **Language:** Python 3.11.5
- **Data:** pandas, requests
- **Storage:** SQLite
- **Docs:** Docusaurus + GitHub Pages
- **CI/CD:** GitHub Actions
