import pandas as pd
import numpy as np


# ==========================================
# REQUIRED DATASET COLUMNS
# ==========================================

REQUIRED_COLUMNS = {
    "orders": [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp"
    ],

    "order_items": [
        "order_id",
        "product_id",
        "seller_id",
        "price",
        "freight_value"
    ],

    "products": [
        "product_id",
        "product_category_name_english"
    ],

    "customers": [
        "customer_id",
        "customer_unique_id"
    ],

    "sellers": [
        "seller_id"
    ],

    "payments": [
        "order_id",
        "payment_value",
        "payment_type"
    ],

    "reviews": [
        "order_id",
        "review_score"
    ],

    "category_translation": [
        "product_category_name",
        "product_category_name_english"
    ]
}


# ==========================================
# PRIMARY KEYS
# ==========================================

PRIMARY_KEYS = {
    "orders": "order_id",
    "customers": "customer_id",
    "products": "product_id",
    "sellers": "seller_id"
}


# ==========================================
# VALIDATION ENGINE
# ==========================================

def validate_datasets(datasets: dict) -> dict:

    errors = []
    warnings = []

    # 1. Check required datasets

    missing_datasets = [
        name for name in REQUIRED_COLUMNS
        if name not in datasets
    ]

    if missing_datasets:
        errors.append(
            f"Missing datasets: {missing_datasets}"
        )

        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings
        }

    # 2. Check empty datasets and required columns

    for name, required_columns in REQUIRED_COLUMNS.items():

        df = datasets[name]

        if df.empty:
            errors.append(
                f"{name} dataset is empty."
            )
            continue

        missing_columns = [
            column for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            errors.append(
                f"{name} is missing columns: {missing_columns}"
            )

    if errors:
        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings
        }

    # 3. Check primary key uniqueness

    for name, key in PRIMARY_KEYS.items():

        duplicate_count = (
            datasets[name][key].duplicated().sum()
        )

        if duplicate_count > 0:
            errors.append(
                f"{name}: {duplicate_count} duplicate "
                f"primary key values in {key}."
            )

    # 4. Check foreign key relationships

    relationships = [
        ("orders", "customer_id", "customers", "customer_id"),
        ("order_items", "order_id", "orders", "order_id"),
        ("order_items", "product_id", "products", "product_id"),
        ("order_items", "seller_id", "sellers", "seller_id"),
        ("payments", "order_id", "orders", "order_id"),
        ("reviews", "order_id", "orders", "order_id")
    ]

    for child, child_key, parent, parent_key in relationships:

        unmatched = (
            ~datasets[child][child_key].isin(
                datasets[parent][parent_key]
            )
        ).sum()

        if unmatched > 0:
            errors.append(
                f"{child}.{child_key} contains "
                f"{unmatched} unmatched values "
                f"against {parent}.{parent_key}."
            )

    # 5. Validate financial columns

    financial_columns = {
        "order_items": ["price", "freight_value"],
        "payments": ["payment_value"]
    }

    for dataset_name, columns in financial_columns.items():

        df = datasets[dataset_name]

        for column in columns:

            values = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            invalid_count = values.isna().sum()

            if invalid_count > 0:
                errors.append(
                    f"{dataset_name}.{column} contains "
                    f"{invalid_count} invalid or missing values."
                )

            negative_count = (
                values.notna() & (values < 0)
            ).sum()

            if negative_count > 0:
                warnings.append(
                    f"{dataset_name}.{column} contains "
                    f"{negative_count} negative values."
                )

            non_finite_count = (
                values.notna() & ~np.isfinite(values)
            ).sum()

            if non_finite_count > 0:
                errors.append(
                    f"{dataset_name}.{column} contains "
                    f"{non_finite_count} non-finite values."
                )

    # 6. Validate review scores

    review_scores = pd.to_numeric(
        datasets["reviews"]["review_score"],
        errors="coerce"
    )

    invalid_reviews = (
        review_scores.isna()
        | ~review_scores.between(1, 5)
    ).sum()

    if invalid_reviews > 0:
        errors.append(
            f"Found {invalid_reviews} invalid review scores."
        )

    # 7. Validate order dates

    purchase_dates = pd.to_datetime(
        datasets["orders"]["order_purchase_timestamp"],
        errors="coerce",
        format="mixed"
    )

    invalid_dates = purchase_dates.isna().sum()

    if invalid_dates > 0:
        warnings.append(
            f"Found {invalid_dates} missing or invalid "
            "purchase timestamps."
        )

    # 8. Check product category labels

    missing_categories = (
        datasets["products"][
            "product_category_name_english"
        ].isna().sum()
    )

    if missing_categories > 0:
        warnings.append(
            f"Found {missing_categories} products "
            "without English category labels."
        )

    # 9. Check duplicate records

    for name, df in datasets.items():

        duplicate_count = df.duplicated().sum()

        if duplicate_count > 0:
            warnings.append(
                f"{name} contains {duplicate_count} "
                "exact duplicate rows."
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }