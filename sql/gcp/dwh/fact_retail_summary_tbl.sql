CREATE OR REPLACE TABLE `{{params.dwh_project}}.skulytics_DMART.fact_retail_summary_tbl`
partition by DATE_TRUNC(month_start_date, MONTH)
cluster by brand_key, retailer_key, product_key
OPTIONS(description="Retail summary fact table")
AS
WITH
primary_keys as (
  SELECT distinct region_key, brand_key, product_key, retailer_key
  FROM `{{params.dwh_project}}.skulytics_DMART.stg_fact_retail_summary_tbl` f
  WHERE region_key is not null
  AND brand_key is not null
  --AND product_key is not null
  AND retailer_key is not null
),

keys_with_dates AS (
  SELECT region_key, brand_key, product_key, retailer_key, date_key
  FROM primary_keys
  CROSS JOIN UNNEST (
    GENERATE_DATE_ARRAY(
      DATE '2022-07-01',
      DATE_SUB(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 DAY),
      INTERVAL 1 DAY
    )
  ) AS date_key
),
fact_keys as (
    SELECT 
        f.region_key,
        f.brand_key, 
        f.product_key,
        f.retailer_key, 
        f.date_key,
        if(f.region_key in (0,27), dd.na_ly_date, dd.row_ly_date) as last_year_date,
        dd.na_ly_date as fisc_ly_date, 
        dd.row_ly_date as greg_ly_date
    FROM keys_with_dates f
    LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_date_tbl` dd ON f.date_key = dd.date_key
),
joining_all_ly_columns as (
    
SELECT CONCAT(
    COALESCE(CAST(fact_keys.retailer_key as STRING),''), '#',
    COALESCE(CAST(fact_keys.product_key as STRING),''), '#',
    COALESCE(CAST(fact_keys.brand_key as STRING),''), '#',
    COALESCE(CAST(fact_keys.date_key AS STRING),'')
) AS retail_summary_key
,    CONCAT(
  COALESCE(CAST(fact_keys.retailer_key as STRING),''), '#',
  COALESCE(CAST(fact_keys.product_key as STRING),'')
)AS retailer_product_key
    ,CAST(fact_keys.brand_key as INT64) as brand_key
    ,fact_keys.region_key
    ,fact_keys.retailer_key
    ,fact_keys.product_key
    -- ,COALESCE(ty.unmapped_product_name,ly.unmapped_product_name) as unmapped_product_name
    ,ty.week_end_date as week_end_date
    ,ty.month_start_date as month_start_date

    ,fact_keys.date_key
    -- ,ty.file_date
    ,fact_keys.last_year_date
    ,fact_keys.fisc_ly_date
    ,fact_keys.greg_ly_date,

       -- Sales Metrics
    ty.gross_sales AS gross_sales_ty,
    ly.gross_sales AS gross_sales_ly,
    fisc_ly.gross_sales AS gross_sales_fisc_ly,
    greg_ly.gross_sales AS gross_sales_greg_ly,

    ty.full_size_units_sold AS full_size_units_sold_ty,
    ly.full_size_units_sold AS full_size_units_sold_ly,
    fisc_ly.full_size_units_sold AS full_size_units_sold_fisc_ly,
    greg_ly.full_size_units_sold AS full_size_units_sold_greg_ly,
    
    -- Stock Metrics (Montly level)
    ty.oos_within_month AS oos_within_month_ty,
    greg_ly.oos_within_month AS oos_within_month_ly,
    greg_ly.oos_within_month AS oos_within_month_fisc_ly,
    greg_ly.oos_within_month AS oos_within_month_greg_ly,

    ty.oos_percent_month AS oos_percent_month_ty,
    greg_ly.oos_percent_month AS oos_percent_month_ly,
    greg_ly.oos_percent_month AS oos_percent_month_fisc_ly,
    greg_ly.oos_percent_month AS oos_percent_month_greg_ly,
    
    ty.oos_within_retail_month AS oos_within_retail_month_ty,
    greg_ly.oos_within_retail_month AS oos_within_retail_month_ly,
    greg_ly.oos_within_retail_month AS oos_within_retail_month_fisc_ly,
    greg_ly.oos_within_retail_month AS oos_within_retail_month_greg_ly,

    ty.oos_percent_retail_month AS oos_percent_retail_month_ty,
    greg_ly.oos_percent_retail_month AS oos_percent_retail_month_ly,
    greg_ly.oos_percent_retail_month AS oos_percent_retail_month_fisc_ly,
    greg_ly.oos_percent_retail_month AS oos_percent_retail_month_greg_ly,

    -- Stock Metrics (Daily level)
    ty.unit_price AS unit_price_ty,
    ly.unit_price AS unit_price_ly,
    fisc_ly.unit_price AS unit_price_fisc_ly,
    greg_ly.unit_price AS unit_price_greg_ly,

    ty.selling_price AS selling_price_ty,
    ly.selling_price AS selling_price_ly,
    fisc_ly.selling_price AS selling_price_fisc_ly,
    greg_ly.selling_price AS selling_price_greg_ly,

    -- Health Score Metrics
    ty.health_score AS health_score_ty,
    greg_ly.health_score AS health_score_ly,
    greg_ly.health_score AS health_score_fisc_ly,
    greg_ly.health_score AS health_score_greg_ly,

    ty.product_title_score AS product_title_score_ty,
    greg_ly.product_title_score AS product_title_score_ly,
    greg_ly.product_title_score AS product_title_score_fisc_ly,
    greg_ly.product_title_score AS product_title_score_greg_ly,

    ty.product_description_score AS product_description_score_ty,
    greg_ly.product_description_score AS product_description_score_ly,
    greg_ly.product_description_score AS product_description_score_fisc_ly,
    greg_ly.product_description_score AS product_description_score_greg_ly,

    ty.gallery_image_score AS gallery_image_score_ty,
    greg_ly.gallery_image_score AS gallery_image_score_ly,
    greg_ly.gallery_image_score AS gallery_image_score_fisc_ly,
    greg_ly.gallery_image_score AS gallery_image_score_greg_ly,

    ty.keyword_analysis_score AS keyword_analysis_score_ty,
    greg_ly.keyword_analysis_score AS keyword_analysis_score_ly,
    greg_ly.keyword_analysis_score AS keyword_analysis_score_fisc_ly,
    greg_ly.keyword_analysis_score AS keyword_analysis_score_greg_ly,

    ty.rating_score AS rating_score_ty,
    greg_ly.rating_score AS rating_score_ly,
    greg_ly.rating_score AS rating_score_fisc_ly,
    greg_ly.rating_score AS rating_score_greg_ly,

    ty.review_score AS review_score_ty,
    greg_ly.review_score AS review_score_ly,
    greg_ly.review_score AS review_score_fisc_ly,
    greg_ly.review_score AS review_score_greg_ly,

    ty.emerch_record_count AS emerch_record_count_ty,
    greg_ly.emerch_record_count AS emerch_record_count_ly,
    greg_ly.emerch_record_count AS emerch_record_count_fisc_ly,
    greg_ly.emerch_record_count AS emerch_record_count_greg_ly,

    -- Sponsored Products Metrics
    ty.sponsored_product_spend AS sponsored_product_spend_ty,
    ly.sponsored_product_spend AS sponsored_product_spend_ly,
    fisc_ly.sponsored_product_spend AS sponsored_product_spend_fisc_ly,
    greg_ly.sponsored_product_spend AS sponsored_product_spend_greg_ly,

    ty.sponsored_product_sales_revenue AS sponsored_product_sales_revenue_ty,
    ly.sponsored_product_sales_revenue AS sponsored_product_sales_revenue_ly,
    fisc_ly.sponsored_product_sales_revenue AS sponsored_product_sales_revenue_fisc_ly,
    greg_ly.sponsored_product_sales_revenue AS sponsored_product_sales_revenue_greg_ly,

    ty.sponsored_product_number_of_impressions AS sponsored_product_number_of_impressions_ty,
    ly.sponsored_product_number_of_impressions AS sponsored_product_number_of_impressions_ly,
    fisc_ly.sponsored_product_number_of_impressions AS sponsored_product_number_of_impressions_fisc_ly,
    greg_ly.sponsored_product_number_of_impressions AS sponsored_product_number_of_impressions_greg_ly,

    ty.sponsored_product_number_of_clicks AS sponsored_product_number_of_clicks_ty,
    ly.sponsored_product_number_of_clicks AS sponsored_product_number_of_clicks_ly,
    fisc_ly.sponsored_product_number_of_clicks AS sponsored_product_number_of_clicks_fisc_ly,
    greg_ly.sponsored_product_number_of_clicks AS sponsored_product_number_of_clicks_greg_ly,

    ty.sponsored_product_units AS sponsored_product_units_ty,
    ly.sponsored_product_units AS sponsored_product_units_ly,
    fisc_ly.sponsored_product_units AS sponsored_product_units_fisc_ly,
    greg_ly.sponsored_product_units AS sponsored_product_units_greg_ly,

    -- Conversion Metrics
    ty.revenue_ty AS revenue_ty,
    COALESCE(ty.revenue_ly, ly.revenue_ty) AS revenue_ly,
    COALESCE(ty.revenue_ly, fisc_ly.revenue_ty) AS revenue_fisc_ly,
    COALESCE(ty.revenue_ly, greg_ly.revenue_ty) AS revenue_greg_ly,

    ty.units_ty AS units_ty,
    COALESCE(ty.units_ly, ly.units_ty) AS units_ly,
    COALESCE(ty.units_ly, fisc_ly.units_ty) AS units_fisc_ly,
    COALESCE(ty.units_ly, greg_ly.units_ty) AS units_greg_ly,

    ty.unit_conversion_ty AS unit_conversion_ty,
    COALESCE(ty.unit_conversion_ly, ly.unit_conversion_ty) AS unit_conversion_ly,
    COALESCE(ty.unit_conversion_ly, fisc_ly.unit_conversion_ty) AS unit_conversion_fisc_ly,
    COALESCE(ty.unit_conversion_ly, greg_ly.unit_conversion_ty) AS unit_conversion_greg_ly,

    ty.traffic_conversion_rate_ty AS traffic_conversion_rate_ty,
    COALESCE(ty.traffic_conversion_rate_ly, ly.traffic_conversion_rate_ty) AS traffic_conversion_rate_ly,
    COALESCE(ty.traffic_conversion_rate_ly, fisc_ly.traffic_conversion_rate_ty) AS traffic_conversion_rate_fisc_ly,
    COALESCE(ty.traffic_conversion_rate_ly, greg_ly.traffic_conversion_rate_ty) AS traffic_conversion_rate_greg_ly,

    ty.browse_traffic_ty AS browse_traffic_ty,
    COALESCE(ty.browse_traffic_ly, ly.browse_traffic_ty) AS browse_traffic_ly,
    COALESCE(ty.browse_traffic_ly, fisc_ly.browse_traffic_ty) AS browse_traffic_fisc_ly,
    COALESCE(ty.browse_traffic_ly, greg_ly.browse_traffic_ty) AS browse_traffic_greg_ly,

    ty.pptraffic_ty AS pptraffic_ty,
    COALESCE(ty.pptraffic_ly, ly.pptraffic_ty) AS pptraffic_ly,
    COALESCE(ty.pptraffic_ly, fisc_ly.pptraffic_ty) AS pptraffic_fisc_ly,
    COALESCE(ty.pptraffic_ly, greg_ly.pptraffic_ty) AS pptraffic_greg_ly,

    CURRENT_TIMESTAMP() AS record_created_date,
    CURRENT_TIMESTAMP() AS record_updated_date

FROM fact_keys
LEFT JOIN `{{params.dwh_project}}.skulytics_DMART.stg_fact_retail_summary_tbl` ty 
    ON fact_keys.brand_key = ty.brand_key and fact_keys.region_key = ty.region_key and fact_keys.retailer_key =  ty.retailer_key and COALESCE(fact_keys.product_key, '1') = COALESCE(ty.product_key,'1') and fact_keys.date_key = ty.date_key
LEFT JOIN `{{params.dwh_project}}.skulytics_DMART.stg_fact_retail_summary_tbl` ly
    ON fact_keys.brand_key = ly.brand_key and fact_keys.region_key = ly.region_key and fact_keys.retailer_key =  ly.retailer_key and COALESCE(fact_keys.product_key, '1') = COALESCE(ly.product_key,'1') and fact_keys.last_year_date =  ly.date_key
LEFT JOIN `{{params.dwh_project}}.skulytics_DMART.stg_fact_retail_summary_tbl` greg_ly
    ON fact_keys.brand_key = greg_ly.brand_key and fact_keys.region_key = greg_ly.region_key and fact_keys.retailer_key = greg_ly.retailer_key and COALESCE(fact_keys.product_key, '1') = COALESCE(greg_ly.product_key,'1') and fact_keys.greg_ly_date = greg_ly.date_key 
LEFT JOIN `{{params.dwh_project}}.skulytics_DMART.stg_fact_retail_summary_tbl` fisc_ly
    ON fact_keys.brand_key = fisc_ly.brand_key and fact_keys.region_key = fisc_ly.region_key and fact_keys.retailer_key = fisc_ly.retailer_key and COALESCE(fact_keys.product_key, '1') = COALESCE(fisc_ly.product_key, '1') and fact_keys.fisc_ly_date = fisc_ly.date_key 
)
SELECT * FROM joining_all_ly_columns