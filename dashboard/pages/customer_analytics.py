import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.data_service import load_dashboard_data
from dashboard.components.filters import display_sidebar_filters


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.title("Customer Analytics")

st.caption(
    "Understand customer acquisition, repeat purchases, "
    "purchase frequency and customer behaviour."
)


try:

    # ==================================================
    # LOAD DATA
    # ==================================================

    with st.spinner("Loading customer analytics..."):

        datasets, master = load_dashboard_data()

    if master.empty:
        st.warning("No customer data available.")
        st.stop()


    # ==================================================
    # APPLY SHARED DASHBOARD FILTERS
    # ==================================================

    filtered_master = display_sidebar_filters(master)

    if filtered_master.empty:
        st.warning("No customers match the selected filters.")
        st.stop()

    selected_order_ids = (
        filtered_master["order_id"]
        .dropna()
        .unique()
    )

    orders = datasets["orders"][
        datasets["orders"]["order_id"].isin(selected_order_ids)
    ].copy()

    customers = datasets["customers"].copy()


    # ==================================================
    # PREPARE CUSTOMER DATA
    # ==================================================

    customer_orders = orders.merge(
        customers[["customer_id", "customer_unique_id"]],
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    # Analyse delivered orders only
    delivered_orders = customer_orders[
        customer_orders["order_status"] == "delivered"
    ].copy()

    delivered_orders = delivered_orders.dropna(
        subset=["customer_unique_id"]
    )

    if delivered_orders.empty:
        st.warning(
            "No delivered customer orders found for the selected filters."
        )
        st.stop()


    # ==================================================
    # CUSTOMER PURCHASE FREQUENCY
    # ==================================================

    customer_frequency = (
        delivered_orders
        .groupby("customer_unique_id")
        .agg(
            purchase_count=("order_id", "nunique"),
            first_purchase=("order_purchase_timestamp", "min"),
            last_purchase=("order_purchase_timestamp", "max")
        )
        .reset_index()
    )


    # ==================================================
    # CUSTOMER METRICS
    # ==================================================

    total_customers = len(customer_frequency)

    total_delivered_orders = delivered_orders["order_id"].nunique()

    repeat_customers = (
        customer_frequency["purchase_count"] > 1
    ).sum()

    one_time_customers = (
        customer_frequency["purchase_count"] == 1
    ).sum()

    repeat_rate = (
        repeat_customers / total_customers * 100
        if total_customers else 0
    )

    average_purchases = (
        total_delivered_orders / total_customers
        if total_customers else 0
    )


    # ==================================================
    # CUSTOMER OVERVIEW
    # ==================================================

    st.subheader("Customer Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Unique Customers",
        f"{total_customers:,}"
    )

    col2.metric(
        "Repeat Customers",
        f"{repeat_customers:,}"
    )

    col3.metric(
        "Repeat Purchase Rate",
        f"{repeat_rate:.2f}%"
    )

    col4.metric(
        "Average Purchases / Customer",
        f"{average_purchases:.2f}"
    )

    st.divider()


    # ==================================================
    # CUSTOMER RETENTION BEHAVIOUR
    # ==================================================

    st.subheader("Customer Retention Behaviour")

    retention_data = pd.DataFrame({
        "Customer Type": [
            "One-time Customers",
            "Repeat Customers"
        ],
        "Customer Count": [
            one_time_customers,
            repeat_customers
        ]
    })

    col1, col2 = st.columns(2)

    with col1:

        retention_chart = px.pie(
            retention_data,
            names="Customer Type",
            values="Customer Count",
            hole=0.45,
            title="One-time vs Repeat Customers"
        )

        st.plotly_chart(
            retention_chart,
            width="stretch"
        )

    with col2:

        st.metric(
            "One-time Customers",
            f"{one_time_customers:,}"
        )

        st.metric(
            "Repeat Customers",
            f"{repeat_customers:,}"
        )

        st.metric(
            "Repeat Purchase Rate",
            f"{repeat_rate:.2f}%"
        )

    st.divider()


    # ==================================================
    # PURCHASE FREQUENCY DISTRIBUTION
    # ==================================================

    st.subheader("Purchase Frequency Analysis")

    frequency_distribution = (
        customer_frequency["purchase_count"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    frequency_distribution.columns = [
        "Number of Purchases",
        "Number of Customers"
    ]

    frequency_chart = px.bar(
        frequency_distribution,
        x="Number of Purchases",
        y="Number of Customers",
        text="Number of Customers",
        title="Customers by Number of Delivered Purchases"
    )

    frequency_chart.update_layout(
        xaxis_title="Number of Delivered Purchases",
        yaxis_title="Number of Customers"
    )

    st.plotly_chart(
        frequency_chart,
        width="stretch"
    )

    st.dataframe(
        frequency_distribution,
        width="stretch",
        hide_index=True
    )

    st.divider()


    # ==================================================
    # CUSTOMER SEGMENT ANALYSIS
    # ==================================================

    st.subheader("Customer Purchase Behaviour")

    behaviour_data = customer_frequency.copy()

    behaviour_data["Customer Segment"] = behaviour_data[
        "purchase_count"
    ].apply(
        lambda count: (
            "One-time Buyer"
            if count == 1
            else "Repeat Buyer"
        )
    )

    segment_summary = (
        behaviour_data
        .groupby("Customer Segment")
        .agg(
            Customers=("customer_unique_id", "count"),
            Total_Purchases=("purchase_count", "sum"),
            Average_Purchases=("purchase_count", "mean")
        )
        .reset_index()
    )

    st.dataframe(
        segment_summary,
        width="stretch",
        hide_index=True
    )

    st.divider()


    # ==================================================
    # MONTHLY CUSTOMER ACTIVITY
    # ==================================================

    st.subheader("Monthly Customer Activity")

    delivered_orders["order_purchase_timestamp"] = pd.to_datetime(
        delivered_orders["order_purchase_timestamp"],
        errors="coerce"
    )

    monthly_customers = (
        delivered_orders
        .dropna(subset=["order_purchase_timestamp"])
        .groupby(
            pd.Grouper(
                key="order_purchase_timestamp",
                freq="MS"
            )
        )
        .agg(
            Unique_Customers=("customer_unique_id", "nunique"),
            Delivered_Orders=("order_id", "nunique")
        )
        .reset_index()
    )

    if not monthly_customers.empty:

        monthly_chart = px.line(
            monthly_customers,
            x="order_purchase_timestamp",
            y="Unique_Customers",
            markers=True,
            title="Monthly Unique Customers"
        )

        monthly_chart.update_layout(
            xaxis_title="Month",
            yaxis_title="Unique Customers",
            hovermode="x unified"
        )

        st.plotly_chart(
            monthly_chart,
            width="stretch"
        )

        display_monthly = monthly_customers.copy()

        display_monthly["order_purchase_timestamp"] = (
            display_monthly["order_purchase_timestamp"]
            .dt.strftime("%b %Y")
        )

        st.dataframe(
            display_monthly,
            width="stretch",
            hide_index=True
        )

    st.divider()


    # ==================================================
    # CUSTOMER INSIGHTS
    # ==================================================

    st.subheader("Customer Insights")

    st.write(
        f"- {total_customers:,} unique customers placed at least "
        "one delivered order."
    )

    st.write(
        f"- {repeat_customers:,} customers made more than "
        "one delivered purchase."
    )

    st.write(
        f"- Repeat purchase rate: {repeat_rate:.2f}%."
    )

    st.write(
        f"- Average delivered purchases per customer: "
        f"{average_purchases:.2f}."
    )

    if repeat_rate < 10:

        st.info(
            "Business Recommendation: Investigate opportunities "
            "to improve repeat purchases through customer engagement, "
            "retention campaigns and better post-purchase experiences."
        )

    else:

        st.info(
            "Business Recommendation: Monitor repeat purchase behaviour "
            "and identify factors contributing to customer retention."
        )

    st.divider()


    # ==================================================
    # DOWNLOAD CUSTOMER REPORT
    # ==================================================

    st.subheader("Download Customer Report")

    csv_data = customer_frequency.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="Download Customer Analytics (CSV)",
        data=csv_data,
        file_name="salesscope_customer_analytics.csv",
        mime="text/csv"
    )


except Exception as error:

    st.error(
        "An error occurred while loading Customer Analytics."
    )

    st.exception(error)