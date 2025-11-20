CREATE OR REPLACE TABLE `{{params.transform_project}}.skulytics_NA.stg_search_rank_tbl` AS

WITH mapping_macys_product_key AS (
  SELECT
    macys_product_key,
    product_key,
    brand_key,
    ROW_NUMBER() OVER (PARTITION BY macys_product_key, brand_key ORDER BY product_key) AS rn
  FROM `{{params.transform_project}}.skulytics_NA.retailer_product_mapping_tbl`
  WHERE macys_product_key IS NOT NULL
  QUALIFY rn = 1
),


perfect_mappings AS (
  SELECT
    CASE
      WHEN REGEXP_INSTR(TRAFFIC_CVR_WEB_ID, ':') > 0 THEN SAFE_CAST(SUBSTRING(TRAFFIC_CVR_WEB_ID, 1, REGEXP_INSTR(TRAFFIC_CVR_WEB_ID, ':') - 1) AS INT64)
      ELSE NULL
    END AS retailer_product_key,
    
    b.brand_key,
    b.product_key
  FROM `{{params.transform_project}}.skulytics_NA.retailer_top_products_tbl` pr
  LEFT JOIN `{{params.dwh_project}}.skulytics_DMART.dim_retail_product_tbl` b
    ON (
      CASE
        WHEN LENGTH(CAST(pr.UPC_CODE AS STRING)) = 11 THEN CONCAT('0', CAST(pr.UPC_CODE AS STRING))
        ELSE CAST(pr.UPC_CODE AS STRING)
      END
    ) = b.UPC_CODE
    AND b.retailer_key = 1
  WHERE LOWER(retailer) = 'macys.com'
),

modified_mapping_macys_product_key AS (
  SELECT
    a.macys_product_key,
    a.brand_key,
    CASE
      WHEN b.product_key IS NOT NULL THEN 'unmapped'
      ELSE a.product_key
    END AS product_key
  FROM mapping_macys_product_key a
  LEFT JOIN perfect_mappings b
    ON a.brand_key = b.brand_key
    AND a.product_key = b.product_key
),

top_macys_mapping_tbl AS (
  SELECT
    retailer_product_key,
    brand_key,
    MIN(product_key) AS product_key
  FROM perfect_mappings
  GROUP BY 1, 2
),

final_macys_mapping_tbl AS (
  SELECT
    a.macys_product_key,
    a.brand_key,
    COALESCE(b.product_key, a.product_key) AS product_key
  FROM modified_mapping_macys_product_key a
  LEFT JOIN top_macys_mapping_tbl b
    ON CAST(a.macys_product_key AS STRING) = CAST(b.retailer_product_key AS STRING)
    AND a.brand_key = b.brand_key
),

ulta_mapping AS (
  SELECT
    retailer_sku_key,
    primary_product_key AS product_key,
    ROW_NUMBER() OVER (PARTITION BY retailer_sku_key ORDER BY primary_product_key) AS rn
  FROM `{{params.transform_project}}.skulytics_NA.main_ulta_product_mapping_tbl`
  QUALIFY rn = 1
)
,final_tbl AS (
  SELECT DISTINCT
    0 AS region_key,
    search_rank_main.REPORT_DATE AS date_key,
    brd_tbl.brand_id AS brand_key,
    rtl_tbl.retailer_key AS retailer_key,
    CASE
      WHEN rtl_tbl.retailer_key = 2 THEN COALESCE(ulta_tbl.product_key, 'unmapped')
      ELSE COALESCE(drp.product_key, macys_tbl.product_key, 'unmapped')
    END AS product_key,
    CASE WHEN rtl_tbl.retailer_key = 1 THEN search_rank_main.product_id ELSE NULL END AS retailer_product_key,
    CASE WHEN rtl_tbl.retailer_key = 2 THEN search_rank_main.product_id ELSE NULL END AS retailer_sku_key,
    CASE
      WHEN REGEXP_REPLACE(LOWER(COALESCE(search_rank_main.title, '')), r'\s+', '') = REGEXP_REPLACE(LOWER(COALESCE(search_rank_main.brand, '')), r'\s+', '')
        OR REGEXP_REPLACE(LOWER(COALESCE(search_rank_main.title, '')), r'\s+', '') IN ('lamer', 'mac', 'm.a.c', 'm.a.c.', 'cremedelamer')
        OR REGEXP_REPLACE(LOWER(COALESCE(search_rank_main.title, '')), r'\s+', '') LIKE '%cr%medelamer'
        OR REGEXP_REPLACE(LOWER(COALESCE(search_rank_main.title, '')), r'\s+', '') LIKE 'est%lauder'
        OR brd_tbl.brand_name = search_rank_main.title
          AND REGEXP_CONTAINS(ad_url, r'/product/')
      THEN REGEXP_REPLACE(LOWER(REGEXP_EXTRACT(ad_url, r'/product/([^/?]+)')), r'[-]+', ' ')
      ELSE search_rank_main.title
    END AS retailer_product_name,
    search_rank_main.RESULT_TYPE AS result_type,
    search_rank_main.KEYWORD AS search_keyword,
    MIN(search_rank_main.POSITION) AS RANK
  FROM `{{params.ds_project}}.landing.skai_retailer_products` search_rank_main
  LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd_tbl
    ON LOWER(
      CASE
        WHEN LOWER(search_rank_main.brand) = 'prettypink' THEN 'Pretty Pink'
        WHEN LOWER(search_rank_main.brand) = 'monstermakeup' THEN 'Monster Makeup'
        ELSE search_rank_main.brand
      END
    ) = LOWER(brd_tbl.brand_name)
  LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_retailer_tbl` rtl_tbl
    ON LOWER(
      CASE
        WHEN LOWER(search_rank_main.RETAILER) = "macy's" THEN "Macy's.com"
        WHEN LOWER(search_rank_main.RETAILER) = "ulta beauty" THEN 'Ulta.com'
        ELSE search_rank_main.RETAILER
      END
    ) = LOWER(rtl_tbl.retailer_name)
  LEFT JOIN final_macys_mapping_tbl macys_tbl
    ON rtl_tbl.retailer_key = 1
    AND macys_tbl.macys_product_key = search_rank_main.product_id
    AND macys_tbl.brand_key = brd_tbl.brand_id
  LEFT JOIN ulta_mapping ulta_tbl
    ON rtl_tbl.retailer_key = 2
    AND ulta_tbl.retailer_sku_key = search_rank_main.product_id
  LEFT JOIN `{{params.dwh_project}}.skulytics_DMART.dim_retail_product_tbl`  drp
    ON CONCAT('CP',search_rank_main.product_id) = drp.full_product_code
    AND drp.retailer_key = 1
    AND drp.shadename = 'Collection Page'
  WHERE brd_tbl.brand_id IN (1, 2, 4, 5, 10, 27) 
    AND rtl_tbl.retailer_key IN (1, 2)
  GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
)

SELECT
  CONCAT(
    CAST(COALESCE(date_key, '1900-01-01') AS STRING), '#',
    CAST(retailer_key AS STRING), '#',
    CAST(COALESCE(product_key, '') AS STRING), '#',
    CAST(COALESCE(result_type, '') AS STRING), '#',
    CAST(COALESCE(search_keyword, '') AS STRING), '#',
    COALESCE(retailer_product_name, ''), '#',
    COALESCE(retailer_product_key, ''), '#',
    COALESCE(retailer_sku_key, '')
  ) AS search_rank_key,
  *,
  CURRENT_TIMESTAMP() AS record_created_date,
  CURRENT_TIMESTAMP() AS record_updated_date
FROM final_tbl;