```markdown
# Skulytics Databricks Demo: Comprehensive Data Build Instructions

## Project Overview

**Purpose:** Build a complete, production-ready eCommerce analytics data warehouse for a Databricks app demo at a January 2026 conference. The demo showcases AI-powered alerting, root cause analysis, product performance optimization, and content improvement workflows.

**Unity Catalog Location:** `skulytics_dev.default`

**Target Audience:** Google Antigravity AI coding agent (or any developer with no prior project context)

**Key Success Criteria:**
- Data tells compelling business stories through embedded KPI anomalies
- Historical depth (2+ years) for realistic trend analysis
- All alert scenarios trigger correctly via SQL queries
- Professional data quality suitable for executive-level demo

---

## File Structure and Deliverables

### Output Locations

**DDL Files (Table Definitions):**
- Location: `sql/dbx/ddl/dwh/`
- Format: Databricks SQL DDL statements
- Purpose: Define all dimension and fact table schemas

**Population Scripts (Data Generation Logic):**
- Location: `sql/dbx/dwh/`
- Format: INSERT statements or Python/PySpark data generation scripts
- Purpose: Populate tables with synthetic data
- Base them off of sql/GCP/dwh/ scripts

**CSV Data Files:**
- Location: `data/`
- Format: UTF-8 CSV with headers
- Purpose: Exportable data for manual Databricks upload if needed

### Required Files

**DDL Files to Create (in `sql/dbx/ddl/dwh/`):**
1. `dim_date.sql`
2. `dim_region.sql`
3. `dim_brand.sql`
4. `dim_retailer.sql`
5. `dim_product.sql`
6. `fact_retail_summary_tbl.sql`
7. `fact_retail_media_tbl.sql`
8. `fact_retail_search_rank_tbl.sql`
9. `fact_retail_product_mob_tbl.sql`
10. `fact_retail_retailer_mob_tbl.sql`
11. `fact_retail_brand_mob_tbl.sql`
12. `stg_fact_retail_summary_tbl.sql`



**Population Scripts to Create (in `sql/dbx/dwh/`):**
- One script per table matching the DDL files above
- Base them off of sql/GCP/dwh/ scripts

**CSV Files to Generate (in `data/`):**
- One CSV per table matching all table names above

---

## GCP to Databricks Translation Rules

### Critical Syntax Differences

The source DDLs and population scripts were written for Google Cloud Platform (BigQuery). You MUST translate all syntax for Databricks compatibility.

**Data Type Conversions:**
| GCP Type | Databricks Type |
|----------|-----------------|
| `INT64` | `BIGINT` |
| `FLOAT64` | `DOUBLE` |
| `BOOL` | `BOOLEAN` |
| `NUMERIC` | `DECIMAL(precision, scale)` |
| `STRING` | `STRING` (same) |
| `DATE` | `DATE` (same) |
| `TIMESTAMP` | `TIMESTAMP` (same) |
| `ARRAY<TYPE>` | `ARRAY<TYPE>` (same) |

**Column Metadata:**
```
-- GCP
column_name STRING OPTIONS(description='Description text')

-- Databricks
column_name STRING COMMENT 'Description text'
```

**Table Creation:**
```
-- GCP
CREATE TABLE `project.dataset.table_name` (...)

-- Databricks
CREATE TABLE skulytics_dev.default.table_name (...) USING DELTA
```

**Partitioning:**
```
-- GCP
PARTITION BY DATE_TRUNC(month_start_date, MONTH)
CLUSTER BY brand_key, retailer_key

-- Databricks (for Delta tables, clustering is handled by optimization)
PARTITIONED BY (month_start_date)
```

**Date Functions:**
```
-- GCP
GENERATE_DATE_ARRAY(DATE('2024-01-01'), DATE('2025-12-31'), INTERVAL 1 DAY)

-- Databricks
SEQUENCE(DATE('2024-01-01'), DATE('2025-12-31'), INTERVAL 1 DAY)
```

**UNNEST:**
```
-- GCP
CROSS JOIN UNNEST(array_column) AS element

-- Databricks
LATERAL VIEW EXPLODE(array_column) AS element
```

---

## Business Context and Demo Use Case

### What is Skulytics?

Skulytics is an AI-powered eCommerce analytics platform that helps merchandising, sales, and marketing teams:
- Monitor product performance across multiple retailers and channels
- Detect issues through intelligent alerting (sales drops, conversion declines, stock-outs)
- Diagnose root causes (OOS, poor content, review problems, rank changes)
- Take corrective action (content optimization, inventory restocking, pricing adjustments)
- Measure impact of interventions

### Target Demo Flow

1. **Dashboard View:** User sees alert cards highlighting issues (e.g., "Conversion down 22% for SKU003")
2. **Investigation:** User clicks alert, drills into Product Performance module, sees trends and root causes
3. **Action:** System recommends fixes (improve content, restock inventory, adjust pricing)
4. **Content Crafter:** User deploys AI-generated improved product content
5. **Impact Tracking:** System shows before/after KPI improvements

### Key Performance Indicators (KPIs)

The data model must support these critical metrics:
- **Sales Metrics:** Gross sales (USD), units sold, average order value
- **Traffic & Conversion:** Total visits, total orders, conversion rate (CVR)
- **Inventory:** Out of stock (OOS) days, OOS percentage, stock availability
- **Content Health:** Title score, description score, image score, keyword score, rating score, review score, overall content score (all 0-100)
- **Search Performance:** Organic rank, paid rank, search visibility
- **Media Performance:** Ad spend, impressions, clicks, click-through rate (CTR), cost per click (CPC), return on ad spend (ROAS)
- **Reviews:** Review rating (1-5 stars), review count

---

## Dimension Tables: Complete Specifications

### 1. dim_date

**Purpose:** Date dimension for temporal analysis and time-series filtering

**DDL:**
```
CREATE TABLE skulytics_dev.default.dim_date (
    datekey DATE PRIMARY KEY COMMENT 'Date identifier (YYYY-MM-DD)',
    full_date DATE COMMENT 'Full calendar date',
    year INT COMMENT 'Calendar year (e.g., 2024)',
    month INT COMMENT 'Month number (1-12)',
    month_name STRING COMMENT 'Month name (January, February, etc.)',
    month_abbr STRING COMMENT 'Month abbreviation (Jan, Feb, etc.)',
    week INT COMMENT 'Week of year (1-52)',
    week_start_date DATE COMMENT 'Monday of the week',
    week_end_date DATE COMMENT 'Friday of the week',
    day_of_month INT COMMENT 'Day of month (1-31)',
    day_of_week INT COMMENT 'Day of week (1=Monday, 7=Sunday)',
    day_name STRING COMMENT 'Day name (Monday, Tuesday, etc.)',
    day_abbr STRING COMMENT 'Day abbreviation (Mon, Tue, etc.)',
    quarter INT COMMENT 'Quarter (1-4)',
    quarter_name STRING COMMENT 'Quarter name (Q1, Q2, Q3, Q4)',
    is_weekend BOOLEAN COMMENT 'True if Saturday or Sunday',
    is_holiday BOOLEAN COMMENT 'True if major retail holiday',
    holiday_name STRING COMMENT 'Holiday name if applicable',
    fiscal_year INT COMMENT 'Fiscal year',
    fiscal_quarter INT COMMENT 'Fiscal quarter (1-4)',
    fiscal_period INT COMMENT 'Fiscal period/month (1-12)',
    ly_date DATE COMMENT 'Same date last year (for YoY comparison)',
    fiscly_date DATE COMMENT 'Same date last fiscal year',
    gregly_date DATE COMMENT 'Same date last Gregorian year'
) USING DELTA
COMMENT 'Date dimension for temporal analysis';
```

**Data Requirements:**
- **Date Range:** January 1, 2023 to March 1, 2026 
- **Fiscal Year:** Starts February 1 (common retail calendar)
- **Holidays to Flag:** New Year's Day, Memorial Day, July 4th, Labor Day, Black Friday, Cyber Monday, Christmas Eve, Christmas Day, New Year's Eve
- **Week Definition:** Monday-Sunday, with week_end_date being Friday for reporting purposes

**Sample Rows:**
```
datekey,full_date,year,month,month_name,week,day_of_week,day_name,is_weekend,is_holiday,holiday_name
2024-01-01,2024-01-01,2024,1,January,1,1,Monday,false,true,New Year's Day
2024-11-29,2024-11-29,2024,11,November,48,5,Friday,false,true,Black Friday
2024-12-25,2024-12-25,2024,12,December,52,3,Wednesday,false,true,Christmas Day
```

---

### 2. dim_region

**Purpose:** Geographic regions for market analysis

**DDL:**
```
CREATE TABLE skulytics_dev.default.dim_region (
    region_key BIGINT PRIMARY KEY COMMENT 'Region identifier',
    region_name STRING COMMENT 'Region display name',
    region_code STRING COMMENT 'Region abbreviation (2-3 chars)',
    country STRING COMMENT 'Primary country',
    currency STRING COMMENT 'Currency code (USD, EUR, etc.)',
    timezone STRING COMMENT 'Primary timezone'
) USING DELTA
COMMENT 'Geographic regions for market segmentation';
```

**Required Records:**
```
region_key,region_name,region_code,country,currency,timezone
0,Global,GLB,Multiple,USD,UTC
1,North America,NAM,United States,USD,America/New_York
2,Europe,EUR,United Kingdom,EUR,Europe/London
3,Asia Pacific,APAC,Australia,AUD,Australia/Sydney
```

**Why These Regions:**
- Global (region_key=0) for aggregate/multi-region analysis
- North America (key=1) as primary demo market
- Europe and APAC for international expansion stories

---

### 3. dim_brand

**Purpose:** Product brands for portfolio analysis

**DDL:**
```
CREATE TABLE skulytics_dev.default.dim_brand (
    brand_key BIGINT PRIMARY KEY COMMENT 'Brand identifier',
    brand_name STRING COMMENT 'Brand display name',
    category STRING COMMENT 'Product category',
    subcategory STRING COMMENT 'Product subcategory',
    brand_tier STRING COMMENT 'Premium/Standard/Value pricing tier',
    brand_description STRING COMMENT 'Brand positioning statement'
) USING DELTA
COMMENT 'Product brands for portfolio segmentation';
```

**Required Records:**
```
brand_key,brand_name,category,subcategory,brand_tier,brand_description
1,TechNova,Electronics,Audio,Premium,Premium wireless audio devices
2,SmartHome Pro,Electronics,Smart Home,Standard,Affordable smart home automation
3,FitLife,Health & Beauty,Fitness,Standard,Everyday fitness and wellness products
4,HomeEssentials,Home & Kitchen,Kitchen Appliances,Value,Budget-friendly kitchen solutions
5,PureGlow,Health & Beauty,Skincare,Premium,Luxury organic skincare line
6,GadgetMaster,Electronics,Accessories,Standard,Tech accessories and peripherals
7,EcoLiving,Home & Kitchen,Sustainability,Premium,Eco-friendly home products
```

**Category Distribution:**
- Electronics: 3 brands (capturing majority of demo scenarios)
- Health & Beauty: 2 brands
- Home & Kitchen: 2 brands

**Tier Distribution:**
- Premium: 3 brands (higher price points, lower volume, content-sensitive)
- Standard: 3 brands (mid-market, balanced)
- Value: 1 brand (high volume, price-sensitive)

---

### 4. dim_retailer

**Purpose:** Retail channels and partners

**DDL:**
```
CREATE TABLE skulytics_dev.default.dim_retailer (
    retailer_key BIGINT PRIMARY KEY COMMENT 'Retailer identifier',
    retailer_name STRING COMMENT 'Retailer display name',
    retailer_type STRING COMMENT 'Online/Omnichannel/Marketplace/DTC',
    region_key BIGINT COMMENT 'Primary operating region',
    market_share_pct DOUBLE COMMENT 'Approximate market share percentage',
    FOREIGN KEY (region_key) REFERENCES dim_region(region_key)
) USING DELTA
COMMENT 'Retail channels and marketplace partners';
```

**Required Records:**
```
retailer_key,retailer_name,retailer_type,region_key,market_share_pct
1,Amazon,Marketplace,1,38.7
2,Walmart.com,Omnichannel,1,6.3
3,Target.com,Omnichannel,1,3.9
4,Best Buy,Omnichannel,1,2.1
5,Company DTC Site,DTC,1,1.5
```

**Why These Retailers:**
- Amazon (key=1): Largest, most data, primary for alert stories
- Walmart/Target: Major omnichannel competitors
- Best Buy: Category-specific (electronics focus)
- DTC: Direct-to-consumer channel for control comparison

---

### 5. dim_product

**Purpose:** SKU/product catalog

**DDL:**
```
CREATE TABLE skulytics_dev.default.dim_product (
    productkey STRING PRIMARY KEY COMMENT 'SKU identifier',
    product_name STRING COMMENT 'Product display name',
    brand_key BIGINT COMMENT 'Brand foreign key',
    category STRING COMMENT 'Product category',
    subcategory STRING COMMENT 'Product subcategory',
    upc_code STRING COMMENT 'Universal Product Code (12 digits)',
    price_tier STRING COMMENT 'Budget/Mid/Premium price point',
    base_price DOUBLE COMMENT 'Manufacturer suggested retail price (MSRP)',
    is_hero_product BOOLEAN COMMENT 'True if flagship/hero product for brand',
    launch_date DATE COMMENT 'Product launch date',
    product_status STRING COMMENT 'Active/Discontinued/Seasonal',
    FOREIGN KEY (brand_key) REFERENCES dim_brand(brand_key)
) USING DELTA
COMMENT 'Product/SKU dimension for product-level analysis';
```

**Data Requirements:**
- **Total Products:** 50 SKUs
- **Distribution by Brand:** 6-8 products per brand
- **Hero Products:** 12 products flagged as hero (24%)
- **Price Ranges:**
  - Budget: $10-$30
  - Mid: $30-$100
  - Premium: $100-$500
- **Launch Dates:** Staggered from 2022-2024 for lifecycle analysis
- **UPC Codes:** Generate realistic 12-digit codes

**Required Specific Products (for alert stories):**
```
productkey,product_name,brand_key,category,price_tier,base_price,is_hero_product,launch_date
SKU001,TechNova Wireless Earbuds Pro,1,Electronics,Premium,149.99,true,2023-03-15
SKU003,SmartHome WiFi Camera 360,2,Electronics,Mid,79.99,false,2023-06-01
SKU007,FitLife Yoga Mat Premium,3,Health & Beauty,Mid,49.99,false,2023-01-10
SKU009,SmartHome Smart Thermostat,2,Electronics,Mid,129.99,true,2022-11-01
SKU012,TechNova Wireless Charging Pad,1,Electronics,Premium,59.99,true,2023-05-20
SKU015,HomeEssentials Coffee Maker Deluxe,4,Home & Kitchen,Budget,39.99,false,2022-08-15
SKU018,GadgetMaster USB-C Hub 7-in-1,6,Electronics,Mid,34.99,false,2023-09-01
SKU022,PureGlow Vitamin C Serum,5,Health & Beauty,Premium,79.99,false,2023-02-28
```

*Generate remaining 42 products following similar patterns, ensuring good distribution across brands, categories, and price tiers.*

---

## Fact Tables: Complete Specifications

### 1. fact_retail_summary_tbl

**Purpose:** Core table with daily product performance across all KPIs

**Full DDL (adapted from GCP source):**
```
CREATE TABLE skulytics_dev.default.fact_retail_summary_tbl (
    -- Keys
    retail_summary_key STRING COMMENT 'Primary key: concat(retailer_key,"-",productkey,"-",datekey)',
    retailer_product_key STRING COMMENT 'Retailer-product composite key',
    brand_key BIGINT COMMENT 'Brand identifier (FK to dim_brand)',
    region_key BIGINT COMMENT 'Region identifier (FK to dim_region)',
    retailer_key BIGINT COMMENT 'Retailer identifier (FK to dim_retailer)',
    product_key STRING COMMENT 'Product identifier (FK to dim_product)',
    
    -- Temporal Keys
    week_end_date DATE COMMENT 'End of week (Friday)',
    month_start_date DATE COMMENT 'First day of month',
    date_key DATE COMMENT 'Transaction date (FK to dim_date)',
    last_year_date DATE COMMENT 'Same date last year for YoY comparison',
    fiscly_date DATE COMMENT 'Same date last fiscal year',
    gregly_date DATE COMMENT 'Same date last Gregorian year',
    
    -- Sales Metrics (This Year)
    gross_sales_usd_ty DOUBLE COMMENT 'Gross sales in USD - this year',
    gross_units_sold_ty BIGINT COMMENT 'Units sold - this year',
    
    -- Sales Metrics (Last Year Comparisons)
    gross_sales_usd_ly DOUBLE COMMENT 'Gross sales USD - last year same period',
    gross_units_sold_ly BIGINT COMMENT 'Units sold - last year same period',
    gross_sales_usd_fiscly DOUBLE COMMENT 'Gross sales USD - last fiscal year',
    gross_units_sold_fiscly BIGINT COMMENT 'Units sold - last fiscal year',
    gross_sales_usd_gregly DOUBLE COMMENT 'Gross sales USD - last Gregorian year',
    gross_units_sold_gregly BIGINT COMMENT 'Units sold - last Gregorian year',
    
    -- Out of Stock Metrics
    is_out_of_stock BOOLEAN COMMENT 'True if product unavailable this day',
    oos_days_ty BIGINT COMMENT 'Count of OOS days - this period',
    oos_percent_ty DOUBLE COMMENT 'Percentage of days OOS - this period',
    oos_days_ly BIGINT COMMENT 'OOS days - last year',
    oos_percent_ly DOUBLE COMMENT 'OOS percent - last year',
    
    -- Pricing Metrics
    unit_price_ty DOUBLE COMMENT 'List price per unit - this year',
    selling_price_ty DOUBLE COMMENT 'Actual selling price - this year',
    unit_price_ly DOUBLE COMMENT 'Unit price - last year',
    selling_price_ly DOUBLE COMMENT 'Selling price - last year',
    
    -- Content Health Scores (0-100)
    content_score BIGINT COMMENT 'Overall content health composite score',
    title_score BIGINT COMMENT 'Product title quality score',
    desc_score BIGINT COMMENT 'Description completeness/quality score',
    image_score BIGINT COMMENT 'Image quality and count score',
    keyword_score BIGINT COMMENT 'Keyword optimization score',
    rating_score BIGINT COMMENT 'Customer rating health score (normalized to 0-100)',
    review_score BIGINT COMMENT 'Review volume and recency score',
    
    -- Sponsored Product Metrics
    is_sponsored_product BOOLEAN COMMENT 'True if product had paid ads this day',
    sponsored_product_sales_ty DOUBLE COMMENT 'Sales from sponsored placements - this year',
    sponsored_product_units_ty BIGINT COMMENT 'Units from sponsored - this year',
    sponsored_product_sales_ly DOUBLE COMMENT 'Sponsored sales - last year',
    sponsored_product_units_ly BIGINT COMMENT 'Sponsored units - last year',
    
    -- Traffic and Conversion Metrics
    total_orders_ty BIGINT COMMENT 'Total orders - this year',
    total_visits_ty BIGINT COMMENT 'Product page visits - this year',
    cvr_ty DOUBLE COMMENT 'Conversion rate (orders/visits) - this year',
    total_orders_ly BIGINT COMMENT 'Orders - last year',
    total_visits_ly BIGINT COMMENT 'Visits - last year',
    cvr_ly DOUBLE COMMENT 'Conversion rate - last year',
    
    -- Search Rank Metrics
    organic_rank_ty BIGINT COMMENT 'Organic search ranking position - this year',
    paid_rank_ty BIGINT COMMENT 'Paid search ranking position - this year',
    organic_rank_ly BIGINT COMMENT 'Organic rank - last year',
    paid_rank_ly BIGINT COMMENT 'Paid rank - last year',
    
    -- Review Metrics
    review_rating DOUBLE COMMENT 'Average star rating (1.0-5.0)',
    review_count BIGINT COMMENT 'Total number of reviews',
    
    -- Audit Fields
    record_created_date TIMESTAMP COMMENT 'Record creation timestamp',
    record_updated_date TIMESTAMP COMMENT 'Record last updated timestamp'
) USING DELTA
PARTITIONED BY (month_start_date)
COMMENT 'Daily retail performance summary with all KPIs';
```

**Data Volume:**
- **Row Count Target:** ~2.5 million rows
- **Calculation:** 50 products × 5 retailers × 3 years × 365 days = ~273,750 theoretical max
- **Realistic Coverage:** Not every product at every retailer every day. Use ~80% coverage for realism.

**Data Generation Rules:**

**Baseline Patterns (for "normal" periods):**
- **Gross Sales:** 
  - Budget tier: $200-$2,000/day depending on retailer
  - Mid tier: $500-$8,000/day
  - Premium tier: $300-$5,000/day (lower volume, higher price)
  - Amazon gets 40-50% higher sales than other retailers
  
- **Units Sold:** Sales / selling_price (with some variance)

- **Conversion Rate (CVR):**
  - Baseline: 3-7% depending on content health and price tier
  - Premium products: 2-4%
  - Mid products: 4-6%
  - Budget products: 5-8%
  - CVR correlates positively with content_score (higher content = higher CVR)

- **Out of Stock:**
  - Normal: 2-5% of days
  - Holiday periods: 8-12% (higher demand strain)

- **Content Scores:**
  - Most products: 65-90 across all dimensions
  - Products in "poor content" stories: Start at 40-60
  - Hero products: 75-95 (well-maintained)

- **Organic Rank:**
  - Hero products: 1-15 for branded keywords
  - Standard products: 10-40
  - Lower-tier products: 20-60
  - Rank correlates with sales volume and content health

- **Paid Rank:**
  - NULL if not running ads that day
  - 1-10 when sponsored (top of search results)

- **Review Rating:**
  - Most products: 3.8-4.6 stars
  - Top products: 4.3-4.8 stars
  - Problem products in stories: Can dip to 3.2-3.9

- **Review Count:**
  - New products (<1 year): 50-300 reviews
  - Mature products: 500-3000 reviews
  - Hero products: 1000-5000 reviews

**Seasonality Patterns:**
- **November-December (Holiday):** Sales +35-60%, traffic +40-50%, OOS +100-150%
- **January (Post-Holiday):** Sales -20-30% from baseline
- **Back to School (August-September):** Electronics +15-25%
- **Summer (June-July):** Home & Kitchen +10-15%

**Weekly Patterns:**
- **Monday-Thursday:** 90-100% of baseline
- **Friday-Sunday:** 110-120% of baseline (weekend shopping)

---

### Alert Story Data Requirements

You MUST engineer the following specific scenarios into the data. These are not optional—the demo depends on them.

#### Story 1: Conversion Drop Crisis (SKU003 - SmartHome WiFi Camera)

**Timeline:** October 15 - November 18, 2025

**Affected Product:** SKU003 at Amazon (retailer_key=1)

**Narrative:** A perfect storm of issues causes dramatic conversion decline, system detects it, recommends fixes, recovery follows.

**Week-by-Week Data Specifications:**

**Week 1: Baseline (Oct 15-21, 2025)**
```
date_key: 2025-10-15 to 2025-10-21
product_key: SKU003
retailer_key: 1
gross_sales_usd_ty: $4,200/day (normal)
gross_units_sold_ty: 52/day
total_visits_ty: 1,300/day
total_orders_ty: 52/day
cvr_ty: 4.0% (52/1300)
is_out_of_stock: FALSE
oos_days_ty: 0
oos_percent_ty: 0.0
review_rating: 4.2
review_count: 847
review_score: 78
content_score: 72
organic_rank_ty: 23
```

**Week 2: Problem Emerges (Oct 22-28)**
```
date_key: 2025-10-22 to 2025-10-28
-- OOS event begins
is_out_of_stock: TRUE for Oct 24, 25, 26, 27 (4 days)
oos_days_ty: 4
oos_percent_ty: 57.1% (4/7 days)
-- Negative review bomb
review_rating: 3.8 (dropped from 4.2)
review_count: 863 (+16, mostly negative)
review_score: 65 (dropped from 78)
-- Conversion starts declining
cvr_ty: 3.3% (down 17.5% from baseline)
total_visits_ty: 1,250/day (slight decline)
total_orders_ty: 41/day
gross_sales_usd_ty: $3,320/day
-- Content unchanged
content_score: 72 (same)
```

**Week 3: Crisis Deepens (Oct 29 - Nov 4)**
```
date_key: 2025-10-29 to 2025-11-04
-- Continued OOS impact
is_out_of_stock: TRUE for Oct 29, 30, 31 (3 more days)
oos_days_ty: 7 (cumulative over 2 weeks)
oos_percent_ty: 50% (7/14 days)
-- Reviews continue to hurt
review_rating: 3.7
review_count: 891 (+28 more)
review_score: 62
-- Rank drops due to low sales
organic_rank_ty: 31 (dropped from 23)
-- Conversion hits bottom
cvr_ty: 2.6% (down 35% from baseline!)
total_visits_ty: 1,100/day (traffic dropping due to rank)
total_orders_ty: 29/day
gross_sales_usd_ty: $2,349/day (down 44% from baseline)
```

**Week 4: Recovery Begins (Nov 5-11)**
```
date_key: 2025-11-05 to 2025-11-11
-- Stock restored
is_out_of_stock: FALSE (all days)
-- Review response strategy deployed
review_rating: 3.9 (slight improvement from responses)
review_score: 68 (improving)
-- Some recovery
cvr_ty: 3.2% (partial recovery)
total_visits_ty: 1,200/day
total_orders_ty: 38/day
gross_sales_usd_ty: $3,078/day
organic_rank_ty: 28 (improving)
```

**Week 5: Full Recovery (Nov 12-18)**
```
date_key: 2025-11-12 to 2025-11-18
-- Stability
is_out_of_stock: FALSE
oos_percent_ty: 0%
-- Reviews stabilized
review_rating: 4.0
review_score: 72
-- Conversion returns to baseline
cvr_ty: 3.9% (near baseline of 4.0%)
total_visits_ty: 1,280/day
total_orders_ty: 50/day
gross_sales_usd_ty: $4,050/day
organic_rank_ty: 25
```

**Alert Trigger Validation Query:**
```
-- This query MUST return rows for SKU003 in late October 2025
SELECT 
    date_key,
    product_key,
    cvr_ty,
    LAG(cvr_ty, 7) OVER (PARTITION BY product_key, retailer_key ORDER BY date_key) as cvr_1w_ago,
    ((cvr_ty - LAG(cvr_ty, 7) OVER (PARTITION BY product_key, retailer_key ORDER BY date_key)) / 
     LAG(cvr_ty, 7) OVER (PARTITION BY product_key, retailer_key ORDER BY date_key)) * 100 as cvr_wow_pct_change,
    is_out_of_stock,
    oos_percent_ty,
    review_rating,
    review_score
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE product_key = 'SKU003'
  AND retailer_key = 1
  AND date_key BETWEEN '2025-10-15' AND '2025-11-18'
  AND cvr_wow_pct_change < -15.0  -- Alert threshold
ORDER BY date_key;
```

---

#### Story 2: Content Health Transformation (SKU015 & SKU022)

**Timeline:** September 1 - October 31, 2025

**Affected Products:** 
- SKU015 (HomeEssentials Coffee Maker) at Walmart
- SKU022 (PureGlow Vitamin C Serum) at Amazon

**Narrative:** Products with poor content get AI-powered content overhaul, resulting in measurable KPI improvements.

**Phase 1: Poor Content Baseline (Sep 1-15)**
```
product_key: SKU015
retailer_key: 2 (Walmart)
date_key: 2025-09-01 to 2025-09-15

-- Poor content scores
content_score: 48
title_score: 42 (weak, non-descriptive title)
desc_score: 51 (sparse, no bullet points)
keyword_score: 38 (missing key search terms)
image_score: 55 (only 2 images, low quality)
rating_score: 72 (reviews are okay, not the problem)
review_score: 68

-- Poor performance due to bad content
cvr_ty: 2.8% (well below category average of 4.5%)
total_visits_ty: 800/day
total_orders_ty: 22/day
gross_sales_usd_ty: $879/day
organic_rank_ty: 45 (poor discoverability)
```

**Phase 2: Content Improvement Event (Sep 16)**
```
-- Single day marker: Sep 16, 2025
-- No data change on this day, but it's the deployment date
```

**Phase 3: Content Scores Improve (Sep 17-30)**
```
date_key: 2025-09-17 to 2025-09-30

-- Dramatically improved content scores
content_score: 85 (+37 points!)
title_score: 88 (optimized with key features and benefits)
desc_score: 84 (comprehensive bullet points, A+ content)
keyword_score: 82 (full keyword optimization)
image_score: 86 (6 lifestyle images added)
rating_score: 72 (unchanged, not a content element)
review_score: 68 (unchanged)

-- KPIs begin improving
cvr_ty: 3.2% (gradual increase, +14%)
total_visits_ty: 950/day (+19% from better search visibility)
total_orders_ty: 30/day
gross_sales_usd_ty: $1,200/day (+37%)
organic_rank_ty: 36 (improving from 45)
```

**Phase 4: Sustained Impact (Oct 1-31)**
```
date_key: 2025-10-01 to 2025-10-31

-- Content scores remain high
content_score: 87
title_score: 89
desc_score: 86
keyword_score: 84
image_score: 87
rating_score: 75 (slight improvement from increased sales)
review_score: 71

-- Full KPI uplift realized
cvr_ty: 3.6% (+29% vs baseline!)
total_visits_ty: 1,100/day (+38% vs baseline)
total_orders_ty: 40/day
gross_sales_usd_ty: $1,598/day (+82% vs baseline!)
organic_rank_ty: 29 (major improvement)
```

*Repeat similar pattern for SKU022 with slightly different numbers but same narrative arc.*

**Validation Query:**
```
-- Content improvement validation
SELECT 
    date_key,
    product_key,
    content_score,
    title_score,
    desc_score,
    keyword_score,
    cvr_ty,
    gross_sales_usd_ty,
    organic_rank_ty
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE product_key IN ('SKU015', 'SKU022')
  AND date_key BETWEEN '2025-09-01' AND '2025-10-31'
ORDER BY product_key, date_key;

-- Should show clear before/after pattern around Sep 16
```

---

#### Story 3: Rank Decline and Recovery (SKU009 - Smart Thermostat)

**Timeline:** August 1 - September 15, 2025

**Affected Product:** SKU009 at Amazon and Best Buy

**Narrative:** Organic rank drops due to algorithm change or competitor activity, traffic falls, recovery via content optimization + paid ads.

**Phase 1: Strong Baseline (Aug 1-10)**
```
product_key: SKU009
retailer_key: 1 (Amazon)
date_key: 2025-08-01 to 2025-08-10

organic_rank_ty: 8 (excellent visibility)
paid_rank_ty: NULL (not running ads)
total_visits_ty: 2,500/day
total_orders_ty: 125/day
cvr_ty: 5.0% (strong conversion)
gross_sales_usd_ty: $16,250/day ($129.99 price × 125 units)
content_score: 82 (good content)
```

**Phase 2: Rank Drops (Aug 11-31)**
```
date_key: 2025-08-11 to 2025-08-31

-- Gradual rank decline
Aug 11-15: organic_rank_ty: 10 → 12
Aug 16-20: organic_rank_ty: 13 → 14
Aug 21-25: organic_rank_ty: 14 → 15
Aug 26-31: organic_rank_ty: 16 (final declined position)

-- Traffic declines proportionally with rank
Aug 11-15: total_visits_ty: 2,300/day (-8%)
Aug 16-20: total_visits_ty: 2,100/day (-16%)
Aug 21-25: total_visits_ty: 1,950/day (-22%)
Aug 26-31: total_visits_ty: 1,850/day (-26%)

-- CVR remains stable (shows it's a visibility problem, not product problem)
cvr_ty: 5.0% (unchanged)

-- Sales decline due to traffic loss
total_orders_ty: 93/day (by Aug 31)
gross_sales_usd_ty: $12,089/day (-26%)

-- Content unchanged initially
content_score: 82
```

**Phase 3: Multi-Tactic Recovery (Sep 1-15)**
```
date_key: 2025-09-01 to 2025-09-15

-- Content optimization deployed (Sep 1)
content_score: 89 (improved from 82)
title_score: 92
keyword_score: 88

-- Paid ads campaign launched (Sep 3)
is_sponsored_product: TRUE (starting Sep 3)
paid_rank_ty: 3 (top of paid results)
sponsored_product_sales_ty: $3,000-$4,000/day (incremental)

-- Organic rank begins recovering
Sep 1-5: organic_rank_ty: 15 → 14
Sep 6-10: organic_rank_ty: 13 → 12
Sep 11-15: organic_rank_ty: 11 → 10

-- Traffic recovers
total_visits_ty: 2,200/day by Sep 15 (recovering toward baseline)

-- Sales improve
total_orders_ty: 110/day (organic) + sponsored
gross_sales_usd_ty: $14,299/day (organic) + $3,500/day (sponsored)
```

**Validation Query:**
```
-- Rank decline detection
SELECT 
    date_key,
    organic_rank_ty,
    LAG(organic_rank_ty, 7) OVER (ORDER BY date_key) as rank_1w_ago,
    organic_rank_ty - LAG(organic_rank_ty, 7) OVER (ORDER BY date_key) as rank_change,
    total_visits_ty,
    cvr_ty,
    is_sponsored_product,
    paid_rank_ty
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE product_key = 'SKU009'
  AND retailer_key = 1
  AND date_key BETWEEN '2025-08-01' AND '2025-09-15'
ORDER BY date_key;

-- Should show rank increasing (worse) by 5+ positions, then recovery
```

---

#### Story 4: Media Efficiency Decline and Optimization (Multiple SKUs)

**Timeline:** July 1 - August 31, 2025

**Table:** fact_retail_media_tbl

**Narrative:** A summer electronics campaign shows declining ROAS due to ad fatigue, budget reallocation improves efficiency.

**Phase 1: Healthy Campaign (Jul 1-15)**
```
campaign_name: 'Summer_Electronics_2025'
media_type: 'Sponsored Products'
placement_type: 'Search'
brand_key: 1 (TechNova)
retailer_key: 1 (Amazon)
date_key: 2025-07-01 to 2025-07-15

-- Daily metrics
spend_ty: $5,000/day
impressions_ty: 500,000/day
clicks_ty: 7,500/day
click_through_rate_ty: 1.5%
cost_per_click_ty: $0.67
click_sales_ty: $18,000/day
click_roas_ty: 3.6 (healthy: $3.60 revenue per $1 spend)
cvr_ty: 4.8%
new_buyer_ty: 180/day
total_buyer_ty: 360/day
aov_ty: $50
```

**Phase 2: Efficiency Declines (Jul 16-31)**
```
date_key: 2025-07-16 to 2025-07-31

-- Ad fatigue sets in
spend_ty: $5,000/day (unchanged budget)
impressions_ty: 650,000/day (increased frequency, same audience)
clicks_ty: 8,500/day (more clicks but lower quality)
click_through_rate_ty: 1.3% (declining)
cost_per_click_ty: $0.59 (lower CPC but worse targeting)
click_sales_ty: $14,000/day (declining despite more clicks!)
click_roas_ty: 2.8 (below 3.0 threshold - ALERT!)
cvr_ty: 3.3% (declining landing page performance)
new_buyer_ty: 140/day (fewer new customers)
total_buyer_ty: 280/day
aov_ty: $50 (unchanged)
```

**Phase 3: Campaign Paused, Budget Reallocated (Aug 1-15)**
```
date_key: 2025-08-01 to 2025-08-15

-- Old campaign reduced
campaign_name: 'Summer_Electronics_2025'
spend_ty: $2,000/day (60% reduction)
impressions_ty: 250,000/day
clicks_ty: 3,200/day
click_sales_ty: $7,200/day
click_roas_ty: 3.6 (improved with lower spend, less saturation)

-- New optimized campaign launched
campaign_name: 'Summer_Electronics_Optimized_Aug'
media_type: 'Sponsored Products'
placement_type: 'Product Detail Pages' (different placement!)
spend_ty: $3,000/day (reallocation)
impressions_ty: 180,000/day
clicks_ty: 4,500/day
click_through_rate_ty: 2.5% (better targeting)
cost_per_click_ty: $0.67
click_sales_ty: $12,000/day
click_roas_ty: 4.0 (excellent efficiency)
cvr_ty: 5.3% (better audience fit)
new_buyer_ty: 190/day
aov_ty: $50
```

**Phase 4: Sustained Optimized Performance (Aug 16-31)**
```
-- Optimized campaign continues
campaign_name: 'Summer_Electronics_Optimized_Aug'
date_key: 2025-08-16 to 2025-08-31

spend_ty: $3,000/day
click_sales_ty: $12,500/day
click_roas_ty: 4.17 (sustained improvement)
cvr_ty: 5.4%
```

**Validation Query:**
```
-- Media efficiency monitoring
SELECT 
    date_key,
    campaign_name,
    spend_ty,
    click_sales_ty,
    click_roas_ty,
    click_through_rate_ty,
    cvr_ty
FROM skulytics_dev.default.fact_retail_media_tbl
WHERE brand_key = 1
  AND retailer_key = 1
  AND date_key BETWEEN '2025-07-01' AND '2025-08-31'
  AND campaign_name LIKE 'Summer_Electronics%'
ORDER BY date_key;

-- Should show ROAS drop below 3.0, then recovery above 4.0
```

---

#### Story 5: Prolonged OOS Impact (SKU012 - Hero Product)

**Timeline:** June 15 - July 31, 2025

**Affected Product:** SKU012 (TechNova Wireless Charging Pad) at Amazon

**Narrative:** Hero product goes OOS for 15 days during peak season, loses rank and sales, takes weeks to recover.

**Phase 1: Pre-OOS Baseline (Jun 15-25)**
```
product_key: SKU012
retailer_key: 1
date_key: 2025-06-15 to 2025-06-25

-- Strong hero product performance
gross_sales_usd_ty: $8,500/day
gross_units_sold_ty: 142/day ($59.99 price)
is_out_of_stock: FALSE
oos_days_ty: 0
total_visits_ty: 3,200/day
total_orders_ty: 142/day
cvr_ty: 4.4%
organic_rank_ty: 5 (excellent)
review_rating: 4.6
content_score: 88
```

**Phase 2: OOS Event (Jun 26 - Jul 10)**
```
date_key: 2025-06-26 to 2025-07-10 (15 consecutive days)

-- Complete stock-out
is_out_of_stock: TRUE (all 15 days)
oos_days_ty: 15
oos_percent_ty: 100%
gross_sales_usd_ty: $0 (can't sell)
gross_units_sold_ty: 0
total_orders_ty: 0

-- Traffic declines as visibility drops
Jun 26-30: total_visits_ty: 2,500/day (-22%)
Jul 1-5: total_visits_ty: 2,000/day (-38%)
Jul 6-10: total_visits_ty: 1,900/day (-41%)

-- Rank penalty from algorithm
Jun 26-30: organic_rank_ty: 7 (starting to drop)
Jul 1-5: organic_rank_ty: 9
Jul 6-10: organic_rank_ty: 12 (significant penalty)

-- Review activity stops (no new purchases)
review_count: 2,847 (frozen, no new reviews)
```

**Phase 3: Initial Recovery (Jul 11-25)**
```
date_key: 2025-07-11 to 2025-07-25

-- Stock restored
is_out_of_stock: FALSE
oos_percent_ty: 0%

-- Sales resume but below baseline
gross_sales_usd_ty: $6,000/day (71% of baseline)
gross_units_sold_ty: 100/day

-- Traffic slowly recovering
total_visits_ty: 2,400/day
total_orders_ty: 100/day
cvr_ty: 4.2% (slight decline, some customers lost trust)

-- Rank recovering slowly
organic_rank_ty: 10 → 9 → 8 (gradual improvement)
```

**Phase 4: Full Recovery (Jul 26-31)**
```
date_key: 2025-07-26 to 2025-07-31

-- Near baseline performance
gross_sales_usd_ty: $8,100/day (95% of baseline)
gross_units_sold_ty: 135/day
total_visits_ty: 3,000/day
cvr_ty: 4.5% (recovered)
organic_rank_ty: 6 (almost back to pre-OOS rank of 5)

-- Reviews resume
review_count: 2,872 (+25 new reviews)
```

**Validation Query:**
```
-- OOS impact tracking
SELECT 
    date_key,
    is_out_of_stock,
    oos_days_ty,
    gross_sales_usd_ty,
    total_visits_ty,
    organic_rank_ty,
    cvr_ty
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE product_key = 'SKU012'
  AND retailer_key = 1
  AND date_key BETWEEN '2025-06-15' AND '2025-07-31'
ORDER BY date_key;

-- Should show 15 consecutive TRUE days for is_out_of_stock
-- Sales should be 0 during OOS period
-- Rank should degrade and slowly recover
```

---

### 2. fact_retail_media_tbl

**Purpose:** Campaign-level media/advertising performance

**Full DDL:**
```
CREATE TABLE skulytics_dev.default.fact_retail_media_tbl (
    -- Keys
    retailer_media_key STRING COMMENT 'Primary key: concat(retailer_key,"-",brand_key,"-",campaignname,"-",datekey)',
    region_key BIGINT COMMENT 'Region identifier',
    brand_key BIGINT COMMENT 'Brand identifier',
    retailer_key BIGINT COMMENT 'Retailer identifier',
    date_key DATE COMMENT 'Campaign date',
    
    -- Temporal Comparison Keys
    ly_date DATE COMMENT 'Last year same date',
    fiscly_date DATE COMMENT 'Fiscal last year date',
    gregly_date DATE COMMENT 'Gregorian last year date',
    
    -- Campaign Attributes
    campaign_name STRING COMMENT 'Campaign identifier/name',
    media_type STRING COMMENT 'Sponsored Products/Sponsored Brands/Display/Video',
    placement_type STRING COMMENT 'Search/Product Detail/Homepage/Category',
    line_item STRING COMMENT 'Specific ad line item',
    spend_bucket STRING COMMENT 'Low/Medium/High spend category',
    
    -- Spend Metrics
    spend_ty DOUBLE COMMENT 'Ad spend USD - this year',
    spend_ly DOUBLE COMMENT 'Ad spend - last year',
    spend_fiscly DOUBLE COMMENT 'Ad spend - fiscal last year',
    spend_gregly DOUBLE COMMENT 'Ad spend - Gregorian last year',
    
    -- Impression Metrics
    impressions_ty BIGINT COMMENT 'Ad impressions - this year',
    impressions_ly BIGINT COMMENT 'Impressions - last year',
    impressions_fiscly BIGINT COMMENT 'Impressions - fiscal last year',
    impressions_gregly BIGINT COMMENT 'Impressions - Gregorian last year',
    
    -- Click Metrics
    clicks_ty BIGINT COMMENT 'Ad clicks - this year',
    clicks_ly BIGINT COMMENT 'Clicks - last year',
    clicks_fiscly BIGINT COMMENT 'Clicks - fiscal last year',
    clicks_gregly BIGINT COMMENT 'Clicks - Gregorian last year',
    
    -- Performance Metrics
    click_through_rate_ty DOUBLE COMMENT 'CTR (clicks/impressions) - this year',
    click_through_rate_ly DOUBLE COMMENT 'CTR - last year',
    cost_per_click_ty DOUBLE COMMENT 'CPC (spend/clicks) - this year',
    cost_per_click_ly DOUBLE COMMENT 'CPC - last year',
    cost_per_mille_ty DOUBLE COMMENT 'CPM (spend/impressions*1000) - this year',
    cost_per_mille_ly DOUBLE COMMENT 'CPM - last year',
    
    -- Sales & ROAS Metrics
    click_sales_ty DOUBLE COMMENT 'Sales attributed to ads - this year',
    click_sales_ly DOUBLE COMMENT 'Click sales - last year',
    click_sales_fiscly DOUBLE COMMENT 'Click sales - fiscal last year',
    click_sales_gregly DOUBLE COMMENT 'Click sales - Gregorian last year',
    click_roas_ty DOUBLE COMMENT 'Return on ad spend (sales/spend) - this year',
    click_roas_ly DOUBLE COMMENT 'ROAS - last year',
    click_roas_fiscly DOUBLE COMMENT 'ROAS - fiscal last year',
    click_roas_gregly DOUBLE COMMENT 'ROAS - Gregorian last year',
    
    -- Customer Metrics
    new_buyer_ty BIGINT COMMENT 'New customers from ads - this year',
    new_buyer_ly BIGINT COMMENT 'New buyers - last year',
    total_buyer_ty BIGINT COMMENT 'Total buyers from ads - this year',
    total_buyer_ly BIGINT COMMENT 'Total buyers - last year',
    
    -- Order Metrics
    aov_ty DOUBLE COMMENT 'Average order value - this year',
    aov_ly DOUBLE COMMENT 'AOV - last year',
    cvr_ty DOUBLE COMMENT 'Conversion rate (orders/clicks) - this year',
    cvr_ly DOUBLE COMMENT 'CVR - last year',
    campaign_repeat_count BIGINT COMMENT 'Number of times campaign has run',
    
    -- Audit
    record_created_date TIMESTAMP,
    record_updated_date TIMESTAMP
) USING DELTA
PARTITIONED BY (date_key)
COMMENT 'Retail media campaign performance metrics';
```

**Data Requirements:**
- **Row Count:** ~100,000 rows
- **Campaign Count:** 15-20 active campaigns across brands and retailers
- **Coverage:** Daily records for each campaign when active
- **Time Range:** Full 3 years (2023-2025)

**Campaign Examples (Required):**
```
campaign_name,brand_key,retailer_key,media_type,placement_type,active_dates
'Summer_Electronics_2025',1,1,'Sponsored Products','Search','2025-06-01 to 2025-08-31'
'Holiday_SmartHome_2024',2,1,'Sponsored Brands','Homepage','2024-11-01 to 2024-12-31'
'Q1_Fitness_Launch_2025',3,2,'Display','Category','2025-01-15 to 2025-03-31'
'Prime_Day_TechNova_2025',1,1,'Sponsored Products','Search','2025-07-15 to 2025-07-16'
'Back_to_School_Gadgets',6,3,'Sponsored Products','Product Detail','2024-08-01 to 2024-09-15'
```

**Performance Benchmarks:**
- **CTR:** 0.8-2.5% (varies by placement type)
- **CPC:** $0.35-$1.20 (higher for competitive keywords)
- **ROAS:** 2.5-5.0 (healthy range, <3.0 triggers alerts)
- **CVR:** 3-8% (from click to purchase)

---

### 3. fact_retail_search_rank_tbl

**Purpose:** Keyword-level search ranking data

**Full DDL:**
```
CREATE TABLE skulytics_dev.default.fact_retail_search_rank_tbl (
    -- Keys
    search_rank_key STRING COMMENT 'Primary key',
    retailer_product_key STRING COMMENT 'Retailer-product composite',
    region_key BIGINT COMMENT 'Region identifier',
    brand_key BIGINT COMMENT 'Brand identifier',
    retailer_key BIGINT COMMENT 'Retailer identifier',
    product_key STRING COMMENT 'Product identifier',
    date_key DATE COMMENT 'Ranking date',
    
    -- Temporal Keys
    ly_date DATE,
    fiscly_date DATE,
    gregly_date DATE,
    
    -- Search Attributes
    search_result_type STRING COMMENT 'Organic/Sponsored/Both',
    keyword STRING COMMENT 'Search keyword/phrase',
    keyword_position BIGINT COMMENT 'Position in keyword list (1-5)',
    
    -- Flags
    is_hero BOOLEAN COMMENT 'Is this a hero/priority product for the brand',
    is_top_product BOOLEAN COMMENT 'Is this in top products for the keyword',
    is_top_keyword BOOLEAN COMMENT 'Is this a top-performing keyword for product',
    is_keyword_match BOOLEAN COMMENT 'Does keyword exactly match product title',
    
    -- Audit
    record_created_date TIMESTAMP,
    record_updated_date TIMESTAMP
) USING DELTA
PARTITIONED BY (date_key)
COMMENT 'Product search ranking by keyword';
```

**Data Requirements:**
- **Row Count:** ~50,000 rows
- **Coverage:** Daily keyword rankings for hero products and top 20 products
- **Keywords per Product:** 3-7 keywords each
- **Time Range:** Full 3 years

**Keyword Strategy:**

**Branded Keywords (always rank well):**
```
Product: SKU001 (TechNova Wireless Earbuds Pro)
Keywords:
- 'technova earbuds' (position 1-3, is_top_keyword=TRUE)
- 'technova wireless' (position 2-5)
```

**Generic Keywords (competitive, rank varies):**
```
Product: SKU001
Keywords:
- 'wireless earbuds' (position 15-40, varies with content/sales)
- 'bluetooth headphones' (position 25-60)
- 'noise canceling earbuds' (position 30-80)
```

**Long-tail Keywords (less competitive, better conversion):**
```
Product: SKU003 (SmartHome WiFi Camera)
Keywords:
- '360 wifi camera indoor' (position 5-15, is_top_keyword=TRUE)
- 'smart security camera' (position 20-40)
```

---

### 4-6. Mobility Tables (Aggregates)

**fact_retail_product_mob_tbl, fact_retail_retailer_mob_tbl, fact_retail_brand_mob_tbl**

These are rollup tables. Generate by aggregating fact_retail_summary_tbl:

```
-- Example: Product Mobility
CREATE TABLE skulytics_dev.default.fact_retail_product_mob_tbl AS
SELECT 
    CONCAT(retailer_key, '-', product_key, '-', date_key) as sku_mob_key,
    CONCAT(retailer_key, '-', product_key) as retailer_product_key,
    region_key,
    retailer_key,
    brand_key,
    product_key,
    date_key,
    SUM(gross_sales_usd_ty) as gross_sales_ty,
    SUM(gross_sales_usd_fiscly) as gross_sales_fiscly,
    SUM(gross_sales_usd_gregly) as gross_sales_gregly,
    CURRENT_TIMESTAMP() as record_created_date,
    CURRENT_TIMESTAMP() as record_updated_date
FROM skulytics_dev.default.fact_retail_summary_tbl
GROUP BY region_key, retailer_key, brand_key, product_key, date_key;
```

*Generate similar for retailer_mob and brand_mob.*

---

## Comprehensive Data Validation Tests

Create a validation script `sql/dbx/tests/data_validation.sql` with all these tests:

```
-- TEST 1: Date Range Coverage
SELECT 'Date Range Test' as test_name,
       MIN(date_key) as min_date,
       MAX(date_key) as max_date,
       COUNT(DISTINCT date_key) as distinct_dates,
       CASE 
           WHEN MIN(date_key) = '2023-01-01' 
            AND MAX(date_key) = '2025-12-31' 
            AND COUNT(DISTINCT date_key) >= 1090 
           THEN 'PASS' 
           ELSE 'FAIL' 
       END as result
FROM skulytics_dev.default.fact_retail_summary_tbl;

-- TEST 2: No Orphaned Keys (Product)
SELECT 'Product Key Integrity' as test_name,
       COUNT(*) as orphaned_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl f
LEFT JOIN skulytics_dev.default.dim_product p ON f.product_key = p.productkey
WHERE p.productkey IS NULL;

-- TEST 3: No Orphaned Keys (Brand)
SELECT 'Brand Key Integrity' as test_name,
       COUNT(*) as orphaned_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl f
LEFT JOIN skulytics_dev.default.dim_brand b ON f.brand_key = b.brand_key
WHERE b.brand_key IS NULL;

-- TEST 4: No Orphaned Keys (Retailer)
SELECT 'Retailer Key Integrity' as test_name,
       COUNT(*) as orphaned_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl f
LEFT JOIN skulytics_dev.default.dim_retailer r ON f.retailer_key = r.retailer_key
WHERE r.retailer_key IS NULL;

-- TEST 5: No Orphaned Keys (Region)
SELECT 'Region Key Integrity' as test_name,
       COUNT(*) as orphaned_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl f
LEFT JOIN skulytics_dev.default.dim_region r ON f.region_key = r.region_key
WHERE r.region_key IS NULL;

-- TEST 6: No Orphaned Keys (Date)
SELECT 'Date Key Integrity' as test_name,
       COUNT(*) as orphaned_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl f
LEFT JOIN skulytics_dev.default.dim_date d ON f.date_key = d.datekey
WHERE d.datekey IS NULL;

-- TEST 7: Content Scores in Valid Range (0-100)
SELECT 'Content Score Range' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE content_score < 0 OR content_score > 100
   OR title_score < 0 OR title_score > 100
   OR desc_score < 0 OR desc_score > 100
   OR image_score < 0 OR image_score > 100
   OR keyword_score < 0 OR keyword_score > 100;

-- TEST 8: CVR in Valid Range (0-100%)
SELECT 'CVR Range' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE cvr_ty < 0 OR cvr_ty > 100;

-- TEST 9: Review Rating in Valid Range (1.0-5.0)
SELECT 'Review Rating Range' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE review_rating < 1.0 OR review_rating > 5.0;

-- TEST 10: No Negative Sales
SELECT 'No Negative Sales' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE gross_sales_usd_ty < 0;

-- TEST 11: No Negative Units
SELECT 'No Negative Units' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE gross_units_sold_ty < 0;

-- TEST 12: Price Consistency (sales = units * price, with tolerance)
SELECT 'Price Consistency' as test_name,
       COUNT(*) as inconsistent_count,
       CASE WHEN COUNT(*) < 100 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE gross_units_sold_ty > 0
  AND ABS(gross_sales_usd_ty - (gross_units_sold_ty * selling_price_ty)) > (selling_price_ty * 2);
  -- Allow for some rounding/bundling variance

-- TEST 13: CVR Math Check (orders/visits)
SELECT 'CVR Calculation' as test_name,
       COUNT(*) as inconsistent_count,
       CASE WHEN COUNT(*) < 50 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE total_visits_ty > 0
  AND ABS(cvr_ty - ((total_orders_ty * 100.0) / total_visits_ty)) > 0.5;
  -- Allow small rounding tolerance

-- TEST 14: OOS Days Don't Exceed Date Range
SELECT 'OOS Days Logic' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE oos_days_ty > 365;  -- Can't have more OOS days than a year

-- TEST 15: Sales Should Be Zero When OOS (for single-day records)
SELECT 'OOS Sales Check' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) < 100 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE is_out_of_stock = TRUE
  AND gross_sales_usd_ty > 0;
  -- Some tolerance for partial-day OOS

-- TEST 16: Story 1 - Conversion Drop Exists (SKU003)
SELECT 'Story 1: Conversion Drop' as test_name,
       COUNT(*) as matching_rows,
       CASE WHEN COUNT(*) >= 7 THEN 'PASS' ELSE 'FAIL' END as result
FROM (
    SELECT 
        date_key,
        cvr_ty,
        LAG(cvr_ty, 7) OVER (PARTITION BY product_key, retailer_key ORDER BY date_key) as cvr_1w_ago
    FROM skulytics_dev.default.fact_retail_summary_tbl
    WHERE product_key = 'SKU003'
      AND retailer_key = 1
      AND date_key BETWEEN '2025-10-15' AND '2025-11-05'
) subq
WHERE ((cvr_ty - cvr_1w_ago) / cvr_1w_ago) < -0.15;

-- TEST 17: Story 2 - Content Improvement Exists (SKU015)
SELECT 'Story 2: Content Improvement' as test_name,
       MAX(content_score) - MIN(content_score) as score_delta,
       CASE WHEN (MAX(content_score) - MIN(content_score)) >= 30 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE product_key = 'SKU015'
  AND retailer_key = 2
  AND date_key BETWEEN '2025-09-01' AND '2025-10-31';

-- TEST 18: Story 3 - Rank Decline Exists (SKU009)
SELECT 'Story 3: Rank Decline' as test_name,
       MAX(organic_rank_ty) - MIN(organic_rank_ty) as rank_change,
       CASE WHEN (MAX(organic_rank_ty) - MIN(organic_rank_ty)) >= 5 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE product_key = 'SKU009'
  AND retailer_key = 1
  AND date_key BETWEEN '2025-08-01' AND '2025-08-31';

-- TEST 19: Story 4 - ROAS Decline Exists (Media Table)
SELECT 'Story 4: ROAS Decline' as test_name,
       MIN(click_roas_ty) as min_roas,
       CASE WHEN MIN(click_roas_ty) < 3.0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_media_tbl
WHERE campaign_name = 'Summer_Electronics_2025'
  AND date_key BETWEEN '2025-07-16' AND '2025-07-31';

-- TEST 20: Story 5 - Extended OOS Exists (SKU012)
SELECT 'Story 5: Extended OOS' as test_name,
       SUM(CASE WHEN is_out_of_stock = TRUE THEN 1 ELSE 0 END) as oos_days,
       CASE WHEN SUM(CASE WHEN is_out_of_stock = TRUE THEN 1 ELSE 0 END) >= 15 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE product_key = 'SKU012'
  AND retailer_key = 1
  AND date_key BETWEEN '2025-06-26' AND '2025-07-10';

-- TEST 21: Seasonality Check - Holiday Lift Exists
SELECT 'Seasonality: Holiday Lift' as test_name,
       AVG(CASE WHEN MONTH(date_key) IN (11,12) THEN gross_sales_usd_ty END) / 
       AVG(CASE WHEN MONTH(date_key) NOT IN (11,12) THEN gross_sales_usd_ty END) as holiday_multiplier,
       CASE WHEN (AVG(CASE WHEN MONTH(date_key) IN (11,12) THEN gross_sales_usd_ty END) / 
                  AVG(CASE WHEN MONTH(date_key) NOT IN (11,12) THEN gross_sales_usd_ty END)) > 1.2 
            THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE YEAR(date_key) = 2024;

-- TEST 22: Data Volume Check
SELECT 'Data Volume Check' as test_name,
       COUNT(*) as total_rows,
       CASE WHEN COUNT(*) BETWEEN 2000000 AND 3000000 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl;

-- TEST 23: Product Coverage Check
SELECT 'Product Coverage' as test_name,
       COUNT(DISTINCT product_key) as distinct_products,
       CASE WHEN COUNT(DISTINCT product_key) = 50 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl;

-- TEST 24: Retailer Coverage Check
SELECT 'Retailer Coverage' as test_name,
       COUNT(DISTINCT retailer_key) as distinct_retailers,
       CASE WHEN COUNT(DISTINCT retailer_key) = 5 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl;

-- TEST 25: No Future Dates
SELECT 'No Future Dates' as test_name,
       COUNT(*) as future_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE date_key > CURRENT_DATE();

-- SUMMARY REPORT
SELECT 
    'VALIDATION SUMMARY' as report_type,
    SUM(CASE WHEN result = 'PASS' THEN 1 ELSE 0 END) as tests_passed,
    SUM(CASE WHEN result = 'FAIL' THEN 1 ELSE 0 END) as tests_failed,
    COUNT(*) as total_tests,
    CASE 
        WHEN SUM(CASE WHEN result = 'FAIL' THEN 1 ELSE 0 END) = 0 THEN 'ALL TESTS PASSED ✓'
        ELSE CONCAT('FAILURES DETECTED: ', SUM(CASE WHEN result = 'FAIL' THEN 1 ELSE 0 END))
    END as final_status
FROM (
    -- Union all test results here
    -- (Each SELECT 'test_name', 'result' FROM above)
);
```

---

## Deliverables Checklist

### Files to Create in `sql/dbx/ddl/dwh/`
- [ ] dim_date.sql
- [ ] dim_region.sql
- [ ] dim_brand.sql
- [ ] dim_retailer.sql
- [ ] dim_product.sql
- [ ] fact_retail_summary_tbl.sql
- [ ] fact_retail_media_tbl.sql
- [ ] fact_retail_search_rank_tbl.sql
- [ ] fact_retail_product_mob_tbl.sql
- [ ] fact_retail_retailer_mob_tbl.sql
- [ ] fact_retail_brand_mob_tbl.sql
- [ ] stg_fact_retail_summary_tbl.sql (if needed for staging)

### Files to Create in `sql/dbx/dwh/`
- [ ] populate_dim_date.sql
- [ ] populate_dim_region.sql
- [ ] populate_dim_brand.sql
- [ ] populate_dim_retailer.sql
- [ ] populate_dim_product.sql
- [ ] populate_fact_retail_summary_tbl.sql (or .py for Python generation)
- [ ] populate_fact_retail_media_tbl.sql
- [ ] populate_fact_retail_search_rank_tbl.sql
- [ ] populate_mob_tables.sql (aggregation logic for all 3 mob tables)

### Files to Create in `data/`
- [ ] dim_date.csv
- [ ] dim_region.csv
- [ ] dim_brand.csv
- [ ] dim_retailer.csv
- [ ] dim_product.csv
- [ ] fact_retail_summary_tbl.csv (may be split into parts)
- [ ] fact_retail_media_tbl.csv
- [ ] fact_retail_search_rank_tbl.csv
- [ ] fact_retail_product_mob_tbl.csv
- [ ] fact_retail_retailer_mob_tbl.csv
- [ ] fact_retail_brand_mob_tbl.csv

### Tests to Create in `sql/dbx/tests/`
- [ ] data_validation.sql (comprehensive test suite above)

### Documentation to Create
- [ ] README.md (overview of data model and how to use)
- [ ] ALERT_STORIES.md (detailed description of each embedded scenario)
- [ ] DATA_DICTIONARY.md (all tables, columns, definitions)

---

## Final Success Criteria

- ✅ All 25 validation tests pass
- ✅ All 5 alert stories are clearly present and trigger correctly
- ✅ Data exhibits realistic seasonality, weekly patterns, and business logic
- ✅ Zero orphaned foreign keys
- ✅ All KPIs within valid ranges
- ✅ Historical depth of 3 years (2023-2025)
- ✅ Professional quality suitable for executive demo

---

## Notes for Antigravity

- You are building a **production-quality demo**, not a toy dataset
- Every number should tell part of a story
- Alert scenarios are **mandatory** and must be engineered precisely
- Use the validation queries to verify your work
- When in doubt, favor realism over randomness
- This data will be presented to C-level executives at a major conference
- Quality > speed, but both matter for the January deadline

---

**End of Comprehensive Instructions**
```

This markdown file contains everything Antigravity needs to build your complete data warehouse from scratch, with no ambiguity about requirements, specifications, or success criteria.