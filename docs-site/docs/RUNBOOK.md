---
sidebar_position: 8
---
# Runbook

## Overview
This runbook provides step-by-step instructions for setting up, running, and troubleshooting the Data Governance Pipeline. Follow this guide to get the pipeline running from a fresh clone.

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.11.5+ | [Download](https://www.python.org/downloads/) |
| Git | Any | [Download](https://git-scm.com/) |
| Internet connection | — | Required for NYC Open Data API |

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Escuhlade/data-governance-pipeline.git
cd data-governance-pipeline
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Setup
```bash
python -c "import pandas, requests; print('Setup complete')"
```

Should print `Setup complete` with no errors.

---

## Running the Pipeline

### Full Pipeline Run (recommended)
```bash
python main.py
```

Runs with default limit of 1,000 rows.

### Custom Row Limit
```bash
python main.py --limit 5000
```

### Individual Modules
Run each module independently for testing or debugging:
```bash
# From the pipeline/ directory
cd pipeline

# Test extraction only
python extract.py

# Test transform only
python transform.py

# Test DQ checks only
python dq_checks.py

# Test load only
python load.py
```

---

## Expected Output

A successful pipeline run looks like this:
```
============================================================
NYC 311 DATA GOVERNANCE PIPELINE — STARTING
Run timestamp: 2026-02-24T01:45:59
Row limit: 5,000
============================================================
[STEP 1/4] Extract
Extraction successful — 5,000 rows, 44 columns
[STEP 2/4] Transform
Transformation complete — 5,000 rows, 36 columns
[STEP 3/4] DQ Checks
DQ checks complete — PASS: 3 | FAIL: 1 | WARN: 2
[STEP 4/4] Load
Load successful — 4,970 rows written to 'nyc311_clean'
============================================================
PIPELINE COMPLETE
Duration: 1.90 seconds
Rows extracted: 5,000
Rows after DQ: 4,970
Rows dropped: 30
============================================================
```

### Output Files
After a successful run you will find:

| File | Location | Description |
|------|----------|-------------|
| nyc311.db | reports/nyc311.db | SQLite database with clean data |
| dq_report_TIMESTAMP.csv | reports/ | DQ report for this run |

---

## Verifying a Successful Run

### Check Row Count in Database
```python
from pipeline.load import query
print(query("SELECT COUNT(*) as count FROM nyc311_clean"))
```

### Check Lineage Log
```python
from pipeline.load import query
print(query("SELECT * FROM lineage_log"))
```

### Check DQ Report
```bash
ls reports/
cat reports/dq_report_TIMESTAMP.csv
```

### Spot Check Data
```python
from pipeline.load import query

# Top complaint types
print(query("""
    SELECT complaint_type, COUNT(*) as count
    FROM nyc311_clean
    GROUP BY complaint_type
    ORDER BY count DESC
    LIMIT 5
"""))

# Complaints by borough
print(query("""
    SELECT borough, COUNT(*) as count
    FROM nyc311_clean
    GROUP BY borough
    ORDER BY count DESC
"""))
```

---

## Troubleshooting

### Connection Error — API Unreachable
```
ERROR: Connection failed — could not reach NYC Open Data API
```
**Cause:** No internet connection or NYC Open Data API is down.  
**Fix:** Check internet connection. Visit https://data.cityofnewyork.us to verify API is up. Retry after a few minutes.

---

### HTTP Error from API
```
ERROR: HTTP error from API: 429 Too Many Requests
```
**Cause:** Rate limited by NYC Open Data API.  
**Fix:** Wait 60 seconds and retry. Reduce `--limit` to a smaller value.

---

### Pandas Deprecation Warning
```
Pandas4Warning: For backward compatibility, 'str' dtypes are included...
```
**Cause:** Pandas version compatibility in transform.py.  
**Fix:** Already handled — `select_dtypes(include=["object", "str"])` resolves this.

---

### SQLite Database Locked
```
ERROR: SQLite error: database is locked
```
**Cause:** Another process has the database open.  
**Fix:** Close any SQLite browser tools (e.g. DB Browser for SQLite) and retry.

---

### Module Not Found Error
```
ModuleNotFoundError: No module named 'pandas'
```
**Cause:** Virtual environment not activated or dependencies not installed.  
**Fix:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

### Virtual Environment Not Activated
**Symptom:** You don't see `(venv)` in your terminal prompt.  
**Fix:**
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

---

## Maintenance

### Update Dependencies
```bash
pip install --upgrade pandas requests python-dotenv
pip freeze > requirements.txt
git add requirements.txt
git commit -m "chore: update dependencies"
git push origin main
```

### Re-run Pipeline After Schema Change
If the NYC 311 API changes its schema:
1. Run `python pipeline/extract.py` and check logged column names
2. Update `COLUMNS_TO_DROP` in `transform.py` if needed
3. Update `DATE_COLUMNS` in `transform.py` if needed
4. Update `DATA_DICTIONARY.md` to reflect schema changes
5. Re-run full pipeline with `python main.py`

### Regenerate Database
If `nyc311.db` becomes corrupted or needs a fresh rebuild:
```bash
rm reports/nyc311.db
python main.py
```

The database is fully rebuilt on every pipeline run.