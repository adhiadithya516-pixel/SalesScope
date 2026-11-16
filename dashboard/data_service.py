import time
import streamlit as st

from src.data_loader import load_core_datasets
from src.data_cleaning import clean_datasets
from src.data_integration import build_master_dataset


@st.cache_data
def load_dashboard_data():
    """Load, clean and integrate datasets for the dashboard."""

    total_start = time.perf_counter()

    start = time.perf_counter()
    raw_datasets = load_core_datasets()
    print(f"DATA LOADING TIME: {time.perf_counter() - start:.2f} seconds")

    start = time.perf_counter()
    datasets = clean_datasets(raw_datasets)
    print(f"DATA CLEANING TIME: {time.perf_counter() - start:.2f} seconds")

    start = time.perf_counter()
    master = build_master_dataset(datasets)
    print(f"DATA INTEGRATION TIME: {time.perf_counter() - start:.2f} seconds")

    print(f"TOTAL PIPELINE TIME: {time.perf_counter() - total_start:.2f} seconds")

    return datasets, master