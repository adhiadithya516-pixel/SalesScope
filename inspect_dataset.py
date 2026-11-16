from pathlib import Path

RAW_DATA_DIR = Path("data/raw")

print("\n========== OLIST DATASET FILE INSPECTION ==========")

if not RAW_DATA_DIR.exists():
    print("ERROR: Raw data folder not found!")
else:
    files = list(RAW_DATA_DIR.iterdir())

    for file in files:
        if file.is_file():
            size_kb = file.stat().st_size / 1024

            print(f"File: {file.name}")
            print(f"Size: {size_kb:.2f} KB")
            print("-" * 50)

print("\n========== INSPECTION COMPLETED ==========")