import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import streamlit as st

st.set_page_config(
    page_title="SalesScope | Retail Intelligence",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Centralized navigation
pages = {
    "WORKSPACE": [
        st.Page(
            "pages/overview.py",
            title="Overview",
            icon=":material/dashboard:",
            default=True
        )
    ],

    "ANALYTICS": [
        st.Page(
            "pages/sales_analysis.py",
            title="Sales Analytics",
            icon=":material/trending_up:"
        ),
        st.Page(
            "pages/product_performance.py",
            title="Product Performance",
            icon=":material/inventory_2:"
        ),
        st.Page(
            "pages/category_analysis.py",
            title="Category Analytics",
            icon=":material/category:"
        ),
        st.Page(
            "pages/customer_analytics.py",
            title="Customer Analytics",
            icon=":material/groups:"
        ),
        st.Page(
            "pages/payments_finance.py",
            title="Payments & Finance",
            icon=":material/payments:"
        ),
        st.Page(
            "pages/delivery_reviews.py",
            title="Delivery & Reviews",
            icon=":material/local_shipping:"
        )
    ],

    "REPORTING": [
        st.Page(
            "pages/reports.py",
            title="Reports",
            icon=":material/description:"
        )
    ]
}

navigation = st.navigation(pages)

navigation.run()