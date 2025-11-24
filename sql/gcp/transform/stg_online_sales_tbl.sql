CREATE OR REPLACE TABLE `{{params.transform_project}}.skulytics_NA.stg_online_sales_tbl` AS
WITH online_sales AS (
  SELECT
    0 AS region_key,
    sales.W_E_DATE AS date_key,
    DATE_TRUNC(sales.W_E_DATE, WEEK) AS week_start_date,
    sales.W_E_DATE AS week_end_date,
    DATE_TRUNC(sales.W_E_DATE, MONTH) AS month_start_date,
    LAST_DAY(sales.W_E_DATE) AS month_end_date,
    brd_tbl.brand_id AS brand_key,
    rtl_tbl.retailer_key AS retailer_key,
    dim_prod.PRODUCT_KEY AS product_key,      
    PRODUCT_DESC AS retailer_product_name,
    SHADE_DESCRIPTION AS retailer_shade_name,
    pr.UPC_CODE AS retailer_upc_code,
    SELL_THRU_GROSS_UNITS_SOLD AS gross_units_sold,
    SELL_THRU_GROSS_DOLLARS AS gross_sales_usd,
    CUSTOMERS_RETURN_UNIT AS returned_units,
    CUSTOMER_RETURN_DOLLARS AS returned_sales_usd,
    ROW_NUMBER() OVER(
      PARTITION BY sales.W_E_DATE, rtl_tbl.retailer_key, brd_tbl.brand_id, dim_prod.PRODUCT_KEY 
      ORDER BY SELL_THRU_GROSS_DOLLARS DESC
    ) AS rn     
  FROM
    `{{params.ds_project}}.landing.retailer_sales` sales
  LEFT JOIN
    `{{params.ds_project}}.landing.retailer_brands` br
    ON sales.BRAND_ID = br.BRAND_ID
  LEFT JOIN
    (
      SELECT 
        product_key,
        upc_code,
        PRODUCT_DESC,
        SHADE_DESCRIPTION,
        ROW_NUMBER() OVER(PARTITION BY UPC_CODE, PRODUCT_KEY ORDER BY PRODUCT_DESC DESC, SHADE_DESCRIPTION DESC) AS rn 
      FROM 
        `{{params.ds_project}}.landing.retailer_products` 
      QUALIFY 
        rn = 1
    ) pr
    ON sales.PRODUCT_KEY = pr.PRODUCT_KEY
  LEFT JOIN
    `{{params.ds_project}}.landing.retailer_doors` rd
    ON sales.DOOR_KEY = rd.LEGACY_DOOR_KEY
  LEFT JOIN
    `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd_tbl
    ON LOWER(
      CASE
        WHEN br.BRAND_DESC = "prettypink " THEN "Pretty Pink"
        WHEN br.BRAND_DESC = "monster " THEN "Monster Makeup"
      END
    ) = LOWER(brd_tbl.brand_name)
  LEFT JOIN
    `{{params.dwh_project}}.COMMON_DMART.dim_retailer_tbl` rtl_tbl
    ON LOWER(
      CASE
        WHEN rd.LEGACY_DOOR_DESC = "MACYS.COM" THEN "Macy's.com"
        WHEN rd.LEGACY_DOOR_DESC = "ULTA-ECOMMERCE #902" THEN 'Ulta.com'
      END
    ) = LOWER(rtl_tbl.retailer_name)
  LEFT JOIN
    (
      SELECT 
        *, 
        ROW_NUMBER() OVER(PARTITION BY UPC_CODE ORDER BY product_key) AS rn
      FROM 
        (SELECT * FROM `{{params.dwh_project}}.COMMON_DMART.dim_product_tbl` WHERE region_id = 0)
      QUALIFY 
        rn = 1
    ) dim_prod
    ON CAST(dim_prod.UPC_CODE AS STRING) = (
      CASE
        WHEN LENGTH(CAST(pr.UPC_CODE AS STRING)) = 11 THEN CONCAT('0', CAST(pr.UPC_CODE AS STRING))
        ELSE CAST(pr.UPC_CODE AS STRING)
      END 
    ) 
    AND dim_prod.brand_id = brd_tbl.brand_id 
    AND region_id = 0
  WHERE
    rtl_tbl.retailer_key IN (1, 2)
    AND brd_tbl.brand_id IN (1, 2, 4, 5, 10, 27) 
    AND dim_prod.PRODUCT_KEY IS NOT NULL
  QUALIFY 
    rn = 1
)

SELECT 
  CONCAT(
    COALESCE(CAST(date_key as string), ''), '#',
    COALESCE(CAST(retailer_key as string), ''), '#',
    COALESCE(CAST(brand_key as string), ''), '#',
    COALESCE(product_key, '')
  ) AS retailer_online_sales_key,
  *,
  CURRENT_TIMESTAMP() AS record_created_date,
  CURRENT_TIMESTAMP() AS record_updated_date
FROM 
  online_sales