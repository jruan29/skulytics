CREATE TABLE skulytics_dev.default.dim_brand (
    brand_key BIGINT PRIMARY KEY COMMENT 'Brand identifier',
    brand_name STRING COMMENT 'Brand display name',
    category STRING COMMENT 'Product category',
    subcategory STRING COMMENT 'Product subcategory',
    brand_tier STRING COMMENT 'Premium/Standard/Value pricing tier',
    brand_description STRING COMMENT 'Brand positioning statement'
) USING DELTA
COMMENT 'Product brands for portfolio segmentation';
