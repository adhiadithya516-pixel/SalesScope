import pandas as pd
import pytest

from src.sales_analysis import (
    get_sales_summary,
    get_sales_trend,
    get_order_status_summary
)

from src.product_analysis import (
    get_product_summary,
    get_top_products,
    get_top_products_by_orders
)

from src.category_analysis import (
    get_category_summary,
    get_top_categories,
    get_category_order_ranking
)

from src.weekly_comparison import get_weekly_sales_comparison


@pytest.fixture
def sample_master():
    """Create sample order-item-level data for analytics tests."""

    return pd.DataFrame([
        {
            "order_id": "O1",
            "order_item_id": 1,
            "order_status": "delivered",
            "order_purchase_timestamp": "2018-01-02",
            "product_id": "P1",
            "product_category_name_english": "Health & Beauty",
            "price": 100.0,
            "freight_value": 10.0
        },
        {
            "order_id": "O1",
            "order_item_id": 2,
            "order_status": "delivered",
            "order_purchase_timestamp": "2018-01-02",
            "product_id": "P2",
            "product_category_name_english": "Electronics",
            "price": 50.0,
            "freight_value": 5.0
        },
        {
            "order_id": "O2",
            "order_item_id": 1,
            "order_status": "delivered",
            "order_purchase_timestamp": "2018-01-09",
            "product_id": "P1",
            "product_category_name_english": "Health & Beauty",
            "price": 200.0,
            "freight_value": 20.0
        },
        {
            "order_id": "O3",
            "order_item_id": 1,
            "order_status": "shipped",
            "order_purchase_timestamp": "2018-01-10",
            "product_id": "P3",
            "product_category_name_english": "Electronics",
            "price": 500.0,
            "freight_value": 50.0
        }
    ])


def test_sales_summary(sample_master):
    result = get_sales_summary(sample_master)

    assert result["total_product_sales"] == 350.0
    assert result["total_freight"] == 35.0
    assert result["delivered_orders"] == 2
    assert result["average_order_value"] == 175.0


def test_sales_summary_excludes_non_delivered_orders(sample_master):
    result = get_sales_summary(sample_master)

    assert result["total_product_sales"] == 350.0
    assert result["delivered_orders"] == 2


def test_sales_summary_missing_column():
    df = pd.DataFrame({"order_id": ["O1"]})

    with pytest.raises(ValueError):
        get_sales_summary(df)


def test_daily_sales_trend(sample_master):
    result = get_sales_trend(sample_master, frequency="D")

    assert not result.empty
    assert "product_sales_value" in result.columns
    assert "freight_value" in result.columns
    assert "order_count" in result.columns
    assert result["product_sales_value"].sum() == 350.0


def test_weekly_sales_trend(sample_master):
    result = get_sales_trend(sample_master, frequency="W")

    assert not result.empty
    assert result["product_sales_value"].sum() == 350.0


def test_monthly_sales_trend(sample_master):
    result = get_sales_trend(sample_master, frequency="MS")

    assert len(result) == 1
    assert result.iloc[0]["product_sales_value"] == 350.0


def test_invalid_sales_trend_frequency(sample_master):
    with pytest.raises(ValueError):
        get_sales_trend(sample_master, frequency="YEARLY")


def test_order_status_summary():
    orders = pd.DataFrame({
        "order_id": ["O1", "O2", "O3", "O4", "O5"],
        "order_status": [
            "delivered",
            "delivered",
            "shipped",
            "canceled",
            "delivered"
        ]
    })

    result = get_order_status_summary(orders)

    delivered = result[
        result["order_status"] == "delivered"
    ]["order_count"].iloc[0]

    assert delivered == 3
    assert result["order_count"].sum() == 5


def test_product_summary(sample_master):
    result = get_product_summary(sample_master)

    assert len(result) == 2
    assert result.iloc[0]["product_id"] == "P1"

    product_p1 = result[result["product_id"] == "P1"].iloc[0]

    assert product_p1["product_sales_value"] == 300.0
    assert product_p1["order_count"] == 2
    assert product_p1["order_item_count"] == 2


def test_top_products(sample_master):
    result = get_top_products(sample_master, top_n=1)

    assert len(result) == 1
    assert result.iloc[0]["product_id"] == "P1"


def test_top_products_by_orders(sample_master):
    result = get_top_products_by_orders(sample_master, top_n=2)

    assert len(result) == 2
    assert result.iloc[0]["product_id"] == "P1"


def test_product_top_n_must_be_positive(sample_master):
    with pytest.raises(ValueError):
        get_top_products(sample_master, top_n=0)


def test_category_summary(sample_master):
    result = get_category_summary(sample_master)

    assert len(result) == 2
    assert result.iloc[0]["category"] == "Health & Beauty"

    health = result[
        result["category"] == "Health & Beauty"
    ].iloc[0]

    assert health["category_sales"] == 300.0
    assert health["product_count"] == 1
    assert health["order_count"] == 2


def test_top_categories(sample_master):
    result = get_top_categories(sample_master, top_n=1)

    assert len(result) == 1
    assert result.iloc[0]["category"] == "Health & Beauty"


def test_category_order_ranking(sample_master):
    result = get_category_order_ranking(sample_master, top_n=2)

    assert len(result) == 2
    assert result.iloc[0]["category"] == "Health & Beauty"


def test_category_top_n_must_be_positive(sample_master):
    with pytest.raises(ValueError):
        get_top_categories(sample_master, top_n=0)


def test_weekly_sales_comparison(sample_master):
    result = get_weekly_sales_comparison(sample_master)

    assert len(result) == 2
    assert result.iloc[0]["weekly_sales"] == 150.0
    assert result.iloc[1]["weekly_sales"] == 200.0
    assert result.iloc[1]["previous_week_sales"] == 150.0


def test_weekly_sales_growth(sample_master):
    result = get_weekly_sales_comparison(sample_master)

    growth = result.iloc[1]["sales_growth_percent"]

    assert growth == pytest.approx(33.3333, rel=1e-3)


def test_weekly_comparison_missing_columns():
    df = pd.DataFrame({"order_id": ["O1"]})

    with pytest.raises(ValueError):
        get_weekly_sales_comparison(df)