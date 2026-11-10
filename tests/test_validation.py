import pandas as pd

from src.data_validation import validate_sales_data


def test_valid_sales_data():

    df = pd.DataFrame({
        "Date": ["2026-01-01", "2026-01-02"],
        "Product": ["Laptop", "Mouse"],
        "Category": ["Electronics", "Accessories"],
        "Quantity": [2, 5],
        "Amount": [100000, 2500]
    })

    result = validate_sales_data(df)

    assert result["valid"] is True
    assert len(result["errors"]) == 0


def test_missing_columns():

    df = pd.DataFrame({
        "Date": ["2026-01-01"],
        "Product": ["Laptop"]
    })

    result = validate_sales_data(df)

    assert result["valid"] is False
    assert len(result["errors"]) > 0


def test_missing_values():

    df = pd.DataFrame({
        "Date": ["2026-01-01", None],
        "Product": ["Laptop", "Mouse"],
        "Category": ["Electronics", "Accessories"],
        "Quantity": [2, 5],
        "Amount": [100000, 2500]
    })

    result = validate_sales_data(df)

    assert result["valid"] is True
    assert len(result["warnings"]) > 0