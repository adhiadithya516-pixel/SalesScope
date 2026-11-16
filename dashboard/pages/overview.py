import streamlit as st

from dashboard.data_service import load_dashboard_data
from dashboard.components.filters import display_sidebar_filters
from dashboard.components.kpi_cards import display_kpi_cards
from dashboard.components.charts import (
    display_sales_chart,
    display_category_chart
)

from src.kpi_engine import get_dashboard_kpis
from src.sales_analysis import get_sales_trend
from src.category_analysis import get_category_summary
from src.product_analysis import get_top_products


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.title("SalesScope")
st.caption("RETAIL INTELLIGENCE")

st.markdown(
    "Retail performance. Product intelligence. Business insights."
)


try:

    # ==================================================
    # LOAD DATA
    # ==================================================

    with st.spinner("Loading dashboard analytics..."):
        datasets, master = load_dashboard_data()

    if master.empty:
        st.warning("No data available.")
        st.stop()

    # ==================================================
    # APPLY DASHBOARD FILTERS
    # ==================================================

    filtered_master = display_sidebar_filters(master)


    if filtered_master.empty:
        st.warning("No records match the selected filters.")
        st.stop()


    # ==================================================
    # FILTER RELATED DATASETS
    # ==================================================

    selected_order_ids = (
        filtered_master["order_id"]
        .dropna()
        .unique()
    )

    filtered_datasets = datasets.copy()

    # Filter orders
    filtered_datasets["orders"] = datasets["orders"][
        datasets["orders"]["order_id"].isin(selected_order_ids)
    ].copy()

    # Filter customers
    selected_customer_ids = (
        filtered_datasets["orders"]["customer_id"]
        .dropna()
        .unique()
    )

    filtered_datasets["customers"] = datasets["customers"][
        datasets["customers"]["customer_id"].isin(
            selected_customer_ids
        )
    ].copy()

    # Filter payments
    filtered_datasets["payments"] = datasets["payments"][
        datasets["payments"]["order_id"].isin(selected_order_ids)
    ].copy()

    # Filter reviews
    filtered_datasets["reviews"] = datasets["reviews"][
        datasets["reviews"]["order_id"].isin(selected_order_ids)
    ].copy()


    # ==================================================
    # KPI CARDS
    # ==================================================

    st.subheader("Business Performance Overview")

    kpis = get_dashboard_kpis(
        filtered_datasets,
        filtered_master
    )

    display_kpi_cards(kpis)


    st.divider()


    # ==================================================
    # SALES PERFORMANCE
    # ==================================================

    st.subheader("Monthly Sales Performance")

    sales_trend = get_sales_trend(
        filtered_master,
        frequency="MS"
    )

    if not sales_trend.empty:

        display_sales_chart(sales_trend)

    else:

        st.info("No sales trend data available.")


    st.divider()


    # ==================================================
    # CATEGORY PERFORMANCE
    # ==================================================

    st.subheader("Category Performance")

    category_summary = get_category_summary(
        filtered_master
    )

    if not category_summary.empty:

        display_category_chart(category_summary)

    else:

        st.info("No category data available.")


    st.divider()


    # ==================================================
    # TOP 5 PRODUCTS
    # ==================================================

    st.subheader("Top 5 Products")

    top_products = get_top_products(
        filtered_master,
        top_n=5
    )

    if not top_products.empty:

        st.dataframe(
            top_products,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No product data available.")


    st.divider()


    # ==================================================
    # FILTERED DATA SUMMARY
    # ==================================================

    st.subheader("Filtered Dataset Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Filtered Item Records",
        f"{len(filtered_master):,}"
    )

    col2.metric(
        "Filtered Orders",
        f"{filtered_master['order_id'].nunique():,}"
    )

    col3.metric(
        "Filtered Products",
        f"{filtered_master['product_id'].nunique():,}"
    )


except Exception as error:

    st.error(
        "An error occurred while loading the Overview page."
    )

    st.exception(error)