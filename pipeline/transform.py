import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Columns to drop — 90%+ null, no analytical value
COLUMNS_TO_DROP = [
    "facility_type",
    "due_date",
    "descriptor_2",
    "vehicle_type",
    "taxi_company_borough",
    "taxi_pick_up_location",
    "bridge_highway_name",
    "bridge_highway_direction",
    "road_ramp",
    "bridge_highway_segment",
    "landmark",
    "bbl"
]

# Date columns to parse
DATE_COLUMNS = [
    "created_date",
    "closed_date",
    "resolution_action_updated_date"
]


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all transformations to raw NYC 311 dataframe.

    Args:
        df: Raw dataframe from extract.py

    Returns:
        pd.DataFrame: Cleaned, transformed dataframe
    """
    logger.info(f"Starting transformation — input shape: {df.shape}")

    df = _drop_columns(df)
    df = _parse_dates(df)
    df = _fix_dtypes(df)
    df = _standardize_strings(df)
    df = _add_derived_columns(df)

    logger.info(f"Transformation complete — output shape: {df.shape}")
    return df


def _drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop columns with no analytical value."""
    cols_to_drop = [c for c in COLUMNS_TO_DROP if c in df.columns]
    df = df.drop(columns=cols_to_drop)
    logger.info(f"Dropped {len(cols_to_drop)} columns: {cols_to_drop}")
    return df


def _parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convert date strings to datetime objects."""
    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            null_count = df[col].isnull().sum()
            logger.info(f"Parsed {col} to datetime — {null_count} nulls remaining")
    return df


def _fix_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Fix incorrect data types."""
    # incident_zip should be string not float
    if "incident_zip" in df.columns:
        df["incident_zip"] = df["incident_zip"].apply(
            lambda x: str(int(x)).zfill(5) if pd.notnull(x) else None
        )
        logger.info("Fixed incident_zip: float64 -> string (zero-padded)")

    # council_district should be int not float
    if "council_district" in df.columns:
        df["council_district"] = df["council_district"].astype("Int64")
        logger.info("Fixed council_district: float64 -> Int64")

    return df


def _standardize_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize string columns — strip whitespace, title case key fields."""
    string_cols = df.select_dtypes(include=["object", "str"]).columns

    for col in string_cols:
        df[col] = df[col].str.strip()
    # Title case key categorical fields
    for col in ["borough", "city", "complaint_type", "status"]:
        if col in df.columns:
            df[col] = df[col].str.title()

    logger.info(f"Standardized {len(string_cols)} string columns")
    return df


def _add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns useful for analysis and DQ reporting."""

    # Resolution time in hours
    if "created_date" in df.columns and "closed_date" in df.columns:
        df["resolution_hours"] = (
            df["closed_date"] - df["created_date"]
        ).dt.total_seconds() / 3600
        logger.info("Added derived column: resolution_hours")

    # Flag open vs closed complaints
    if "closed_date" in df.columns:
        df["is_open"] = df["closed_date"].isnull()
        logger.info("Added derived column: is_open")

    # Extract year and month from created_date for reporting
    if "created_date" in df.columns:
        df["created_year"] = df["created_date"].dt.year
        df["created_month"] = df["created_date"].dt.month
        logger.info("Added derived columns: created_year, created_month")

    return df


if __name__ == "__main__":
    from extract import extract_nyc_311

    raw_df = extract_nyc_311(limit=1000)
    transformed_df = transform(raw_df)

    print("\n--- TRANSFORMED PREVIEW ---")
    print(transformed_df.head())
    print("\n--- SCHEMA AFTER TRANSFORM ---")
    print(transformed_df.dtypes)
    print("\n--- SHAPE ---")
    print(f"Rows: {transformed_df.shape[0]:,} | Columns: {transformed_df.shape[1]}")
    print("\n--- NULL COUNTS AFTER TRANSFORM ---")
    print(transformed_df.isnull().sum())