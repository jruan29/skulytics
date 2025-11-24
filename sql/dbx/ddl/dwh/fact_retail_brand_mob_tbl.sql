CREATE TABLE skulytics_dev.default.fact_retail_brand_mob_tbl (
    brand_mob_key STRING COMMENT 'Primary key: concat(brand_key,"-",date_key)',
    region_key BIGINT COMMENT 'Region identifier',
    brand_key BIGINT COMMENT 'Brand identifier',
    date_key DATE COMMENT 'Transaction date',
    gross_sales_ty DOUBLE COMMENT 'Gross sales in USD - this year',
    gross_sales_fiscly DOUBLE COMMENT 'Gross sales USD - last fiscal year',
    gross_sales_gregly DOUBLE COMMENT 'Gross sales USD - last Gregorian year',
    record_created_date TIMESTAMP,
    record_updated_date TIMESTAMP
) USING DELTA
COMMENT 'Brand mobility aggregate table';
