import pandas as pd
from pathlib import Path

RAW_DATA_DIR = Path("data/raw")

orders = pd.read_csv(RAW_DATA_DIR / "olist_orders_dataset.csv")
items = pd.read_csv(RAW_DATA_DIR / "olist_order_items_dataset.csv")
payments = pd.read_csv(RAW_DATA_DIR / "olist_order_payments_dataset.csv")
reviews = pd.read_csv(RAW_DATA_DIR / "olist_order_reviews_dataset.csv")
customers = pd.read_csv(RAW_DATA_DIR / "olist_customers_dataset.csv")

print("\n========== BUSINESS METRICS INVESTIGATION ==========")

# 1. Order item analysis
print("\n1. ORDER ITEM ANALYSIS")

print("Unique orders in items:", items["order_id"].nunique())
print("Unique products sold:", items["product_id"].nunique())
print("Total item records:", len(items))

print("\nPrice statistics:")
print(items["price"].describe())

print("\nFreight statistics:")
print(items["freight_value"].describe())


# 2. Payment analysis
print("\n2. PAYMENT ANALYSIS")

print("Payment types:")
print(payments["payment_type"].value_counts())

print("\nPayment values:")
print(payments["payment_value"].describe())

print("\nPayment installments:")
print(payments["payment_installments"].describe())


# 3. Review analysis
print("\n3. REVIEW ANALYSIS")

print("Review scores:")
print(reviews["review_score"].value_counts().sort_index())

print("\nReview score average:")
print(reviews["review_score"].mean())


# 4. Customer analysis
print("\n4. CUSTOMER ANALYSIS")

print("Unique customer IDs:", customers["customer_id"].nunique())
print("Unique actual customers:", customers["customer_unique_id"].nunique())

orders_per_customer = (
    customers.groupby("customer_unique_id")["customer_id"].count()
)

print("\nOrders per customer:")
print(orders_per_customer.describe())

print(
    "Repeat customers:",
    (orders_per_customer > 1).sum()
)


# 5. Order item quantity
print("\n5. ITEM QUANTITY ANALYSIS")

print(items["order_item_id"].describe())

print("\n========== INVESTIGATION COMPLETED ==========")