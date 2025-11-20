CREATE OR REPLACE TABLE `{{params.transform_project}}.skulytics_NA.main_ulta_product_mapping_tbl` AS

WITH perfect_mappings AS (
  SELECT 
    CASE 
      WHEN pr.RETAILER = "MACYS.COM" THEN 1 
      ELSE 2 
    END AS retailer_key,
    pr.* EXCEPT(product_key, retailer),
    b.product_key 
  FROM `{{params.transform_project}}.skulytics_NA.retailer_top_products_tbl` pr
  LEFT JOIN `{{params.dwh_project}}.skulytics_DMART.dim_retail_product_tbl` b
    ON CASE
         WHEN LENGTH(CAST(pr.UPC_CODE AS STRING)) = 11 THEN CONCAT('0', CAST(pr.UPC_CODE AS STRING))
         ELSE CAST(pr.UPC_CODE AS STRING)
       END = b.UPC_CODE 
       AND b.region_KEY = 0 
       AND b.retailer_key = 2
  WHERE LOWER(retailer) = 'ulta.com'
),

modified_product_keys AS (
  SELECT 
    a.* EXCEPT(primary_product_key),
    CASE 
      WHEN b.product_key IS NOT NULL THEN NULL 
      ELSE a.primary_product_key 
    END AS product_key  
  FROM `{{params.transform_project}}.skulytics_NA.ulta_product_mapping_tbl` a 
  LEFT JOIN perfect_mappings b 
    ON a.primary_product_key = b.product_key
)

SELECT DISTINCT 
  'Ulta' AS retailer_name,
  a.brand_name,
  retailer_product_key,
  COALESCE(b.retailer_sku_key, a.retailer_sku_key) AS retailer_sku_key,
  COALESCE(b.product_key, a.product_key) AS primary_product_key 
FROM modified_product_keys a 
FULL JOIN (
  SELECT 
    PPAGE_WEB_ID AS retailer_sku_key,
    MAX(product_key) AS product_key 
  FROM perfect_mappings 
  GROUP BY 1
) b
  ON a.retailer_sku_key = b.retailer_sku_key
WHERE COALESCE(b.retailer_sku_key, a.retailer_sku_key) IS NOT NULL
