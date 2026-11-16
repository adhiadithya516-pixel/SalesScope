import pandas as pd


# ==========================================
# SALES DATA VALIDATION
# ==========================================

def _validate_sales_data(df: pd.DataFrame):

    required_columns = [
        "order_id",
        "order_status",
        "order_purchase_timestamp",
        "price",
        "freight_value"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )


# ==========================================
# SALES SUMMARY
# ==========================================

def get_sales_summary(df: pd.DataFrame) -> dict:
    """
    Calculate overall delivered sales metrics.
    """

    _validate_sales_data(df)

    delivered = df[
        df["order_status"] == "delivered"
    ]

    total_sales = delivered["price"].sum()

    total_freight = delivered["freight_value"].sum()

    total_orders = delivered["order_id"].nunique()

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0 else 0
    )

    return {
        "total_product_sales": round(total_sales, 2),
        "total_freight": round(total_freight, 2),
        "delivered_orders": int(total_orders),
        "average_order_value": round(
            average_order_value, 2
        )
    }


# ==========================================
# SALES TREND ANALYSIS
# ==========================================

def get_sales_trend(
    df: pd.DataFrame,
    frequency: str = "D"
) -> pd.DataFrame:
    """
    Calculate delivered sales trends.

    Supported frequencies:
    D  = Daily
    W  = Weekly
    MS = Monthly
    """

    _validate_sales_data(df)

    if frequency not in ["D", "W", "MS"]:
        raise ValueError(
            "Frequency must be D, W or MS."
        )

    delivered = df[
        df["order_status"] == "delivered"
    ].copy()

    delivered["order_purchase_timestamp"] = (
        pd.to_datetime(
            delivered["order_purchase_timestamp"],
            errors="coerce"
        )
    )

    delivered = delivered.dropna(
        subset=["order_purchase_timestamp"]
    )

    trend = (
        delivered.groupby(
            pd.Grouper(
                key="order_purchase_timestamp",
                freq=frequency
            )
        )
        .agg(
            product_sales_value=("price", "sum"),
            freight_value=("freight_value", "sum"),
            order_count=("order_id", "nunique")
        )
        .reset_index()
    )

    trend["average_order_value"] = (
        trend["product_sales_value"]
        / trend["order_count"].replace(0, pd.NA)
    )

    trend["average_order_value"] = (
        trend["average_order_value"].fillna(0)
    )

    return trend


# ==========================================
# SALES BY ORDER STATUS
# ==========================================

def get_order_status_summary(
    orders: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate order counts by status.

    Uses the original orders dataset so orders
    without order-item records are preserved.
    """

    required_columns = [
        "order_id",
        "order_status"
    ]

    missing = [
        column for column in required_columns
        if column not in orders.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    return (
        orders.groupby("order_status")
        .agg(
            order_count=("order_id", "nunique")
        )
        .reset_index()
        .sort_values(
            "order_count",
            ascending=False
        )
    )