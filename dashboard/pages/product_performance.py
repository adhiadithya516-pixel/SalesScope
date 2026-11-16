import streamlit as st
import plotly.express as px

from dashboard.data_service import load_dashboard_data
from dashboard.components.filters import display_sidebar_filters

from src.product_analysis import (
    get_product_summary,
    get_top_products,
    get_top_products_by_orders
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.title("Product Performance")

st.caption(
    "Discover best-selling products and product performance."
)


try:

    # ==================================================
    # LOAD DATA
    # ==================================================

    with st.spinner("Loading product analytics..."):

        datasets, master = load_dashboard_data()

    if master.empty:
        st.warning("No product data available.")
        st.stop()


    # ==================================================
    # APPLY DASHBOARD FILTERS
    # ==================================================

    filtered_master = display_sidebar_filters(master)

    if filtered_master.empty:
        st.warning("No records match the selected filters.")
        st.stop()


    # ==================================================
    # PRODUCT SUMMARY
    # ==================================================

    summary = get_product_summary(filtered_master)

    if summary.empty:
        st.warning("No product sales data available.")
        st.stop()


    # ==================================================
    # PRODUCT KPI CARDS
    # ==================================================

    total_products = summary["product_id"].nunique()

    top_product = summary.iloc[0]

    total_categories = (
        summary["product_category_name_english"].nunique()
    )

    st.subheader("Product Performance Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Products Sold",
        f"{total_products:,}"
    )

    col2.metric(
        "Top Product Sales",
        f"R$ {top_product['product_sales_value']:,.2f}"
    )

    col3.metric(
        "Product Categories",
        f"{total_categories:,}"
    )


    st.divider()


    # ==================================================
    # TOP 10 PRODUCTS BY SALES
    # ==================================================

    st.subheader("Top 10 Products by Sales")

    top_sales = get_top_products(
        filtered_master,
        top_n=10
    )

    if not top_sales.empty:

        fig = px.bar(
            top_sales,
            x="product_sales_value",
            y="product_id",
            orientation="h",
            title="Top Products by Sales Value",
            labels={
                "product_sales_value": "Sales (R$)",
                "product_id": "Product ID"
            }
        )

        fig.update_layout(
            template="plotly_white",
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    else:
        st.info("No product sales data available.")


    st.divider()


    # ==================================================
    # MOST FREQUENTLY ORDERED PRODUCTS
    # ==================================================

    st.subheader("Most Frequently Ordered Products")

    top_orders = get_top_products_by_orders(
        filtered_master,
        top_n=10
    )

    if not top_orders.empty:

        fig = px.bar(
            top_orders,
            x="order_count",
            y="product_id",
            orientation="h",
            title="Top Products by Number of Orders",
            labels={
                "order_count": "Number of Orders",
                "product_id": "Product ID"
            }
        )

        fig.update_layout(
            template="plotly_white",
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    else:
        st.info("No order frequency data available.")


    st.divider()


    # ==================================================
    # COMPLETE PRODUCT PERFORMANCE
    # ==================================================

    st.subheader("Complete Product Performance")

    st.dataframe(
        summary,
        width="stretch",
        hide_index=True
    )


    # ==================================================
    # DOWNLOAD PRODUCT REPORT
    # ==================================================

    st.subheader("Download Product Report")

    csv_data = summary.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="Download Product Analysis CSV",
        data=csv_data,
        file_name="product_performance.csv",
        mime="text/csv"
    )


    # ==================================================
    # FILTERED DATA SUMMARY
    # ==================================================

    st.divider()

    st.subheader("Filtered Dataset Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Filtered Item Records",
        f"{len(filtered_master):,}"
    )

    col2.metric(
        "Unique Orders",
        f"{filtered_master['order_id'].nunique():,}"
    )

    col3.metric(
        "Unique Products",
        f"{filtered_master['product_id'].nunique():,}"
    )


except Exception as error:

    st.error(
        "An error occurred while loading Product Performance."
    )

    st.exception(error)