import pandas as pd

from src.data_cleaning import (
    clean_orders,
    clean_order_items,
    clean_products,
    clean_payments,
    clean_reviews,
    clean_datasets
)


def test_clean_orders_converts_dates():
    df = pd.DataFrame({
        "order_purchase_timestamp": ["2018-01-01", "2018-01-02"],
        "order_approved_at": ["2018-01-01", None],
        "order_delivered_carrier_date": [None, "2018-01-03"],
        "order_delivered_customer_date": ["2018-01-05", None],
        "order_estimated_delivery_date": ["2018-01-06", "2018-01-07"]
    })

    result = clean_orders(df)

    assert pd.api.types.is_datetime64_any_dtype(
        result["order_purchase_timestamp"]
    )
    assert pd.isna(result.loc[1, "order_approved_at"])


def test_clean_orders_preserves_original():
    df = pd.DataFrame({
        "order_purchase_timestamp": ["2018-01-01"],
        "order_approved_at": [None],
        "order_delivered_carrier_date": [None],
        "order_delivered_customer_date": [None],
        "order_estimated_delivery_date": [None]
    })

    clean_orders(df)

    assert isinstance(df.loc[0, "order_purchase_timestamp"], str)


def test_clean_order_items_converts_numeric_values():
    df = pd.DataFrame({
        "price": ["100.50", "200"],
        "freight_value": ["10.25", "20"]
    })

    result = clean_order_items(df)

    assert pd.api.types.is_numeric_dtype(result["price"])
    assert pd.api.types.is_numeric_dtype(result["freight_value"])
    assert result.loc[0, "price"] == 100.50


def test_clean_order_items_handles_invalid_values():
    df = pd.DataFrame({
        "price": ["100", "invalid"],
        "freight_value": ["10", "unknown"]
    })

    result = clean_order_items(df)

    assert pd.isna(result.loc[1, "price"])
    assert pd.isna(result.loc[1, "freight_value"])


def test_clean_products_translates_categories():
    products = pd.DataFrame({
        "product_category_name": ["beleza_saude", "informatica_acessorios"]
    })

    translations = pd.DataFrame({
        "product_category_name": [
            "beleza_saude",
            "informatica_acessorios"
        ],
        "product_category_name_english": [
            "health_beauty",
            "computers_accessories"
        ]
    })

    result = clean_products(products, translations)

    assert result.loc[0, "product_category_name_english"] == "health_beauty"
    assert result.loc[1, "product_category_name_english"] == "computers_accessories"


def test_clean_products_handles_untranslated_categories():
    products = pd.DataFrame({
        "product_category_name": [
            "pc_gamer",
            "portateis_cozinha_e_preparadores_de_alimentos"
        ]
    })

    translations = pd.DataFrame({
        "product_category_name": [],
        "product_category_name_english": []
    })

    result = clean_products(products, translations)

    assert result["product_category_name_english"].notna().all()


def test_clean_products_handles_missing_categories():
    products = pd.DataFrame({
        "product_category_name": [None, "unknown_category"]
    })

    translations = pd.DataFrame({
        "product_category_name": [],
        "product_category_name_english": []
    })

    result = clean_products(products, translations)

    assert (result["product_category_name_english"] == "Uncategorized").all()


def test_clean_payments_converts_numeric_values():
    df = pd.DataFrame({
        "payment_value": ["100.50", "250"]
    })

    result = clean_payments(df)

    assert pd.api.types.is_numeric_dtype(result["payment_value"])
    assert result.loc[0, "payment_value"] == 100.50


def test_clean_payments_handles_invalid_values():
    df = pd.DataFrame({
        "payment_value": ["100", "invalid"]
    })

    result = clean_payments(df)

    assert pd.isna(result.loc[1, "payment_value"])


def test_clean_reviews_converts_numeric_values():
    df = pd.DataFrame({
        "review_score": ["5", "4", "3"]
    })

    result = clean_reviews(df)

    assert pd.api.types.is_numeric_dtype(result["review_score"])
    assert result.loc[0, "review_score"] == 5


def test_clean_reviews_handles_invalid_values():
    df = pd.DataFrame({
        "review_score": ["5", "invalid"]
    })

    result = clean_reviews(df)

    assert pd.isna(result.loc[1, "review_score"])


def test_clean_datasets_integrates_cleaning_functions():
    datasets = {
        "orders": pd.DataFrame({
            "order_purchase_timestamp": ["2018-01-01"],
            "order_approved_at": [None],
            "order_delivered_carrier_date": [None],
            "order_delivered_customer_date": [None],
            "order_estimated_delivery_date": [None]
        }),
        "order_items": pd.DataFrame({
            "price": ["100"],
            "freight_value": ["10"]
        }),
        "products": pd.DataFrame({
            "product_category_name": ["beleza_saude"]
        }),
        "category_translation": pd.DataFrame({
            "product_category_name": ["beleza_saude"],
            "product_category_name_english": ["health_beauty"]
        }),
        "payments": pd.DataFrame({
            "payment_value": ["110"]
        }),
        "reviews": pd.DataFrame({
            "review_score": ["5"]
        })
    }

    result = clean_datasets(datasets)

    assert pd.api.types.is_datetime64_any_dtype(
        result["orders"]["order_purchase_timestamp"]
    )
    assert result["order_items"].loc[0, "price"] == 100
    assert result["products"].loc[0, "product_category_name_english"] == "health_beauty"
    assert result["payments"].loc[0, "payment_value"] == 110
    assert result["reviews"].loc[0, "review_score"] == 5