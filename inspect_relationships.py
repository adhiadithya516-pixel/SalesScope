import pandas as pd
from pathlib import Path

RAW_DATA_DIR = Path("data/raw")

print("\n========== RELATIONSHIP INVESTIGATION ==========")

# Load relevant datasets
orders = pd.read_csv(RAW_DATA_DIR / "olist_orders_dataset.csv")
items = pd.read_csv(RAW_DATA_DIR / "olist_order_items_dataset.csv")
products = pd.read_csv(RAW_DATA_DIR / "olist_products_dataset.csv")
customers = pd.read_csv(RAW_DATA_DIR / "olist_customers_dataset.csv")
payments = pd.read_csv(RAW_DATA_DIR / "olist_order_payments_dataset.csv")
reviews = pd.read_csv(RAW_DATA_DIR / "olist_order_reviews_dataset.csv")
sellers = pd.read_csv(RAW_DATA_DIR / "olist_sellers_dataset.csv")


# 1. Primary key uniqueness
print("\n1. PRIMARY KEY VALIDATION")

checks = {
    "orders.order_id": orders["order_id"],
    "customers.customer_id": customers["customer_id"],
    "products.product_id": products["product_id"],
    "sellers.seller_id": sellers["seller_id"],
}

for name, column in checks.items():
    print(
        name,
        "| Unique:", column.nunique(),
        "| Total:", len(column),
        "| Duplicates:", column.duplicated().sum()
    )


# 2. Foreign key validation
print("\n2. FOREIGN KEY VALIDATION")

relationships = [
    ("Orders -> Customers",
     orders["customer_id"], customers["customer_id"]),

    ("Items -> Orders",
     items["order_id"], orders["order_id"]),

    ("Items -> Products",
     items["product_id"], products["product_id"]),

    ("Items -> Sellers",
     items["seller_id"], sellers["seller_id"]),

    ("Payments -> Orders",
     payments["order_id"], orders["order_id"]),

    ("Reviews -> Orders",
     reviews["order_id"], orders["order_id"]),
]

for name, child_key, parent_key in relationships:

    unmatched = (~child_key.isin(parent_key)).sum()

    print(name, "| Unmatched records:", unmatched)


# 3. Relationship cardinality
print("\n3. ORDER CARDINALITY")

print(
    "Orders containing multiple items:",
    (items.groupby("order_id").size() > 1).sum()
)

print(
    "Maximum items per order:",
    items.groupby("order_id").size().max()
)

print(
    "Orders with multiple payment records:",
    (payments.groupby("order_id").size() > 1).sum()
)

print(
    "Orders with multiple review records:",
    (reviews.groupby("order_id").size() > 1).sum()
)


# 4. Order status distribution
print("\n4. ORDER STATUS DISTRIBUTION")

print(orders["order_status"].value_counts(dropna=False))


print("\n========== INVESTIGATION COMPLETED ==========")