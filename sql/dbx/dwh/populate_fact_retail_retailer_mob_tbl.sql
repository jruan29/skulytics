INSERT INTO skulytics_dev.default.fact_retail_retailer_mob_tbl
SELECT 
    CONCAT(retailer_key, '-', date_key) as retailer_mob_key,
    region_key,
    retailer_key,
    date_key,
    SUM(gross_sales_usd_ty) as gross_sales_ty,
    SUM(gross_sales_usd_fiscly) as gross_sales_fiscly,
    SUM(gross_sales_usd_gregly) as gross_sales_gregly,
    CURRENT_TIMESTAMP() as record_created_date,
    CURRENT_TIMESTAMP() as record_updated_date
FROM skulytics_dev.default.fact_retail_summary_tbl
GROUP BY region_key, retailer_key, date_key;
