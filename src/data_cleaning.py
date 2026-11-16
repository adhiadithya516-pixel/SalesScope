import pandas as pd

from src.config import (
    UNTRANSLATED_CATEGORIES,
    CATEGORY_FALLBACK,
)


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Convert order timestamp columns to datetime."""

    df = df.copy()

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
                format="mixed",
            )

    return df


def clean_order_items(df: pd.DataFrame) -> pd.DataFrame:
    """Convert order item price and freight values to numeric."""

    df = df.copy()

    numeric_columns = [
        "price",
        "freight_value",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    return df


def clean_products(
    df: pd.DataFrame,
    translation_df: pd.DataFrame,
) -> pd.DataFrame:
    """Translate product categories into English."""

    df = df.copy()

    translation_map = dict(
        zip(
            translation_df["product_category_name"],
            translation_df["product_category_name_english"],
        )
    )

    translated = (
        df["product_category_name"]
        .map(translation_map)
        .astype("string")
    )

    fallback = (
        df["product_category_name"]
        .map(UNTRANSLATED_CATEGORIES)
        .astype("string")
    )

    df["product_category_name_english"] = (
        translated
        .fillna(fallback)
        .fillna(CATEGORY_FALLBACK)
    )

    return df


def clean_payments(df: pd.DataFrame) -> pd.DataFrame:
    """Convert payment values to numeric."""

    df = df.copy()

    if "payment_value" in df.columns:
        df["payment_value"] = pd.to_numeric(
            df["payment_value"],
            errors="coerce",
        )

    return df


def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """Convert review scores to numeric."""

    df = df.copy()

    if "review_score" in df.columns:
        df["review_score"] = pd.to_numeric(
            df["review_score"],
            errors="coerce",
        )

    return df


def clean_datasets(datasets: dict) -> dict:
    """Apply cleaning functions to all relevant datasets."""

    cleaned = datasets.copy()

    cleaned["orders"] = clean_orders(datasets["orders"])

    cleaned["order_items"] = clean_order_items(
        datasets["order_items"]
    )

    cleaned["products"] = clean_products(
        datasets["products"],
        datasets["category_translation"],
    )

    cleaned["payments"] = clean_payments(
        datasets["payments"]
    )

    cleaned["reviews"] = clean_reviews(
        datasets["reviews"]
    )

    return cleaned