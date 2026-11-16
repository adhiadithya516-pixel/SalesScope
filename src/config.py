from pathlib import Path

# ==========================================
# PROJECT CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

REPORTS_DIR = PROJECT_ROOT / "reports"


# ==========================================
# APPLICATION INFORMATION
# ==========================================

APP_NAME = "SalesScope"

APP_VERSION = "1.0.0"


# ==========================================
# DATASET FILES
# ==========================================

DATA_FILES = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
    "geolocation": "olist_geolocation_dataset.csv"
}


# ==========================================
# BUSINESS RULES
# ==========================================

VALID_SALES_STATUS = ["delivered"]

CATEGORY_FALLBACK = "Uncategorized"

UNTRANSLATED_CATEGORIES = {
    "pc_gamer": "Gaming PC",
    "portateis_cozinha_e_preparadores_de_alimentos":
        "Small Kitchen Appliances"
}