import logging
import argparse
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "pipeline"))

from extract import extract_nyc_311
from transform import transform
from dq_checks import run_dq_checks
from load import load

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def run_pipeline(limit: int = 1000) -> None:
    """
    Run the full NYC 311 data governance pipeline.

    Steps:
        1. Extract — pull from NYC Open Data API
        2. Transform — clean, fix types, add derived columns
        3. DQ Checks — validate against governance rules
        4. Load — persist clean data to SQLite
        5. Export — save DQ report to reports/

    Args:
        limit: Number of rows to pull from API (default 1000)
    """
    start_time = datetime.utcnow()
    logger.info("=" * 60)
    logger.info("NYC 311 DATA GOVERNANCE PIPELINE — STARTING")
    logger.info(f"Run timestamp: {start_time.isoformat()}")
    logger.info(f"Row limit: {limit:,}")
    logger.info("=" * 60)

    try:
        # Step 1 — Extract
        logger.info("[STEP 1/4] Extract")
        raw_df = extract_nyc_311(limit=limit)
        logger.info(f"Extract complete — {len(raw_df):,} rows")

        # Step 2 — Transform
        logger.info("[STEP 2/4] Transform")
        transformed_df = transform(raw_df)
        logger.info(f"Transform complete — {len(transformed_df):,} rows, {len(transformed_df.columns)} columns")

        # Step 3 — DQ Checks
        logger.info("[STEP 3/4] DQ Checks")
        clean_df, dq_report = run_dq_checks(transformed_df)
        logger.info(f"DQ checks complete — {len(clean_df):,} clean rows")

        # Step 4 — Load
        logger.info("[STEP 4/4] Load")
        load(clean_df)
        logger.info("Load complete")

        # Step 5 — Export DQ report
        _export_dq_report(dq_report)

        # Summary
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()

        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETE")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Rows extracted: {len(raw_df):,}")
        logger.info(f"Rows after DQ: {len(clean_df):,}")
        logger.info(f"Rows dropped: {len(raw_df) - len(clean_df):,}")
        logger.info(f"DQ rules passed: {dq_report[dq_report['status'] == 'PASS'].shape[0]}")
        logger.info(f"DQ rules failed: {dq_report[dq_report['status'] == 'FAIL'].shape[0]}")
        logger.info(f"DQ rules warned: {dq_report[dq_report['status'] == 'WARN'].shape[0]}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


def _export_dq_report(dq_report) -> None:
    """Export DQ report to reports/ folder with timestamp."""
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"dq_report_{timestamp}.csv"
    filepath = os.path.join(reports_dir, filename)

    # Drop failed_row_ids column for clean CSV export
    export_df = dq_report.drop(columns=["failed_row_ids"])
    export_df.to_csv(filepath, index=False)

    logger.info(f"DQ report exported to: {filepath}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NYC 311 Data Governance Pipeline")
    parser.add_argument(
        "--limit",
        type=int,
        default=1000,
        help="Number of rows to pull from NYC Open Data API (default: 1000)"
    )
    args = parser.parse_args()

    run_pipeline(limit=args.limit)