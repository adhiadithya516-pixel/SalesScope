import pandas as pd


def _validate_category_data(df):
    required_columns = [
        "product_category_name_english",
        "product_id",
        "order_id",
        "order_status",
        "price"
    ]

    missing = [column for column in required_columns if column not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def get_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate sales performance for each product category."""

    _validate_category_data(df)

    delivered = df[df["order_status"] == "delivered"].copy()

    summary = (
        delivered.groupby("product_category_name_english")
        .agg(
            category_sales=("price", "sum"),
            product_count=("product_id", "nunique"),
            order_count=("order_id", "nunique"),
            order_item_count=("product_id", "count")
        )
        .reset_index()
        .rename(columns={
            "product_category_name_english": "category"
        })
    )

    total_sales = summary["category_sales"].sum()

    summary["sales_contribution_percent"] = (
        summary["category_sales"] / total_sales * 100
    )

    return summary.sort_values(
        "category_sales",
        ascending=False
    ).reset_index(drop=True)


def get_top_categories(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """Return the highest-performing categories by sales."""

    if top_n < 1:
        raise ValueError("top_n must be at least 1")

    return get_category_summary(df).head(top_n)


def get_category_order_ranking(
    df: pd.DataFrame,
    top_n: int = 5
) -> pd.DataFrame:
    """Rank categories by number of distinct orders."""

    if top_n < 1:
        raise ValueError("top_n must be at least 1")

    summary = get_category_summary(df)

    return summary.sort_values(
        ["order_count", "category_sales"],
        ascending=False
    ).head(top_n).reset_index(drop=True)