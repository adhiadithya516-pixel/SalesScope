import pandas as pd


def apply_dashboard_filters(
    df: pd.DataFrame,
    start_date=None,
    end_date=None,
    categories=None,
    products=None,
    order_statuses=None,
    states=None
):
    """Apply dashboard filters without modifying the original dataset."""

    filtered = df.copy()

    if start_date is not None:
        start_date = pd.to_datetime(start_date)

        filtered = filtered[
            pd.to_datetime(
                filtered["order_purchase_timestamp"],
                errors="coerce"
            ) >= start_date
        ]

    if end_date is not None:
        end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1)

        filtered = filtered[
            pd.to_datetime(
                filtered["order_purchase_timestamp"],
                errors="coerce"
            ) < end_date
        ]

    if categories:
        filtered = filtered[
            filtered["product_category_name_english"].isin(categories)
        ]

    if products:
        filtered = filtered[
            filtered["product_id"].isin(products)
        ]

    if order_statuses:
        filtered = filtered[
            filtered["order_status"].isin(order_statuses)
        ]

    if states:
        filtered = filtered[
            filtered["customer_state"].isin(states)
        ]

    return filtered.reset_index(drop=True)