import pandas as pd


def get_weekly_sales_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """Compare weekly delivered sales with the previous week."""

    required_columns = [
        "order_id",
        "order_status",
        "order_purchase_timestamp",
        "price"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    data = df[df["order_status"] == "delivered"].copy()

    data["order_purchase_timestamp"] = pd.to_datetime(
        data["order_purchase_timestamp"],
        errors="coerce"
    )

    data["price"] = pd.to_numeric(
        data["price"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["order_purchase_timestamp", "price"]
    )

    if data.empty:
        return pd.DataFrame()

    data["week"] = (
        data["order_purchase_timestamp"]
        .dt.to_period("W")
        .dt.start_time
    )

    weekly = (
        data.groupby("week")
        .agg(
            weekly_sales=("price", "sum"),
            delivered_orders=("order_id", "nunique")
        )
        .reset_index()
        .sort_values("week")
    )

    weekly["average_order_value"] = (
        weekly["weekly_sales"] / weekly["delivered_orders"]
    )

    weekly["previous_week_sales"] = weekly["weekly_sales"].shift(1)

    weekly["sales_growth_percent"] = (
        (
            weekly["weekly_sales"] - weekly["previous_week_sales"]
        )
        / weekly["previous_week_sales"].replace(0, pd.NA)
    ) * 100

    weekly["previous_week_orders"] = (
        weekly["delivered_orders"].shift(1)
    )

    weekly["order_growth_percent"] = (
        (
            weekly["delivered_orders"] - weekly["previous_week_orders"]
        )
        / weekly["previous_week_orders"].replace(0, pd.NA)
    ) * 100

    return weekly.reset_index(drop=True)