
import os
from functools import lru_cache
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, URL


# Load environment variables from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Only allow these aggregate tables to be queried.
AGGREGATE_TABLES = {
    "monthly_performance": "agg_monthly_hotel_performance",
    "monthly_satisfaction": "agg_monthly_guest_satisfaction",
    "annual_turnover": "agg_annual_employee_turnover",
    "annual_kpi": "agg_annual_hotel_kpi",
}


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Create and reuse the MySQL database engine."""

    required_settings = {
        "DB_HOST": DB_HOST,
        "DB_USER": DB_USER,
        "DB_PASSWORD": DB_PASSWORD,
        "DB_NAME": DB_NAME,
    }

    missing_settings = [
        key for key, value in required_settings.items() if not value
    ]

    if missing_settings:
        raise ValueError(
            f"Missing database settings in .env: {', '.join(missing_settings)}"
        )

    database_url = URL.create(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME,
    )

    return create_engine(database_url, pool_pre_ping=True)


def test_connection() -> bool:
    """Check whether the MySQL database connection works."""

    engine = get_engine()

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return True


def load_aggregate_data(table_key: str) -> pd.DataFrame:
    """Load data from an approved aggregate table."""

    if table_key not in AGGREGATE_TABLES:
        raise ValueError(f"Unknown aggregate table: {table_key}")

    table_name = AGGREGATE_TABLES[table_key]
    query = f"SELECT * FROM `{DB_NAME}`.`{table_name}`"

    return pd.read_sql(query, get_engine())
