import streamlit as st
import plotly.express as px

from dashboard.data_service import load_dashboard_data
from dashboard.components.filters import display_sidebar_filters

from src.sales_analysis import (
    get_sales_trend,
    get_order_status_summary
)

from src.weekly_comparison import get_weekly_sales_comparison


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.title("Sales Analytics")

st.caption(
    "Analyze daily, weekly and monthly sales performance, "
    "revenue trends and business growth."
)


try:

    # ==================================================
    # LOAD DATA
    # ==================================================

    with st.spinner("Loading sales analytics..."):

        datasets, master = load_dashboard_data()

    if master.empty:
        st.warning("No sales data available.")
        st.stop()


    # ==================================================
    # APPLY COMMON DASHBOARD FILTERS
    # ==================================================

    filtered_master = display_sidebar_filters(master)

    if filtered_master.empty:
        st.warning("No records match the selected filters.")
        st.stop()


    # Get selected order IDs
    selected_order_ids = (
        filtered_master["order_id"]
        .dropna()
        .unique()
    )

    filtered_orders = datasets["orders"][
        datasets["orders"]["order_id"].isin(selected_order_ids)
    ].copy()


    # ==================================================
    # SALES PERIOD SELECTION
    # ==================================================

    st.sidebar.subheader("Sales Analysis")

    frequency_label = st.sidebar.selectbox(
        "Select Sales Period",
        ["Daily", "Weekly", "Monthly"],
        index=2
    )

    frequency_map = {
        "Daily": "D",
        "Weekly": "W",
        "Monthly": "MS"
    }

    frequency = frequency_map[frequency_label]


    # ==================================================
    # GENERATE SALES TREND
    # ==================================================

    sales_trend = get_sales_trend(
        filtered_master,
        frequency=frequency
    )

    if sales_trend.empty:
        st.warning("No sales records found for the selected filters.")
        st.stop()


    # ==================================================
    # SALES KPI CALCULATIONS
    # ==================================================

    total_sales = sales_trend[
        "product_sales_value"
    ].sum()

    total_orders = sales_trend[
        "order_count"
    ].sum()

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    latest_period = sales_trend.iloc[-1]

    latest_period_sales = latest_period[
        "product_sales_value"
    ]

    latest_period_orders = latest_period[
        "order_count"
    ]


    # ==================================================
    # KPI CARDS
    # ==================================================

    st.subheader("Sales Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Product Sales",
        f"R$ {total_sales:,.2f}"
    )

    col2.metric(
        f"Latest {frequency_label} Sales",
        f"R$ {latest_period_sales:,.2f}"
    )

    col3.metric(
        "Delivered Orders",
        f"{total_orders:,.0f}"
    )

    col4.metric(
        "Average Order Value",
        f"R$ {average_order_value:,.2f}"
    )


    st.divider()


    # ==================================================
    # DAILY / WEEKLY / MONTHLY SALES TREND
    # ==================================================

    st.subheader(
        f"{frequency_label} Product Sales Trend"
    )

    sales_chart = px.line(
        sales_trend,
        x="order_purchase_timestamp",
        y="product_sales_value",
        markers=True,
        title=f"{frequency_label} Product Sales"
    )

    sales_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Product Sales (R$)",
        hovermode="x unified"
    )

    st.plotly_chart(
        sales_chart,
        use_container_width=True
    )


    # ==================================================
    # PERIOD-WISE SALES TABLE
    # ==================================================

    st.subheader(
        f"{frequency_label} Sales Breakdown"
    )

    display_data = sales_trend.copy()

    display_data["order_purchase_timestamp"] = (
        display_data["order_purchase_timestamp"]
        .dt.strftime("%d %b %Y")
    )

    display_data = display_data.rename(
        columns={
            "order_purchase_timestamp": "Period",
            "product_sales_value": "Product Sales (R$)",
            "freight_value": "Freight (R$)",
            "order_count": "Delivered Orders",
            "average_order_value": "Average Order Value (R$)"
        }
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    # ==================================================
    # WEEK-OVER-WEEK COMPARISON
    # ==================================================

    st.subheader("Week-over-Week Sales Comparison")

    weekly_comparison = get_weekly_sales_comparison(
        filtered_master
    )

    if not weekly_comparison.empty:

        st.dataframe(
            weekly_comparison.tail(12),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Growth percentages compare each week with the "
            "previous week. The latest week may be incomplete."
        )

    else:

        st.info("Weekly comparison data is unavailable.")


    st.divider()


    # ==================================================
    # ORDER STATUS ANALYSIS
    # ==================================================

    st.subheader("Order Status Analysis")

    status_summary = get_order_status_summary(
        filtered_orders
    )

    if not status_summary.empty:

        status_chart = px.bar(
            status_summary,
            x="order_status",
            y="order_count",
            text="order_count",
            title="Orders by Status"
        )

        status_chart.update_layout(
            xaxis_title="Order Status",
            yaxis_title="Number of Orders"
        )

        st.plotly_chart(
            status_chart,
            use_container_width=True
        )

        st.dataframe(
            status_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No order status data available.")


    st.divider()


    # ==================================================
    # DOWNLOAD SALES REPORT
    # ==================================================

    st.subheader("Download Sales Report")

    csv_data = sales_trend.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Sales Report (CSV)",
        data=csv_data,
        file_name=f"salesscope_{frequency_label.lower()}_sales.csv",
        mime="text/csv"
    )


except Exception as error:

    st.error(
        "An error occurred while loading Sales Analytics."
    )

    st.exception(error)