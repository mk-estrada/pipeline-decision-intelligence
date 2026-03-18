from pathlib import Path
import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def load_csv(file_name: str) -> pd.DataFrame:
    file_path = DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"{file_name} not found in data/raw/")

    df = pd.read_csv(file_path)

    print(f"Loaded {file_name}")
    print(f"Shape: {df.shape}")

    return df


def main():
    
    files = [
        "accounts.csv",
        "metadata.csv",
        "products.csv",
        "sales_pipeline.csv",
        "sales_teams.csv"
    ]

    data = {}

    for file in files:
        try:
            df = load_csv(file)
            data[file] = df
        except Exception as e:
            print(f"Error loading {file}: {e}")

    return data


if __name__ == "__main__":
    data = main()