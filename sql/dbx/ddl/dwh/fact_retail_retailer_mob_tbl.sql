CREATE TABLE skulytics_dev.default.fact_retail_retailer_mob_tbl (
    retailer_mob_key STRING COMMENT 'Primary key: concat(retailer_key,"-",date_key)',
    region_key BIGINT COMMENT 'Region identifier',
    retailer_key BIGINT COMMENT 'Retailer identifier',
    date_key DATE COMMENT 'Transaction date',
    gross_sales_ty DOUBLE COMMENT 'Gross sales in USD - this year',
    gross_sales_fiscly DOUBLE COMMENT 'Gross sales USD - last fiscal year',
    gross_sales_gregly DOUBLE COMMENT 'Gross sales USD - last Gregorian year',
    record_created_date TIMESTAMP,
    record_updated_date TIMESTAMP
) USING DELTA
COMMENT 'Retailer mobility aggregate table';
