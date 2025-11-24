# Skulytics Databricks Demo Data

This repository contains the DDLs, data generation scripts, and validation tests for the Skulytics eCommerce Analytics Demo.

## Overview

The data model represents a multi-retailer eCommerce environment with 50 products (SKUs) across 5 retailers (Amazon, Walmart, Target, Best Buy, DTC). It includes 3 years of historical data (2023-2025) and is designed to showcase AI-powered alerting and root cause analysis.

## Directory Structure

- `sql/dbx/ddl/dwh/`: Databricks SQL DDL files for all dimension and fact tables.
- `sql/dbx/dwh/`: Population scripts (or placeholders).
- `sql/dbx/tests/`: Data validation SQL scripts.
- `data/`: Generated CSV data files ready for upload.
- `generate_demo_data.py`: Python script used to generate the synthetic data.

## Key Features

- **Realistic Seasonality**: Holiday peaks, January slumps, weekend lifts.
- **Embedded Alert Stories**: Specific scenarios engineered into the data to trigger alerts (see `ALERT_STORIES.md`).
- **Comprehensive Metrics**: Sales, Traffic, Conversion, OOS, Content Health, Search Rank, Media Performance.

## How to Use

1. **Create Tables**: Run the DDL scripts in `sql/dbx/ddl/dwh/` in your Databricks SQL Warehouse.
2. **Load Data**: Upload the CSV files from `data/` to the corresponding tables (or use `COPY INTO`).
3. **Validate**: Run `sql/dbx/tests/data_validation.sql` to ensure data integrity and verify that alert stories are present.

## Unity Catalog Location

Target Catalog/Schema: `skulytics_dev.default`
