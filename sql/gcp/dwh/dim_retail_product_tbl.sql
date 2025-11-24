CREATE OR REPLACE TABLE `{{params.dwh_project}}.skulytics_DMART.dim_retail_product_tbl` AS

WITH dim_product_tbl AS (
  SELECT DISTINCT
    PRODUCT_KEY AS product_key,
    BRAND_ID AS brand_key,
    REGION_ID AS region_key,
    PROD_RGN_NAME AS prod_rgn_name,
    PRODUCT_SIZE AS product_size,
    SHADENAME AS shadename,
    MAJOR_CATEGORY_SHORT_DESCRIPTION AS major_category_short_description,
    MAJOR_CATEGORY_MEDIUM_DESCRIPTION AS major_category_medium_description,
    CATEGORY_SHORT_DESCRIPTION AS category_short_description,
    CATEGORY_MEDIUM_DESCRIPTION AS category_medium_description,
    SUB_CATEGORY_SHORT_DESCRIPTION AS sub_category_short_description,
    SUB_CATEGORY_MEDIUM_DESCRIPTION AS sub_category_medium_description,
    CATEGORY_NAME AS category_name,
    FULL_PRODUCT_CODE AS full_product_code,
    UPC_CODE AS upc_code,
    ROW_NUMBER() OVER (PARTITION BY PRODUCT_KEY) AS rn
  FROM `{{params.dwh_project}}.COMMON_DMART.dim_product_tbl` dp
  WHERE region_id = 0
    AND brand_id IN (1, 2, 4, 5, 10, 27)
  QUALIFY rn = 1
),

dim_product_tbl_upc_dedup AS (
  SELECT
    * EXCEPT (rn),
    ROW_NUMBER() OVER (PARTITION BY upc_code ORDER BY product_key) AS rn
  FROM dim_product_tbl
  QUALIFY rn = 1
),

dim_retail_product_tbl AS (
  SELECT
    dr.retailer_key,
    dp.*
  FROM dim_product_tbl_upc_dedup dp
  CROSS JOIN `{{params.dwh_project}}.COMMON_DMART.dim_retailer_tbl` dr
),

top_products AS (
  SELECT
    dr.retailer_key,
    top.*,
    ROW_NUMBER() OVER (
      PARTITION BY
        retailer,
        upc_code
      ORDER BY
        PPAGE_WEB_ID
    ) rn
  FROM `{{params.transform_project}}.skulytics_NA.retailer_top_products_tbl` top
  LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_retailer_tbl` dr
    ON CASE 
         WHEN top.retailer = 'MACYS.COM' THEN 1
         ELSE 2 
       END = dr.retailer_key
  QUALIFY rn = 1
),
macys_collection_page AS (
  SELECT DISTINCT
    1 AS retailer_key,
    0 AS region_key,
    BRAND_KEY brand_key,
    ELC_Standardized_Product_Name master_product_name,
    CONCAT('CP',PPAGE_WEB_ID) full_product_code,
    CONCAT('CP',PPAGE_WEB_ID,'#',BRAND_KEY,'#',0) AS product_key,
    CONCAT(1,'#','CP',PPAGE_WEB_ID,'#',BRAND_KEY,'#',0) AS retailer_product_key,
    'Collection Page' AS shadename
  FROM
    `{{params.transform_project}}.skulytics_NA.retailer_top_products_tbl`
  WHERE
    retailer='MACYS.COM'
)

SELECT
  dp.* EXCEPT (rn, product_size, shadename),
  CONCAT(dp.retailer_key, '#', dp.product_key) AS retailer_product_key,
  top.ELC_Standardized_Product_Name AS master_product_name,
  COALESCE(dp.product_size, top.SIZE_OZ, top.SIZE_ML) AS product_size,
  COALESCE(dp.shadename, INITCAP(top.SHADE)) AS shadename
FROM dim_retail_product_tbl dp
LEFT JOIN top_products top
  ON CASE 
       WHEN CHAR_LENGTH(CAST(top.UPC_CODE AS STRING)) = 11 
         THEN CONCAT('0', CAST(top.UPC_CODE AS STRING))
       ELSE CAST(top.UPC_CODE AS STRING)
     END = dp.UPC_CODE
  AND dp.retailer_key = top.retailer_key  
UNION ALL
SELECT
  retailer_key,
  product_key,
  brand_key,
  region_key,
  master_product_name AS prod_rgn_name,
  NULL AS major_category_short_description,
  NULL AS major_category_medium_description,
  NULL AS category_short_description,
  NULL AS category_medium_description,
  NULL AS sub_category_short_description,
  NULL AS sub_category_medium_description,
  NULL AS category_name,
  full_product_code,
  NULL AS upc_code,
  retailer_product_key,
  master_product_name,
  NULL AS product_size,
  shadename
FROM
  macys_collection_page; 