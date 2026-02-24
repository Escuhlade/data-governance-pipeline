---
sidebar_position: 3
---
# Decision Log

## Overview
This log documents all key architectural and program decisions made during delivery of the Data Governance Pipeline. Each entry includes the options considered, the decision made, rationale, and tradeoffs accepted.

---

## DEC-001 — Dataset Selection
**Date:** February 23, 2026  
**Status:** Closed  

### Context
Needed a public dataset that would realistically demonstrate data governance challenges — schema inconsistencies, null values, data quality issues, and lineage tracking requirements.

### Options Considered
| Option | Pros | Cons |
|--------|------|------|
| NYC 311 Service Requests | Large, messy, real quality issues, well known, free API | No financial domain context |
| Kaggle financial dataset | Closer to banking domain | Static file, no live API, requires download |
| OSFI public data | Directly relevant to CIBC experience | Limited dataset size, less interesting quality issues |

### Decision
**NYC 311 Service Requests** via NYC Open Data API.

### Rationale
NYC 311 is large enough to surface real DQ issues at scale, has a live API endpoint making the pipeline dynamic, and is well known enough that any interviewer can immediately understand the domain without explanation.

### Tradeoffs Accepted
Less domain-specific to financial services. Mitigated by the governance framework which mirrors enterprise banking practices regardless of dataset.

---

## DEC-002 — API vs Static CSV
**Date:** February 23, 2026  
**Status:** Closed  

### Context
Needed to decide whether to pull data dynamically from the NYC Open Data API or download a static CSV file and include it in the repo.

### Options Considered
| Option | Pros | Cons |
|--------|------|------|
| Live API pull | Dynamic, no large files in repo, always fresh data | API could change schema, requires internet |
| Static CSV | No dependency on external API, predictable schema | Large file in repo, not a real pipeline pattern |

### Decision
**Live API pull** via requests library with configurable row limit.

### Rationale
A real ETL pipeline pulls from a live source. Static CSV would undermine the point of building a pipeline. The `--limit` flag makes it flexible enough to test at small scale or run at full scale.

### Tradeoffs Accepted
Schema changes in the source API could break the pipeline. Mitigated by try/catch error handling in extract.py and tracked as R-001 in the Risk Register.

---

## DEC-003 — SQLite vs PostgreSQL
**Date:** February 23, 2026  
**Status:** Closed  

### Context
Needed a storage layer for the clean dataframe output. Evaluated SQLite vs PostgreSQL.

### Options Considered
| Option | Pros | Cons |
|--------|------|------|
| SQLite | Zero setup, file-based, built into Python, portable | Not suitable for concurrent writes or production scale |
| PostgreSQL | Production grade, concurrent access, advanced features | Requires server setup, credentials, extra dependencies |

### Decision
**SQLite** stored in reports/nyc311.db.

### Rationale
This is a portfolio project where the goal is demonstrating governance thinking not infrastructure complexity. SQLite means anyone can clone the repo and run the pipeline instantly with no setup. PostgreSQL would add friction with zero benefit at this scale.

### Tradeoffs Accepted
Not suitable for concurrent access or production scale. Acceptable given this is a single-user portfolio project. If this were productionized, PostgreSQL or a cloud data warehouse would be the appropriate choice.

---

## DEC-004 — Modular Pipeline Architecture
**Date:** February 23, 2026  
**Status:** Closed  

### Context
Needed to decide whether to write the pipeline as a single script or split it into separate modules.

### Options Considered
| Option | Pros | Cons |
|--------|------|------|
| Single script | Simpler, fewer files | Hard to test, maintain, or extend individual steps |
| Modular (extract/transform/dq/load) | Clean separation of concerns, testable, extensible | More files to manage |

### Decision
**Modular architecture** — separate files for extract, transform, dq_checks, and load, orchestrated by main.py.

### Rationale
Mirrors real enterprise pipeline patterns. Each module has a single responsibility, making it easy to swap out components (e.g. replace SQLite with Postgres in load.py without touching anything else). Also makes the codebase readable for anyone reviewing it.

### Tradeoffs Accepted
More files to manage. Acceptable given the clarity and maintainability benefits.

---

## DEC-005 — DQ Rule Severity Levels
**Date:** February 23, 2026  
**Status:** Closed  

### Context
Needed to decide how to handle DQ rule violations — drop all failing rows vs flag and continue vs tiered severity.

### Options Considered
| Option | Pros | Cons |
|--------|------|------|
| Drop all violations | Simple, clean output | Too aggressive, loses valid data |
| Flag and keep all | No data loss | Pollutes clean dataset with known bad data |
| Tiered (FAIL/WARN/PASS) | Nuanced, mirrors enterprise governance | More complex to implement |

### Decision
**Tiered severity** — FAIL drops rows (critical rules), WARN flags but keeps rows (non-critical rules), PASS is clean.

### Rationale
Mirrors how real data governance frameworks operate. Critical violations (null descriptors, duplicate keys, coordinate mismatches) should never reach downstream systems. Non-critical issues (zip code format, missing resolution descriptions) are flagged for visibility without losing otherwise valid records.

### Tradeoffs Accepted
More complex logic in dq_checks.py. Acceptable given the governance value of preserving non-critical data while still surfacing issues.

---

## DEC-006 — Docusaurus for Documentation Site
**Date:** February 23, 2026  
**Status:** Closed  

### Context
Needed a way to present governance artifacts in a polished, professional format beyond raw GitHub markdown.

### Options Considered
| Option | Pros | Cons |
|--------|------|------|
| Raw GitHub markdown | Zero setup | Plain, no navigation, no diagrams |
| Docusaurus + GitHub Pages | Professional UI, free hosting, Mermaid support, auto-deploy | Initial setup required |
| Notion or Confluence | Familiar enterprise tools | External dependency, not tied to repo |

### Decision
**Docusaurus hosted on GitHub Pages** via GitHub Actions CI/CD.

### Rationale
Keeps everything in the GitHub ecosystem, deploys automatically on every push, supports Mermaid diagrams natively, and produces a professional documentation site that mirrors what real tech companies use. Free with no external dependencies.

### Tradeoffs Accepted
Initial setup effort for Docusaurus config and GitHub Actions workflow. One-time cost with long-term benefit.