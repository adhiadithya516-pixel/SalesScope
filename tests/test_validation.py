import pandas as pd

from src.data_validation import validate_datasets


def create_valid_datasets():
    """Create small valid Olist datasets for testing."""

    return {
        "orders": pd.DataFrame({
            "order_id": ["O1", "O2"],
            "customer_id": ["C1", "C2"],
            "order_status": ["delivered", "delivered"],
            "order_purchase_timestamp": [
                "2018-01-01",
                "2018-01-02"
            ]
        }),

        "order_items": pd.DataFrame({
            "order_id": ["O1", "O2"],
            "product_id": ["P1", "P2"],
            "seller_id": ["S1", "S2"],
            "price": [100.0, 200.0],
            "freight_value": [10.0, 20.0]
        }),

        "products": pd.DataFrame({
            "product_id": ["P1", "P2"],
            "product_category_name_english": [
                "electronics",
                "computers"
            ]
        }),

        "customers": pd.DataFrame({
            "customer_id": ["C1", "C2"],
            "customer_unique_id": ["U1", "U2"]
        }),

        "sellers": pd.DataFrame({
            "seller_id": ["S1", "S2"]
        }),

        "payments": pd.DataFrame({
            "order_id": ["O1", "O2"],
            "payment_value": [110.0, 220.0],
            "payment_type": ["credit_card", "boleto"]
        }),

        "reviews": pd.DataFrame({
            "order_id": ["O1", "O2"],
            "review_score": [5, 4]
        }),

        "category_translation": pd.DataFrame({
            "product_category_name": [
                "eletronicos",
                "computadores"
            ],
            "product_category_name_english": [
                "electronics",
                "computers"
            ]
        })
    }


def test_valid_datasets():
    datasets = create_valid_datasets()

    result = validate_datasets(datasets)

    assert result["valid"] is True
    assert len(result["errors"]) == 0


def test_missing_dataset():
    datasets = create_valid_datasets()
    datasets.pop("payments")

    result = validate_datasets(datasets)

    assert result["valid"] is False
    assert any("Missing datasets" in error for error in result["errors"])


def test_missing_required_columns():
    datasets = create_valid_datasets()

    datasets["orders"] = datasets["orders"].drop(
        columns=["customer_id"]
    )

    result = validate_datasets(datasets)

    assert result["valid"] is False
    assert any("missing columns" in error for error in result["errors"])


def test_duplicate_primary_key():
    datasets = create_valid_datasets()

    datasets["orders"].loc[1, "order_id"] = "O1"

    result = validate_datasets(datasets)

    assert result["valid"] is False
    assert any("duplicate primary key" in error for error in result["errors"])


def test_unmatched_foreign_key():
    datasets = create_valid_datasets()

    datasets["order_items"].loc[0, "product_id"] = "INVALID"

    result = validate_datasets(datasets)

    assert result["valid"] is False
    assert any("unmatched values" in error for error in result["errors"])


def test_invalid_financial_value():
    datasets = create_valid_datasets()

    # Convert column to object before inserting invalid text
    datasets["order_items"]["price"] = (
        datasets["order_items"]["price"].astype(object)
    )

    datasets["order_items"].loc[0, "price"] = "invalid"

    result = validate_datasets(datasets)

    assert result["valid"] is False
    assert any(
        "invalid or missing values" in error
        for error in result["errors"]
    )


def test_negative_financial_value_generates_warning():
    datasets = create_valid_datasets()

    datasets["order_items"].loc[0, "price"] = -100

    result = validate_datasets(datasets)

    assert result["valid"] is True
    assert any("negative values" in warning for warning in result["warnings"])


def test_invalid_review_score():
    datasets = create_valid_datasets()

    datasets["reviews"].loc[0, "review_score"] = 7

    result = validate_datasets(datasets)

    assert result["valid"] is False
    assert any("invalid review scores" in error for error in result["errors"])


def test_invalid_purchase_date_generates_warning():
    datasets = create_valid_datasets()

    datasets["orders"].loc[0, "order_purchase_timestamp"] = "invalid-date"

    result = validate_datasets(datasets)

    assert result["valid"] is True
    assert any("purchase timestamps" in warning for warning in result["warnings"])


def test_missing_category_generates_warning():
    datasets = create_valid_datasets()

    datasets["products"].loc[
        0, "product_category_name_english"
    ] = None

    result = validate_datasets(datasets)

    assert result["valid"] is True
    assert any("without English category labels" in warning for warning in result["warnings"])


def test_exact_duplicate_records_generate_warning():
    datasets = create_valid_datasets()

    datasets["payments"] = pd.concat(
        [
            datasets["payments"],
            datasets["payments"].iloc[[0]]
        ],
        ignore_index=True
    )

    result = validate_datasets(datasets)

    assert result["valid"] is True
    assert any("exact duplicate rows" in warning for warning in result["warnings"])