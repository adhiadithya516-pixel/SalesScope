import pandas as pd
from pathlib import Path

RAW = Path("data/raw")

orders = pd.read_csv(RAW / "olist_orders_dataset.csv")
items = pd.read_csv(RAW / "olist_order_items_dataset.csv")
payments = pd.read_csv(RAW / "olist_order_payments_dataset.csv")
products = pd.read_csv(RAW / "olist_products_dataset.csv")
translation = pd.read_csv(RAW / "product_category_name_translation.csv")

print("\n========== FINANCIAL INTEGRITY INVESTIGATION ==========")

# 1. Order status of item records
print("\n1. ORDER ITEM STATUS")

item_orders = items.merge(
    orders[["order_id", "order_status"]],
    on="order_id",
    how="left"
)

print(item_orders["order_status"].value_counts(dropna=False))


# 2. Payment reconciliation
print("\n2. PAYMENT RECONCILIATION")

item_totals = (
    items.groupby("order_id")
    .agg(
        item_price=("price", "sum"),
        freight=("freight_value", "sum")
    )
)

payment_totals = (
    payments.groupby("order_id")["payment_value"]
    .sum()
    .rename("payment_total")
)

comparison = item_totals.join(payment_totals, how="outer")

comparison["difference"] = (
    comparison["payment_total"]
    - comparison["item_price"]
    - comparison["freight"]
)

print("Orders compared:", len(comparison))
print("Missing payment totals:", comparison["payment_total"].isna().sum())
print("Missing item totals:", comparison["item_price"].isna().sum())

print("\nDifference statistics:")
print(comparison["difference"].describe())

print(
    "Orders with difference above R$0.01:",
    (comparison["difference"].abs() > 0.01).sum()
)


# 3. Product category translation coverage
print("\n3. CATEGORY TRANSLATION")

product_categories = set(
    products["product_category_name"].dropna().unique()
)

translated_categories = set(
    translation["product_category_name"].unique()
)

print("Unique product categories:", len(product_categories))
print("Translated categories:", len(translated_categories))

print(
    "Untranslated categories:",
    product_categories - translated_categories
)

print(
    "Categories without a product category:",
    products["product_category_name"].isna().sum()
)

print("\n========== INVESTIGATION COMPLETED ==========")