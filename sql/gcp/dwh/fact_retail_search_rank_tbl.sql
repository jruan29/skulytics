CREATE OR REPLACE TABLE `{{params.dwh_project}}.skulytics_DMART.fact_retail_search_rank_tbl` AS
WITH dim_date AS (
  SELECT
    dd.*,
    dd.na_ly_date AS fisc_ly_date,
    dd.row_ly_date AS greg_ly_date
  FROM `{{params.dwh_project}}.COMMON_DMART.dim_date_tbl` dd
),
top_products_search_keyword AS (
  SELECT
    CASE WHEN LOWER(TRIM(pr.Retailer)) = "macys.com" THEN 1 ELSE 2 END AS retailer_key,
    pr.brand_key,
    pr.PPAGE_WEB_ID,
    b.product_key,
    pr.Keywords AS original_keywords,
    LOWER(TRIM(keyword)) AS keyword,
    keyword_offset AS keyword_position
  FROM `{{params.transform_project}}.skulytics_NA.retailer_top_products_tbl` pr
  LEFT JOIN `{{params.dwh_project}}.skulytics_DMART.dim_retail_product_tbl` b
    ON CASE
         WHEN LENGTH(CAST(pr.UPC_CODE AS STRING)) = 11 THEN CONCAT('0', CAST(pr.UPC_CODE AS STRING))
         ELSE CAST(pr.UPC_CODE AS STRING)
       END = b.UPC_CODE
       AND b.region_KEY = 0
       AND b.retailer_key = CASE WHEN LOWER(TRIM(pr.Retailer)) = "macys.com" THEN 1 ELSE 2 END
  CROSS JOIN UNNEST(SPLIT(pr.Keywords, ',')) AS keyword WITH OFFSET AS keyword_offset
  WHERE b.product_key IS NOT NULL
),
top_search_keyword_tbl AS (
  SELECT DISTINCT
    retailer_key,
    brand_key,
    product_key,
    keyword,
    CASE WHEN keyword_position = 0 THEN 1 ELSE 0 END AS is_first_keyword
  FROM top_products_search_keyword
  WHERE keyword_position = 0
  UNION ALL
  SELECT DISTINCT
    retailer_key,
    brand_key,
    CONCAT('CP',PPAGE_WEB_ID,'#',BRAND_KEY,'#',0) AS product_key,
    keyword,
    CASE WHEN keyword_position = 0 THEN 1 ELSE 0 END AS is_first_keyword
  FROM top_products_search_keyword
  WHERE keyword_position = 0
),
result_types AS (
  SELECT DISTINCT result_type
  FROM `{{params.transform_project}}.skulytics_NA.stg_search_rank_tbl`
),
max_date AS (
  SELECT MAX(date_key) AS max_date_key
  FROM `{{params.transform_project}}.skulytics_NA.stg_search_rank_tbl`
),
dates AS (
  SELECT date_key
  FROM `{{params.dwh_project}}.COMMON_DMART.dim_date_tbl`
  WHERE date_key >= DATE('2022-07-01')
    AND date_key <= (SELECT max_date_key FROM max_date)
),
top_search_keywords as (
  SELECT
    tsk.retailer_key,
    tsk.brand_key,
    tsk.product_key,
    tsk.keyword,
    tsk.is_first_keyword,
    rt.result_type,
    d.date_key
  FROM top_search_keyword_tbl tsk
  CROSS JOIN result_types rt
  CROSS JOIN dates d
),
base_data AS (
    SELECT
    COALESCE(sr.region_key, 0) AS region_key,
    COALESCE(sr.date_key, tp_search_key.date_key) AS date_key,
    COALESCE(sr.brand_key, tp_search_key.brand_key) AS brand_key,
    COALESCE(sr.retailer_key, tp_search_key.retailer_key) AS retailer_key,
    COALESCE(sr.product_key, tp_search_key.product_key) AS product_key,
    COALESCE(sr.result_type, tp_search_key.result_type) AS search_result_type,
    COALESCE(sr.search_keyword, tp_search_key.keyword) AS search_keyword,
    CASE
      WHEN tp.product_key IS NOT NULL
      OR tp_search_key.product_key IS NOT NULL THEN 1
      ELSE 0
    END AS hero_product_flag,
    tp_search_key.is_first_keyword AS top_search_keyword_flag,
    SUM(sr.rank) AS search_rank,
    COUNT(sr.rank) AS search_rank_record_count
  FROM
    `{{params.transform_project}}.skulytics_NA.stg_search_rank_tbl` sr
    LEFT JOIN (
      SELECT DISTINCT
        retailer_key,
        product_key
      FROM
        top_products_search_keyword
    ) tp ON sr.product_key=tp.product_key
    AND sr.retailer_key=tp.retailer_key
    FULL JOIN top_search_keywords tp_search_key ON sr.product_key=tp_search_key.product_key
    AND sr.retailer_key=tp_search_key.retailer_key
    AND sr.date_key=tp_search_key.date_key
    AND LOWER(TRIM(sr.search_keyword))=LOWER(TRIM(tp_search_key.keyword))
    AND sr.result_type=tp_search_key.result_type
  WHERE
    COALESCE(sr.date_key, tp_search_key.date_key)>='2022-07-01'
  GROUP BY 1,2,3,4,5,6,7,8,9
),
fact_keys AS (
  SELECT
    bd.region_key,
    bd.brand_key,
    bd.retailer_key,
    bd.product_key,
    bd.search_result_type,
    bd.search_keyword,
    bd.hero_product_flag,
    bd.top_search_keyword_flag,
    dd.as_date AS date_key,
    CASE
      WHEN bd.region_key IN (0, 27) THEN dd.na_ly_date
      ELSE dd.row_ly_date
    END AS ly_date,
    dd.na_ly_date AS fisc_ly_date,
    dd.row_ly_date AS greg_ly_date
  FROM base_data bd
  LEFT JOIN dim_date dd ON dd.as_date = bd.date_key
)
SELECT
  CONCAT(
    COALESCE(CAST(fk.date_key AS STRING), ''), '#',
    COALESCE(CAST(fk.retailer_key AS STRING), ''), '#',
    COALESCE(CAST(fk.product_key AS STRING), ''), '#',
    COALESCE(CAST(fk.search_result_type AS STRING), ''), '#',
    COALESCE(CAST(fk.search_keyword AS STRING), ''), '#',
    COALESCE(CAST(fk.brand_key AS STRING), '')
  ) AS search_rank_key,
 
  CONCAT(
    COALESCE(CAST(fk.retailer_key AS STRING), ''), '#',
    COALESCE(CAST(fk.product_key AS STRING), '')
  ) AS retailer_product_key,
 
  fk.region_key,
  fk.brand_key,
  fk.date_key,
  fk.ly_date,
  fk.fisc_ly_date,
  fk.greg_ly_date,
  fk.retailer_key,
  fk.product_key,
  fk.search_result_type,
  fk.search_keyword,
  fk.hero_product_flag,
  fk.top_search_keyword_flag,
  ty.search_rank AS search_rank_ty,
  ly.search_rank AS search_rank_ly,
  fisc_ly.search_rank AS search_rank_fisc_ly,
  greg_ly.search_rank AS search_rank_greg_ly,
  ty.search_rank_record_count AS search_rank_record_count_ty,
  ly.search_rank_record_count AS search_rank_record_count_ly,
  fisc_ly.search_rank_record_count AS search_rank_record_count_fisc_ly,
  greg_ly.search_rank_record_count AS search_rank_record_count_greg_ly,
  CURRENT_TIMESTAMP() AS record_created_date,
  CURRENT_TIMESTAMP() AS record_updated_date
FROM fact_keys fk
LEFT JOIN base_data ty
  ON fk.region_key = ty.region_key
  AND fk.brand_key = ty.brand_key
  AND fk.retailer_key = ty.retailer_key
  AND fk.product_key = ty.product_key
  AND fk.search_result_type = ty.search_result_type
  AND fk.search_keyword = ty.search_keyword
  AND fk.date_key = ty.date_key
LEFT JOIN base_data ly
  ON fk.region_key = ly.region_key
  AND fk.brand_key = ly.brand_key
  AND fk.retailer_key = ly.retailer_key
  AND fk.product_key = ly.product_key
  AND fk.search_result_type = ly.search_result_type
  AND fk.search_keyword = ly.search_keyword
  AND fk.ly_date = ly.date_key
LEFT JOIN base_data fisc_ly
  ON fk.region_key = fisc_ly.region_key
  AND fk.brand_key = fisc_ly.brand_key
  AND fk.retailer_key = fisc_ly.retailer_key
  AND fk.product_key = fisc_ly.product_key
  AND fk.search_result_type = fisc_ly.search_result_type
  AND fk.search_keyword = fisc_ly.search_keyword
  AND fk.fisc_ly_date = fisc_ly.date_key
LEFT JOIN base_data greg_ly
  ON fk.region_key = greg_ly.region_key
  AND fk.brand_key = greg_ly.brand_key
  AND fk.retailer_key = greg_ly.retailer_key
  AND fk.product_key = greg_ly.product_key
  AND fk.search_result_type = greg_ly.search_result_type
  AND fk.search_keyword = greg_ly.search_keyword
  AND fk.greg_ly_date = greg_ly.date_key;