
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas


load_dotenv()

def get_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema="ANALYTICS",
        role=os.getenv("SNOWFLAKE_ROLE"),
        login_timeout=10
    )

def load_ml_dataset(conn):
    query = """
        select
            opportunity_id,
            pipeline_status,
            won_flag,
            estimated_deal_size_band,
            regional_office,
            deal_age_days,
            product_name
        from int_closed_opportunities_for_ml
    """

    return conn.cursor().execute(query).fetch_pandas_all()


def main():

    print("Connecting to Snowflake...")
    conn = get_connection()

    print("Database:", os.getenv("SNOWFLAKE_DATABASE"))
    print("Requested schema: ANALYTICS")
    
    df = load_ml_dataset(conn)

    df.columns = df.columns.str.lower()

    print("Shape:", df.shape)
    print(df.head())


    print(df['won_flag'].value_counts())
    print("Unique deal sizes:", df['estimated_deal_size_band'].unique())
    print("Unique regions:", df['regional_office'].unique())
    print("Product count:", df['product_name'].nunique())
    print(df['deal_age_days'].describe())

    feature_cols = [
    "estimated_deal_size_band",
    "regional_office",
    "product_name",
    "deal_age_days"
    ]

    target_col = "won_flag"

    X = df[feature_cols]
    y = df[target_col]
    
    categorical_features = [
    "estimated_deal_size_band",
    "regional_office",
    "product_name"
    ]

    numeric_features = [
        "deal_age_days"
    ]

    conn.close()

if __name__ == "__main__":
    main()