import streamlit as st
import pandas as pd


def display_sidebar_filters(master: pd.DataFrame) -> pd.DataFrame:
    """
    Display dashboard filters and return the filtered master dataset.

    Supported filters:
    - Purchase date
    - Product category
    - Product
    - Order status
    - Customer state
    """

    # Always start with a fresh copy of the original dataset
    filtered = master.copy()

    st.sidebar.header("Dashboard Filters")

    # -----------------------------------------
    # 1. DATE FILTER
    # -----------------------------------------

    dates = filtered["order_purchase_timestamp"].dropna()

    if dates.empty:
        st.sidebar.warning("No valid purchase dates available.")
        return filtered

    min_date = dates.min().date()
    max_date = dates.max().date()

    selected_dates = st.sidebar.date_input(
        "Purchase Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates

        filtered = filtered[
            filtered["order_purchase_timestamp"].dt.date.between(
                start_date,
                end_date
            )
        ]

    # -----------------------------------------
    # 2. CATEGORY FILTER
    # -----------------------------------------

    categories = sorted(
        master["category"].dropna().unique().tolist()
    )

    selected_categories = st.sidebar.multiselect(
        "Product Category",
        options=categories,
        default=[]
    )

    if selected_categories:
        filtered = filtered[
            filtered["category"].isin(selected_categories)
        ]

    # -----------------------------------------
    # 3. PRODUCT FILTER
    # -----------------------------------------

    selected_product = st.sidebar.text_input(
        "Search Product ID",
        placeholder="Enter a product ID..."
    ).strip()

    if selected_product:
        filtered = filtered[
            filtered["product_id"].astype(str).str.contains(
                selected_product,
                case=False,
                regex=False
            )
        ]

    # -----------------------------------------
    # 4. ORDER STATUS FILTER
    # -----------------------------------------

    statuses = sorted(
        master["order_status"].dropna().unique().tolist()
    )

    selected_statuses = st.sidebar.multiselect(
        "Order Status",
        options=statuses,
        default=[]
    )

    if selected_statuses:
        filtered = filtered[
            filtered["order_status"].isin(selected_statuses)
        ]

    # -----------------------------------------
    # 5. CUSTOMER STATE FILTER
    # -----------------------------------------

    states = sorted(
        master["customer_state"].dropna().unique().tolist()
    )

    selected_states = st.sidebar.multiselect(
        "Customer State",
        options=states,
        default=[]
    )

    if selected_states:
        filtered = filtered[
            filtered["customer_state"].isin(selected_states)
        ]

    # -----------------------------------------
    # 6. FILTER SUMMARY
    # -----------------------------------------

    st.sidebar.divider()

    st.sidebar.subheader("Filtered Dataset")

    st.sidebar.metric(
        "Item Records",
        f"{len(filtered):,}"
    )

    st.sidebar.metric(
        "Unique Orders",
        f"{filtered['order_id'].nunique():,}"
    )

    st.sidebar.metric(
        "Unique Products",
        f"{filtered['product_id'].nunique():,}"
    )

    return filtered.reset_index(drop=True)