import plotly.express as px
import streamlit as st

def display_sales_chart(data):
    fig = px.line(
        data,
        x="order_purchase_timestamp",
        y="product_sales_value",
        title="Monthly Sales Performance",
        markers=True,
        labels={
            "order_purchase_timestamp": "Month",
            "product_sales_value": "Product Sales (R$)"
        }
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)


def display_category_chart(data):
    fig = px.bar(
        data.head(10),
        x="category_sales",
        y="category",
        orientation="h",
        title="Top 10 Product Categories",
        labels={
            "category_sales": "Sales (R$)",
            "category": "Category"
        }
    )

    fig.update_layout(
        template="plotly_white",
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig, use_container_width=True)


def display_payment_chart(data):
    fig = px.pie(
        data,
        names="payment_method",
        values="payment_value",
        title="Payment Method Distribution",
        hole=0.45
    )

    st.plotly_chart(fig, use_container_width=True)