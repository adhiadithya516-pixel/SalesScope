import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/OnlineRetail.csv")

df = pd.read_csv(DATA_PATH)

df["OrderDate"] = pd.to_datetime(
    df["OrderDate"],
    errors="coerce"
)

print("\n========== ADVANCED EDA ==========")

# 1. Date coverage
print("\n1. DATE COVERAGE")

print("First Date:", df["OrderDate"].min())
print("Last Date:", df["OrderDate"].max())

print("Unique Order Dates:", df["OrderDate"].nunique())

# 2. Order ID investigation
print("\n2. ORDER ID INVESTIGATION")

print("Total records:", len(df))
print("Unique Order IDs:", df["OrderID"].nunique())
print("Repeated Order ID records:",
      df["OrderID"].duplicated().sum())

print("\nRepeated Order IDs:")

print(
    df[df["OrderID"].duplicated(keep=False)]
    .sort_values("OrderID")
    [["OrderID", "OrderDate", "ProductCategory",
      "ProductSubCategory", "Quantity", "FinalAmount"]]
    .head(20)
)

# 3. Financial consistency
print("\n3. FINANCIAL VALIDATION")

df["CalculatedTotal"] = df["UnitPrice"] * df["Quantity"]

df["TotalDifference"] = (
    df["TotalAmount"] - df["CalculatedTotal"]
)

df["FinalDifference"] = (
    df["FinalAmount"] -
    (df["TotalAmount"] - df["DiscountAmount"])
)

print("TotalAmount mismatches:",
      (df["TotalDifference"].abs() > 0.01).sum())

print("FinalAmount mismatches:",
      (df["FinalDifference"].abs() > 0.01).sum())

# 4. Returns
print("\n4. RETURN ANALYSIS")

print(df["Returned"].value_counts())

print("\nReturned revenue:")

print(
    df.groupby("Returned")["FinalAmount"].agg(
        ["count", "sum", "mean"]
    )
)

# 5. Product analysis
print("\n5. PRODUCT DIMENSIONS")

print("Unique Categories:",
      df["ProductCategory"].nunique())

print("Unique Subcategories:",
      df["ProductSubCategory"].nunique())

print("\nCategory distribution:")

print(df["ProductCategory"].value_counts())

# 6. Numeric quality
print("\n6. NUMERIC VALIDATION")

for column in [
    "UnitPrice",
    "Quantity",
    "TotalAmount",
    "DiscountAmount",
    "FinalAmount",
    "DiscountPercent",
    "ShippingDays",
    "ReviewScore"
]:
    print(
        column,
        "| Minimum:", df[column].min(),
        "| Maximum:", df[column].max()
    )

# 7. Weekly coverage
print("\n7. WEEKLY COVERAGE")

df["Week"] = (
    df["OrderDate"]
    .dt.to_period("W")
)

print("Unique weeks:", df["Week"].nunique())

print(
    df.groupby("Week")
    .size()
    .describe()
)

print("\n========== INVESTIGATION COMPLETED ==========")