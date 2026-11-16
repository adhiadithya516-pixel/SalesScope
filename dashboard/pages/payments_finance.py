import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.data_service import load_dashboard_data

st.title("Payments & Finance")
st.caption("Explore payment methods and financial reconciliation.")

datasets, master = load_dashboard_data()

payments = datasets["payments"]
items = datasets["order_items"]
orders = datasets["orders"]

payment_total = payments["payment_value"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Payment Value", f"R$ {payment_total:,.2f}")
col2.metric("Payment Records", f"{len(payments):,}")
col3.metric("Payment Methods", f"{payments['payment_type'].nunique():,}")

st.divider()

st.subheader("Payment Method Analysis")

payment_summary = (
    payments.groupby("payment_type")
    .agg(
        payment_value=("payment_value", "sum"),
        transaction_count=("order_id", "count")
    )
    .reset_index()
    .sort_values("payment_value", ascending=False)
)

fig = px.pie(
    payment_summary,
    names="payment_type",
    values="payment_value",
    hole=0.45,
    title="Payment Value by Method"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(
    payment_summary,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Financial Reconciliation")

st.write(
    "Compare aggregated order-item value (product price + freight) "
    "against aggregated payment value."
)

item_totals = (
    items.groupby("order_id")
    .agg(
        product_value=("price", "sum"),
        freight_value=("freight_value", "sum")
    )
)

item_totals["item_plus_freight"] = (
    item_totals["product_value"] + item_totals["freight_value"]
)

payment_totals = (
    payments.groupby("order_id")["payment_value"]
    .sum()
    .rename("payment_value")
)

reconciliation = (
    orders[["order_id", "order_status"]]
    .set_index("order_id")
    .join(item_totals)
    .join(payment_totals)
)

reconciliation["difference"] = (
    reconciliation["payment_value"]
    - reconciliation["item_plus_freight"]
)

reconciliation["reconciliation_status"] = "Matched"

reconciliation.loc[
    reconciliation["payment_value"].isna(),
    "reconciliation_status"
] = "Missing Payment"

reconciliation.loc[
    reconciliation["item_plus_freight"].isna(),
    "reconciliation_status"
] = "Missing Items"

mismatch = (
    reconciliation["payment_value"].notna()
    & reconciliation["item_plus_freight"].notna()
    & (reconciliation["difference"].abs() > 0.01)
)

reconciliation.loc[
    mismatch,
    "reconciliation_status"
] = "Unexplained Difference"

col1, col2, col3 = st.columns(3)

col1.metric("Unexplained Differences", f"{int(mismatch.sum()):,}")

col2.metric(
    "Missing Payment Orders",
    f"{int(reconciliation['payment_value'].isna().sum()):,}"
)

col3.metric(
    "Missing Item Orders",
    f"{int(reconciliation['item_plus_freight'].isna().sum()):,}"
)

st.subheader("Reconciliation Exceptions")

exceptions = reconciliation[
    reconciliation["reconciliation_status"] != "Matched"
].reset_index()

st.dataframe(
    exceptions,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "Download Reconciliation Report",
    exceptions.to_csv(index=False).encode("utf-8-sig"),
    file_name="financial_reconciliation.csv",
    mime="text/csv"
)

st.caption(
    "Payment values are not treated as product revenue. "
    "Differences are flagged, not automatically corrected."
)