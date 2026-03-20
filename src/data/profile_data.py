from pathlib import Path
import pandas as pd

INTERIM_DIR = Path("data/interim")
PROFILE_DIR = Path("outputs/profiling")

# Load each interim data file
def load_interim_csv(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(file_path)

# Profile information for data file
def profile_dataframe(df: pd.DataFrame, file_name: str) -> dict:
    row_count = len(df)
    column_count  = len(df.columns)

    column_profiles = []

    for col in df.columns:
        null_count = df[col].isna().sum()
        null_pct = float(round((null_count / row_count) * 100, 2)) if row_count > 0 else 0.0
        unique_count = df[col].nunique(dropna=True)

        column_profiles.append({
            "column_name": col,
            "dtype": str(df[col].dtype),
            "null_count": int(null_count),
            "null_pct": null_pct,
            "unique_count": int(unique_count)
        })


    return {
        "file_name": file_name,
        "row_count": row_count,
        "column_count": column_count,
        "columns": list(df.columns),
        "column_profiles": column_profiles,
        "candidate_keys": identify_candidate_keys(df),
        "join_candidates": identify_join_candidates(df)
    }

def identify_candidate_keys(df: pd.DataFrame) -> list[str]:
    candidate_keys = []

    for col in df.columns:
        if df[col].notna().all() and df[col].nunique() == len(df):
            candidate_keys.append(col)

    return candidate_keys

def identify_join_candidates(df: pd.DataFrame) -> list[str]:
    common_join_names ={
        "opportunity_id", "sales_agent", "product", "account", 
        "table", "field"  
    }

    return [col for col in df.columns if col in common_join_names]


def write_profile_markdown(profile: dict) -> None:
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    file_stem = Path(profile["file_name"]).stem
    output_path = PROFILE_DIR / f"{file_stem}_profile.md"

    lines = []
    lines.append(f"# {file_stem} profile")
    lines.append("")
    lines.append("## Dataset summary")
    lines.append(f"- Rows: {profile['row_count']}")
    lines.append(f"- Columns: {profile['column_count']}")
    lines.append(f"- Potential Unique fields: {', '.join(profile['candidate_keys']) if profile['candidate_keys'] else 'None identified'}")
    lines.append(f"- Likely join fields: {', '.join(profile['join_candidates']) if profile['join_candidates'] else 'None identified'}")
    lines.append("")
    lines.append("## Column summary")
    lines.append("")
    lines.append("| Column | Dtype | Null Count | Null % | Unique Count |")
    lines.append("|---|---|---:|---:|---:|")

    for col in profile["column_profiles"]:
        lines.append(
            f"| {col['column_name']} | {col['dtype']} | {col['null_count']} | {col['null_pct']} | {col['unique_count']} |"
        )

    lines.append("")
    lines.append("## Notes")
    lines.append("- Add observations here after reviewing the profile.")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote profile to {output_path}")


def main():
    
    csv_files = list(INTERIM_DIR.glob("*.csv"))

    if not csv_files:
        print("No interim CSV files found.")
        return
    
    for file_path in csv_files:
        print("-" * 60)
        print(f"Profiling {file_path.name}")

        df = load_interim_csv(file_path)
        profile = profile_dataframe(df, file_path.name)
        write_profile_markdown(profile)
        
        # Used for testing
        print(f"Rows: {profile['row_count']}")
        print(f"Columns: {profile['column_count']}")
        print(f"Potential unique fields: {profile['candidate_keys']}")
        print(f"Join Candidates: {profile['join_candidates']}")


if __name__ == "__main__":
    main()