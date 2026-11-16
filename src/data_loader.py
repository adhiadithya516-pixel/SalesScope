import pandas as pd
import time

from src.config import RAW_DATA_DIR, DATA_FILES


def load_dataset(dataset_name: str) -> pd.DataFrame:
    """
    Load a CSV dataset from the raw data directory.
    """

    if dataset_name not in DATA_FILES:
        raise ValueError(
            f"Unknown dataset: {dataset_name}. "
            f"Available datasets: {list(DATA_FILES.keys())}"
        )

    file_path = RAW_DATA_DIR / DATA_FILES[dataset_name]

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    df = pd.read_csv(
        file_path,
        low_memory=False
    )

    return df


def load_core_datasets() -> dict:
    """
    Load core datasets and measure individual loading times.
    """

    dataset_names = [
        "orders",
        "order_items",
        "products",
        "customers",
        "sellers",
        "payments",
        "reviews",
        "category_translation"
    ]

    datasets = {}

    total_start = time.perf_counter()

    for name in dataset_names:

        start = time.perf_counter()

        datasets[name] = load_dataset(name)

        elapsed = time.perf_counter() - start

        print(
            f"Loaded {name}: "
            f"{datasets[name].shape[0]:,} rows, "
            f"{datasets[name].shape[1]} columns "
            f"| Time: {elapsed:.2f} seconds"
        )

    total_elapsed = time.perf_counter() - total_start

    print(
        f"\nTotal CSV loading time: "
        f"{total_elapsed:.2f} seconds"
    )

    return datasets