import pandas as pd
import sqlite3
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Database path — lives in reports/ folder
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "reports", "nyc311.db")


def load(df: pd.DataFrame, table_name: str = "nyc311_clean") -> None:
    """
    Load clean dataframe into SQLite database.

    Args:
        df: Clean dataframe from dq_checks.py
        table_name: Target table name (default: nyc311_clean)
    """
    logger.info(f"Starting load — {len(df):,} rows into table '{table_name}'")

    try:
        conn = _get_connection()

        # Write dataframe to SQLite
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists="replace",  # replace table on each run
            index=False
        )

        # Verify load
        count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table_name}", conn).iloc[0]["count"]
        logger.info(f"Load successful — {count:,} rows written to '{table_name}'")

        # Log load metadata
        _log_load_metadata(conn, table_name, df)

        conn.close()
        logger.info(f"Database connection closed — {DB_PATH}")

    except sqlite3.Error as e:
        logger.error(f"SQLite error during load: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during load: {e}")
        raise


def _get_connection() -> sqlite3.Connection:
    """Create and return SQLite connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    logger.info(f"Connected to SQLite database at: {DB_PATH}")
    return conn


def _log_load_metadata(conn: sqlite3.Connection, table_name: str, df: pd.DataFrame) -> None:
    """Log load metadata to a lineage tracking table."""
    metadata = pd.DataFrame([{
        "table_name": table_name,
        "rows_loaded": len(df),
        "columns_loaded": len(df.columns),
        "loaded_at": datetime.utcnow().isoformat(),
        "source": "NYC 311 Open Data API"
    }])

    metadata.to_sql(
        name="lineage_log",
        con=conn,
        if_exists="append",
        index=False
    )
    logger.info("Lineage metadata written to lineage_log table")


def query(sql: str) -> pd.DataFrame:
    """
    Run a query against the SQLite database and return results as dataframe.

    Args:
        sql: SQL query string

    Returns:
        pd.DataFrame: Query results
    """
    try:
        conn = _get_connection()
        df = pd.read_sql(sql, conn)
        conn.close()
        return df
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise


if __name__ == "__main__":
    from extract import extract_nyc_311
    from transform import transform
    from dq_checks import run_dq_checks

    # Run full pipeline
    raw_df = extract_nyc_311(limit=1000)
    transformed_df = transform(raw_df)
    clean_df, dq_report = run_dq_checks(transformed_df)

    # Load to SQLite
    load(clean_df)

    # Verify with a few queries
    print("\n--- VERIFICATION QUERIES ---")

    print("\nTop 5 complaint types:")
    print(query("""
        SELECT complaint_type, COUNT(*) as count
        FROM nyc311_clean
        GROUP BY complaint_type
        ORDER BY count DESC
        LIMIT 5
    """))

    print("\nComplaints by borough:")
    print(query("""
        SELECT borough, COUNT(*) as count
        FROM nyc311_clean
        GROUP BY borough
        ORDER BY count DESC
    """))

    print("\nLineage log:")
    print(query("SELECT * FROM lineage_log"))