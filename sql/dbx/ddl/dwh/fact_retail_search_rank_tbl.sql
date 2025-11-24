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
