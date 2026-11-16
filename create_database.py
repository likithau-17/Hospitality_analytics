
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# Load database settings from the project's .env file
PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")


def create_database():
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    # Validate database configuration
    if not all([db_host, db_user, db_password, db_name]):
        raise ValueError(
            "Missing database settings. Please check your .env file."
        )

    # Validate database name before using it as an SQL identifier
    if not re.fullmatch(r"[A-Za-z0-9_]+", db_name):
        raise ValueError("Invalid database name in .env file.")

    # Connect to MySQL server without selecting a database
    database_url = URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_password,
        host=db_host,
    )

    engine = create_engine(database_url)

    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
                    "CHARACTER SET utf8mb4 "
                    "COLLATE utf8mb4_unicode_ci"
                )
            )

        print(f"Database '{db_name}' is ready.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    create_database()
