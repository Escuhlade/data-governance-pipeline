import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def run_dq_checks(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Run all data quality checks against the transformed dataframe.

    Args:
        df: Transformed dataframe from transform.py

    Returns:
        tuple: (clean_df, dq_report_df)
            - clean_df: rows that passed all critical DQ rules
            - dq_report_df: full DQ report with pass/fail per rule
    """
    logger.info("Starting DQ checks...")

    results = []

    results.append(_check_null_descriptors(df))
    results.append(_check_zip_format(df))
    results.append(_check_coordinate_completeness(df))
    results.append(_check_open_complaint_flags(df))
    results.append(_check_duplicate_keys(df))
    results.append(_check_resolution_consistency(df))

    dq_report = pd.DataFrame(results)

    # Log summary
    passed = dq_report[dq_report["status"] == "PASS"].shape[0]
    failed = dq_report[dq_report["status"] == "FAIL"].shape[0]
    warned = dq_report[dq_report["status"] == "WARN"].shape[0]

    logger.info(f"DQ checks complete — PASS: {passed} | FAIL: {failed} | WARN: {warned}")

    # Clean df = drop rows that failed critical rules
    critical_failures = dq_report[
        (dq_report["status"] == "FAIL") & (dq_report["critical"] == True)
    ]["failed_row_ids"].explode().dropna().unique()

    clean_df = df[~df["unique_key"].isin(critical_failures)].copy()
    logger.info(f"Clean dataframe shape after DQ: {clean_df.shape}")

    return clean_df, dq_report


def _check_null_descriptors(df: pd.DataFrame) -> dict:
    """
    Rule DQ-001: descriptor must not be null.
    Complaint type descriptor is a core required field.
    """
    rule_id = "DQ-001"
    failed_rows = df[df["descriptor"].isnull()]
    failed_ids = failed_rows["unique_key"].tolist()
    count = len(failed_rows)
    status = "PASS" if count == 0 else "FAIL"

    logger.info(f"[{rule_id}] Null descriptors — {count} violations | {status}")

    return {
        "rule_id": rule_id,
        "rule_name": "Descriptor Not Null",
        "description": "complaint descriptor must not be null",
        "column": "descriptor",
        "critical": True,
        "violations": count,
        "violation_pct": round(count / len(df) * 100, 2),
        "status": status,
        "failed_row_ids": failed_ids,
        "checked_at": datetime.utcnow().isoformat()
    }


def _check_zip_format(df: pd.DataFrame) -> dict:
    """
    Rule DQ-002: incident_zip must be a valid 5-digit US zip code.
    """
    rule_id = "DQ-002"

    # Valid zip = 5 digits, not null
    invalid_mask = df["incident_zip"].notnull() & ~df["incident_zip"].str.match(r"^\d{5}$")
    null_mask = df["incident_zip"].isnull()
    failed_rows = df[invalid_mask | null_mask]
    failed_ids = failed_rows["unique_key"].tolist()
    count = len(failed_rows)
    status = "PASS" if count == 0 else "WARN"

    logger.info(f"[{rule_id}] Invalid zip codes — {count} violations | {status}")

    return {
        "rule_id": rule_id,
        "rule_name": "Zip Code Format",
        "description": "incident_zip must be a valid 5-digit zip code",
        "column": "incident_zip",
        "critical": False,
        "violations": count,
        "violation_pct": round(count / len(df) * 100, 2),
        "status": status,
        "failed_row_ids": failed_ids,
        "checked_at": datetime.utcnow().isoformat()
    }


def _check_coordinate_completeness(df: pd.DataFrame) -> dict:
    """
    Rule DQ-003: latitude and longitude must both be present or both be null.
    A record with one but not the other is malformed.
    """
    rule_id = "DQ-003"

    lat_null = df["latitude"].isnull()
    lon_null = df["longitude"].isnull()
    mismatched = df[lat_null != lon_null]
    failed_ids = mismatched["unique_key"].tolist()
    count = len(mismatched)
    status = "PASS" if count == 0 else "FAIL"

    logger.info(f"[{rule_id}] Coordinate mismatch — {count} violations | {status}")

    return {
        "rule_id": rule_id,
        "rule_name": "Coordinate Completeness",
        "description": "latitude and longitude must both be present or both null",
        "column": "latitude, longitude",
        "critical": True,
        "violations": count,
        "violation_pct": round(count / len(df) * 100, 2),
        "status": status,
        "failed_row_ids": failed_ids,
        "checked_at": datetime.utcnow().isoformat()
    }


def _check_open_complaint_flags(df: pd.DataFrame) -> dict:
    """
    Rule DQ-004: Open complaints (is_open=True) must not have a closed_date.
    Closed complaints (is_open=False) must have a closed_date.
    """
    rule_id = "DQ-004"

    open_with_date = df[df["is_open"] & df["closed_date"].notnull()]
    closed_without_date = df[~df["is_open"] & df["closed_date"].isnull()]
    failed_rows = pd.concat([open_with_date, closed_without_date])
    failed_ids = failed_rows["unique_key"].tolist()
    count = len(failed_rows)
    status = "PASS" if count == 0 else "FAIL"

    logger.info(f"[{rule_id}] Open/closed flag inconsistency — {count} violations | {status}")

    return {
        "rule_id": rule_id,
        "rule_name": "Open Complaint Flag Consistency",
        "description": "is_open flag must be consistent with closed_date presence",
        "column": "is_open, closed_date",
        "critical": True,
        "violations": count,
        "violation_pct": round(count / len(df) * 100, 2),
        "status": status,
        "failed_row_ids": failed_ids,
        "checked_at": datetime.utcnow().isoformat()
    }


def _check_duplicate_keys(df: pd.DataFrame) -> dict:
    """
    Rule DQ-005: unique_key must be unique across all records.
    """
    rule_id = "DQ-005"

    duplicates = df[df.duplicated(subset=["unique_key"], keep=False)]
    failed_ids = duplicates["unique_key"].tolist()
    count = len(duplicates)
    status = "PASS" if count == 0 else "FAIL"

    logger.info(f"[{rule_id}] Duplicate unique_keys — {count} violations | {status}")

    return {
        "rule_id": rule_id,
        "rule_name": "Unique Key Integrity",
        "description": "unique_key must be unique across all records",
        "column": "unique_key",
        "critical": True,
        "violations": count,
        "violation_pct": round(count / len(df) * 100, 2),
        "status": status,
        "failed_row_ids": failed_ids,
        "checked_at": datetime.utcnow().isoformat()
    }


def _check_resolution_consistency(df: pd.DataFrame) -> dict:
    """
    Rule DQ-006: Closed complaints must have a resolution_description.
    Open complaints may have null resolution_description.
    """
    rule_id = "DQ-006"

    closed_without_resolution = df[
        ~df["is_open"] & df["resolution_description"].isnull()
    ]
    failed_ids = closed_without_resolution["unique_key"].tolist()
    count = len(closed_without_resolution)
    status = "PASS" if count == 0 else "WARN"

    logger.info(f"[{rule_id}] Missing resolution on closed complaints — {count} violations | {status}")

    return {
        "rule_id": rule_id,
        "rule_name": "Resolution Description Consistency",
        "description": "closed complaints must have a resolution_description",
        "column": "resolution_description, is_open",
        "critical": False,
        "violations": count,
        "violation_pct": round(count / len(df) * 100, 2),
        "status": status,
        "failed_row_ids": failed_ids,
        "checked_at": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    from extract import extract_nyc_311
    from transform import transform

    raw_df = extract_nyc_311(limit=1000)
    transformed_df = transform(raw_df)
    clean_df, dq_report = run_dq_checks(transformed_df)

    print("\n--- DQ REPORT ---")
    print(dq_report[["rule_id", "rule_name", "violations", "violation_pct", "status", "critical"]])
    print("\n--- CLEAN DF SHAPE ---")
    print(f"Rows after DQ: {clean_df.shape[0]:,} | Columns: {clean_df.shape[1]}")