CREATE TABLE `{dwh-project}.skulytics_dev.fact_retail_retailer_mob_tbl`
(
  retailer_mob_key STRING,
  region_key INT64,
  retailer_key INT64,
  date_key DATE,
  gross_sales_ty FLOAT64,
  gross_sales_fisc_ly FLOAT64,
  gross_sales_greg_ly FLOAT64,
  record_created_date TIMESTAMP,
  record_updated_date TIMESTAMP
);