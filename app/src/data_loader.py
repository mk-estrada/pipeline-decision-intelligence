import pandas as pd
import streamlit as st
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@st.cache_data
def load_csv(filename: str) -> pd.DataFrame:
    """
    Load a CSV file from the data folder.
    Streamlit caches this so the app does not reload the file unnecessarily.
    """
    file_path = DATA_DIR / filename
    

    if not file_path.exists():
        raise FileNotFoundError(f"Could not find file: {file_path}")
    
    df = pd.read_csv(file_path)

    # Standardize column names
    df.columns = df.columns.str.lower()

    return df


@st.cache_data
def load_all_data() -> dict:
    """
    Load all core app datasets.
    """
    return {
        "summary": load_csv("mart_pipeline_summary.csv"),
        "health": load_csv("mart_open_pipeline_health.csv"),
        "region": load_csv("mart_pipeline_by_region.csv"),
        "deal_size": load_csv("mart_pipeline_by_deal_size.csv"),
        "forecast": load_csv("fct_pipeline_forecast.csv"),
    }