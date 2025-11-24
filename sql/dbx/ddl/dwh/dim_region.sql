CREATE TABLE skulytics_dev.default.dim_region (
    region_key BIGINT PRIMARY KEY COMMENT 'Region identifier',
    region_name STRING COMMENT 'Region display name',
    region_code STRING COMMENT 'Region abbreviation (2-3 chars)',
    country STRING COMMENT 'Primary country',
    currency STRING COMMENT 'Currency code (USD, EUR, etc.)',
    timezone STRING COMMENT 'Primary timezone'
) USING DELTA
COMMENT 'Geographic regions for market segmentation';
