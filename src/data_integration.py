import pandas as pd


# ==========================================
# PRODUCT INTEGRATION
# ==========================================

def integrate_products(
    order_items: pd.DataFrame,
    products: pd.DataFrame
) -> pd.DataFrame:

    integrated = order_items.merge(
        products,
        on="product_id",
        how="left",
        validate="many_to_one"
    )

    # Create one standardized category column
    if "product_category_name_english" in integrated.columns:
        integrated["category"] = (
            integrated["product_category_name_english"]
            .fillna(integrated["product_category_name"])
        )
    else:
        integrated["category"] = integrated["product_category_name"]

    integrated["category"] = (
        integrated["category"]
        .fillna("Uncategorized")
        .astype(str)
    )

    return integrated


# ==========================================
# CUSTOMER INTEGRATION
# ==========================================

def integrate_customers(
    orders: pd.DataFrame,
    customers: pd.DataFrame
) -> pd.DataFrame:

    integrated = orders.merge(
        customers,
        on="customer_id",
        how="left",
        validate="one_to_one"
    )

    return integrated


# ==========================================
# SELLER INTEGRATION
# ==========================================

def integrate_sellers(
    order_items: pd.DataFrame,
    sellers: pd.DataFrame
) -> pd.DataFrame:

    integrated = order_items.merge(
        sellers,
        on="seller_id",
        how="left",
        validate="many_to_one"
    )

    return integrated


# ==========================================
# ORDER INTEGRATION
# ==========================================

def integrate_orders(
    order_items: pd.DataFrame,
    orders: pd.DataFrame
) -> pd.DataFrame:

    integrated = order_items.merge(
        orders,
        on="order_id",
        how="left",
        validate="many_to_one"
    )

    return integrated


# ==========================================
# PAYMENT AGGREGATION
# ==========================================

def aggregate_payments(
    payments: pd.DataFrame
) -> pd.DataFrame:

    # Numerical payment summaries
    aggregated = (
        payments.groupby("order_id", sort=False)
        .agg(
            total_payment=("payment_value", "sum"),
            payment_record_count=("payment_value", "count"),
            payment_method_count=("payment_type", "nunique")
        )
        .reset_index()
    )

    # Extract unique, non-null payment methods
    unique_methods = (
        payments[["order_id", "payment_type"]]
        .dropna(subset=["payment_type"])
        .drop_duplicates()
        .sort_values(
            ["order_id", "payment_type"],
            kind="stable"
        )
    )

    # Concatenate sorted payment methods by order
    payment_methods = (
        unique_methods.groupby("order_id", sort=False)["payment_type"]
        .agg(", ".join)
    )

    # Attach payment method summaries
    aggregated["payment_methods"] = (
        aggregated["order_id"]
        .map(payment_methods)
        .fillna("")
    )

    return aggregated


# ==========================================
# REVIEW AGGREGATION
# ==========================================

def aggregate_reviews(
    reviews: pd.DataFrame
) -> pd.DataFrame:

    aggregated = (
        reviews.groupby("order_id")
        .agg(
            average_review_score=("review_score", "mean"),
            review_count=("review_score", "count")
        )
        .reset_index()
    )

    return aggregated


# ==========================================
# MASTER ANALYTICAL DATASET
# ==========================================

def build_master_dataset(
    datasets: dict
) -> pd.DataFrame:
    """
    Build the master analytical dataset.

    Grain: One row per order item.

    Payments and reviews are aggregated before joining
    to prevent row multiplication.
    """

    # 1. Integrate product information
    master = integrate_products(
        datasets["order_items"],
        datasets["products"]
    )

    # 2. Integrate seller information
    master = integrate_sellers(
        master,
        datasets["sellers"]
    )

    # 3. Integrate customer information into orders
    orders_with_customers = integrate_customers(
        datasets["orders"],
        datasets["customers"]
    )

    # 4. Integrate orders and customer information
    master = master.merge(
        orders_with_customers,
        on="order_id",
        how="left",
        validate="many_to_one"
    )

    # 5. Aggregate payments separately
    payment_summary = aggregate_payments(
        datasets["payments"]
    )

    master = master.merge(
        payment_summary,
        on="order_id",
        how="left",
        validate="many_to_one"
    )

    # 6. Aggregate reviews separately
    review_summary = aggregate_reviews(
        datasets["reviews"]
    )

    master = master.merge(
        review_summary,
        on="order_id",
        how="left",
        validate="many_to_one"
    )

    # 7. Verify final dataset structure
    if len(master) != len(datasets["order_items"]):
        raise ValueError(
            "Master dataset row count does not match "
            "the original order items dataset."
        )

    if master["order_id"].isna().any():
        raise ValueError(
            "Some order items have missing order information."
        )

    if "category" not in master.columns:
        raise ValueError(
            "Category column was not created during integration."
        )

    return master