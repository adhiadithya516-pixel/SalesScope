import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.data_service import load_dashboard_data


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.title("Delivery & Review Analytics")

st.caption(
    "Monitor delivery performance, delays, "
    "delivery duration and customer satisfaction."
)


try:

    # --------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------

    with st.spinner("Loading delivery and review analytics..."):

        datasets, master = load_dashboard_data()

    orders = datasets["orders"]
    reviews = datasets["reviews"]

    if orders.empty:
        st.warning("Order data is unavailable.")
        st.stop()


    # --------------------------------------------------
    # PREPARE DELIVERY DATA
    # --------------------------------------------------

    delivery_data = orders.copy()

    date_columns = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:

        delivery_data[column] = pd.to_datetime(
            delivery_data[column],
            errors="coerce"
        )

    # Consider delivered orders only
    delivered = delivery_data[
        delivery_data["order_status"] == "delivered"
    ].copy()

    delivered = delivered.dropna(
        subset=[
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
            "order_purchase_timestamp"
        ]
    )

    if delivered.empty:
        st.warning("No valid delivered order records found.")
        st.stop()


    # --------------------------------------------------
    # DELIVERY METRICS
    # --------------------------------------------------

    delivered["delivery_days"] = (
        delivered["order_delivered_customer_date"]
        - delivered["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    delivered["delay_days"] = (
        delivered["order_delivered_customer_date"]
        - delivered["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    delivered["delivery_status"] = delivered[
        "delay_days"
    ].apply(
        lambda days: "Delayed" if days > 0 else "On Time"
    )

    total_delivered = delivered["order_id"].nunique()

    delayed_orders = delivered[
        delivered["delivery_status"] == "Delayed"
    ]["order_id"].nunique()

    on_time_orders = total_delivered - delayed_orders

    delay_rate = (
        delayed_orders / total_delivered * 100
        if total_delivered else 0
    )

    average_delivery_days = delivered[
        "delivery_days"
    ].mean()


    # --------------------------------------------------
    # DELIVERY KPI CARDS
    # --------------------------------------------------

    st.subheader("Delivery Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Delivered Orders",
        f"{total_delivered:,}"
    )

    col2.metric(
        "Delayed Orders",
        f"{delayed_orders:,}"
    )

    col3.metric(
        "Delivery Delay Rate",
        f"{delay_rate:.2f}%"
    )

    col4.metric(
        "Average Delivery Time",
        f"{average_delivery_days:.2f} days"
    )

    st.divider()


    # --------------------------------------------------
    # ON-TIME VS DELAYED ORDERS
    # --------------------------------------------------

    st.subheader("Delivery Status Distribution")

    delivery_distribution = pd.DataFrame({
        "Delivery Status": [
            "On Time",
            "Delayed"
        ],
        "Number of Orders": [
            on_time_orders,
            delayed_orders
        ]
    })

    col1, col2 = st.columns(2)

    with col1:

        delivery_chart = px.pie(
            delivery_distribution,
            names="Delivery Status",
            values="Number of Orders",
            hole=0.45,
            title="On-Time vs Delayed Deliveries"
        )

        st.plotly_chart(
            delivery_chart,
            use_container_width=True
        )

    with col2:

        st.metric(
            "On-Time Orders",
            f"{on_time_orders:,}"
        )

        st.metric(
            "Delayed Orders",
            f"{delayed_orders:,}"
        )

        st.metric(
            "On-Time Delivery Rate",
            f"{100 - delay_rate:.2f}%"
        )

    st.divider()


    # --------------------------------------------------
    # DELIVERY TIME DISTRIBUTION
    # --------------------------------------------------

    st.subheader("Delivery Duration Analysis")

    delivery_duration = px.histogram(
        delivered,
        x="delivery_days",
        nbins=30,
        title="Distribution of Delivery Duration",
        labels={
            "delivery_days": "Delivery Duration (Days)"
        }
    )

    st.plotly_chart(
        delivery_duration,
        use_container_width=True
    )

    st.divider()


    # --------------------------------------------------
    # MONTHLY DELIVERY PERFORMANCE
    # --------------------------------------------------

    st.subheader("Monthly Delivery Performance")

    monthly_delivery = (
        delivered
        .groupby(
            pd.Grouper(
                key="order_purchase_timestamp",
                freq="MS"
            )
        )
        .agg(
            Delivered_Orders=("order_id", "nunique"),
            Delayed_Orders=(
                "delivery_status",
                lambda values: (values == "Delayed").sum()
            ),
            Average_Delivery_Days=("delivery_days", "mean")
        )
        .reset_index()
    )

    monthly_delivery["Delay_Rate"] = (
        monthly_delivery["Delayed_Orders"]
        / monthly_delivery["Delivered_Orders"]
        * 100
    )

    if not monthly_delivery.empty:

        monthly_chart = px.line(
            monthly_delivery,
            x="order_purchase_timestamp",
            y="Average_Delivery_Days",
            markers=True,
            title="Monthly Average Delivery Time"
        )

        monthly_chart.update_layout(
            xaxis_title="Month",
            yaxis_title="Average Delivery Time (Days)",
            hovermode="x unified"
        )

        st.plotly_chart(
            monthly_chart,
            use_container_width=True
        )

        st.dataframe(
            monthly_delivery,
            use_container_width=True,
            hide_index=True
        )

    st.divider()


    # --------------------------------------------------
    # CUSTOMER REVIEW ANALYTICS
    # --------------------------------------------------

    st.subheader("Customer Satisfaction Overview")

    if reviews.empty:

        st.warning("Review data is unavailable.")

    else:

        review_data = reviews.copy()

        review_data["review_score"] = pd.to_numeric(
            review_data["review_score"],
            errors="coerce"
        )

        review_data = review_data.dropna(
            subset=["review_score"]
        )

        total_reviews = len(review_data)

        average_review = review_data[
            "review_score"
        ].mean()

        positive_reviews = review_data[
            review_data["review_score"].isin([4, 5])
        ].shape[0]

        negative_reviews = review_data[
            review_data["review_score"].isin([1, 2])
        ].shape[0]

        positive_rate = (
            positive_reviews / total_reviews * 100
            if total_reviews else 0
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Reviews",
            f"{total_reviews:,}"
        )

        col2.metric(
            "Average Review Score",
            f"{average_review:.2f} / 5"
        )

        col3.metric(
            "Positive Reviews",
            f"{positive_reviews:,}"
        )

        col4.metric(
            "Negative Reviews",
            f"{negative_reviews:,}"
        )

        st.divider()


        # --------------------------------------------------
        # REVIEW SCORE DISTRIBUTION
        # --------------------------------------------------

        st.subheader("Review Score Distribution")

        review_distribution = (
            review_data["review_score"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        review_distribution.columns = [
            "Review Score",
            "Number of Reviews"
        ]

        review_chart = px.bar(
            review_distribution,
            x="Review Score",
            y="Number of Reviews",
            text="Number of Reviews",
            title="Customer Review Ratings"
        )

        review_chart.update_layout(
            xaxis_title="Review Score (1 to 5)",
            yaxis_title="Number of Reviews"
        )

        st.plotly_chart(
            review_chart,
            use_container_width=True
        )

        st.dataframe(
            review_distribution,
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            "Positive Review Rate",
            f"{positive_rate:.2f}%"
        )


    st.divider()


    # --------------------------------------------------
    # BUSINESS INSIGHTS
    # --------------------------------------------------

    st.subheader("Delivery & Customer Satisfaction Insights")

    st.write(
        f"- {delayed_orders:,} delivered orders arrived "
        f"after their estimated delivery date."
    )

    st.write(
        f"- The delivery delay rate is {delay_rate:.2f}%."
    )

    st.write(
        f"- Average delivery duration is "
        f"{average_delivery_days:.2f} days."
    )

    if delay_rate > 10:

        st.warning(
            "Business Recommendation: Investigate logistics "
            "operations and delivery bottlenecks to reduce delays."
        )

    else:

        st.info(
            "Business Recommendation: Continue monitoring "
            "delivery performance and maintain on-time delivery."
        )

    if not reviews.empty and total_reviews > 0:

        st.write(
            f"- Average customer review score: "
            f"{average_review:.2f}/5."
        )

        st.write(
            f"- Positive review rate: {positive_rate:.2f}%."
        )

        if positive_rate < 70:

            st.warning(
                "Business Recommendation: Investigate customer "
                "complaints and identify service quality issues."
            )

        else:

            st.info(
                "Customer feedback is predominantly positive. "
                "Continue monitoring review trends."
            )


    st.divider()


    # --------------------------------------------------
    # DOWNLOAD DELIVERY REPORT
    # --------------------------------------------------

    st.subheader("Download Delivery Report")

    delivery_report = delivered[
        [
            "order_id",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
            "delivery_days",
            "delay_days",
            "delivery_status"
        ]
    ].copy()

    csv_data = delivery_report.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Delivery Analytics (CSV)",
        data=csv_data,
        file_name="salesscope_delivery_analytics.csv",
        mime="text/csv"
    )


    # REVIEW REPORT DOWNLOAD

    if not reviews.empty:

        review_csv = reviews.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Customer Reviews (CSV)",
            data=review_csv,
            file_name="salesscope_customer_reviews.csv",
            mime="text/csv"
        )


except Exception as error:

    st.error(
        "An error occurred while loading Delivery & Review Analytics."
    )

    st.exception(error)