import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.data_service import load_dashboard_data
from dashboard.components.filters import display_sidebar_filters


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.title("Payments & Finance")
st.caption(
    "Explore payment methods, transaction values "
    "and financial reconciliation."
)


# ==========================================
# LOAD DATA
# ==========================================

datasets, master = load_dashboard_data()

# Apply shared dashboard filters
filtered_master = display_sidebar_filters(master)

if filtered_master.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


# Identify orders included in the filtered dataset
selected_order_ids = filtered_master["order_id"].unique()

# Filter related datasets
payments = datasets["payments"][
    datasets["payments"]["order_id"].isin(selected_order_ids)
].copy()

items = datasets["order_items"][
    datasets["order_items"]["order_id"].isin(selected_order_ids)
].copy()

orders = datasets["orders"][
    datasets["orders"]["order_id"].isin(selected_order_ids)
].copy()


if payments.empty:
    st.warning("No payment records available for the selected filters.")
    st.stop()


# ==========================================
# PAYMENT OVERVIEW
# ==========================================

st.subheader("Payment Overview")

payment_total = payments["payment_value"].sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Payment Value",
    f"R$ {payment_total:,.2f}"
)

col2.metric(
    "Payment Records",
    f"{len(payments):,}"
)

col3.metric(
    "Payment Methods",
    f"{payments['payment_type'].nunique():,}"
)

st.divider()


# ==========================================
# PAYMENT METHOD ANALYSIS
# ==========================================

st.subheader("Payment Method Analysis")

payment_summary = (
    payments.groupby("payment_type", dropna=False)
    .agg(
        payment_value=("payment_value", "sum"),
        transaction_count=("order_id", "count")
    )
    .reset_index()
    .sort_values("payment_value", ascending=False)
)

# Payment distribution chart
fig = px.pie(
    payment_summary,
    names="payment_type",
    values="payment_value",
    hole=0.45,
    title="Payment Value by Method"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.subheader("Payment Method Summary")

st.dataframe(
    payment_summary,
    width="stretch",
    hide_index=True
)

# Download payment summary
st.download_button(
    "Download Payment Summary",
    payment_summary.to_csv(index=False).encode("utf-8-sig"),
    file_name="payment_method_summary.csv",
    mime="text/csv"
)

st.divider()


# ==========================================
# FINANCIAL RECONCILIATION
# ==========================================

st.subheader("Financial Reconciliation")

st.write(
    "Compare aggregated order-item value "
    "(product price + freight) against aggregated payment value."
)


# Calculate product and freight totals
item_totals = (
    items.groupby("order_id")
    .agg(
        product_value=("price", "sum"),
        freight_value=("freight_value", "sum")
    )
)

item_totals["item_plus_freight"] = (
    item_totals["product_value"]
    + item_totals["freight_value"]
)


# Calculate payment totals
payment_totals = (
    payments.groupby("order_id")["payment_value"]
    .sum()
    .rename("payment_value")
)


# Combine financial information
reconciliation = (
    orders[["order_id", "order_status"]]
    .set_index("order_id")
    .join(item_totals)
    .join(payment_totals)
)


# Calculate difference
reconciliation["difference"] = (
    reconciliation["payment_value"]
    - reconciliation["item_plus_freight"]
)


# Classify reconciliation status
reconciliation["reconciliation_status"] = "Matched"

reconciliation.loc[
    reconciliation["payment_value"].isna(),
    "reconciliation_status"
] = "Missing Payment"

reconciliation.loc[
    reconciliation["item_plus_freight"].isna(),
    "reconciliation_status"
] = "Missing Items"


# Identify unexplained differences
mismatch = (
    reconciliation["payment_value"].notna()
    & reconciliation["item_plus_freight"].notna()
    & (reconciliation["difference"].abs() > 0.01)
)

reconciliation.loc[
    mismatch,
    "reconciliation_status"
] = "Unexplained Difference"


# ==========================================
# RECONCILIATION KPI CARDS
# ==========================================

st.subheader("Reconciliation Summary")

missing_payments = reconciliation["payment_value"].isna().sum()

missing_items = reconciliation["item_plus_freight"].isna().sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Unexplained Differences",
    f"{int(mismatch.sum()):,}"
)

col2.metric(
    "Missing Payment Orders",
    f"{int(missing_payments):,}"
)

col3.metric(
    "Missing Item Orders",
    f"{int(missing_items):,}"
)


# ==========================================
# RECONCILIATION EXCEPTIONS
# ==========================================

st.divider()

st.subheader("Reconciliation Exceptions")

exceptions = reconciliation[
    reconciliation["reconciliation_status"] != "Matched"
].reset_index()

if exceptions.empty:
    st.success("No reconciliation exceptions found.")

else:
    st.dataframe(
        exceptions,
        width="stretch",
        hide_index=True
    )

    st.download_button(
        "Download Reconciliation Report",
        exceptions.to_csv(index=False).encode("utf-8-sig"),
        file_name="financial_reconciliation.csv",
        mime="text/csv"
    )


# ==========================================
# FINANCIAL INTERPRETATION
# ==========================================

st.divider()

st.caption(
    "Payment values are not treated as product revenue. "
    "Financial differences are flagged for investigation "
    "and are not automatically corrected."
)

st.caption(
    "Reconciliation results follow the selected dashboard filters. "
    "Orders without order-item records are included when no "
    "filters exclude them."
)