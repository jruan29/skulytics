CREATE OR REPLACE TABLE `{{params.transform_project}}.skulytics_NA.stg_stock_level_tbl` AS
WITH ulta_mapping AS (
    SELECT
        retailer_sku_key,
        primary_product_key AS product_key,
        ROW_NUMBER() OVER (PARTITION BY retailer_sku_key ORDER BY primary_product_key) AS rn
    FROM `{{params.transform_project}}.skulytics_NA.main_ulta_product_mapping_tbl`
    QUALIFY rn = 1
),
ulta_stock AS (
    SELECT
        0 AS region_key,
        CAST(ulta_stk_tbl.TIMESTAMP AS DATE) AS date_key,
        brd_tbl.brand_id AS brand_key,
        2 AS retailer_key,
        COALESCE(ulta_map.product_key, 'unmapped') AS product_key,
        CAST(ulta_stk_tbl.productid AS STRING) AS retailer_product_key,
        CAST(ulta_stk_tbl.skuid AS STRING) AS retailer_sku_key,
        ulta_stk_tbl.title AS retailer_product_name,
        ulta_stk_tbl.description AS retailer_product_description,
        ulta_stk_tbl.name AS retailer_product_shadename,
        ulta_stk_tbl.category AS retailer_product_category,
        ulta_stk_tbl.subcategory AS retailer_product_subcategory,
        ulta_stk_tbl.price AS unit_price,
        CASE
            WHEN ulta_stk_tbl.salePrice > ulta_stk_tbl.price or ulta_stk_tbl.salePrice is null THEN ulta_stk_tbl.price
            ELSE ulta_stk_tbl.salePrice
        END AS selling_price,
        ulta_stk_tbl.isoutofstock
    FROM `{{params.ds_project}}.landing.ulta_products` ulta_stk_tbl
    LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd_tbl
        ON LOWER(
            CASE
                WHEN LOWER(ulta_stk_tbl.brand) = 'prettypink' THEN 'Pretty Pink'
                WHEN LOWER(ulta_stk_tbl.brand) IN ('monster', 'monstermakeup') THEN 'Monster Makeup'
                ELSE ulta_stk_tbl.brand
            END
        ) = LOWER(brd_tbl.brand_name)
    LEFT JOIN ulta_mapping ulta_map
        ON CAST(ulta_stk_tbl.skuid AS STRING) = ulta_map.retailer_sku_key
    WHERE brd_tbl.brand_id IN (1, 2, 4, 5, 27)
),
macys_stock AS (
    SELECT
        0 AS region_key,
        CAST(macys_stk_tbl.TIMESTAMP AS DATE) AS date_key,
        brd_tbl.brand_id AS brand_key,
        1 AS retailer_key,
        COALESCE(pd_tbl.PRODUCT_KEY, 'unmapped') AS product_key,
        CAST(macys_stk_tbl.productid AS STRING) AS retailer_product_key,
        CAST(NULL AS STRING) AS retailer_sku_key,
        macys_stk_tbl.title AS retailer_product_name,
        macys_stk_tbl.description AS retailer_product_description,
        macys_stk_tbl.color AS retailer_product_shadename,
        macys_stk_tbl.category AS retailer_product_category,
        macys_stk_tbl.subcategory AS retailer_product_subcategory,
        macys_stk_tbl.price AS unit_price,
        CASE
            WHEN macys_stk_tbl.salePrice > macys_stk_tbl.price or macys_stk_tbl.salePrice is null THEN macys_stk_tbl.price
            ELSE macys_stk_tbl.salePrice
        END AS selling_price,
        macys_stk_tbl.islowstock AS isoutofstock
    FROM `{{params.ds_project}}.landing.macys_products` macys_stk_tbl
    LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd_tbl
        ON LOWER(
            CASE
                WHEN LOWER(macys_stk_tbl.brand) = 'prettypink' THEN 'Pretty Pink'
                WHEN LOWER(macys_stk_tbl.brand) IN ('monster makeup', 'monster') THEN 'Monster Makuep'
                ELSE macys_stk_tbl.brand
            END
        ) = LOWER(brd_tbl.brand_name)
    LEFT JOIN `{{params.dwh_project}}.skulytics_DMART.dim_retail_product_tbl` pd_tbl
        ON pd_tbl.UPC_CODE = (
            CASE
                WHEN LENGTH(SUBSTRING(macys_stk_tbl.skuId, 1, LENGTH(macys_stk_tbl.skuId) - 3)) = 11 THEN CONCAT('0', SUBSTRING(macys_stk_tbl.skuId, 1, LENGTH(macys_stk_tbl.skuId) - 3))
                WHEN LENGTH(SUBSTRING(macys_stk_tbl.skuId, 1, LENGTH(macys_stk_tbl.skuId) - 3)) = 12 THEN SUBSTRING(macys_stk_tbl.skuId, 1, LENGTH(macys_stk_tbl.skuId) - 3)
                WHEN LENGTH(macys_stk_tbl.skuId) = 11 THEN CONCAT('0', CAST(macys_stk_tbl.skuId AS STRING))
                ELSE macys_stk_tbl.skuId
            END
        )
        AND pd_tbl.retailer_key = 1
    WHERE brd_tbl.brand_id IN (1, 2, 4, 5, 10, 27)
),
stock_main AS (
    SELECT * FROM ulta_stock
    UNION ALL
    SELECT * FROM macys_stock
),
final_stock_level AS (
    SELECT
        date_key,
        region_key,
        brand_key,
        retailer_key,
        product_key,
        retailer_product_key,
        retailer_sku_key,
        retailer_product_name,
        MAX(retailer_product_description) AS retailer_product_description,
        retailer_product_shadename,
        MAX(retailer_product_category) AS retailer_product_category,
        MAX(retailer_product_subcategory) AS retailer_product_subcategory,
        MAX(unit_price) AS unit_price,
        MAX(selling_price) AS selling_price,
        MIN(isoutofstock) AS isoutofstock  -- FALSE if any variant is in stock
    FROM stock_main
    GROUP BY
        date_key,
        region_key,
        brand_key,
        retailer_key,
        product_key,
        retailer_product_key,
        retailer_sku_key,
        retailer_product_name,
        retailer_product_shadename
)
SELECT
    CONCAT(
        COALESCE(CAST(date_key AS STRING), ''), '#',
        COALESCE(CAST(retailer_key AS STRING), ''), '#',
        COALESCE(CAST(product_key AS STRING), ''), '#',
        COALESCE(CAST(region_key AS STRING), ''), '#',
        COALESCE(CAST(retailer_product_key AS STRING), ''), '#',
        COALESCE(CAST(retailer_sku_key AS STRING), ''), '#',
        COALESCE(CAST(retailer_product_shadename AS STRING), ''), '#',
        COALESCE(CAST(retailer_product_name AS STRING), '')
    ) AS stock_level_key,
    *,
    CURRENT_TIMESTAMP() AS record_created_date,
    CURRENT_TIMESTAMP() AS record_updated_date
FROM final_stock_level;
