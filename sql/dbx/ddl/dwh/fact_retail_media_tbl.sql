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
