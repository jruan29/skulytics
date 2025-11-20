CREATE OR REPLACE TABLE `{{params.transform_project}}.skulytics_NA.stg_conversion_pptraffic_tbl` AS
with retailer_months as (
 SELECT
    row_month_start_date AS date_key,
    na_month_start_date,
    na_month_end_date,
    count(na_month_start_date) AS na_month_start_date_count,
    count(na_month_end_date) AS na_month_end_date_count
  FROM `{{params.dwh_project}}.COMMON_DMART.dim_date_tbl`
  WHERE row_month_start_date >= '2020-01-01'
  GROUP BY 1,2,3
),
retail_months_date_key_mapping AS (
  select date_key,na_month_start_date,na_month_end_date,row_number() over(partition by date_key order by na_month_start_date_count desc )  as rn from retailer_months
  qualify rn = 1
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
        ON CASE 
               WHEN LENGTH(CAST(pr.UPC_CODE AS STRING)) = 11 
                    THEN CONCAT('0', CAST(pr.UPC_CODE AS STRING)) 
               ELSE CAST(pr.UPC_CODE AS STRING) 
           END = b.UPC_CODE
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
        COALESCE(b.product_key, a.product_key, 'unmapped') AS product_key
    FROM modified_mapping_macys_product_key a
    LEFT JOIN top_macys_mapping_tbl b
        ON CAST(a.macys_product_key AS STRING) = CAST(b.retailer_product_key AS STRING)
        AND a.brand_key = b.brand_key
),
final_tbl AS (
    SELECT DISTINCT
        0 AS region_key,
        conv_ppt.file_date AS file_date,
        dim_date.na_month_start_date AS date_key,
        brd_tbl.brand_id AS brand_key,
        1 AS retailer_key,
        COALESCE(rtl_prd_tbl.product_key, 'unmapped') AS product_key,
        conv_ppt.product_id AS retailer_product_key,
        conv_ppt.title AS retailer_product_name,
        conv_ppt.revenue_ty,
        conv_ppt.revenue_ly,
        conv_ppt.units_ty AS units_ty,
        conv_ppt.units_ly AS units_ly,
        conv_ppt.unit_conv_ty AS unit_conversion_ty,
        conv_ppt.unit_conv_ly AS unit_conversion_ly,
        conv_ppt.cvr_ty AS traffic_conversion_rate_ty,
        conv_ppt.cvr_ly AS traffic_conversion_rate_ly
    FROM `{{params.source_project}}.skulytics.sh_conversion_pptraffic_tbl` AS conv_ppt
    LEFT JOIN retail_months_date_key_mapping dim_date
        ON dim_date.date_key = conv_ppt.file_date
    LEFT JOIN `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd_tbl
        ON LOWER(
            CASE 
                WHEN LOWER(conv_ppt.brand) = 'prettypink' THEN 'Pretty Pink'
                WHEN LOWER(conv_ppt.brand) = 'glitter glow' THEN 'Glitter Glow'
                WHEN LOWER(conv_ppt.brand) = 'monster makeup' THEN 'Monster Makeup'
                ELSE conv_ppt.brand
            END
        ) = LOWER(brd_tbl.brand_name)
    LEFT JOIN final_macys_mapping_tbl rtl_prd_tbl
        ON rtl_prd_tbl.macys_product_key = CAST(conv_ppt.product_id AS STRING)
        AND rtl_prd_tbl.brand_key = brd_tbl.brand_key
    WHERE brd_tbl.brand_id IN (1, 2, 4, 5, 10, 27)
      AND conv_ppt.title IS NOT NULL
)
SELECT 
    CONCAT(
        COALESCE(date_key, '1900-01-01'), '#',
        retailer_key, '#',
        CAST(COALESCE(product_key, '') AS STRING), '#',
        CAST(COALESCE(retailer_product_name, '') AS STRING), '#',
        retailer_product_key
    ) AS conversion_pptraffic_key,
    *,
    CURRENT_TIMESTAMP() AS record_created_date,
    CURRENT_TIMESTAMP() AS record_updated_date
FROM final_tbl;
