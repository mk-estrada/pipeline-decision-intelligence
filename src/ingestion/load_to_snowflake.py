"""
Load cleaned interim CSV files into Snowflake RAW tables.

Purpose:
- move trusted local interim datasets into Snowflake
- create a reproducible RAW data loading step
- establish Snowflake as the warehouse source layer for dbt
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

LOAD_DIR = Path("data/interim")

load_dotenv()

def get_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        login_timeout=10
    )

def load_csv_to_raw_table(csv_path: Path, table_name: str):
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    conn = get_connection()

    try:
        df =pd.read_csv(csv_path)

        success, nchunks, nrows, _ = write_pandas(
            conn=conn, 
            df=df,
            table_name=table_name,
            auto_create_table=True,
            overwrite=True,
        )
        
        print(f"Loaded {csv_path.name} -> {table_name}")
        print(f"Success: {success} | Chunks: {nchunks} | Rows: {nrows}")

    finally:
        conn.close()

def main():

    file_table_map = [
        ("sales_teams.csv", "sales_teams_raw"),
        ("accounts.csv", "accounts_raw"),
        ("products.csv", "products_raw"),
        ("sales_pipeline.csv", "sales_pipeline_raw"),
    ]

    interim_dir = Path("data/interim")
    loaded_tables = []

    for file_name, table_name in file_table_map:
        csv_path = interim_dir / file_name
        print(f"\nLoading file: {csv_path}")
        load_csv_to_raw_table(csv_path, table_name)
        loaded_tables.append(table_name)

    print("\nRAW load complete.")
    print("Loaded tables:")
    for table_name in loaded_tables:
        print(f"- {table_name}")

if __name__ == "__main__":
    main()
