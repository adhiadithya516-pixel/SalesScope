import streamlit as st

from dashboard.data_service import load_dashboard_data

from src.sales_analysis import get_sales_trend
from src.product_analysis import get_top_products, get_product_summary
from src.category_analysis import get_category_summary
from src.weekly_comparison import get_weekly_sales_comparison

from src.report_generator import (
    generate_csv_report,
    generate_excel_report
)

st.title("Reports & Downloads")
st.caption("Export business analytics for further analysis.")

datasets, master = load_dashboard_data()

sales = get_sales_trend(master, "MS")
products = get_product_summary(master)
categories = get_category_summary(master)
weekly = get_weekly_sales_comparison(master)

reports = {
    "Sales Trend": sales,
    "Top Products": get_top_products(master, 10),
    "Product Analysis": products,
    "Category Analysis": categories,
    "Weekly Comparison": weekly
}

st.subheader("Excel Business Intelligence Report")

excel_file = generate_excel_report(reports)

st.download_button(
    "Download Complete Excel Report",
    data=excel_file,
    file_name="SalesScope_Retail_Analytics.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

st.divider()

st.subheader("Individual CSV Reports")

for name, dataframe in reports.items():

    st.write(name)

    csv_file = generate_csv_report(dataframe)

    st.download_button(
        f"Download {name} CSV",
        data=csv_file,
        file_name=f"{name.lower().replace(' ', '_')}.csv",
        mime="text/csv",
        key=f"download_{name}"
    )