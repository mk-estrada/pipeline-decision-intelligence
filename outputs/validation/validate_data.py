from pathlib import Path
import pandas as pd

INTERIM_DIR = Path("data/interim")
VALIDATION_DIR = Path("outputs/validation")

VALIDATION_RULES = {
    "sales_pipeline.csv": {
        "not_null": ["opportunity_id", "sales_agent", "product", "deal_stage"],
        "unique": ["opportunity_id"]
    },
    "accounts.csv": {
        "not_null": ["account", "sector", "office_location"],
        "unique": ["account"]
    },
    "products.csv": {
        "not_null": ["product", "series", "sales_price"],
        "unique": ["product"]
    },
    "sales_teams.csv": {
        "not_null": ["sales_agent"],
        "unique": ["sales_agent"]
    },
    "metadata.csv": {
        "not_null": [],
        "unique": []
    }


}

# Load each interim data file
def load_interim_csv(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(file_path)

# Check if all values in column are not null 
def check_not_null(df: pd.DataFrame, column: str) -> dict:
    null_count = df[column].isna().sum()
    total_rows = len(df)

    return {
        "check_type": "not_null",
        "column": column,
        "null_count": int(null_count),
        "total_rows": total_rows,
        "passed": bool(null_count == 0)
    }

# Check if all values in column are unique
def check_unique(df: pd.DataFrame, column: str) -> dict:
    total_rows = len(df)
    unique_count = df[column].nunique(dropna=True)

    return {
        "check_type": "unique",
        "column": column,
        "unique_count": int(unique_count),
        "total_rows": total_rows,
        "passed": bool(unique_count == total_rows)
    }

def run_validations(df: pd.DataFrame, file_name: str) -> list[dict]:
    results = []

    rules = VALIDATION_RULES.get(file_name, {})

    for column in rules.get("not_null", {}):
        results.append(check_not_null(df, column))

    for column in rules.get("unique", {}):
        results.append(check_unique(df, column))

    return results


def write_validation_summary(all_results: dict[str, list[dict]]) -> None:
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)

    output_path = VALIDATION_DIR / "validation_summary.md"

    all_checks = sum(len(results) for results in all_results.values())
    all_passed = sum(1 for results in all_results.values() for result in results if result["passed"])
    all_failed = all_checks - all_passed

    lines = []
    lines.append("# Validation Summary")
    lines.append("")
    lines.append("This report summarizes dataset-level validation checks for interim source tables.")
    lines.append("")

    lines.append("## Overall Summary")
    lines.append("")
    lines.append(f"- Total checks run: {all_checks}")
    lines.append(f"- Total checks passed: {all_passed}")
    lines.append(f"- Total failed: {all_failed}")
    lines.append("")

    for file_name, results in all_results.items():
        lines.append(f"## {file_name}")
        lines.append("")
    
        total_checks = len(results)
        passed_checks = sum(1 for result in results if result["passed"])
        failed_checks = total_checks - passed_checks

        lines.append(f"- Total checks: {total_checks}")
        lines.append(f"- Passed: {passed_checks}")
        lines.append(f"- Failed: {failed_checks}")
        lines.append("")
        lines.append("| Check Type | Column | Passed | Details |")
        lines.append("|---|---|---|---|")

        for result in results:
            if result["check_type"] == "not_null":
                details = f"null_count={result['null_count']} of {result['total_rows']}"
            elif result["check_type"] == "unique":
                details = f"unique_count={result['unique_count']} of {result['total_rows']}"
            else:
                details = ""

        if not results:
            lines.append("- No validation rules configured for this table.")
            lines.append("")
            continue

        lines.append(
                f"| {result['check_type']} | {result['column']} | {result['passed']} | {details} |"
            )

        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote validation summary to {output_path}")

def main():

    csv_files = list(INTERIM_DIR.glob("*.csv"))

    if not csv_files:
        print("No interim CSV files found.")
        return
    
    all_results = {}
    
    for file_path in csv_files:
        print("-" * 60)
        print(f"Validating {file_path.name}")

        df = load_interim_csv(file_path)
        results = run_validations(df, file_path.name)
        all_results[file_path.name] = results

        total_checks = len(results)
        passed_checks = sum(1 for result in results if result["passed"])
        failed_checks = total_checks - passed_checks

        print(f"Total checks: {total_checks}")
        print(f"Passed: {passed_checks}")
        print(f"Failed: {failed_checks}")

    write_validation_summary(all_results)
          

if __name__ == "__main__":
    main()