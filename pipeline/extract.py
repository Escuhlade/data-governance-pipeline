import pandas as pd
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# NYC 311 API endpoint
NYC_311_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"

def extract_nyc_311(limit: int = 50000) -> pd.DataFrame:
    """
    Extract NYC 311 Service Request data from the NYC Open Data API.
    
    Args:
        limit: Number of records to fetch (default 50,000)
    
    Returns:
        pd.DataFrame: Raw extracted data
    
    Raises:
        ConnectionError: If API is unreachable
        ValueError: If response is empty or malformed
    """
    logger.info(f"Starting extraction from NYC Open Data API — limit: {limit} rows")

    params = {
        "$limit": limit,
        "$order": "created_date DESC"
    }

    try:
        # Ping the API
        logger.info(f"Pinging endpoint: {NYC_311_URL}")
        response = requests.get(NYC_311_URL, params=params, timeout=30)
        response.raise_for_status()

        # Load into dataframe
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))

        # Validate we got data back
        if df.empty:
            raise ValueError("API returned an empty dataset.")

        logger.info(f"Extraction successful — {len(df):,} rows, {len(df.columns)} columns")
        logger.info(f"Columns detected: {list(df.columns)}")

        # Log extraction metadata
        _log_extraction_metadata(df, limit)

        return df

    except requests.exceptions.ConnectionError:
        logger.error("Connection failed — could not reach NYC Open Data API. Check your internet connection.")
        raise
    except requests.exceptions.Timeout:
        logger.error("Request timed out after 30 seconds.")
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error from API: {e}")
        raise
    except ValueError as e:
        logger.error(f"Data validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during extraction: {e}")
        raise


def _log_extraction_metadata(df: pd.DataFrame, limit: int) -> None:
    """Log extraction metadata for lineage tracking."""
    metadata = {
        "timestamp": datetime.utcnow().isoformat(),
        "source": NYC_311_URL,
        "rows_fetched": len(df),
        "columns": len(df.columns),
        "limit_requested": limit,
        "column_names": list(df.columns)
    }
    logger.info(f"Lineage metadata: {metadata}")


if __name__ == "__main__":
    df = extract_nyc_311(limit=1000)  # small pull to test
    print("\n--- DATAFRAME PREVIEW ---")
    print(df.head())
    print("\n--- SCHEMA ---")
    print(df.dtypes)
    print("\n--- SHAPE ---")
    print(f"Rows: {df.shape[0]:,} | Columns: {df.shape[1]}")
    print("\n--- NULL COUNTS ---")
    print(df.isnull().sum())