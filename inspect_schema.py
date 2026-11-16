import pandas as pd
from pathlib import Path

RAW_DATA_DIR = Path("data/raw")

FILES = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_products_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "product_category_name_translation.csv"
]

print("\n========== OLIST STRUCTURAL DATA PROFILING ==========")

for filename in FILES:

    file_path = RAW_DATA_DIR / filename

    print("\n" + "=" * 65)
    print(f"DATASET: {filename}")
    print("=" * 65)

    df = pd.read_csv(file_path, low_memory=False)

    # 1. Dataset dimensions
    print("\n1. SHAPE")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    # 2. Column information
    print("\n2. COLUMN NAMES AND DATA TYPES")
    print(df.dtypes)

    # 3. Missing values
    print("\n3. MISSING VALUES")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.any() else "No missing values")

    # 4. Duplicate records
    print("\n4. DUPLICATE RECORDS")
    print("Duplicate rows:", df.duplicated().sum())

    # 5. Memory usage
    print("\n5. MEMORY USAGE")
    print(f"{df.memory_usage(deep=True).sum() / (1024 ** 2):.2f} MB")

print("\n========== PROFILING COMPLETED ==========")