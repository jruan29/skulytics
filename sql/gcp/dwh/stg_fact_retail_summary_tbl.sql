CREATE OR REPLACE TABLE `{{params.dwh_project}}.skulytics_DMART.stg_fact_retail_summary_tbl` AS

WITH weekly_sales AS (
  SELECT
    region_key,
    brand_key,
    retailer_key,
    product_key,
    week_start_date,
    week_end_date,
    month_start_date,
    SUM(gross_units_sold) AS gross_units_sold,
    SUM(gross_sales_usd) AS gross_sales_usd
  FROM `{{params.transform_project}}.skulytics_NA.stg_online_sales_tbl`
  GROUP BY 1,2,3,4,5,6,7
),

union_stock_level_daily AS (
  SELECT
    region_key,
    brand_key,
    product_key,
    retailer_key,
    date_key,
    MAX(unit_price) AS unit_price,
    MAX(selling_price) AS selling_price,
    CASE
      WHEN COUNTIF (isoutofstock)>=COUNTIF (NOT isoutofstock) THEN TRUE
      ELSE FALSE
    END AS isoutofstock
  FROM
    `{{params.transform_project}}.skulytics_NA.stg_stock_level_tbl`
  WHERE
    date_key>='2023-01-01'
  GROUP BY
    region_key,
    brand_key,
    product_key,
    retailer_key,
    date_key
),
stock_level_all_dates AS (
  SELECT
    stk_lvl_tbl.region_key,
    stk_lvl_tbl.brand_key,
    stk_lvl_tbl.product_key,
    stk_lvl_tbl.retailer_key,
    dim_date.date_key,
    CAST(NULL AS FLOAT64) AS unit_price,
    CAST(NULL AS FLOAT64) AS selling_price,
    TRUE AS isoutofstock
  FROM
    `{{params.transform_project}}.skulytics_NA.stg_stock_level_tbl` stk_lvl_tbl
    CROSS JOIN `{{params.dwh_project}}.COMMON_DMART.dim_date_tbl` dim_date
  WHERE
    dim_date.date_key >= '2023-01-01'
    AND dim_date.date_key <= (
      SELECT
        MAX(date_key)
      FROM
        `{{params.transform_project}}.skulytics_NA.stg_stock_level_tbl`
    )
  GROUP BY
    stk_lvl_tbl.region_key,
    stk_lvl_tbl.brand_key,
    stk_lvl_tbl.product_key,
    stk_lvl_tbl.retailer_key,
    dim_date.date_key
  HAVING
    DATE_TRUNC (MIN(stk_lvl_tbl.date_key), MONTH)<=dim_date.date_key
),
stock_level_daily AS (
  SELECT
    COALESCE(a.region_key, b.region_key) region_key,
    COALESCE(a.retailer_key, b.retailer_key) retailer_key,
    COALESCE(a.brand_key, b.brand_key) brand_key,
    COALESCE(a.product_key, b.product_key) product_key,
    COALESCE(a.date_key, b.date_key) date_key,
    COALESCE(a.unit_price, b.unit_price) unit_price,
    COALESCE(a.selling_price, b.selling_price) selling_price,
    COALESCE(a.isoutofstock, b.isoutofstock) isoutofstock
  FROM
    union_stock_level_daily a
    FULL JOIN stock_level_all_dates b ON a.region_key=b.region_key
    AND a.brand_key=b.brand_Key
    AND a.product_key=b.product_key
    AND a.retailer_key=b.retailer_key
    AND a.date_key=b.date_key
),
stock_level_greg_monthly AS (
  SELECT
    region_key,
    brand_key,
    product_key,
    retailer_key,
    DATE_TRUNC (date_key, MONTH) AS month_start_date,
    COUNTIF (isoutofstock=TRUE) AS oos_within_month,
    SAFE_DIVIDE (COUNTIF (isoutofstock=TRUE), COUNT(*))*100 AS oos_percent_month,
    CAST(NULL AS int64) AS oos_within_retail_month,
    CAST(NULL AS float64) AS oos_percent_retail_month
  FROM
    stock_level_daily
  GROUP BY
    region_key,
    brand_key,
    product_key,
    retailer_key,
    DATE_TRUNC (date_key, MONTH)
),
stock_level_retail_monthly AS (
  SELECT
    region_key,
    brand_key,
    product_key,
    retailer_key,
    na_month_start_date AS month_start_date,
    CAST(NULL AS int64) AS oos_within_month,
    CAST(NULL AS float64) AS oos_percent_month,
    COUNTIF (isoutofstock=TRUE) AS oos_within_retail_month,
    SAFE_DIVIDE (COUNTIF (isoutofstock=TRUE), COUNT(*))*100 AS oos_percent_retail_month
  FROM
    stock_level_daily a
    JOIN `{{params.dwh_project}}.COMMON_DMART.dim_date_tbl` b ON a.date_key=b.date_key
  GROUP BY
    region_key,
    brand_key,
    product_key,
    retailer_key,
    na_month_start_date
),
stock_level_final AS (
  SELECT
    COALESCE(a.region_key, b.region_key) region_key,
    COALESCE(a.retailer_key, b.retailer_key) retailer_key,
    COALESCE(a.brand_key, b.brand_key) brand_key,
    COALESCE(a.product_key, b.product_key) product_key,
    COALESCE(a.month_start_date, b.month_start_date) month_start_date,
    a.oos_within_month,
    a.oos_percent_month,
    b.oos_within_retail_month,
    b.oos_percent_retail_month
  FROM
    stock_level_greg_monthly a
    FULL JOIN stock_level_retail_monthly b ON a.retailer_key=b.retailer_key
    AND a.brand_key=b.brand_key
    AND a.product_key=b.product_key
    AND a.month_start_date=b.month_start_date
),

sponsored_products_daily AS (
  SELECT
    region_key,
    brand_key,
    product_key,
    retailer_key,
    date_key,
    SUM(impression) AS impression,
    SUM(clicks) AS clicks,
    SUM(sales_revenue) AS sales_revenue,
    SUM(spend) AS spend,
    SUM(units) AS units
  FROM `{{params.transform_project}}.skulytics_NA.stg_sponsored_products_tbl`
  GROUP BY region_key, brand_key, product_key, retailer_key, date_key
),

emerch_scores_monthly AS (
  SELECT
    region_key,
    brand_key,
    product_key,
    retailer_key,
    date_key,
    
    SUM(health_score) AS health_score,
    SUM(title_score) AS title_score,
    SUM(description_score) AS description_score,
    SUM(image_score) AS image_score,
    SUM(keyword_score) AS keyword_score,
    SUM(rating_score) AS rating_score,
    SUM(review_score) AS review_score,
    COUNT(*) AS emerch_record_count
  FROM `{{params.transform_project}}.skulytics_NA.stg_emerch_scores_tbl`
  GROUP BY region_key, brand_key, product_key, retailer_key, date_key
),

conversion_pptraffic_monthly AS (
  SELECT
    region_key,
    brand_key,
    product_key,
    retailer_key,
    date_key,
    MAX(file_date) AS file_date,
    SUM(revenue_ty) AS revenue_ty,
    SUM(revenue_ly) AS revenue_ly,
    SUM(units_ty) AS units_ty,
    SUM(units_ly) AS units_ly,
    AVG(unit_conversion_ty) AS unit_conversion_ty,
    AVG(unit_conversion_ly) AS unit_conversion_ly,
    AVG(traffic_conversion_rate_ty) AS traffic_conversion_rate_ty,
    AVG(traffic_conversion_rate_ly) AS traffic_conversion_rate_ly,
    SUM(SAFE_DIVIDE(units_ty, traffic_conversion_rate_ty)) AS browse_traffic_ty,
    SUM(SAFE_DIVIDE(units_ly, traffic_conversion_rate_ly)) AS browse_traffic_ly,
    SUM(SAFE_DIVIDE(units_ty, unit_conversion_ty)) AS pptraffic_ty,
    SUM(SAFE_DIVIDE(units_ty, unit_conversion_ly)) AS pptraffic_ly
  FROM `{{params.transform_project}}.skulytics_NA.stg_conversion_pptraffic_tbl`
  GROUP BY region_key, brand_key, product_key, retailer_key, date_key
),

keys AS (
  SELECT region_key, brand_key, retailer_key, product_key, week_end_date AS date_key FROM weekly_sales
  UNION DISTINCT
  SELECT region_key, brand_key, retailer_key, product_key, month_start_date AS date_key FROM stock_level_final
  UNION DISTINCT
  SELECT region_key, brand_key, retailer_key, product_key, date_key FROM stock_level_daily
  UNION DISTINCT
  SELECT region_key, brand_key, retailer_key, product_key, date_key FROM sponsored_products_daily
  UNION DISTINCT
  SELECT region_key, brand_key, retailer_key, product_key, date_key FROM emerch_scores_monthly
  UNION DISTINCT
  SELECT region_key, brand_key, retailer_key, product_key, date_key FROM conversion_pptraffic_monthly
)

SELECT DISTINCT
  -- Primary Keys
  k.region_key,
  k.brand_key,
  k.product_key,
  k.retailer_key,

  -- Date Columns
  k.date_key,
  com.file_date,
  os.week_start_date,
  os.week_end_date,
  os.month_start_date,

  -- Online Sales
  os.gross_sales_usd AS gross_sales,
  os.gross_units_sold AS full_size_units_sold,

  -- Stock Level
  sld.unit_price,
  sld.selling_price,
  slm.oos_within_month,
  slm.oos_percent_month,
  slm.oos_within_retail_month,
  slm.oos_percent_retail_month,

  -- eMerch Scores
  emm.health_score,
  emm.title_score AS product_title_score,
  emm.description_score AS product_description_score,
  emm.image_score AS gallery_image_score,
  emm.keyword_score AS keyword_analysis_score,
  emm.rating_score,
  emm.review_score,
  emm.emerch_record_count,

  -- Sponsored Products
  spd.spend AS sponsored_product_spend,
  spd.sales_revenue AS sponsored_product_sales_revenue,
  spd.impression AS sponsored_product_number_of_impressions,
  spd.clicks AS sponsored_product_number_of_clicks,
  spd.units AS sponsored_product_units,

  -- Conversion / PP Traffic
  com.revenue_ty,
  com.revenue_ly,
  com.units_ty,
  com.units_ly,
  com.unit_conversion_ty,
  com.unit_conversion_ly,
  com.traffic_conversion_rate_ty,
  com.traffic_conversion_rate_ly,
  com.browse_traffic_ty,
  com.browse_traffic_ly,
  com.pptraffic_ty,
  com.pptraffic_ly

FROM keys k
LEFT JOIN weekly_sales os
  ON k.region_key = os.region_key
  AND k.brand_key = os.brand_key
  AND k.product_key = os.product_key
  AND k.retailer_key = os.retailer_key
  AND k.date_key = os.week_end_date
LEFT JOIN stock_level_daily sld
  ON k.region_key = sld.region_key
  AND k.brand_key = sld.brand_key
  AND k.product_key = sld.product_key
  AND k.retailer_key = sld.retailer_key
  AND k.date_key = sld.date_key
LEFT JOIN stock_level_final slm
  ON k.region_key = slm.region_key
  AND k.brand_key = slm.brand_key
  AND k.product_key = slm.product_key
  AND k.retailer_key = slm.retailer_key
  AND k.date_key = slm.month_start_date
LEFT JOIN emerch_scores_monthly emm
  ON k.region_key = emm.region_key
  AND k.brand_key = emm.brand_key
  AND k.product_key = emm.product_key
  AND k.retailer_key = emm.retailer_key
  AND k.date_key = emm.date_key
LEFT JOIN sponsored_products_daily spd
  ON k.region_key = spd.region_key
  AND k.brand_key = spd.brand_key
  AND k.product_key = spd.product_key
  AND k.retailer_key = spd.retailer_key
  AND k.date_key = spd.date_key
LEFT JOIN conversion_pptraffic_monthly com
  ON k.region_key = com.region_key
  AND k.brand_key = com.brand_key
  AND k.product_key = com.product_key
  AND k.retailer_key = com.retailer_key
  AND k.date_key = com.date_key;