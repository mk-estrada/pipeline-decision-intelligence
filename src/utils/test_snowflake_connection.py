"""
Simple Snowflake connectivity test for the Decision Intelligence project.

Purpose:
- verify Python can connect to Snowflake
- confirm correct warehouse/database/schema context
- provide a reusable connection pattern for future loading scripts
"""

import os 
from dotenv import load_dotenv
import snowflake.connector

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

def main():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 
                current_warehouse(),
                current_database(),
                current_schema(),
                current_role()
          """)
        result = cur.fetchone()

        print("Snowflake connection successful")
        print(f"Warehouse: {result[0]}")
        print(f"Database: {result[1]}")
        print(f"Schema: {result[2]}")
        print(f"Role: {result[3]}")

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()