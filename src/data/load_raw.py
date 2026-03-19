from pathlib import Path
import pandas as pd
import re #regular expression library

RAW_DIR = Path("data/raw")
INTERIM_DIR = Path("data/interim")

DATE_COLUMNS = ["engage_date", "close_date"]
NUMERIC_COLUMNS = ["close_value", "year_established", "revenue", "employees", "sales_price"]
NULL_LIKE_VALUES = ["", " ", "NA", "N/A", "null", "None"]

# Remove any white space or special characters, add underscores for blanks spaces
def to_snake_case(col_name: str) -> str:
    col_name = col_name.strip().lower()
    col_name = re.sub(r"[^\w\s]", "", col_name)
    col_name = re.sub(r"[\s\-]+", "_", col_name)
    col_name = re.sub(r"_+", "_", col_name)
    return col_name.strip("_")


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [to_snake_case(col) for col in df.columns]
    return df

# Clean strings and nulls in the datasets 
def clean_strings_and_nulls(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Trim whitespace from string/object columns
    object_cols = df.select_dtypes(include=["object", "string"]).columns

    for col in object_cols:
        df[col] = df[col].astype("string").str.strip()

    # Replace common null-like values
    df = df.replace(NULL_LIKE_VALUES, pd.NA)

    return df

# Standardize data types
def standardize_data_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()  

    # Convert numeric columns
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert date columns
    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df

def load_csv(file_name: str) -> pd.DataFrame:
    file_path = RAW_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"{file_name} not found in data/raw/")

    df = pd.read_csv(file_path)
    df = standardize_columns(df)
    df = clean_strings_and_nulls(df)
    df = standardize_data_types(df)

    print(f"Loaded {file_name}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Null counts:\n{df.isna().sum()}")
    print(f"Dtypes:\n{df.dtypes}")

    return df

# Save function
def save_interim(df: pd.DataFrame, file_name: str) -> Path:
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)

    output_path = INTERIM_DIR / file_name
    df.to_csv(output_path, index=False)

    print(f"Saved Cleaned file to {output_path}")

    return output_path

def main():
    
    files = [
        "accounts.csv",
        "metadata.csv",
        "products.csv",
        "sales_pipeline.csv",
        "sales_teams.csv"
    ]

    data = {}
    print("-" * 60) #Creates visual space betweeen file prints
    for file in files:
        try:
            df = load_csv(file)
            data[file] = df
            save_interim(df, file)
        except Exception as e:
            print(f"Error loading {file}: {e}")

    return data


if __name__ == "__main__":
    data = main()