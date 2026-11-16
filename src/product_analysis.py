import pandas as pd


def _validate_product_data(df):

    required_columns = [
        "product_id",
        "product_category_name_english",
        "order_id",
        "order_status",
        "price"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )


def get_product_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate sales metrics for each delivered product."""

    _validate_product_data(df)

    delivered = df[
        df["order_status"] == "delivered"
    ]

    summary = (
        delivered.groupby(
            ["product_id", "product_category_name_english"]
        )
        .agg(
            product_sales_value=("price", "sum"),
            order_count=("order_id", "nunique"),
            order_item_count=("order_item_id", "count")
        )
        .reset_index()
    )

    summary["sales_contribution_percent"] = (
        summary["product_sales_value"]
        / summary["product_sales_value"].sum()
        * 100
    )

    return summary.sort_values(
        "product_sales_value",
        ascending=False
    )


def get_top_products(
    df: pd.DataFrame,
    top_n: int = 5
) -> pd.DataFrame:
    """Return top products ranked by delivered product sales value."""

    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    return (
        get_product_summary(df)
        .head(top_n)
        .reset_index(drop=True)
    )


def get_top_products_by_orders(
    df: pd.DataFrame,
    top_n: int = 5
) -> pd.DataFrame:
    """Return products ranked by distinct delivered orders."""

    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    return (
        get_product_summary(df)
        .sort_values(
            ["order_count", "product_sales_value"],
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )