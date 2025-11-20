CREATE OR REPLACE TABLE `{{params.transform_project}}.skulytics_NA.stg_emerch_scores_tbl` AS

WITH emerch_product_names AS (
    SELECT
        LOWER(title) AS title,
        MAX(retailer_id) AS main_retailer_id,
        MAX(product_number) AS main_product_number,
        brd_tbl.brand_key AS brand_key
    FROM `{{params.source_project}}.skulytics.sh_emerch_scores_tbl` emerch_tbl
    LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd_tbl
        ON LOWER(
            CASE
                WHEN LOWER(emerch_tbl.brand) = 'prettypink' THEN 'Pretty Pink'
                WHEN LOWER(emerch_tbl.brand) = 'monster' THEN 'Monster Makeup'
                ELSE emerch_tbl.brand
            END
        ) = LOWER(brd_tbl.brand_name)
    GROUP BY LOWER(title), brd_tbl.brand_key
),

mapping_macys_product_key AS (
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
            WHEN REGEXP_INSTR(TRAFFIC_CVR_WEB_ID, ':') > 0 
                THEN SAFE_CAST(SUBSTRING(TRAFFIC_CVR_WEB_ID, 1, REGEXP_INSTR(TRAFFIC_CVR_WEB_ID, ':') - 1) AS INT64)
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
        ON a.brand_key = b.brand_key AND a.product_key = b.product_key
),

top_macys_mapping_tbl AS (
    SELECT
        retailer_product_key,
        brand_key,
        MIN(product_key) AS product_key
    FROM perfect_mappings
    GROUP BY 1, 2
),


mapping_macys_product_title_top_products AS (
    SELECT
        LOWER(retailer_product_name) AS retailer_product_name,
        brand_key,
        product_key,
        ROW_NUMBER() OVER (PARTITION BY LOWER(retailer_product_name), brand_key ORDER BY product_key) AS rn
    FROM `{{params.transform_project}}.skulytics_NA.sh_emerch_sp_macys_product_name_product_keys_mappings_tbl`
    WHERE source = 'emerch score'
    QUALIFY rn = 1
),

ulta_mapping AS (
    SELECT
        retailer_sku_key,
        primary_product_key AS product_key,
        ROW_NUMBER() OVER (PARTITION BY retailer_sku_key ORDER BY primary_product_key) AS rn
    FROM `{{params.transform_project}}.skulytics_NA.main_ulta_product_mapping_tbl`
    QUALIFY rn = 1
),

final_mapping AS (
    SELECT DISTINCT
        0 AS region_key,
        names.brand_key,
        rtl.retailer_key,
        date AS date_key,
        COALESCE(
            macys_mapping_title.product_key,
            macys_map_tbl.product_key,
            ulta_map_tbl.product_key,
            'unmapped'
        ) AS product_key,
        emerch.title AS retailer_product_name,
        retailer_id AS retailer_product_key,
        product_number AS retailer_sku_key,
        health_score AS health_score,
        title_score AS title_score,
        description_score AS description_score,
        image_score AS image_score,
        rating_score AS rating_score,
        keyword_score AS keyword_score,
        review_score AS review_score
    FROM `{{params.source_project}}.skulytics.sh_emerch_scores_tbl` emerch
    LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd
        ON LOWER(
            CASE
                WHEN LOWER(emerch.brand) = 'mac' THEN 'MAC Cosmetics'
                WHEN LOWER(emerch.brand) = 'la mer' THEN 'Creme de la Mer'
                ELSE emerch.brand
            END
        ) = LOWER(brd.brand_name)
    LEFT JOIN emerch_product_names names
        ON LOWER(names.title) = LOWER(emerch.title)
        AND brd.brand_key = names.brand_key
    LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_retailer_tbl` rtl
        ON LOWER(
            CASE
                WHEN TRIM(emerch.retailer) = "Macys.com" THEN "Macy's.com"  
                ELSE TRIM(emerch.retailer)
            END
        ) = LOWER(rtl.retailer_name)
    LEFT JOIN mapping_macys_product_key macys_map_tbl
        ON rtl.retailer_key = 1
        AND macys_map_tbl.macys_product_key = CAST(names.main_retailer_id AS STRING)
        AND macys_map_tbl.brand_key = brd.brand_key
    LEFT JOIN ulta_mapping ulta_map_tbl
        ON rtl.retailer_key = 2
        AND ulta_map_tbl.retailer_sku_key = CAST(names.main_product_number AS STRING)
    LEFT JOIN mapping_macys_product_title_top_products macys_mapping_title
        ON LOWER(macys_mapping_title.retailer_product_name) = LOWER(emerch.title)
        AND macys_mapping_title.brand_key = brd.brand_key
        AND rtl.retailer_key = 1
    where brd.brand_key in (1,2,4,5,10,27) and  rtl.retailer_key in (1,2)
)

SELECT
    CONCAT(
        COALESCE(product_key, ''), '#',
        retailer_key, '#',
        COALESCE(date_key, '1900-01-01'), '#',
        COALESCE(retailer_product_name, ''),'#',
        retailer_product_key,'#',
        retailer_sku_key
    ) AS emerch_scores_key,
    *,
    CURRENT_TIMESTAMP() AS record_created_date,
    CURRENT_TIMESTAMP() AS record_updated_date
FROM final_mapping;