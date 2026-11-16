import pandas as pd
from pathlib import Path

RAW = Path("data/raw")

orders = pd.read_csv(RAW / "olist_orders_dataset.csv")
items = pd.read_csv(RAW / "olist_order_items_dataset.csv")
payments = pd.read_csv(RAW / "olist_order_payments_dataset.csv")

# Aggregate item totals by order
item_totals = (
    items.groupby("order_id")
    .agg(
        item_price=("price", "sum"),
        freight=("freight_value", "sum")
    )
)

# Aggregate payment totals by order
payment_totals = (
    payments.groupby("order_id")["payment_value"]
    .sum()
    .rename("payment_total")
)

# Combine totals
comparison = item_totals.join(payment_totals, how="outer")

comparison["difference"] = (
    comparison["payment_total"]
    - comparison["item_price"]
    - comparison["freight"]
)

# Add order status
comparison = comparison.merge(
    orders[["order_id", "order_status"]],
    on="order_id",
    how="left"
)

print("\n========== RECONCILIATION INVESTIGATION ==========")

# 1. Orders without item records
print("\n1. ORDERS WITHOUT ITEM RECORDS")

no_items = comparison[comparison["item_price"].isna()]

print("Total:", len(no_items))
print("\nOrder status:")
print(no_items["order_status"].value_counts(dropna=False))

# 2. Orders without payment records
print("\n2. ORDERS WITHOUT PAYMENT RECORDS")

no_payments = comparison[comparison["payment_total"].isna()]

print("Total:", len(no_payments))
print("\nOrder status:")
print(no_payments["order_status"].value_counts(dropna=False))

# 3. Mismatched orders
print("\n3. FINANCIAL MISMATCHES")

mismatches = comparison[
    comparison["difference"].abs() > 0.01
]

print("Total mismatches:", len(mismatches))

print("\nMismatch by order status:")
print(mismatches["order_status"].value_counts())

print("\nLargest mismatches:")
print(
    mismatches.assign(
        absolute_difference=mismatches["difference"].abs()
    )
    .sort_values("absolute_difference", ascending=False)
    [[
        "order_id",
        "order_status",
        "item_price",
        "freight",
        "payment_total",
        "difference"
    ]]
    .head(15)
)

# 4. Delivered order reconciliation
print("\n4. DELIVERED ORDER RECONCILIATION")

delivered = comparison[
    comparison["order_status"] == "delivered"
]

print("Delivered orders:", len(delivered))

print(
    "Delivered mismatches:",
    (delivered["difference"].abs() > 0.01).sum()
)

print("\n========== INVESTIGATION COMPLETED ==========")