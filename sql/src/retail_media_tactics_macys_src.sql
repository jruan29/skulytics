DECLARE VAR1 TIMESTAMP;

SET VAR1 = (
    SELECT IFNULL(MAX(upload_timestamp), CAST("1900-01-01 00:00:00" AS TIMESTAMP))
    FROM `{{params.source_project}}.skulytics.sh_macys_tactics_tbl`
);

DELETE FROM `{{params.source_project}}.skulytics.sh_macys_tactics_tbl` t
WHERE EXISTS (
    SELECT 1 
    FROM `{{params.landing_project}}.skulytics.sh_macys_tactics_tbl` l
    WHERE 
        l.reload_required = 'True'
        AND (
            CASE
                WHEN REGEXP_CONTAINS(l.upload_timestamp, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') THEN SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', l.upload_timestamp)
                WHEN REGEXP_CONTAINS(l.upload_timestamp, r'^\d{14}$') THEN SAFE.PARSE_TIMESTAMP('%Y%m%d%H%M%S', l.upload_timestamp)
                ELSE NULL
            END > VAR1
        )
        AND CAST(t.file_date AS STRING) = CAST(l.file_date AS STRING)
);


MERGE INTO `{{params.source_project}}.skulytics.sh_macys_tactics_tbl` AS a
USING (
    WITH int_operation AS (
        SELECT 
            CAST(brand AS STRING) AS brand,
            CAST(tactic AS STRING) AS tactic,
            SAFE_CAST(REGEXP_REPLACE(revenue_percentage_ttl_ty, r'[%]', '') AS FLOAT64) / 100 AS revenue_percentage_ttl_ty,
            SAFE_CAST(REGEXP_REPLACE(revenue_percentage_change_to_ly, r'[%]', '') AS FLOAT64) / 100 AS revenue_percentage_change_to_ly,
            SAFE_CAST(REGEXP_REPLACE(traffic_percentage_ttl_ty, r'[%]', '') AS FLOAT64) / 100 AS traffic_percentage_ttl_ty,
            SAFE_CAST(REGEXP_REPLACE(traffic_percentage_change_to_ly, r'[%]', '') AS FLOAT64) / 100 AS traffic_percentage_change_to_ly,
            SAFE_CAST(REGEXP_REPLACE(unit_conv_ty, r'[%]', '') AS FLOAT64) / 100 AS unit_conv_ty,
            SAFE_CAST(REGEXP_REPLACE(unit_conv_ly, r'[%]', '') AS FLOAT64) / 100 AS unit_conv_ly,
            SAFE_CAST(REGEXP_REPLACE(unit_conv_percentage_change_to_ly, r'[%]', '') AS FLOAT64) / 100 AS unit_conv_percentage_change_to_ly,
            SAFE_CAST(REGEXP_REPLACE(aov_ty, r'[$,]', '') AS FLOAT64) AS aov_ty,
            SAFE_CAST(REGEXP_REPLACE(aov_ly, r'[$,]', '') AS FLOAT64) AS aov_ly,
            CAST(REGEXP_REPLACE(aov_percentage_change_to_ly, r'[%]', '') AS STRING) AS aov_percentage_change_to_ly,
            CASE
                WHEN REGEXP_CONTAINS(CAST(file_date AS STRING), r'^\d{4}-\d{2}-\d{2}$') THEN SAFE.PARSE_DATE('%Y-%m-%d', CAST(file_date AS STRING))
                WHEN REGEXP_CONTAINS(CAST(file_date AS STRING), r'^\d{8}$') THEN SAFE.PARSE_DATE('%Y%m%d', CAST(file_date AS STRING))
                ELSE NULL
            END AS file_date,
            CASE
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') THEN SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', upload_timestamp)
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{14}$') THEN SAFE.PARSE_TIMESTAMP('%Y%m%d%H%M%S', upload_timestamp)
                ELSE NULL
            END AS upload_timestamp,
            DENSE_RANK() OVER(PARTITION BY file_date ORDER BY CASE WHEN reload_required = 'True' THEN 1 ELSE 2 END,
                TIMESTAMP_TRUNC(PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', upload_timestamp),MINUTE) DESC) AS priority_rank
        FROM `{{params.landing_project}}.skulytics.sh_macys_tactics_tbl`
        WHERE
            CASE
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') THEN SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', upload_timestamp)
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{14}$') THEN SAFE.PARSE_TIMESTAMP('%Y%m%d%H%M%S', upload_timestamp)
                ELSE NULL
            END > VAR1
        QUALIFY priority_rank = 1
    )
    SELECT
        CONCAT(
            COALESCE(brand, ''), '#',
            COALESCE(tactic, ''), '#',
            COALESCE(cast(file_date as string), '')
        ) AS retail_media_tactics_macys_key,   
        *,
        ROW_NUMBER() OVER (PARTITION BY brand, tactic, file_date ORDER BY file_date DESC,upload_timestamp DESC) AS rn
    FROM int_operation
) b
ON a.retail_media_tactics_macys_key = b.retail_media_tactics_macys_key  
WHEN MATCHED AND b.rn = 1 THEN
    UPDATE SET
        a.revenue_percentage_ttl_ty = b.revenue_percentage_ttl_ty,
        a.revenue_percentage_change_to_ly = b.revenue_percentage_change_to_ly,
        a.traffic_percentage_ttl_ty = b.traffic_percentage_ttl_ty,
        a.traffic_percentage_change_to_ly = b.traffic_percentage_change_to_ly,
        a.unit_conv_ty = b.unit_conv_ty,
        a.unit_conv_ly = b.unit_conv_ly,
        a.unit_conv_percentage_change_to_ly = b.unit_conv_percentage_change_to_ly,
        a.aov_ty = b.aov_ty,
        a.aov_ly = b.aov_ly,
        a.aov_percentage_change_to_ly = b.aov_percentage_change_to_ly,
        a.upload_timestamp = b.upload_timestamp,
        a.updated_date = CURRENT_TIMESTAMP()
WHEN NOT MATCHED BY TARGET AND b.rn = 1 THEN
    INSERT (
        brand,
        tactic,
        revenue_percentage_ttl_ty,
        revenue_percentage_change_to_ly,
        traffic_percentage_ttl_ty,
        traffic_percentage_change_to_ly,
        unit_conv_ty,
        unit_conv_ly,
        unit_conv_percentage_change_to_ly,
        aov_ty,
        aov_ly,
        aov_percentage_change_to_ly,
        file_date,
        upload_timestamp,
        retail_media_tactics_macys_key,  
        inserted_date
    )
    VALUES (
        b.brand,
        b.tactic,
        b.revenue_percentage_ttl_ty,
        b.revenue_percentage_change_to_ly,
        b.traffic_percentage_ttl_ty,
        b.traffic_percentage_change_to_ly,
        b.unit_conv_ty,
        b.unit_conv_ly,
        b.unit_conv_percentage_change_to_ly,
        b.aov_ty,
        b.aov_ly,
        b.aov_percentage_change_to_ly,
        b.file_date,
        b.upload_timestamp,
        b.retail_media_tactics_macys_key,  
        CURRENT_TIMESTAMP()
    );