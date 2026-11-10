from pathlib import Path

# Project directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Report directory
REPORTS_DIR = PROJECT_ROOT / "reports"

# Application configuration
APP_NAME = "SalesScope"
APP_VERSION = "1.0.0"

# Standard analytical schema
REQUIRED_COLUMNS = [
    "Date",
    "Product",
    "Category",
    "Quantity",
    "Amount"
]

# Column classifications
DATE_COLUMN = "Date"

CATEGORICAL_COLUMNS = [
    "Product",
    "Category"
]

NUMERIC_COLUMNS = [
    "Quantity",
    "Amount"
]