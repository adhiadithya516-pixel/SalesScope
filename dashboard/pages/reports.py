import streamlit as st

from dashboard.data_service import load_dashboard_data
from dashboard.components.filters import display_sidebar_filters

from src.sales_analysis import get_sales_trend
from src.product_analysis import get_top_products, get_product_summary
from src.category_analysis import get_category_summary
from src.weekly_comparison import get_weekly_sales_comparison

from src.report_generator import (
    generate_csv_report,
    generate_excel_report
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.title("Reports & Downloads")
st.caption(
    "Generate and export filtered business analytics "
    "for further analysis and reporting."
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

datasets, master = load_dashboard_data()

# --------------------------------------------------
# SHARED SIDEBAR FILTERS
# --------------------------------------------------

filtered_master = display_sidebar_filters(master)

if filtered_master.empty:
    st.warning(
        "No records found for the selected filters. "
        "Please adjust your filters to generate reports."
    )
    st.stop()

# --------------------------------------------------
# REPORT OVERVIEW
# --------------------------------------------------

st.subheader("Business Summary")

total_revenue = filtered_master["price"].sum()
total_orders = filtered_master["order_id"].nunique()
total_products = filtered_master["product_id"].nunique()

categories = get_category_summary(filtered_master)
total_categories = len(categories)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Product Revenue",
    f"R$ {total_revenue:,.2f}"
)

col2.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Products Sold",
    f"{total_products:,}"
)

col4.metric(
    "Categories",
    f"{total_categories:,}"
)

st.caption(
    "Revenue represents product price and excludes freight charges. "
    "All figures reflect the currently selected filters."
)

# --------------------------------------------------
# GENERATE REPORT DATA
# --------------------------------------------------

sales = get_sales_trend(filtered_master, "MS")

top_products = get_top_products(filtered_master, 10)

products = get_product_summary(filtered_master)

categories = get_category_summary(filtered_master)

weekly = get_weekly_sales_comparison(filtered_master)

# --------------------------------------------------
# REPORT COLLECTION
# --------------------------------------------------

reports = {
    "Sales Trend": sales,
    "Top Products": top_products,
    "Product Analysis": products,
    "Category Analysis": categories,
    "Weekly Comparison": weekly
}

# --------------------------------------------------
# COMPLETE EXCEL REPORT
# --------------------------------------------------

st.divider()

st.subheader("Complete Business Intelligence Report")

st.write(
    "Download all five analytical reports together "
    "in a single Excel workbook."
)

excel_file = generate_excel_report(reports)

st.download_button(
    label="Download Complete Excel Report",
    data=excel_file,
    file_name="SalesScope_Retail_Analytics.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    width="stretch"
)

# --------------------------------------------------
# INDIVIDUAL CSV REPORTS
# --------------------------------------------------

st.divider()

st.subheader("Individual CSV Reports")

st.write(
    "Download individual reports in CSV format "
    "for additional analysis."
)

for name, dataframe in reports.items():
    st.write(f"**{name}**")

    csv_file = generate_csv_report(dataframe)

    st.download_button(
        label=f"Download {name} CSV",
        data=csv_file,
        file_name=f"{name.lower().replace(' ', '_')}.csv",
        mime="text/csv",
        key=f"download_{name}"
    )

# --------------------------------------------------
# REPORT INFORMATION
# --------------------------------------------------

st.divider()

st.subheader("Report Information")

st.markdown(
    """
    - **Sales Trend:** Monthly sales performance.
    - **Top Products:** Top 10 products based on sales.
    - **Product Analysis:** Product-level performance.
    - **Category Analysis:** Category-level sales performance.
    - **Weekly Comparison:** Comparison of weekly sales.

    All reports are generated using the data selected
    through the shared sidebar filters.
    """
)