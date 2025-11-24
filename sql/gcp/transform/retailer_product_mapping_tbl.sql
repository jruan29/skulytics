CREATE OR REPLACE TABLE `{{params.transform_project}}.skulytics_NA.retailer_product_mapping_tbl` AS 

WITH dim_prod AS (
    SELECT DISTINCT 
        brand_id,
        product_key,
        upc_code
    FROM `{{params.dwh_project}}.COMMON_DMART.dim_product_tbl`
    WHERE 
        region_id = 0 
        AND brand_id IN (1, 2, 4, 5, 10, 27) 
        AND product_key IS NOT NULL
),

macys_products AS (
    SELECT 
        1 AS retailer_key,
        dim_prod.brand_id AS brand_key,
        dim_prod.product_key AS product_key,
        CAST(macys_prod.productId AS STRING) AS macys_product_key,
        macys_prod.title AS retailer_product_name,
        CAST(NULL AS STRING) AS ulta_sku_key,
        'macys_products' AS source_name
    FROM dim_prod
    LEFT JOIN (
        SELECT DISTINCT 
            skuId,
            productId, 
            title 
        FROM `{{params.ds_project}}.landing.macys_products`
    ) macys_prod
        ON dim_prod.upc_code = (
            CASE
                WHEN LENGTH(SUBSTRING(macys_prod.skuId, 1, LENGTH(macys_prod.skuId) - 3)) = 11
                    THEN CONCAT('0', SUBSTRING(macys_prod.skuId, 1, LENGTH(macys_prod.skuId) - 3))
                WHEN LENGTH(SUBSTRING(macys_prod.skuId, 1, LENGTH(macys_prod.skuId) - 3)) = 12
                    THEN SUBSTRING(macys_prod.skuId, 1, LENGTH(macys_prod.skuId) - 3)
                WHEN LENGTH(macys_prod.skuId) = 11 
                    THEN CONCAT('0', CAST(macys_prod.skuId AS STRING))
                ELSE macys_prod.skuId
            END
        )
    WHERE macys_prod.productId IS NOT NULL 
),

lamer_mapping AS (
    SELECT 
        1 AS retailer_key,
        10 AS brand_key,
        dim_prod.product_key AS product_key,
        CAST(lamer_mapping.retailer_product_key AS STRING) AS macys_product_key,
        lamer_mapping.retailer_product_name,
        CAST(NULL AS STRING) AS ulta_sku_key,
        lamer_mapping.source_name
    FROM dim_prod
    LEFT JOIN `{{params.transform_project}}.skulytics_NA.lamer_product_mapping_tbl` lamer_mapping 
        ON dim_prod.product_key = lamer_mapping.primary_product_key 
    WHERE
        lamer_mapping.primary_product_key IS NOT NULL AND lamer_mapping.brand_name = 'Creme de la Mer' 
),

macys_mapping AS (
    SELECT 
        1 AS retailer_id,
        dim_prod.brand_id AS brand_key,
        dim_prod.product_key AS product_key,
        CAST(retailer_sku_key AS STRING) AS macys_product_key,
        retailer_product_name,
        CAST(NULL AS STRING) AS ulta_sku_key,
        macys_mapping.source_name AS source_name
    FROM dim_prod
    LEFT JOIN `{{params.transform_project}}.skulytics_NA.macys_product_mapping_tbl` macys_mapping
        ON dim_prod.product_key = macys_mapping.primary_product_key 
    WHERE macys_mapping.retailer_sku_key IS NOT NULL OR macys_mapping.retailer_product_name IS NOT NULL
),

ulta_mapping AS (
    SELECT 
        2 AS retailer_key,
        dim_prod.brand_id AS brand_key,
        dim_prod.product_key AS product_key,
        CAST(NULL AS STRING) AS macys_product_key,
        ulta_mapping.retailer_product_name AS retailer_product_name,
        CAST(ulta_mapping.retailer_sku_key AS STRING) AS ulta_sku_key,
        ulta_mapping.source_name AS source_name
    FROM dim_prod
    LEFT JOIN `{{params.transform_project}}.skulytics_NA.ulta_product_mapping_tbl` ulta_mapping
        ON ulta_mapping.primary_product_key = dim_prod.product_key 
    WHERE ulta_mapping.retailer_sku_key IS NOT NULL OR ulta_mapping.retailer_product_name IS NOT NULL
)

SELECT DISTINCT * FROM (
    SELECT * FROM macys_products
    UNION ALL
    SELECT * FROM lamer_mapping
    UNION ALL
    SELECT * FROM macys_mapping
    UNION ALL
    SELECT * FROM ulta_mapping

)