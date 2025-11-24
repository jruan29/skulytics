CREATE OR REPLACE TABLE `{{params.transform_project}}.skulytics_NA.stg_sponsored_products_tbl` AS
WITH 
mapping_macys_product_title_top_products AS (
    SELECT
        LOWER(retailer_product_name) AS retailer_product_name,
        brand_key,
        product_key,
        ROW_NUMBER() OVER (PARTITION BY LOWER(retailer_product_name), brand_key ORDER BY product_key) AS rn
    FROM `{{params.transform_project}}.skulytics_NA.sh_emerch_sp_macys_product_name_product_keys_mappings_tbl`
    WHERE source = 'sponsored products'
    QUALIFY rn = 1
),
mapping_macys_product_title AS (
    SELECT
        LOWER(retailer_product_name) AS retailer_product_name,
        brand_key,
        product_key,
        ROW_NUMBER() OVER (PARTITION BY LOWER(retailer_product_name), brand_key ORDER BY product_key) AS rn
    FROM `{{params.transform_project}}.skulytics_NA.retailer_product_mapping_tbl`
    QUALIFY rn = 1
),
unmap_macys_product_title_non_top AS (
    SELECT 
        a.retailer_product_name, 
        a.brand_key,
        CASE 
            WHEN b.product_key IS NOT NULL THEN 'unmapped' 
            ELSE a.product_key 
        END AS product_key
    FROM mapping_macys_product_title a
    LEFT JOIN mapping_macys_product_title_top_products b 
        ON a.product_key = b.product_key
),
ulta_mapping AS (
    SELECT
        retailer_sku_key,
        primary_product_key AS product_key,
        ROW_NUMBER() OVER (PARTITION BY retailer_sku_key ORDER BY primary_product_key) AS rn
    FROM `{{params.transform_project}}.skulytics_NA.main_ulta_product_mapping_tbl`
    QUALIFY rn = 1
),
dim_product AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY product_key) AS rn
    FROM `{{params.dwh_project}}.COMMON_DMART.dim_product_tbl`
    WHERE region_id = 0
      AND brand_id IN (1, 2, 4, 5, 10, 27)
    QUALIFY rn = 1
),
dim_product_tbl_upc_dedup AS (
    SELECT 
        * EXCEPT (rn),
        ROW_NUMBER() OVER (PARTITION BY upc_code ORDER BY product_key) AS rn
    FROM dim_product
    QUALIFY rn = 1
),
macy_main_map_tbl AS (
    SELECT DISTINCT 
        title,
        skuId,
        brd_tbl.brand_key,
        ROW_NUMBER() OVER (PARTITION BY LOWER(title), brd_tbl.brand_key ORDER BY skuId DESC) AS rn
    FROM `{{params.ds_project}}.landing.macys_products` macys_stk_tbl
    LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd_tbl
        ON LOWER(
            CASE
                WHEN LOWER(macys_stk_tbl.brand) = 'pretty pink' THEN 'Pretty Pink'
                WHEN LOWER(macys_stk_tbl.brand) IN ('monster', 'monstermakeup') THEN 'Monster Makuep'
                ELSE macys_stk_tbl.brand
            END
        ) = LOWER(brd_tbl.brand_name)
    WHERE brd_tbl.brand_key IN (1, 2, 4, 5, 10, 27)
    QUALIFY rn = 1
),
macy_main_map_tbl_unmap_non_top_products AS (
    SELECT DISTINCT 
        macy_map_tbl.brand_key,
        macy_map_tbl.title,
        CASE 
            WHEN tp.product_key IS NOT NULL THEN 'unmapped' 
            ELSE pd_tbl.product_key 
        END AS product_key
    FROM macy_main_map_tbl macy_map_tbl
    LEFT JOIN dim_product_tbl_upc_dedup pd_tbl ON pd_tbl.UPC_CODE = (
        CASE
            WHEN LENGTH(SUBSTRING(macy_map_tbl.skuId, 1, LENGTH(macy_map_tbl.skuId) - 3)) = 11 
                THEN CONCAT('0', SUBSTRING(macy_map_tbl.skuId, 1, LENGTH(macy_map_tbl.skuId) - 3))
            WHEN LENGTH(SUBSTRING(macy_map_tbl.skuId, 1, LENGTH(macy_map_tbl.skuId) - 3)) = 12 
                THEN SUBSTRING(macy_map_tbl.skuId, 1, LENGTH(macy_map_tbl.skuId) - 3)
            WHEN LENGTH(macy_map_tbl.skuId) = 11 
                THEN CONCAT('0', CAST(macy_map_tbl.skuId AS STRING))
            ELSE macy_map_tbl.skuId
        END
    ) AND pd_tbl.region_id = 0
    LEFT JOIN mapping_macys_product_title_top_products tp 
        ON tp.product_key = pd_tbl.product_key
),
final_tbl AS (
    SELECT DISTINCT
        0 AS region_key,
        spon_prod.day AS date_key,
        brd_tbl.brand_key AS brand_key,
        rtl_tbl.retailer_key AS retailer_key,
        CASE 
            WHEN rtl_tbl.retailer_key = 1 THEN 
                COALESCE(macy_map_tbl_tp.product_key, macys_mapping_title.product_key, 'unmapped')
            WHEN rtl_tbl.retailer_key = 2 THEN 
                COALESCE(ulta_map.product_key, 'unmapped')
        END AS product_key,
        COALESCE(spon_prod.title, spon_prod.headline_1) AS retailer_product_name,
        spon_prod.day AS day,
        spon_prod.sku AS retailer_sku_key,
        spon_prod.ad_id,
        spon_prod.dimension_retailer AS sp_retailer_name,
        spon_prod.dimension_elc_brand AS retailer_brand_name,
        spon_prod.campaign_name AS campaign_name,
        spon_prod.channel AS sponsored_products_channel,
        spon_prod.ad AS ad,
        spon_prod.Profile_name AS profile_name,
        spon_prod.ad_group_name,
        spon_prod.imp AS impression,
        spon_prod.clicks AS clicks,
        spon_prod.rev AS sales_revenue,
        spon_prod.cost AS spend,
        spon_prod.conv AS units
    FROM `{{params.source_project}}.skulytics.sh_sponsored_products_tbl` spon_prod
    LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd_tbl
        ON LOWER(
            CASE
                WHEN LOWER(spon_prod.dimension_elc_brand) = 'prettypink' THEN 'Pretty Pink'
                WHEN LOWER(spon_prod.dimension_elc_brand) = 'monster' THEN 'Monster Makeup'
                ELSE spon_prod.dimension_elc_brand
            END
        ) = LOWER(brd_tbl.brand_name)
    LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_retailer_tbl` rtl_tbl
        ON LOWER(
            CASE
                WHEN LOWER(spon_prod.dimension_retailer) = 'macys' THEN "Macy's.com"
                WHEN LOWER(spon_prod.dimension_retailer) = 'ulta' THEN 'Ulta.com'
                ELSE spon_prod.dimension_retailer
            END
        ) = LOWER(rtl_tbl.retailer_name)
    -- Macy’s product mapping
    LEFT JOIN macy_main_map_tbl_unmap_non_top_products macy_map_tbl
        ON LOWER(macy_map_tbl.title) = LOWER(
            CASE
                WHEN REGEXP_CONTAINS(headline_1, r'^pretty pink ') THEN REGEXP_REPLACE(headline_1, r'^Pretty Pink ', '')
                WHEN REGEXP_CONTAINS(headline_1, r'^monster ') THEN REGEXP_REPLACE(headline_1, r'^Monster ', '')
                ELSE headline_1
            END
        ) AND macy_map_tbl.brand_key = brd_tbl.brand_key
    -- Ulta mapping
    LEFT JOIN ulta_mapping ulta_map
        ON CAST(spon_prod.sku AS STRING) = CAST(ulta_map.retailer_sku_key AS STRING)
        AND rtl_tbl.retailer_key = 2
    -- Macy’s product title mappings
    LEFT JOIN mapping_macys_product_title_top_products macy_map_tbl_tp
        ON LOWER(macy_map_tbl_tp.retailer_product_name) = LOWER(spon_prod.headline_1)
        AND macy_map_tbl_tp.brand_key = brd_tbl.brand_id
    LEFT JOIN unmap_macys_product_title_non_top macys_mapping_title
        ON LOWER(macys_mapping_title.retailer_product_name) = LOWER(spon_prod.headline_1)
        AND macys_mapping_title.brand_key = brd_tbl.brand_id
    WHERE brd_tbl.brand_key IN (1, 2, 4, 5, 10, 27)
      AND rtl_tbl.retailer_key IN (1, 2)
)
SELECT 
    CONCAT(
        CAST(date_key AS STRING), '#',
        CAST(retailer_key AS STRING), '#',
        CAST(COALESCE(product_key, '') AS STRING), '#',
        CAST(COALESCE(ad_id, 0) AS STRING), '#',
        CAST(COALESCE(retailer_product_name, '') AS STRING)
    ) AS sponsored_products_key,
    *,
    CURRENT_TIMESTAMP() AS record_created_date,
    CURRENT_TIMESTAMP() AS record_updated_date
FROM final_tbl;
