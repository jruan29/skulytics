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
