import pandas as pd
import numpy as np

from src.config import REQUIRED_COLUMNS


def validate_sales_data(df):

    errors = []
    warnings = []

    # 1. Check whether dataset is empty
    if df.empty:
        errors.append("Dataset is empty.")
        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings
        }

    # 2. Check required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing required columns: {missing_columns}"
        )

        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings
        }

    # 3. Check missing values
    missing_values = df[REQUIRED_COLUMNS].isnull().sum()

    for column, count in missing_values.items():
        if count > 0:
            warnings.append(
                f"{column} contains {count} missing values."
            )

    # 4. Validate date values
    parsed_dates = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    invalid_dates = parsed_dates.isna().sum()

    if invalid_dates > 0:
        warnings.append(
            f"Found {invalid_dates} invalid or missing dates."
        )

    # 5. Validate numeric columns
    for column in ["Quantity", "Amount"]:

        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        invalid_count = numeric_values.isna().sum()

        if invalid_count > 0:
            warnings.append(
                f"{column} contains {invalid_count} "
                "invalid or missing numeric values."
            )

        non_finite_count = (
            numeric_values.notna()
            & ~np.isfinite(numeric_values)
        ).sum()

        if non_finite_count > 0:
            warnings.append(
                f"{column} contains {non_finite_count} "
                "non-finite values."
            )

    # 6. Check categorical columns
    for column in ["Product", "Category"]:

        blank_count = (
            df[column]
            .astype("string")
            .str.strip()
            .eq("")
            .sum()
        )

        if blank_count > 0:
            warnings.append(
                f"{column} contains {blank_count} blank values."
            )

    # 7. Detect potential duplicate records
    duplicate_count = df.duplicated(
        subset=REQUIRED_COLUMNS
    ).sum()

    if duplicate_count > 0:
        warnings.append(
            f"Found {duplicate_count} potential duplicate records."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }