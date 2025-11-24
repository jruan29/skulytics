# Skulytics Data Dictionary

## Dimension Tables

### dim_date
Time dimension with fiscal and Gregorian attributes.
- `datekey`: Primary Key (YYYY-MM-DD)
- `fiscal_year`: Starts Feb 1
- `is_holiday`: Flag for major retail holidays

### dim_product
Product catalog.
- `productkey`: SKU ID (e.g., SKU001)
- `brand_key`: FK to dim_brand
- `price_tier`: Budget/Mid/Premium
- `is_hero_product`: Flag for priority products

### dim_retailer
Retail partners.
- `retailer_key`: ID
- `retailer_name`: Amazon, Walmart, etc.
- `market_share_pct`: Approximate share

### dim_brand
Brand portfolio.
- `brand_key`: ID
- `brand_name`: TechNova, SmartHome Pro, etc.

### dim_region
Geographic regions.
- `region_key`: ID
- `region_name`: North America, Europe, etc.

## Fact Tables

### fact_retail_summary_tbl
Daily performance metrics at Product x Retailer level.
- `gross_sales_usd_ty`: Gross Sales (This Year)
- `gross_units_sold_ty`: Units Sold
- `cvr_ty`: Conversion Rate
- `is_out_of_stock`: OOS Flag
- `content_score`: 0-100 Content Health
- `organic_rank_ty`: Search Rank Position
- `review_rating`: 1-5 Star Rating

### fact_retail_media_tbl
Campaign performance metrics.
- `campaign_name`: Name
- `spend_ty`: Ad Spend
- `click_roas_ty`: Return on Ad Spend
- `impressions_ty`: Ad Impressions

### fact_retail_search_rank_tbl
Keyword-level ranking data.
- `keyword`: Search term
- `keyword_position`: Rank position
- `search_result_type`: Organic/Sponsored
