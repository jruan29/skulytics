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
