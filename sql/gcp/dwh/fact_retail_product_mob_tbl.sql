CREATE OR REPLACE TABLE `{{params.dwh_project}}.skulytics_DMART.fact_retail_product_mob_tbl` AS
SELECT
  CONCAT(retailer_key, '#', product_key, "#", date_key) AS sku_mob_key,
  CONCAT(retailer_key, '#', product_key) AS retailer_product_key,
  region_key,
  retailer_key,
  brand_key,
  product_key,
  date_key,
  SUM(gross_sales_ty) gross_sales_ty,
  SUM(gross_sales_fisc_ly) gross_sales_fisc_ly,
  SUM(gross_sales_greg_ly) gross_sales_greg_ly,
  CURRENT_TIMESTAMP() AS record_created_date,
  CURRENT_TIMESTAMP() AS record_updated_date
FROM
  `{{params.dwh_project}}.skulytics_DMART.fact_retail_summary_tbl` 
  group by 
  region_key,
  retailer_key,
  brand_key,
  product_key,
  date_key