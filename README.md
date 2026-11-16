# SalesScope – Retail Sales Analytics Dashboard

**A Python-powered business intelligence dashboard for retail and e-commerce sales analytics.**

SalesScope is an interactive retail sales analytics platform designed to transform raw e-commerce transaction data into meaningful business insights. It enables users to monitor sales performance, analyse products and categories, understand customer behaviour, examine payment and delivery performance, and generate downloadable business reports.

Built using Python, Pandas and Streamlit, SalesScope provides an interactive analytical environment with reusable data-processing modules, dynamic filters and automated data validation.

---

## Project Overview

Retail businesses generate large volumes of transactional data, making it difficult to monitor performance and identify meaningful patterns manually.

SalesScope addresses this challenge by integrating multiple e-commerce datasets into a unified analytical dataset and presenting the results through an interactive dashboard.

The application provides insights into:

- Overall sales and revenue performance.
- Daily, weekly and monthly sales trends.
- Top-performing products.
- Product category performance.
- Customer purchasing behaviour.
- Payment methods and financial reconciliation.
- Delivery performance and customer reviews.
- Exportable business intelligence reports.

## Dashboard Modules

SalesScope contains eight analytical modules.

### 1. Overview
- Key business performance indicators.
- Monthly sales trends.
- Category-level sales distribution.
- Top-performing products.
- Filtered business summaries.

### 2. Sales Analytics
- Daily, weekly and monthly sales analysis.
- Sales trend visualisation.
- Weekly sales comparison.
- Order status analysis.
- Percentage change in sales.

### 3. Product Performance
- Top products by sales.
- Product performance ranking.
- Product-level sales summaries.
- Product frequency analysis.

### 4. Category Analytics
- Category-wise revenue analysis.
- Category contribution to total sales.
- Category ranking.
- Category-level performance summaries.

### 5. Customer Analytics
- Customer purchasing behaviour.
- Repeat and one-time customer analysis.
- Customer segmentation.
- Purchase frequency.
- Monthly customer activity.

### 6. Payments & Finance
- Payment method distribution.
- Payment value analysis.
- Payment transaction summaries.
- Financial reconciliation.
- Identification of payment discrepancies.

### 7. Delivery & Reviews
- Delivery performance analysis.
- Average delivery time.
- Delayed delivery analysis.
- Review score distribution.
- Positive and negative review analysis.

### 8. Reports & Downloads
- Consolidated Excel business intelligence report.
- Individual CSV reports.
- Filter-based report generation.
- Exportable analytical summaries.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Streamlit | Interactive dashboard development |
| Plotly | Interactive data visualisation |
| Matplotlib | Data visualisation, where used |
| OpenPyXL | Excel report generation, where used |
| Pytest | Automated testing |
| Git & GitHub | Version control and source code management |

---

## Dataset

SalesScope uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains multiple interconnected CSV files representing different aspects of an e-commerce business.

### Dataset Files

| Dataset | Description |
|---|---|
| olist_orders_dataset.csv | Order information |
| olist_order_items_dataset.csv | Products associated with orders |
| olist_products_dataset.csv | Product information |
| olist_customers_dataset.csv | Customer information |
| olist_sellers_dataset.csv | Seller information |
| olist_order_payments_dataset.csv | Payment transactions |
| olist_order_reviews_dataset.csv | Customer reviews |
| product_category_name_translation.csv | Product category translations |

### Data Processing

The project follows a structured data pipeline:

1. Load raw CSV datasets.
2. Clean and validate individual datasets.
3. Handle missing and invalid values.
4. Integrate related datasets using their keys.
5. Aggregate payment and review records at order level.
6. Generate a unified master dataset.
7. Perform analytical calculations.
8. Display results through the Streamlit dashboard.

**Master dataset grain:** One row per order item.

Payment and review records are aggregated before integration to avoid multiplying order-item records during joins.

### Data Interpretation

- Product revenue is calculated using product prices.
- Freight charges are analysed separately.
- Payment values are not treated as identical to product revenue.
- Profit is not calculated because product cost information is unavailable.
- Order item records are not interpreted as individual product quantities.

---

## Project Architecture

```text
SalesScope/
│
├── dashboard/
│   ├── app.py
│   ├── data_service.py
│   │
│   ├── components/
│   │   ├── charts.py
│   │   ├── filters.py
│   │   └── kpi_cards.py
│   │
│   └── pages/
│       ├── overview.py
│       ├── sales_analysis.py
│       ├── product_performance.py
│       ├── category_analysis.py
│       ├── customer_analytics.py
│       ├── payments_finance.py
│       ├── delivery_reviews.py
│       └── reports.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── data_cleaning.py
│   ├── data_validation.py
│   ├── data_integration.py
│   ├── filter_engine.py
│   ├── kpi_engine.py
│   ├── sales_analysis.py
│   ├── product_analysis.py
│   ├── category_analysis.py
│   ├── weekly_comparison.py
│   └── report_generator.py
│
├── tests/
│   ├── test_analysis.py
│   ├── test_cleaning.py
│   └── test_validation.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation and Setup

### Prerequisites

- Python 3.13 or compatible Python environment.
- pip package manager.
- Git.
- GitHub repository access.
- Olist dataset CSV files.

### 1. Clone the Repository

```bash
git clone https://github.com/adhiadithya516-pixel/SalesScope.git
```

### 2. Navigate to the Project

```bash
cd SalesScope
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Add the Dataset

Download the Olist dataset and place the required CSV files inside:

```text
data/raw/
```

Ensure that the filenames match those listed in the Dataset section.

### 7. Run the Application

```bash
python -m streamlit run dashboard/app.py
```

The application will open in your browser.

---

## Testing

SalesScope includes automated tests using Pytest.

The test suite covers:

- Sales analysis.
- Product analysis.
- Category analysis.
- Weekly sales comparison.
- Data cleaning.
- Dataset validation.
- Primary key and foreign key checks.
- Financial data validation.

Run the complete test suite:

```bash
python -m pytest -v
```

### Current Test Results

| Metric | Result |
|---|---:|
| Total tests | 42 |
| Passed | 42 |
| Failed | 0 |
| Execution time | 3.08 seconds |

All 42 tests passed in the latest recorded test run.

---

## Key Features

- Interactive multi-page Streamlit dashboard.
- Reusable data-processing and analytical modules.
- Shared sidebar filters.
- KPI-based business performance monitoring.
- Daily, weekly and monthly sales analysis.
- Product and category ranking.
- Customer purchasing behaviour analysis.
- Payment and delivery performance analysis.
- Financial reconciliation and exception reporting.
- Excel and CSV report generation.
- Automated data validation.
- Automated testing with Pytest.

---

## Project Limitations

- Profitability analysis is not available because product cost data is not provided.
- Geographic intelligence is outside the current project scope.
- Results depend on the quality and completeness of the source dataset.
- Financial reconciliation differences are reported rather than artificially adjusted.
- The dashboard analyses historical data and does not provide real-time transaction monitoring.

---

## Future Enhancements

Potential improvements include:

- Additional business performance indicators.
- Enhanced report customisation.
- More advanced analytical visualisations.
- Improved dashboard deployment and accessibility.
- Additional automated data quality checks.

---

## Author

**Adithya A V**

GitHub: [adhiadithya516-pixel](https://github.com/adhiadithya516-pixel)

Project Repository: [SalesScope](https://github.com/adhiadithya516-pixel/SalesScope)

---

## Project Objective

SalesScope demonstrates practical skills in Python programming, data cleaning, data integration, exploratory data analysis, business analytics, data visualisation, automated testing and interactive dashboard development.

**Turning retail transaction data into actionable business insights.**