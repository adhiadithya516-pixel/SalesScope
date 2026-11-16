import streamlit as st


def display_kpi_cards(kpis):
    """Display the main business KPIs."""

    metrics = [
        ("Product Sales", f"R$ {kpis['total_product_sales']:,.2f}"),
        ("Delivered Orders", f"{kpis['delivered_orders']:,}"),
        ("Average Order Value", f"R$ {kpis['average_order_value']:,.2f}"),
        ("Total Customers", f"{kpis['total_customers']:,}"),
        ("Repeat Customers", f"{kpis['repeat_customers']:,}"),
        ("Average Review", f"{kpis['average_review_score']:.2f}/5"),
        ("Delayed Orders", f"{kpis['delayed_orders']:,}"),
        ("Delivery Delay Rate", f"{kpis['delayed_delivery_rate']:.2f}%")
    ]

    columns = st.columns(4)

    for index, (label, value) in enumerate(metrics):
        with columns[index % 4]:
            st.metric(label=label, value=value)