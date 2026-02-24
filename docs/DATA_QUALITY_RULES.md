# Data Quality Rules

## Overview
This document defines all data quality rules implemented in `pipeline/dq_checks.py`. Each rule is assigned a unique ID, severity level, and pass/fail criteria. Rules are applied to every pipeline run and results are exported to `reports/` as a timestamped CSV.

**Rule Status Legend**
| Status | Meaning |
|--------|---------|
| PASS | No violations detected |
| FAIL | Critical violations detected — affected rows dropped from clean dataset |
| WARN | Non-critical violations detected — rows flagged but retained |

---

## DQ-001 — Descriptor Not Null
**Severity:** Critical  
**Status:** Active  
**Column:** `descriptor`  

### Definition
Every service request must have a complaint descriptor. This field describes the specific nature of the complaint and is required for downstream categorization and reporting.

### Rule Logic
```python
failed_rows = df[df["descriptor"].isnull()]
```

### Pass Criteria
Zero null values in the `descriptor` column.

### Fail Criteria
Any null value in `descriptor` triggers a FAIL. Affected rows are dropped from the clean dataset.

### Rationale
A complaint record without a descriptor has no analytical value and cannot be correctly categorized. Allowing null descriptors downstream would corrupt complaint type reporting.

### Results on Last Run (5,000 rows)
| Metric | Value |
|--------|-------|
| Violations | 30 |
| Violation % | 0.60% |
| Status | FAIL |
| Rows Dropped | 30 |

---

## DQ-002 — Zip Code Format
**Severity:** Non-Critical  
**Status:** Active  
**Column:** `incident_zip`  

### Definition
Incident zip codes must conform to the standard US 5-digit format. Invalid or missing zip codes are flagged for review but do not invalidate the record.

### Rule Logic
```python
invalid_mask = df["incident_zip"].notnull() & ~df["incident_zip"].str.match(r"^\d{5}$")
null_mask = df["incident_zip"].isnull()
failed_rows = df[invalid_mask | null_mask]
```

### Pass Criteria
All zip codes are either null or match the pattern `^\d{5}$`.

### Warn Criteria
Any zip code that is null or does not match 5-digit format triggers a WARN. Rows are flagged but retained.

### Rationale
Invalid zip codes affect geographic analysis but do not invalidate the complaint record itself. Flagging rather than dropping preserves valid complaint data while surfacing location quality issues.

### Results on Last Run (5,000 rows)
| Metric | Value |
|--------|-------|
| Violations | 53 |
| Violation % | 1.06% |
| Status | WARN |
| Rows Dropped | 0 |

---

## DQ-003 — Coordinate Completeness
**Severity:** Critical  
**Status:** Active  
**Column:** `latitude`, `longitude`  

### Definition
Latitude and longitude must either both be present or both be null. A record with one coordinate but not the other is malformed and cannot be used for spatial analysis.

### Rule Logic
```python
lat_null = df["latitude"].isnull()
lon_null = df["longitude"].isnull()
mismatched = df[lat_null != lon_null]
```

### Pass Criteria
Every record has either both latitude and longitude populated, or both null.

### Fail Criteria
Any record where exactly one of latitude or longitude is null triggers a FAIL. Affected rows are dropped.

### Rationale
Partial coordinates are worse than no coordinates — they create silent errors in spatial analysis. A record with latitude but no longitude cannot be mapped and should not be treated as a valid location record.

### Results on Last Run (5,000 rows)
| Metric | Value |
|--------|-------|
| Violations | 0 |
| Violation % | 0.00% |
| Status | PASS |
| Rows Dropped | 0 |

---

## DQ-004 — Open/Closed Flag Consistency
**Severity:** Critical  
**Status:** Active  
**Column:** `is_open`, `closed_date`  

### Definition
The `is_open` derived flag must be consistent with the presence or absence of `closed_date`. An open complaint must not have a closed date, and a closed complaint must have one.

### Rule Logic
```python
open_with_date = df[df["is_open"] & df["closed_date"].notnull()]
closed_without_date = df[~df["is_open"] & df["closed_date"].isnull()]
failed_rows = pd.concat([open_with_date, closed_without_date])
```

### Pass Criteria
All open complaints have null `closed_date`. All closed complaints have a populated `closed_date`.

### Fail Criteria
Any inconsistency between `is_open` and `closed_date` triggers a FAIL. Affected rows are dropped.

### Rationale
Inconsistent open/closed flags corrupt resolution time calculations and complaint status reporting. This rule ensures the derived `is_open` column is always trustworthy.

### Results on Last Run (5,000 rows)
| Metric | Value |
|--------|-------|
| Violations | 0 |
| Violation % | 0.00% |
| Status | PASS |
| Rows Dropped | 0 |

---

## DQ-005 — Unique Key Integrity
**Severity:** Critical  
**Status:** Active  
**Column:** `unique_key`  

### Definition
Every service request must have a unique identifier. Duplicate `unique_key` values indicate either data pipeline duplication or source data corruption.

### Rule Logic
```python
duplicates = df[df.duplicated(subset=["unique_key"], keep=False)]
```

### Pass Criteria
Zero duplicate values in the `unique_key` column.

### Fail Criteria
Any duplicate `unique_key` value triggers a FAIL. All copies of duplicated records are dropped.

### Rationale
Duplicate records corrupt all aggregate metrics — counts, averages, resolution times. Unique key integrity is a foundational governance requirement for any dataset.

### Results on Last Run (5,000 rows)
| Metric | Value |
|--------|-------|
| Violations | 0 |
| Violation % | 0.00% |
| Status | PASS |
| Rows Dropped | 0 |

---

## DQ-006 — Resolution Description Consistency
**Severity:** Non-Critical  
**Status:** Active  
**Column:** `resolution_description`, `is_open`  

### Definition
Closed complaints should have a resolution description explaining how the complaint was addressed. Open complaints may have null resolution descriptions.

### Rule Logic
```python
closed_without_resolution = df[
    ~df["is_open"] & df["resolution_description"].isnull()
]
```

### Pass Criteria
All closed complaints have a populated `resolution_description`.

### Warn Criteria
Any closed complaint missing a `resolution_description` triggers a WARN. Rows are flagged but retained.

### Rationale
Missing resolution descriptions on closed complaints suggest incomplete data entry at the source. While not critical enough to drop the record, it is a data quality signal worth monitoring for source system quality improvement.

### Results on Last Run (5,000 rows)
| Metric | Value |
|--------|-------|
| Violations | 13 |
| Violation % | 0.26% |
| Status | WARN |
| Rows Dropped | 0 |

---

## Rules Summary

| Rule ID | Rule Name | Column | Severity | Last Status |
|---------|-----------|--------|----------|-------------|
| DQ-001 | Descriptor Not Null | descriptor | Critical | FAIL |
| DQ-002 | Zip Code Format | incident_zip | Non-Critical | WARN |
| DQ-003 | Coordinate Completeness | latitude, longitude | Critical | PASS |
| DQ-004 | Open/Closed Flag Consistency | is_open, closed_date | Critical | PASS |
| DQ-005 | Unique Key Integrity | unique_key | Critical | PASS |
| DQ-006 | Resolution Description Consistency | resolution_description | Non-Critical | WARN |