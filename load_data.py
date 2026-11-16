
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

load_dotenv()

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME")
)

engine = create_engine(connection_url)

# Load tables in foreign-key order
tables = [
    "dim_hotel",
    "dim_room",
    "dim_guest",
    "dim_employee",
    "dim_date",
    "fact_room_night",
    "fact_guest_feedback",
    "fact_employee_movement"
]

for table in tables:
    file_path = f"data/{table}.csv"

    print(f"Loading {table}...")

    df = pd.read_csv(file_path)

    df.to_sql(
        name=table,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=5000
    )

    print(f"{len(df)} records loaded into {table}")

print("\nAll datasets loaded successfully!")
