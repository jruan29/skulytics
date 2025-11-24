CREATE TABLE skulytics_dev.default.dim_retailer (
    retailer_key BIGINT PRIMARY KEY COMMENT 'Retailer identifier',
    retailer_name STRING COMMENT 'Retailer display name',
    retailer_type STRING COMMENT 'Online/Omnichannel/Marketplace/DTC',
    region_key BIGINT COMMENT 'Primary operating region',
    market_share_pct DOUBLE COMMENT 'Approximate market share percentage',
    FOREIGN KEY (region_key) REFERENCES dim_region(region_key)
) USING DELTA
COMMENT 'Retail channels and marketplace partners';
