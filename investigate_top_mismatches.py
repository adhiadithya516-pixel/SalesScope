import pandas as pd
from pathlib import Path

RAW = Path("data/raw")

orders = pd.read_csv(RAW / "olist_orders_dataset.csv")
items = pd.read_csv(RAW / "olist_order_items_dataset.csv")
payments = pd.read_csv(RAW / "olist_order_payments_dataset.csv")

# 1. Aggregate item values
item_totals = (
    items.groupby("order_id")
    .agg(
        item_price=("price", "sum"),
        freight=("freight_value", "sum"),
        item_records=("order_item_id", "count")
    )
)

# 2. Aggregate payment values
payment_totals = (
    payments.groupby("order_id")
    .agg(
        payment_total=("payment_value", "sum"),
        payment_records=("payment_value", "count")
    )
)

# 3. Combine financial information
comparison = item_totals.join(
    payment_totals,
    how="outer"
)

comparison["difference"] = (
    comparison["payment_total"]
    - comparison["item_price"]
    - comparison["freight"]
)

# 4. Add order status
comparison = comparison.merge(
    orders[["order_id", "order_status"]],
    left_index=True,
    right_on="order_id",
    how="left"
)

# 5. Identify delivered mismatches
mismatches = comparison[
    (comparison["order_status"] == "delivered") &
    (comparison["difference"].abs() > 0.01)
].copy()

mismatches["absolute_difference"] = (
    mismatches["difference"].abs()
)

# 6. Select five largest mismatches
top_five = mismatches.nlargest(
    5,
    "absolute_difference"
)

print("\n========== TOP FIVE DELIVERED MISMATCHES ==========")

for _, row in top_five.iterrows():

    order_id = row["order_id"]

    print("\n" + "=" * 65)
    print("ORDER ID:", order_id)

    print("\nORDER ITEMS:")

    print(
        items[items["order_id"] == order_id][
            [
                "order_item_id",
                "product_id",
                "seller_id",
                "price",
                "freight_value"
            ]
        ].to_string(index=False)
    )

    print("\nPAYMENT RECORDS:")

    print(
        payments[payments["order_id"] == order_id][
            [
                "payment_sequential",
                "payment_type",
                "payment_installments",
                "payment_value"
            ]
        ].to_string(index=False)
    )

    print("\nRECONCILIATION:")

    print("Item price:", row["item_price"])
    print("Freight:", row["freight"])
    print("Payment:", row["payment_total"])
    print("Difference:", row["difference"])
    print("Number of item records:", row["item_records"])
    print("Number of payment records:", row["payment_records"])

print("\n========== INVESTIGATION COMPLETED ==========")