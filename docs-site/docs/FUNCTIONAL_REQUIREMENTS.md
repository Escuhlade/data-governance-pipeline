# Functional Requirements

## Overview
This document defines the functional requirements for the Data Governance Pipeline. Requirements are organized by component and assigned a unique ID, priority, and acceptance criteria.

**Priority Legend**
| Priority | Meaning |
|----------|---------|
| P1 | Must have — pipeline cannot function without this |
| P2 | Should have — core governance value |
| P3 | Nice to have — enhances usability |

**Status Legend**
| Status | Meaning |
|--------|---------|
| ✅ Implemented | Requirement is fully implemented and verified |
| 🔄 In Progress | Requirement is partially implemented |
| ⬜ Not Started | Requirement is planned but not yet implemented |

---

## FR-001 — Data Extraction

### FR-001.1 — API Ingestion
| Attribute | Detail |
|-----------|--------|
| Priority | P1 |
| Status | ✅ Implemented |
| Component | extract.py |
| Description | The pipeline must pull NYC 311 service request data from the NYC Open Data API |
| Acceptance Criteria | extract_nyc_311() returns a populated pandas DataFrame with 44 columns |

### FR-001.2 — Configurable Row Limit
| Attribute | Detail |
|-----------|--------|
| Priority | P1 |
| Status | ✅ Implemented |
| Component | extract.py, main.py |
| Description | The pipeline must accept a configurable row limit via CLI argument |
| Acceptance Criteria | `python main.py --limit 5000` pulls exactly 5,000 rows |

### FR-001.3 — Error Handling
| Attribute | Detail |
|-----------|--------|
| Priority | P1 |
| Status | ✅ Implemented |
| Component | extract.py |
| Description | The pipeline must handle API connection failures, timeouts, and HTTP errors gracefully |
| Acceptance Criteria | Connection errors, timeouts, and HTTP errors raise descriptive exceptions and log error messages |

### FR-001.4 — Extraction Lineage Logging
| Attribute | Detail |
|-----------|--------|
| Priority | P2 |
| Status | ✅ Implemented |
| Component | extract.py |
| Description | Every extraction must log metadata including timestamp, source URL, row count, and column names |
| Acceptance Criteria | Lineage metadata appears in logs on every extraction run |

---

## FR-002 — Data Transformation

### FR-002.1 — Column Pruning
| Attribute | Detail |
|-----------|--------|
| Priority | P1 |
| Status | ✅ Implemented |
| Component | transform.py |
| Description | Columns with 90%+ null rate must be dropped from the dataset |
| Acceptance Criteria | Output DataFrame has 36 columns, down from 44 raw columns |

### FR-002.2 — Date Parsing
| Attribute | Detail |
|-----------|--------|
| Priority | P1 |
| Status | ✅ Implemented |
| Component | transform.py |
| Description | Date string columns must be converted to datetime objects |
| Acceptance Criteria | created_date, closed_date, resolution_action_updated_date are datetime64 dtype |

### FR-002.3 — Data Type Fixes
| Attribute | Detail |
|-----------|--------|
| Priority | P1 |
| Status | ✅ Implemented |
| Component | transform.py |
| Description | Incorrectly typed columns must be cast to their correct types |
| Acceptance Criteria | incident_zip is zero-padded string, council_district is Int64 |

### FR-002.4 — String Standardization
| Attribute | Detail |
|-----------|--------|
| Priority | P2 |
| Status | ✅ Implemented |
| Component | transform.py |
| Description | String columns must be stripped of whitespace and key categorical fields must be title-cased |
| Acceptance Criteria | borough, city, complaint_type, status are consistently title-cased |

### FR-002.5 — Derived Column Generation
| Attribute | Detail |
|-----------|--------|
| Priority | P2 |
| Status | ✅ Implemented |
| Component | transform.py |
| Description | The pipeline must generate derived columns to support governance reporting |
| Acceptance Criteria | resolution_hours, is_open, created_year, created_month are present in output DataFrame |

---

## FR-003 — Data Quality Validation

### FR-003.1 — DQ Rule Execution
| Attribute | Detail |
|-----------|--------|
| Priority | P1 |
| Status | ✅ Implemented |
| Component | dq_checks.py |
| Description | The pipeline must run all 6 DQ rules against the transformed DataFrame on every run |
| Acceptance Criteria | All 6 rules execute and return a result on every pipeline run |

### FR-003.2 — Severity Tiering
| Attribute | Detail |
|-----------|--------|
| Priority | P1 |
| Status | ✅ Implemented |
| Component | dq_checks.py |
| Description | DQ rules must be classified as critical (FAIL) or non-critical (WARN) |
| Acceptance Criteria | Critical violations drop rows, non-critical violations flag rows but retain them |

### FR-003.3 — DQ Report Generation
| Attribute | Detail |
|-----------|--------|
| Priority | P1 |
| Status | ✅ Implemented |
| Component | dq_checks.py, main.py |
| Description | A structured DQ report must be generated on every pipeline run |
| Acceptance Criteria | DQ report DataFrame contains rule_id, rule_name, violations, violation_pct, status, critical columns |

### FR-003.4 — DQ Report Export
| Attribute | Detail |
|-----------|--------|
| Priority | P2 |
| Status | ✅ Implemented |
| Component | main.py |
| Description | DQ report must be exported as a timestamped CSV to reports/ on every run |
| Acceptance Criteria | reports/dq_report_TIMESTAMP.csv is created after every successful pipeline run |

---

## FR-004 — Data Loading

### FR-004.1 — SQLite Persistence
| Attribute | Detail |
|-----------|--------|
| Priority | P1 |
| Status | ✅ Implemented |
| Component | load.py |
| Description | Clean DataFrame must be persisted to SQLite database |
| Acceptance Criteria | nyc311_clean table exists in reports/nyc311.db with correct row count after every run |

### FR-004.2 — Load Verification
| Attribute | Detail |
|-----------|--------|
| Priority | P1 |
| Status | ✅ Implemented |
| Component | load.py |
| Description | Row count must be verified after every load operation |
| Acceptance Criteria | Logged row count matches DataFrame length after load |

### FR-004.3 — Lineage Log
| Attribute | Detail |
|-----------|--------|
| Priority | P2 |
| Status | ✅ Implemented |
| Component | load.py |
| Description | Load metadata must be written to a lineage_log table on every run |
| Acceptance Criteria | lineage_log table contains table_name, rows_loaded, columns_loaded, loaded_at, source after every run |

### FR-004.4 — Query Helper
| Attribute | Detail |
|-----------|--------|
| Priority | P3 |
| Status | ✅ Implemented |
| Component | load.py |
| Description | A query helper function must allow SQL queries against the SQLite database |
| Acceptance Criteria | query("SELECT ...") returns a pandas DataFrame |

---

## FR-005 — Pipeline Orchestration

### FR-005.1 — Single Command Execution
| Attribute | Detail |
|-----------|--------|
| Priority | P1 |
| Status | ✅ Implemented |
| Component | main.py |
| Description | The full pipeline must be executable in a single command |
| Acceptance Criteria | `python main.py` runs extract → transform → dq_checks → load successfully |

### FR-005.2 — Pipeline Summary Logging
| Attribute | Detail |
|-----------|--------|
| Priority | P2 |
| Status | ✅ Implemented |
| Component | main.py |
| Description | A summary must be logged at the end of every pipeline run |
| Acceptance Criteria | Summary includes duration, rows extracted, rows after DQ, rows dropped, DQ rule results |

---

## FR-006 — Documentation Site

### FR-006.1 — Docusaurus Site
| Attribute | Detail |
|-----------|--------|
| Priority | P2 |
| Status | ⬜ Not Started |
| Component | Docusaurus |
| Description | All governance artifacts must be accessible via a polished documentation site |
| Acceptance Criteria | Site live at aaiyanvirji.github.io/data-governance-pipeline |

### FR-006.2 — Mermaid Diagram Rendering
| Attribute | Detail |
|-----------|--------|
| Priority | P2 |
| Status | ⬜ Not Started |
| Component | Docusaurus |
| Description | Mermaid diagrams in ARCHITECTURE.md must render natively in the docs site |
| Acceptance Criteria | All 3 Mermaid diagrams render correctly on the Architecture page |

### FR-006.3 — Auto Deployment
| Attribute | Detail |
|-----------|--------|
| Priority | P2 |
| Status | ⬜ Not Started |
| Component | GitHub Actions |
| Description | The docs site must auto-deploy on every push to main |
| Acceptance Criteria | GitHub Actions workflow builds and deploys Docusaurus on every push to main |

---

## Requirements Summary

| Req ID | Description | Priority | Status |
|--------|-------------|----------|--------|
| FR-001.1 | API Ingestion | P1 | ✅ Implemented |
| FR-001.2 | Configurable Row Limit | P1 | ✅ Implemented |
| FR-001.3 | Error Handling | P1 | ✅ Implemented |
| FR-001.4 | Extraction Lineage Logging | P2 | ✅ Implemented |
| FR-002.1 | Column Pruning | P1 | ✅ Implemented |
| FR-002.2 | Date Parsing | P1 | ✅ Implemented |
| FR-002.3 | Data Type Fixes | P1 | ✅ Implemented |
| FR-002.4 | String Standardization | P2 | ✅ Implemented |
| FR-002.5 | Derived Column Generation | P2 | ✅ Implemented |
| FR-003.1 | DQ Rule Execution | P1 | ✅ Implemented |
| FR-003.2 | Severity Tiering | P1 | ✅ Implemented |
| FR-003.3 | DQ Report Generation | P1 | ✅ Implemented |
| FR-003.4 | DQ Report Export | P2 | ✅ Implemented |
| FR-004.1 | SQLite Persistence | P1 | ✅ Implemented |
| FR-004.2 | Load Verification | P1 | ✅ Implemented |
| FR-004.3 | Lineage Log | P2 | ✅ Implemented |
| FR-004.4 | Query Helper | P3 | ✅ Implemented |
| FR-005.1 | Single Command Execution | P1 | ✅ Implemented |
| FR-005.2 | Pipeline Summary Logging | P2 | ✅ Implemented |
| FR-006.1 | Docusaurus Site | P2 | ⬜ Not Started |
| FR-006.2 | Mermaid Diagram Rendering | P2 | ⬜ Not Started |
| FR-006.3 | Auto Deployment | P2 | ⬜ Not Started |