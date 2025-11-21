CREATE TABLE `{dwh-project}.skulytics_dev.fact_retail_product_mob_tbl`
(
  sku_mob_key STRING,
  retailer_product_key STRING,
  region_key INT64,
  retailer_key INT64,
  brand_key INT64,
  product_key STRING,
  date_key DATE,
  gross_sales_ty FLOAT64,
  gross_sales_fisc_ly FLOAT64,
  gross_sales_greg_ly FLOAT64,
  record_created_date TIMESTAMP,
  record_updated_date TIMESTAMP
);