import pandas as pd
from pathlib import Path

# Dataset location
DATA_PATH = Path("data/raw/OnlineRetail.csv")


# Load dataset
df = pd.read_csv(
    DATA_PATH,
    encoding="latin1"
)

print("\n========== SALESCOPE: DATASET OVERVIEW ==========")

# 1. Dataset dimensions
print("\n1. Dataset Shape:")
print(df.shape)

# 2. Column names
print("\n2. Column Names:")
print(df.columns.tolist())

# 3. First five records
print("\n3. First Five Records:")
print(df.head())

# 4. Dataset information
print("\n4. Dataset Information:")
df.info()

# 5. Missing values
print("\n5. Missing Values:")
print(df.isnull().sum())

# 6. Duplicate records
print("\n6. Duplicate Records:")
print(df.duplicated().sum())

# 7. Statistical summary
print("\n7. Statistical Summary:")
print(df.describe(include="all").T)

print("\n========== INITIAL EDA COMPLETED ==========")