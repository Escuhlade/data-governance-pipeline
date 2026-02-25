---
sidebar_position: 12
---
# Testing Workbook

## Overview
This document records all manual verification tests performed on the Data Governance Pipeline. Each test is assigned a unique ID, expected result, actual result, and pass/fail status.

**Test Status Legend**
| Status | Meaning |
|--------|---------|
| ✅ Pass | Test executed and actual result matches expected result |
| ❌ Fail | Test executed and actual result does not match expected result |
| ⬜ Not Run | Test has not been executed yet |

---

## Section 1 — Extraction Tests

### T-001 — API Connection
| Attribute | Detail |
|-----------|--------|
| Test ID | T-001 |
| Component | extract.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify pipeline connects to NYC Open Data API successfully |
| Steps | Run `python pipeline/extract.py` |
| Expected Result | API returns 200 OK, DataFrame populated with 1,000 rows and 44 columns |
| Actual Result | API returned 200 OK, 1,000 rows, 44 columns confirmed |
| Status | ✅ Pass |

---

### T-002 — Configurable Row Limit
| Attribute | Detail |
|-----------|--------|
| Test ID | T-002 |
| Component | extract.py, main.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify `--limit` CLI argument controls number of rows pulled |
| Steps | Run `python main.py --limit 5000` |
| Expected Result | Pipeline pulls exactly 5,000 rows |
| Actual Result | 5,000 rows extracted confirmed in logs |
| Status | ✅ Pass |

---

### T-003 — Lineage Metadata Logging
| Attribute | Detail |
|-----------|--------|
| Test ID | T-003 |
| Component | extract.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify extraction logs lineage metadata on every run |
| Steps | Run `python pipeline/extract.py` and inspect logs |
| Expected Result | Logs contain timestamp, source URL, rows_fetched, columns, column_names |
| Actual Result | Lineage metadata confirmed in logs on every run |
| Status | ✅ Pass |

---

### T-004 — Schema Detection
| Attribute | Detail |
|-----------|--------|
| Test ID | T-004 |
| Component | extract.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify all 44 source columns are detected and logged |
| Steps | Run `python pipeline/extract.py` and check column list in logs |
| Expected Result | All 44 column names logged correctly |
| Actual Result | All 44 columns detected and logged |
| Status | ✅ Pass |

---

## Section 2 — Transformation Tests

### T-005 — Column Pruning
| Attribute | Detail |
|-----------|--------|
| Test ID | T-005 |
| Component | transform.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify 12 high-null columns are dropped during transformation |
| Steps | Run `python pipeline/transform.py` and check output shape |
| Expected Result | Output DataFrame has 36 columns, down from 44 |
| Actual Result | Output shape confirmed as (1000, 36) |
| Status | ✅ Pass |

---

### T-006 — Date Parsing
| Attribute | Detail |
|-----------|--------|
| Test ID | T-006 |
| Component | transform.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify date string columns are converted to datetime objects |
| Steps | Run `python pipeline/transform.py` and check dtypes |
| Expected Result | created_date, closed_date, resolution_action_updated_date are datetime64 |
| Actual Result | All three columns confirmed as datetime64[us] |
| Status | ✅ Pass |

---

### T-007 — Zip Code Type Fix
| Attribute | Detail |
|-----------|--------|
| Test ID | T-007 |
| Component | transform.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify incident_zip is converted from float64 to zero-padded string |
| Steps | Run `python pipeline/transform.py` and check incident_zip dtype |
| Expected Result | incident_zip is string dtype, values are 5-digit zero-padded |
| Actual Result | incident_zip confirmed as str dtype with zero-padded values |
| Status | ✅ Pass |

---

### T-008 — Derived Columns
| Attribute | Detail |
|-----------|--------|
| Test ID | T-008 |
| Component | transform.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify all 4 derived columns are generated correctly |
| Steps | Run `python pipeline/transform.py` and check for derived columns |
| Expected Result | resolution_hours, is_open, created_year, created_month present in output |
| Actual Result | All 4 derived columns confirmed in output DataFrame |
| Status | ✅ Pass |

---

### T-009 — String Standardization
| Attribute | Detail |
|-----------|--------|
| Test ID | T-009 |
| Component | transform.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify key categorical string columns are title-cased |
| Steps | Run `python pipeline/transform.py` and spot check borough, city, complaint_type, status values |
| Expected Result | Values like BROOKLYN → Brooklyn, NOISE - RESIDENTIAL → Noise - Residential |
| Actual Result | Title casing confirmed on all key categorical fields |
| Status | ✅ Pass |

---

## Section 3 — DQ Check Tests

### T-010 — DQ-001 Null Descriptor Detection
| Attribute | Detail |
|-----------|--------|
| Test ID | T-010 |
| Component | dq_checks.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify DQ-001 detects and drops rows with null descriptors |
| Steps | Run `python pipeline/dq_checks.py` and check DQ-001 result |
| Expected Result | DQ-001 returns FAIL with violation count > 0, affected rows dropped |
| Actual Result | DQ-001 FAIL — 4 violations at 1,000 rows, 30 violations at 5,000 rows. Rows dropped confirmed |
| Status | ✅ Pass |

---

### T-011 — DQ-002 Zip Code Validation
| Attribute | Detail |
|-----------|--------|
| Test ID | T-011 |
| Component | dq_checks.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify DQ-002 flags invalid zip codes without dropping rows |
| Steps | Run `python pipeline/dq_checks.py` and check DQ-002 result |
| Expected Result | DQ-002 returns WARN with violation count > 0, no rows dropped |
| Actual Result | DQ-002 WARN — 10 violations at 1,000 rows, 53 at 5,000 rows. No rows dropped confirmed |
| Status | ✅ Pass |

---

### T-012 — DQ-003 Coordinate Completeness
| Attribute | Detail |
|-----------|--------|
| Test ID | T-012 |
| Component | dq_checks.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify DQ-003 detects mismatched latitude/longitude pairs |
| Steps | Run `python pipeline/dq_checks.py` and check DQ-003 result |
| Expected Result | DQ-003 returns PASS or FAIL depending on data |
| Actual Result | DQ-003 PASS — 0 coordinate mismatches detected |
| Status | ✅ Pass |

---

### T-013 — DQ-004 Open/Closed Flag Consistency
| Attribute | Detail |
|-----------|--------|
| Test ID | T-013 |
| Component | dq_checks.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify DQ-004 detects inconsistencies between is_open flag and closed_date |
| Steps | Run `python pipeline/dq_checks.py` and check DQ-004 result |
| Expected Result | DQ-004 returns PASS or FAIL depending on data |
| Actual Result | DQ-004 PASS — 0 flag inconsistencies detected |
| Status | ✅ Pass |

---

### T-014 — DQ-005 Unique Key Integrity
| Attribute | Detail |
|-----------|--------|
| Test ID | T-014 |
| Component | dq_checks.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify DQ-005 detects duplicate unique_key values |
| Steps | Run `python pipeline/dq_checks.py` and check DQ-005 result |
| Expected Result | DQ-005 returns PASS with 0 duplicates |
| Actual Result | DQ-005 PASS — 0 duplicate keys detected |
| Status | ✅ Pass |

---

### T-015 — DQ-006 Resolution Consistency
| Attribute | Detail |
|-----------|--------|
| Test ID | T-015 |
| Component | dq_checks.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify DQ-006 flags closed complaints missing resolution descriptions |
| Steps | Run `python pipeline/dq_checks.py` and check DQ-006 result |
| Expected Result | DQ-006 returns PASS or WARN depending on data, no rows dropped |
| Actual Result | DQ-006 WARN at 5,000 rows — 13 violations, no rows dropped confirmed |
| Status | ✅ Pass |

---

### T-016 — Clean DataFrame Row Count
| Attribute | Detail |
|-----------|--------|
| Test ID | T-016 |
| Component | dq_checks.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify clean DataFrame reflects correct row count after critical DQ failures |
| Steps | Run `python pipeline/dq_checks.py` and check clean_df shape |
| Expected Result | clean_df row count equals input rows minus critical violation rows |
| Actual Result | 5,000 rows in → 4,970 rows out. 30 critical rows dropped confirmed |
| Status | ✅ Pass |

---

## Section 4 — Load Tests

### T-017 — SQLite Load
| Attribute | Detail |
|-----------|--------|
| Test ID | T-017 |
| Component | load.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify clean DataFrame is persisted to SQLite successfully |
| Steps | Run `python pipeline/load.py` and query nyc311_clean table |
| Expected Result | nyc311_clean table exists with correct row count |
| Actual Result | 4,970 rows confirmed in nyc311_clean table |
| Status | ✅ Pass |

---

### T-018 — Lineage Log
| Attribute | Detail |
|-----------|--------|
| Test ID | T-018 |
| Component | load.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify lineage metadata is written to lineage_log table on every run |
| Steps | Run `python pipeline/load.py` and query lineage_log table |
| Expected Result | lineage_log contains one row per pipeline run with correct metadata |
| Actual Result | lineage_log entry confirmed with table_name, rows_loaded, loaded_at, source |
| Status | ✅ Pass |

---

### T-019 — Query Helper
| Attribute | Detail |
|-----------|--------|
| Test ID | T-019 |
| Component | load.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify query() helper returns correct results |
| Steps | Call query("SELECT complaint_type, COUNT(*) FROM nyc311_clean GROUP BY complaint_type ORDER BY COUNT(*) DESC LIMIT 5") |
| Expected Result | Returns top 5 complaint types as DataFrame |
| Actual Result | Noise - Residential (425), Illegal Parking (165), Noise - Commercial (111), Blocked Driveway (75), Noise - Street/Sidewalk (65) |
| Status | ✅ Pass |

---

## Section 5 — Full Pipeline Tests

### T-020 — End to End Pipeline Run
| Attribute | Detail |
|-----------|--------|
| Test ID | T-020 |
| Component | main.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify full pipeline runs end to end in a single command |
| Steps | Run `python main.py --limit 5000` |
| Expected Result | Pipeline completes all 4 steps, DQ report exported, data loaded to SQLite |
| Actual Result | Pipeline completed in 1.90 seconds. All steps confirmed |
| Status | ✅ Pass |

---

### T-021 — DQ Report Export
| Attribute | Detail |
|-----------|--------|
| Test ID | T-021 |
| Component | main.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify DQ report is exported as timestamped CSV after every run |
| Steps | Run `python main.py` and check reports/ directory |
| Expected Result | reports/dq_report_TIMESTAMP.csv created with correct columns |
| Actual Result | dq_report_20260224_014601.csv confirmed in reports/ |
| Status | ✅ Pass |

---

### T-022 — Pipeline Summary Logging
| Attribute | Detail |
|-----------|--------|
| Test ID | T-022 |
| Component | main.py |
| Date | February 23, 2026 |
| Tester | Aaiyan Virji |
| Description | Verify pipeline summary is logged at end of every run |
| Steps | Run `python main.py` and check end of log output |
| Expected Result | Summary includes duration, rows extracted, rows after DQ, rows dropped, DQ rule results |
| Actual Result | Summary confirmed with all expected fields |
| Status | ✅ Pass |

---

## Test Summary

| Section | Tests | Passed | Failed | Not Run |
|---------|-------|--------|--------|---------|
| Section 1 — Extraction | 4 | 4 | 0 | 0 |
| Section 2 — Transformation | 5 | 5 | 0 | 0 |
| Section 3 — DQ Checks | 7 | 7 | 0 | 0 |
| Section 4 — Load | 3 | 3 | 0 | 0 |
| Section 5 — Full Pipeline | 3 | 3 | 0 | 0 |
| **Total** | **22** | **22** | **0** | **0** |

---

## Sign Off

| Attribute | Detail |
|-----------|--------|
| Tested By | Aaiyan Virji |
| Test Date | February 23, 2026 |
| Pipeline Version | v1.0.0 |
| Result | ✅ All 22 tests passed — pipeline approved for Phase 2 |