CREATE OR REPLACE TABLE
  `{{params.dwh_project}}.skulytics_DMART.fact_retail_media_tbl` AS
WITH
  dim_date AS (
  SELECT
    dd.*,
    dd.na_ly_date AS fisc_ly_date,
    dd.row_ly_date AS greg_ly_date
  FROM
    `{{params.dwh_project}}.COMMON_DMART.dim_date_tbl` dd ),
  base_data AS (
  SELECT
    region_key,
    campaign_name,
    date_key,
    brand_key,
    retailer_key,
    media_type,
    placement_type,
    line_item,
    spend_bucket,
    click_sales,
    spend,
    cost_per_mille,
    click_roas,
    impressions,
    clicks,
    click_through_rate,
    cost_per_click,
    new_buyer,
    total_buyer,
    aov,
    cvr,
    campaign_repeat_count
  FROM
    `{{params.transform_project}}.skulytics_NA.union_retail_media_tbl` ),
  ty_data AS (
  SELECT
    region_key,
    campaign_name,
    brand_key,
    retailer_key,
    media_type,
    placement_type,
    line_item,
    spend_bucket,
    dd.date_key,
    CASE
      WHEN bd.region_key IN (0, 27) THEN dd.na_ly_date
      ELSE dd.row_ly_date
  END
    AS ly_date,
    dd.na_ly_date AS fisc_ly_date,
    dd.greg_ly_date AS greg_ly_date,
    click_sales AS click_sales_ty,
    CAST(NULL AS NUMERIC) AS click_sales_ly,
    CAST(NULL AS NUMERIC) AS click_sales_fisc_ly,
    CAST(NULL AS NUMERIC) AS click_sales_greg_ly,
    spend AS spend_ty,
    CAST(NULL AS NUMERIC) AS spend_ly,
    CAST(NULL AS NUMERIC) AS spend_fisc_ly,
    CAST(NULL AS NUMERIC) AS spend_greg_ly,
    cost_per_mille AS cost_per_mille_ty,
    CAST(NULL AS NUMERIC) AS cost_per_mille_ly,
    CAST(NULL AS NUMERIC) AS cost_per_mille_fisc_ly,
    CAST(NULL AS NUMERIC) AS cost_per_mille_greg_ly,
    click_roas AS click_roas_ty,
    CAST(NULL AS NUMERIC) AS click_roas_ly,
    CAST(NULL AS NUMERIC) AS click_roas_fisc_ly,
    CAST(NULL AS NUMERIC) AS click_roas_greg_ly,
    impressions AS impressions_ty,
    CAST(NULL AS NUMERIC) AS impressions_ly,
    CAST(NULL AS NUMERIC) AS impressions_fisc_ly,
    CAST(NULL AS NUMERIC) AS impressions_greg_ly,
    clicks AS clicks_ty,
    CAST(NULL AS NUMERIC) AS clicks_ly,
    CAST(NULL AS NUMERIC) AS clicks_fisc_ly,
    CAST(NULL AS NUMERIC) AS clicks_greg_ly,
    click_through_rate AS click_through_rate_ty,
    CAST(NULL AS NUMERIC) AS click_through_rate_ly,
    CAST(NULL AS NUMERIC) AS click_through_rate_fisc_ly,
    CAST(NULL AS NUMERIC) AS click_through_rate_greg_ly,
    cost_per_click AS cost_per_click_ty,
    CAST(NULL AS NUMERIC) AS cost_per_click_ly,
    CAST(NULL AS NUMERIC) AS cost_per_click_fisc_ly,
    CAST(NULL AS NUMERIC) AS cost_per_click_greg_ly,
    new_buyer AS new_buyer_ty,
    CAST(NULL AS NUMERIC) AS new_buyer_ly,
    CAST(NULL AS NUMERIC) AS new_buyer_fisc_ly,
    CAST(NULL AS NUMERIC) AS new_buyer_greg_ly,
    total_buyer AS total_buyer_ty,
    CAST(NULL AS NUMERIC) AS total_buyer_ly,
    CAST(NULL AS NUMERIC) AS total_buyer_fisc_ly,
    CAST(NULL AS NUMERIC) AS total_buyer_greg_ly,
    aov AS aov_ty,
    CAST(NULL AS NUMERIC) AS aov_ly,
    CAST(NULL AS NUMERIC) AS aov_fisc_ly,
    CAST(NULL AS NUMERIC) AS aov_greg_ly,
    cvr AS cvr_ty,
    CAST(NULL AS NUMERIC) AS cvr_ly,
    CAST(NULL AS NUMERIC) AS cvr_fisc_ly,
    CAST(NULL AS NUMERIC) AS cvr_greg_ly,

    campaign_repeat_count AS campaign_repeat_count_ty,
    CAST(NULL AS NUMERIC) AS campaign_repeat_count_ly,
    CAST(NULL AS NUMERIC) AS campaign_repeat_count_fisc_ly,
    CAST(NULL AS NUMERIC) AS campaign_repeat_count_greg_ly
  FROM
    base_data bd
  LEFT JOIN
    dim_date dd
  ON
    dd.as_date=bd.date_key ),
  ly_data AS (
  SELECT
    bd.region_key,
    bd.campaign_name,
    bd.brand_key,
    bd.retailer_key,
    bd.media_type,
    bd.placement_type,
    bd.line_item,
    bd.spend_bucket,
    dd.date_key,
    CASE
      WHEN bd.region_key IN (0, 27) THEN dd.na_ly_date
      ELSE dd.row_ly_date
  END
    AS ly_date,
    dd.na_ly_date AS fisc_ly_date,
    dd.greg_ly_date AS greg_ly_date,
    CAST(NULL AS NUMERIC) AS click_sales_ty,
    bd.click_sales AS click_sales_ly,
    CAST(NULL AS NUMERIC) AS click_sales_fisc_ly,
    CAST(NULL AS NUMERIC) AS click_sales_greg_ly,
    CAST(NULL AS NUMERIC) AS spend_ty,
    bd.spend AS spend_ly,
    CAST(NULL AS NUMERIC) AS spend_fisc_ly,
    CAST(NULL AS NUMERIC) AS spend_greg_ly,
    CAST(NULL AS NUMERIC) AS cost_per_mille_ty,
    bd.cost_per_mille AS cost_per_mille_ly,
    CAST(NULL AS NUMERIC) AS cost_per_mille_fisc_ly,
    CAST(NULL AS NUMERIC) AS cost_per_mille_greg_ly,
    CAST(NULL AS NUMERIC) AS click_roas_ty,
    bd.click_roas AS click_roas_ly,
    CAST(NULL AS NUMERIC) AS click_roas_fisc_ly,
    CAST(NULL AS NUMERIC) AS click_roas_greg_ly,
    CAST(NULL AS NUMERIC) AS impressions_ty,
    bd.impressions AS impressions_ly,
    CAST(NULL AS NUMERIC) AS impressions_fisc_ly,
    CAST(NULL AS NUMERIC) AS impressions_greg_ly,
    CAST(NULL AS NUMERIC) AS clicks_ty,
    bd.clicks AS clicks_ly,
    CAST(NULL AS NUMERIC) AS clicks_fisc_ly,
    CAST(NULL AS NUMERIC) AS clicks_greg_ly,
    CAST(NULL AS NUMERIC) AS click_through_rate_ty,
    bd.click_through_rate AS click_through_rate_ly,
    CAST(NULL AS NUMERIC) AS click_through_rate_fisc_ly,
    CAST(NULL AS NUMERIC) AS click_through_rate_greg_ly,
    CAST(NULL AS NUMERIC) AS cost_per_click_ty,
    bd.cost_per_click AS cost_per_click_ly,
    CAST(NULL AS NUMERIC) AS cost_per_click_fisc_ly,
    CAST(NULL AS NUMERIC) AS cost_per_click_greg_ly,
    CAST(NULL AS NUMERIC) AS new_buyer_ty,
    bd.new_buyer AS new_buyer_ly,
    CAST(NULL AS NUMERIC) AS new_buyer_fisc_ly,
    CAST(NULL AS NUMERIC) AS new_buyer_greg_ly,
    CAST(NULL AS NUMERIC) AS total_buyer_ty,
    bd.total_buyer AS total_buyer_ly,
    CAST(NULL AS NUMERIC) AS total_buyer_fisc_ly,
    CAST(NULL AS NUMERIC) AS total_buyer_greg_ly,
    CAST(NULL AS NUMERIC) AS aov_ty,
    bd.aov AS aov_ly,
    CAST(NULL AS NUMERIC) AS aov_fisc_ly,
    CAST(NULL AS NUMERIC) AS aov_greg_ly,
    CAST(NULL AS NUMERIC) AS cvr_ty,
    bd.cvr AS cvr_ly,
    CAST(NULL AS NUMERIC) AS cvr_fisc_ly,
    CAST(NULL AS NUMERIC) AS cvr_greg_ly,
    CAST(NULL AS NUMERIC) AS campaign_repeat_count_ty,
    bd.campaign_repeat_count AS campaign_repeat_count_ly,
    CAST(NULL AS NUMERIC) AS campaign_repeat_count_fisc_ly,
    CAST(NULL AS NUMERIC) AS campaign_repeat_count_greg_ly
  FROM
    base_data bd
  JOIN
    dim_date dd
  ON
    CASE
      WHEN bd.region_key IN (0, 27) THEN dd.na_ly_date
      ELSE dd.row_ly_date
  END
    =bd.date_key ),
  fisc_ly_data AS (
  SELECT
    bd.region_key,
    bd.campaign_name,
    bd.brand_key,
    bd.retailer_key,
    bd.media_type,
    bd.placement_type,
    bd.line_item,
    bd.spend_bucket,
    dd.date_key,
    CASE
      WHEN bd.region_key IN (0, 27) THEN dd.na_ly_date
      ELSE dd.row_ly_date
  END
    AS ly_date,
    dd.na_ly_date AS fisc_ly_date,
    dd.greg_ly_date AS greg_ly_date,
    CAST(NULL AS NUMERIC) AS click_sales_ty,
    CAST(NULL AS NUMERIC) AS click_sales_ly,
    bd.click_sales AS click_sales_fisc_ly,
    CAST(NULL AS NUMERIC) AS click_sales_greg_ly,
    CAST(NULL AS NUMERIC) AS spend_ty,
    CAST(NULL AS NUMERIC) AS spend_ly,
    bd.spend AS spend_fisc_ly,
    CAST(NULL AS NUMERIC) AS spend_greg_ly,
    CAST(NULL AS NUMERIC) AS cost_per_mille_ty,
    CAST(NULL AS NUMERIC) AS cost_per_mille_ly,
    bd.cost_per_mille AS cost_per_mille_fisc_ly,
    CAST(NULL AS NUMERIC) AS cost_per_mille_greg_ly,
    CAST(NULL AS NUMERIC) AS click_roas_ty,
    CAST(NULL AS NUMERIC) AS click_roas_ly,
    bd.click_roas AS click_roas_fisc_ly,
    CAST(NULL AS NUMERIC) AS click_roas_greg_ly,
    CAST(NULL AS NUMERIC) AS impressions_ty,
    CAST(NULL AS NUMERIC) AS impressions_ly,
    bd.impressions AS impressions_fisc_ly,
    CAST(NULL AS NUMERIC) AS impressions_greg_ly,
    CAST(NULL AS NUMERIC) AS clicks_ty,
    CAST(NULL AS NUMERIC) AS clicks_ly,
    bd.clicks AS clicks_fisc_ly,
    CAST(NULL AS NUMERIC) AS clicks_greg_ly,
    CAST(NULL AS NUMERIC) AS click_through_rate_ty,
    CAST(NULL AS NUMERIC) AS click_through_rate_ly,
    bd.click_through_rate AS click_through_rate_fisc_ly,
    CAST(NULL AS NUMERIC) AS click_through_rate_greg_ly,
    CAST(NULL AS NUMERIC) AS cost_per_click_ty,
    CAST(NULL AS NUMERIC) AS cost_per_click_ly,
    bd.cost_per_click AS cost_per_click_fisc_ly,
    CAST(NULL AS NUMERIC) AS cost_per_click_greg_ly,
    CAST(NULL AS NUMERIC) AS new_buyer_ty,
    CAST(NULL AS NUMERIC) AS new_buyer_ly,
    bd.new_buyer AS new_buyer_fisc_ly,
    CAST(NULL AS NUMERIC) AS new_buyer_greg_ly,
    CAST(NULL AS NUMERIC) AS total_buyer_ty,
    CAST(NULL AS NUMERIC) AS total_buyer_ly,
    bd.total_buyer AS total_buyer_fisc_ly,
    CAST(NULL AS NUMERIC) AS total_buyer_greg_ly,
    CAST(NULL AS NUMERIC) AS aov_ty,
    CAST(NULL AS NUMERIC) AS aov_ly,
    bd.aov AS aov_fisc_ly,
    CAST(NULL AS NUMERIC) AS aov_greg_ly,
    CAST(NULL AS NUMERIC) AS cvr_ty,
    CAST(NULL AS NUMERIC) AS cvr_ly,
    bd.cvr AS cvr_fisc_ly,
    CAST(NULL AS NUMERIC) AS cvr_greg_ly,
    CAST(NULL AS NUMERIC) AS campaign_repeat_count_ty,
    CAST(NULL AS NUMERIC) AS campaign_repeat_count_ly,
    bd.campaign_repeat_count AS campaign_repeat_count_fisc_ly,
    CAST(NULL AS NUMERIC) AS campaign_repeat_count_greg_ly
  FROM
    base_data bd
  JOIN
    dim_date dd
  ON
    dd.na_ly_date=bd.date_key ),
  greg_ly_data AS (
  SELECT
    bd.region_key,
    bd.campaign_name,
    bd.brand_key,
    bd.retailer_key,
    bd.media_type,
    bd.placement_type,
    bd.line_item,
    bd.spend_bucket,
    dd.date_key,
    CASE
      WHEN bd.region_key IN (0, 27) THEN dd.na_ly_date
      ELSE dd.row_ly_date
  END
    AS ly_date,
    dd.na_ly_date AS fisc_ly_date,
    dd.greg_ly_date AS greg_ly_date,
    CAST(NULL AS NUMERIC) AS click_sales_ty,
    CAST(NULL AS NUMERIC) AS click_sales_ly,
    CAST(NULL AS NUMERIC) AS click_sales_fisc_ly,
    bd.click_sales AS click_sales_greg_ly,
    CAST(NULL AS NUMERIC) AS spend_ty,
    CAST(NULL AS NUMERIC) AS spend_ly,
    CAST(NULL AS NUMERIC) AS spend_fisc_ly,
    bd.spend AS spend_greg_ly,
    CAST(NULL AS NUMERIC) AS cost_per_mille_ty,
    CAST(NULL AS NUMERIC) AS cost_per_mille_ly,
    CAST(NULL AS NUMERIC) AS cost_per_mille_fisc_ly,
    bd.cost_per_mille AS cost_per_mille_greg_ly,
    CAST(NULL AS NUMERIC) AS click_roas_ty,
    CAST(NULL AS NUMERIC) AS click_roas_ly,
    CAST(NULL AS NUMERIC) AS click_roas_fisc_ly,
    bd.click_roas AS click_roas_greg_ly,
    CAST(NULL AS NUMERIC) AS impressions_ty,
    CAST(NULL AS NUMERIC) AS impressions_ly,
    CAST(NULL AS NUMERIC) AS impressions_fisc_ly,
    bd.impressions AS impressions_greg_ly,
    CAST(NULL AS NUMERIC) AS clicks_ty,
    CAST(NULL AS NUMERIC) AS clicks_ly,
    CAST(NULL AS NUMERIC) AS clicks_fisc_ly,
    bd.clicks AS clicks_greg_ly,
    CAST(NULL AS NUMERIC) AS click_through_rate_ty,
    CAST(NULL AS NUMERIC) AS click_through_rate_ly,
    CAST(NULL AS NUMERIC) AS click_through_rate_fisc_ly,
    bd.click_through_rate AS click_through_rate_greg_ly,
    CAST(NULL AS NUMERIC) AS cost_per_click_ty,
    CAST(NULL AS NUMERIC) AS cost_per_click_ly,
    CAST(NULL AS NUMERIC) AS cost_per_click_fisc_ly,
    bd.cost_per_click AS cost_per_click_greg_ly,
    CAST(NULL AS NUMERIC) AS new_buyer_ty,
    CAST(NULL AS NUMERIC) AS new_buyer_ly,
    CAST(NULL AS NUMERIC) AS new_buyer_fisc_ly,
    bd.new_buyer AS new_buyer_greg_ly,
    CAST(NULL AS NUMERIC) AS total_buyer_ty,
    CAST(NULL AS NUMERIC) AS total_buyer_ly,
    CAST(NULL AS NUMERIC) AS total_buyer_fisc_ly,
    bd.total_buyer AS total_buyer_greg_ly,
    CAST(NULL AS NUMERIC) AS aov_ty,
    CAST(NULL AS NUMERIC) AS aov_ly,
    CAST(NULL AS NUMERIC) AS aov_fisc_ly,
    bd.aov AS aov_greg_ly,
    CAST(NULL AS NUMERIC) AS cvr_ty,
    CAST(NULL AS NUMERIC) AS cvr_ly,
    CAST(NULL AS NUMERIC) AS cvr_fisc_ly,
    bd.cvr AS cvr_greg_ly,
    CAST(NULL AS NUMERIC) AS campaign_repeat_count_ty,
    CAST(NULL AS NUMERIC) AS campaign_repeat_count_ly,
    CAST(NULL AS NUMERIC) AS campaign_repeat_count_fisc_ly,
    bd.campaign_repeat_count AS campaign_repeat_count_greg_ly
  FROM
    base_data bd
  JOIN
    dim_date dd
  ON
    dd.row_ly_date=bd.date_key ),
  combined_data AS (
  SELECT
    *
  FROM
    ty_data
  UNION ALL
  SELECT
    *
  FROM
    ly_data
  UNION ALL
  SELECT
    *
  FROM
    fisc_ly_data
  UNION ALL
  SELECT
    *
  FROM
    greg_ly_data )
SELECT
  CONCAT ( CAST(COALESCE(region_key, 0) AS STRING), '#', CAST(COALESCE(brand_key, 0) AS STRING), '#', CAST(COALESCE(retailer_key, 0) AS STRING), '#', CAST(COALESCE(date_key, '1900-01-01') AS STRING), '#', COALESCE(campaign_name, ''), '#', COALESCE(media_type, ''), '#', COALESCE(COALESCE(line_item, ''), ''), '#', COALESCE(spend_bucket, '') ) AS retailer_media_key,
  region_key,
  campaign_name,
  date_key,
  ly_date,
  greg_ly_date,
  fisc_ly_date,
  brand_key,
  retailer_key,
  media_type,
  placement_type,
  line_item,
  spend_bucket,
  SUM(click_sales_ty) AS click_sales_ty,
  SUM(click_sales_ly) AS click_sales_ly,
  SUM(click_sales_fisc_ly) AS click_sales_fisc_ly,
  SUM(click_sales_greg_ly) AS click_sales_greg_ly,
  SUM(spend_ty) AS spend_ty,
  SUM(spend_ly) AS spend_ly,
  SUM(spend_fisc_ly) AS spend_fisc_ly,
  SUM(spend_greg_ly) AS spend_greg_ly,
  SUM(cost_per_mille_ty) AS cost_per_mille_ty,
  SUM(cost_per_mille_ly) AS cost_per_mille_ly,
  SUM(cost_per_mille_fisc_ly) AS cost_per_mille_fisc_ly,
  SUM(cost_per_mille_greg_ly) AS cost_per_mille_greg_ly,
  SUM(click_roas_ty) AS click_roas_ty,
  SUM(click_roas_ly) AS click_roas_ly,
  SUM(click_roas_fisc_ly) AS click_roas_fisc_ly,
  SUM(click_roas_greg_ly) AS click_roas_greg_ly,
  cast(SUM(impressions_ty) as int64) AS impressions_ty,
  cast(SUM(impressions_ly) as int64) AS impressions_ly,
  cast(SUM(impressions_fisc_ly) as int64) AS impressions_fisc_ly,
  cast(SUM(impressions_greg_ly)  as int64) AS impressions_greg_ly,
  cast(SUM(clicks_ty) as int64) AS clicks_ty,
  cast(SUM(clicks_ly) as int64) AS clicks_ly,
  cast(SUM(clicks_fisc_ly) as int64) AS clicks_fisc_ly,
  cast(SUM(clicks_greg_ly) as int64) AS clicks_greg_ly,
  SUM(click_through_rate_ty) AS click_through_rate_ty,
  SUM(click_through_rate_ly) AS click_through_rate_ly,
  SUM(click_through_rate_fisc_ly) AS click_through_rate_fisc_ly,
  SUM(click_through_rate_greg_ly) AS click_through_rate_greg_ly,
  SUM(cost_per_click_ty) AS cost_per_click_ty,
  SUM(cost_per_click_ly) AS cost_per_click_ly,
  SUM(cost_per_click_fisc_ly) AS cost_per_click_fisc_ly,
  SUM(cost_per_click_greg_ly) AS cost_per_click_greg_ly,
  cast(SUM(new_buyer_ty) as int64) AS new_buyer_ty,
  cast(SUM(new_buyer_ly)  as int64) AS new_buyer_ly,
  cast(SUM(new_buyer_fisc_ly)  as int64) AS new_buyer_fisc_ly,
  cast(SUM(new_buyer_greg_ly) as int64) AS new_buyer_greg_ly,
  SUM(total_buyer_ty) AS total_buyer_ty,
  SUM(total_buyer_ly) AS total_buyer_ly,
  SUM(total_buyer_fisc_ly) AS total_buyer_fisc_ly,
  SUM(total_buyer_greg_ly) AS total_buyer_greg_ly,
  AVG(aov_ty) AS aov_ty,
  AVG(aov_ly) AS aov_ly,
  AVG(aov_fisc_ly) AS aov_fisc_ly,
  AVG(aov_greg_ly) AS aov_greg_ly,
  AVG(cvr_ty) AS cvr_ty,
  AVG(cvr_ly) AS cvr_ly,
  AVG(cvr_fisc_ly) AS cvr_fisc_ly,
  AVG(cvr_greg_ly) AS cvr_greg_ly,
  cast(SUM(campaign_repeat_count_ty)  as int64) as campaign_repeat_count_ty,
  cast(SUM(campaign_repeat_count_ly)  as int64)  as campaign_repeat_count_ly,
  cast(SUM(campaign_repeat_count_fisc_ly) as int64) as campaign_repeat_count_fisc_ly,
  cast(SUM(campaign_repeat_count_greg_ly)  as int64) as campaign_repeat_count_greg_ly,

  CURRENT_TIMESTAMP() AS record_created_date,
  CURRENT_TIMESTAMP() AS record_updated_date
FROM
  combined_data
GROUP BY
  retailer_media_key,
  region_key,
  campaign_name,
  date_key,
  ly_date,
  fisc_ly_date,
  greg_ly_date,
  brand_key,
  retailer_key,
  media_type,
  placement_type,
  line_item,
  spend_bucket