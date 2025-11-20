DECLARE VAR1 TIMESTAMP;

SET VAR1 = (
    SELECT IFNULL(MAX(upload_timestamp), CAST("1900-01-01 00:00:00" AS TIMESTAMP))
    FROM `{{params.source_project}}.skulytics.sh_conversion_pptraffic_tbl`
);

MERGE INTO `{{params.source_project}}.skulytics.sh_conversion_pptraffic_tbl` AS a
USING (
    WITH int_operation AS (
        SELECT 
            CAST(brand AS STRING) AS brand,
            CASE
            WHEN REGEXP_INSTR(web_id_product_description, ':') > 0
            THEN SAFE_CAST(SUBSTRING(web_id_product_description, 1, REGEXP_INSTR(web_id_product_description, ':')-1) AS INT64)
            ELSE NULL
        END AS product_id, 
        CASE
            WHEN REGEXP_INSTR(web_id_product_description, ':') > 0
            THEN SAFE_CAST(SUBSTRING(web_id_product_description, REGEXP_INSTR(web_id_product_description, ':') + 1) AS STRING)
            ELSE NULL
        END AS title,  
            SAFE_CAST(REGEXP_REPLACE(revenue_ty, r'[$,]', '') AS FLOAT64) AS revenue_ty,  
            SAFE_CAST(REGEXP_REPLACE(revenue_ly, r'[$,]', '') AS FLOAT64) AS revenue_ly,  
            SAFE_CAST(REGEXP_REPLACE(percent_chg, r'[%]', '') AS FLOAT64) AS percent_chg,  
            SAFE_CAST(REGEXP_REPLACE(visits_percent_chg, r'[%]', '') AS FLOAT64) AS visits_percent_chg,  
            SAFE_CAST(REGEXP_REPLACE(views_percent_chg, r'[%]', '') AS FLOAT64) AS views_percent_chg,  
            SAFE_CAST(REGEXP_REPLACE(units_ty, r'[$,]', '') AS FLOAT64) AS units_ty,  
            SAFE_CAST(REGEXP_REPLACE(units_ly, r'[$,]', '') AS FLOAT64) AS units_ly,  
            SAFE_CAST(REGEXP_REPLACE(units_percent_chg, r'[%]', '') AS FLOAT64) AS units_percent_chg,  
            SAFE_CAST(REGEXP_REPLACE(unit_conv_ty, r'[%]', '') AS FLOAT64) AS unit_conv_ty,  
            SAFE_CAST(REGEXP_REPLACE(unit_conv_ly, r'[%]', '') AS FLOAT64) AS unit_conv_ly,  
            SAFE_CAST(REGEXP_REPLACE(unit_conv_percent_chg, r'[%]', '') AS FLOAT64) AS unit_conv_percent_chg,  
            SAFE_CAST(REGEXP_REPLACE(cvr_ty, r'[%]', '') AS FLOAT64) AS cvr_ty,  
            SAFE_CAST(REGEXP_REPLACE(cvr_ly, r'[%]', '') AS FLOAT64) AS cvr_ly,  
            SAFE_CAST(REGEXP_REPLACE(cvr_percent_chg, r'[%]', '') AS FLOAT64) AS cvr_percent_chg,  
            CASE
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') THEN SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', upload_timestamp)
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{14}$') THEN SAFE.PARSE_TIMESTAMP('%Y%m%d%H%M%S', upload_timestamp)
                ELSE NULL
            END AS upload_timestamp,
            CASE
                WHEN REGEXP_CONTAINS(CAST(file_date AS STRING), r'^\d{4}-\d{2}-\d{2}$') THEN SAFE.PARSE_DATE('%Y-%m-%d', CAST(file_date AS STRING))
                WHEN REGEXP_CONTAINS(CAST(file_date AS STRING), r'^\d{8}$') THEN SAFE.PARSE_DATE('%Y%m%d', CAST(file_date AS STRING))
                ELSE NULL 
            END AS file_date
        FROM `{{params.landing_project}}.skulytics.sh_conversion_pptraffic_tbl`
        WHERE
            CASE
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') THEN SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', upload_timestamp)
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{14}$') THEN SAFE.PARSE_TIMESTAMP('%Y%m%d%H%M%S', upload_timestamp)
                ELSE NULL  
            END > VAR1
    )
    SELECT 
        CONCAT(
            COALESCE(CAST(product_id AS STRING), ''), '#',
            COALESCE(title, ''), '#',
            COALESCE(brand, ''), '#',
            COALESCE(cast(file_date as string), '')
        ) AS conversion_pptraffic_key,
        brand,
        product_id,
        title,
        revenue_ty,
        revenue_ly,
        percent_chg,
        visits_percent_chg,
        views_percent_chg,
        units_ty,
        units_ly,
        units_percent_chg,
        unit_conv_ty,
        unit_conv_ly,
        unit_conv_percent_chg,
        cvr_ty,
        cvr_ly,
        cvr_percent_chg,
        upload_timestamp,
        file_date,
        ROW_NUMBER() OVER (PARTITION BY product_id,title,brand,file_date ORDER BY file_date DESC,upload_timestamp DESC) AS rn
    FROM int_operation
) b
ON a.conversion_pptraffic_key = b.conversion_pptraffic_key  
WHEN MATCHED AND b.rn = 1 THEN
    UPDATE SET
        a.brand = b.brand,
        a.product_id = b.product_id,
        a.title = b.title,
        a.revenue_ty = b.revenue_ty,  
        a.revenue_ly = b.revenue_ly,  
        a.percent_chg = b.percent_chg,  
        a.visits_percent_chg = b.visits_percent_chg,  
        a.views_percent_chg = b.views_percent_chg,  
        a.units_ty = b.units_ty,  
        a.units_ly = b.units_ly,  
        a.units_percent_chg = b.units_percent_chg,  
        a.unit_conv_ty = b.unit_conv_ty,  
        a.unit_conv_ly = b.unit_conv_ly,  
        a.unit_conv_percent_chg = b.unit_conv_percent_chg,  
        a.cvr_ty = b.cvr_ty,  
        a.cvr_ly = b.cvr_ly,  
        a.cvr_percent_chg = b.cvr_percent_chg,  
        a.upload_timestamp = b.upload_timestamp,
        a.file_date = b.file_date,
        a.updated_date = CURRENT_TIMESTAMP()
WHEN NOT MATCHED BY TARGET AND b.rn = 1 THEN
    INSERT (
        brand,
        product_id,
        title,
        revenue_ty,
        revenue_ly,
        percent_chg,
        visits_percent_chg,
        views_percent_chg,
        units_ty,
        units_ly,
        units_percent_chg,
        unit_conv_ty,
        unit_conv_ly,
        unit_conv_percent_chg,
        cvr_ty,
        cvr_ly,
        cvr_percent_chg,
        upload_timestamp,
        file_date,
        conversion_pptraffic_key,  
        inserted_date
    )
    VALUES (
        b.brand,
        b.product_id,
        b.title,
        b.revenue_ty,  
        b.revenue_ly,  
        b.percent_chg, 
        b.visits_percent_chg,  
        b.views_percent_chg,  
        b.units_ty,  
        b.units_ly,  
        b.units_percent_chg, 
        b.unit_conv_ty,  
        b.unit_conv_ly,  
        b.unit_conv_percent_chg,  
        b.cvr_ty,  
        b.cvr_ly,  
        b.cvr_percent_chg,  
        b.upload_timestamp,
        b.file_date,
        b.conversion_pptraffic_key,  
        CURRENT_TIMESTAMP()
    );