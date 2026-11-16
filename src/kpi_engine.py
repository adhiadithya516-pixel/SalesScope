import pandas as pd

from src.sales_analysis import get_sales_summary


def calculate_customer_metrics(orders, customers):
    """Calculate customer and repeat-purchase metrics."""

    customer_orders = orders.merge(
        customers[["customer_id", "customer_unique_id"]],
        on="customer_id",
        how="left",
        validate="one_to_one"
    )

    customer_order_counts = (
        customer_orders.groupby("customer_unique_id")["order_id"]
        .nunique()
    )

    total_customers = customer_order_counts.size
    repeat_customers = (customer_order_counts > 1).sum()

    repeat_rate = (
        repeat_customers / total_customers * 100
        if total_customers else 0
    )

    return {
        "total_customers": int(total_customers),
        "repeat_customers": int(repeat_customers),
        "repeat_customer_rate": round(float(repeat_rate), 2)
    }


def calculate_review_metrics(reviews):
    """Calculate customer review metrics."""

    scores = pd.to_numeric(
        reviews["review_score"],
        errors="coerce"
    ).dropna()

    return {
        "average_review_score": round(float(scores.mean()), 2)
        if not scores.empty else 0,
        "total_reviews": int(len(scores)),
        "positive_reviews": int((scores >= 4).sum()),
        "negative_reviews": int((scores <= 2).sum())
    }


def calculate_payment_metrics(payments):
    """Calculate payment metrics without mixing them with product sales."""

    payment_values = pd.to_numeric(
        payments["payment_value"],
        errors="coerce"
    ).dropna()

    payment_methods = (
        payments["payment_type"]
        .value_counts()
        .to_dict()
    )

    return {
        "total_payment_value": round(float(payment_values.sum()), 2),
        "total_payment_records": int(len(payment_values)),
        "payment_methods": payment_methods
    }


def calculate_delivery_metrics(orders):
    """Calculate delivery performance."""

    delivered = orders[
        orders["order_status"] == "delivered"
    ].copy()

    delivered["order_delivered_customer_date"] = pd.to_datetime(
        delivered["order_delivered_customer_date"],
        errors="coerce"
    )

    delivered["order_estimated_delivery_date"] = pd.to_datetime(
        delivered["order_estimated_delivery_date"],
        errors="coerce"
    )

    valid_dates = delivered.dropna(
        subset=[
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    )

    delayed_orders = (
        valid_dates["order_delivered_customer_date"]
        > valid_dates["order_estimated_delivery_date"]
    ).sum()

    total_valid_deliveries = len(valid_dates)

    delayed_rate = (
        delayed_orders / total_valid_deliveries * 100
        if total_valid_deliveries else 0
    )

    average_delivery_days = (
        (
            valid_dates["order_delivered_customer_date"]
            - pd.to_datetime(
                valid_dates["order_purchase_timestamp"],
                errors="coerce"
            )
        ).dt.total_seconds().div(86400).mean()
    )

    return {
        "delayed_orders": int(delayed_orders),
        "delayed_delivery_rate": round(float(delayed_rate), 2),
        "average_delivery_days": round(float(average_delivery_days), 2)
        if pd.notna(average_delivery_days) else 0
    }


def get_dashboard_kpis(datasets, master):
    """Build the consolidated KPI dictionary for the dashboard."""

    sales = get_sales_summary(master)

    customer_metrics = calculate_customer_metrics(
        datasets["orders"],
        datasets["customers"]
    )

    review_metrics = calculate_review_metrics(
        datasets["reviews"]
    )

    payment_metrics = calculate_payment_metrics(
        datasets["payments"]
    )

    delivery_metrics = calculate_delivery_metrics(
        datasets["orders"]
    )

    return {
        **sales,
        **customer_metrics,
        **review_metrics,
        **payment_metrics,
        **delivery_metrics,
        "total_orders": int(datasets["orders"]["order_id"].nunique()),
        "canceled_orders": int(
            (datasets["orders"]["order_status"] == "canceled").sum()
        ),
        "unavailable_orders": int(
            (datasets["orders"]["order_status"] == "unavailable").sum()
        )
    }