import streamlit as st
import plotly.express as px

from dashboard.data_service import load_dashboard_data
from dashboard.components.filters import display_sidebar_filters

from src.category_analysis import (
    get_category_summary,
    get_top_categories,
    get_category_order_ranking
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.title("Category Analytics")

st.caption(
    "Evaluate product category revenue and contribution."
)


try:

    # ==================================================
    # LOAD DATA
    # ==================================================

    with st.spinner("Loading category analytics..."):

        datasets, master = load_dashboard_data()

    if master.empty:
        st.warning("No category data available.")
        st.stop()


    # ==================================================
    # APPLY DASHBOARD FILTERS
    # ==================================================

    filtered_master = display_sidebar_filters(master)

    if filtered_master.empty:
        st.warning("No records match the selected filters.")
        st.stop()


    # ==================================================
    # CATEGORY SUMMARY
    # ==================================================

    summary = get_category_summary(filtered_master)

    if summary.empty:
        st.warning("No category sales data available.")
        st.stop()


    # ==================================================
    # CATEGORY KPI CARDS
    # ==================================================

    top_category = summary.iloc[0]

    st.subheader("Category Performance Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Categories",
        f"{len(summary):,}"
    )

    col2.metric(
        "Leading Category",
        top_category["category"]
    )

    col3.metric(
        "Leading Category Sales",
        f"R$ {top_category['category_sales']:,.2f}"
    )


    st.divider()


    # ==================================================
    # TOP 10 CATEGORIES BY SALES
    # ==================================================

    st.subheader("Top 10 Categories by Sales")

    top = get_top_categories(
        filtered_master,
        10
    )

    if not top.empty:

        fig = px.bar(
            top,
            x="category_sales",
            y="category",
            orientation="h",
            title="Category Sales Performance",
            labels={
                "category_sales": "Sales (R$)",
                "category": "Category"
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
        st.info("No category sales data available.")


    st.divider()


    # ==================================================
    # CATEGORY CONTRIBUTION
    # ==================================================

    st.subheader("Category Contribution")

    fig = px.pie(
        summary.head(8),
        names="category",
        values="category_sales",
        hole=0.45,
        title="Sales Contribution - Leading 8 Categories"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


    st.divider()


    # ==================================================
    # CATEGORIES BY ORDER COUNT
    # ==================================================

    st.subheader("Categories by Order Count")

    ranking = get_category_order_ranking(
        filtered_master,
        10
    )

    if not ranking.empty:

        fig = px.bar(
            ranking,
            x="order_count",
            y="category",
            orientation="h",
            title="Categories Ranked by Orders",
            labels={
                "order_count": "Number of Orders",
                "category": "Category"
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
        st.info("No category order data available.")


    st.divider()


    # ==================================================
    # COMPLETE CATEGORY REPORT
    # ==================================================

    st.subheader("Complete Category Report")

    st.dataframe(
        summary,
        width="stretch",
        hide_index=True
    )


    # ==================================================
    # DOWNLOAD CATEGORY REPORT
    # ==================================================

    st.subheader("Download Category Report")

    csv_data = summary.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="Download Category Analysis CSV",
        data=csv_data,
        file_name="category_analysis.csv",
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
        "Unique Categories",
        f"{filtered_master['category'].nunique():,}"
    )


except Exception as error:

    st.error(
        "An error occurred while loading Category Analytics."
    )

    st.exception(error)