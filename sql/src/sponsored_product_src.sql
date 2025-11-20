DECLARE VAR1 TIMESTAMP;

SET VAR1 = (
    SELECT IFNULL(MAX(upload_timestamp), CAST('1900-01-01 00:00:00' AS TIMESTAMP))
    FROM `{{params.source_project}}.skulytics.sh_sponsored_products_tbl`
);

MERGE INTO `{{params.source_project}}.skulytics.sh_sponsored_products_tbl` AS a
USING (
    WITH int_operation AS (
        SELECT 
            CAST(channel AS STRING) AS channel,
            CAST(ad AS STRING) AS ad,
            CAST(profile_name AS STRING) AS profile_name,
            CAST(campaign_name AS STRING) AS campaign_name,
            CAST(ad_group_name AS STRING) AS ad_group_name,
            CAST(dimension_elc_brand AS STRING) AS dimension_elc_brand,
            CAST(dimension_retailer AS STRING) AS dimension_retailer,
            CAST(CAST(ad_id AS FLOAT64) AS INT64) AS ad_id,
            CAST(headline_1 AS STRING) AS headline_1,
            CAST(title AS STRING) AS title,
            CAST(CAST(sku AS FLOAT64) AS INT64) AS sku,
            -- Using SAFE_CAST to handle potential conversion errors gracefully (returns NULL instead of error)
            -- Using REGEXP_REPLACE to remove commas and dollar signs from numeric fields before casting
            -- This is necessary because the source data may contain formatted numbers like "$1,000" or "1,000"
            SAFE_CAST(REGEXP_REPLACE(imp, r'[$,]', '') AS INT64) AS imp, 
            SAFE_CAST(REGEXP_REPLACE(clicks, r'[$,]', '') AS INT64) AS clicks, 
            SAFE_CAST(REGEXP_REPLACE(rev, r'[$,]', '') AS FLOAT64) AS rev, 
            SAFE_CAST(REGEXP_REPLACE(cost, r'[$,]', '') AS FLOAT64) AS cost,
            SAFE_CAST(REGEXP_REPLACE(conv, r'[$,]', '') AS FLOAT64) AS conv,
            CASE
                --Handling Multiple date formats
                WHEN REGEXP_CONTAINS(day, r'^\d{2}-\d{2}-\d{4}$') THEN SAFE.PARSE_DATE('%d-%m-%Y', day)  -- For DD-MM-YYYY format
                WHEN REGEXP_CONTAINS(day, r'^\d{4}-\d{2}-\d{2}$') THEN SAFE.PARSE_DATE('%Y-%m-%d', day)  --- For YYYY-MM-DD format
                WHEN REGEXP_CONTAINS(day, r'^\d{1,2}/\d{1,2}/\d{4}$') THEN SAFE.PARSE_DATE('%m/%d/%Y', day)  -- For M/D/YYYY or MM/DD/YYYY
                WHEN REGEXP_CONTAINS(day, r'^\d{2}-[A-Za-z]{3}-\d{4}$') THEN  SAFE.PARSE_DATE('%d-%b-%Y', day)  -- For eg 25-Dec-2023 
                WHEN REGEXP_CONTAINS(day, r'^[A-Za-z]{3} \d{2}, \d{4}$') THEN SAFE.PARSE_DATE('%b %d, %Y', day) -- For eg Dec 25, 2023
                WHEN REGEXP_CONTAINS(day, r'^\d{1,2}/\d{1,2}/\d{2}$') THEN SAFE.PARSE_DATE('%m/%d/%y', day) ----mm/dd/yy
                ELSE NULL  
            END as day,
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
        FROM `{{params.landing_project}}.skulytics.sh_sponsored_products_tbl`
        WHERE 
            CASE
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') THEN SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', upload_timestamp)
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{14}$') THEN SAFE.PARSE_TIMESTAMP('%Y%m%d%H%M%S', upload_timestamp)
                ELSE NULL 
            END > VAR1
    )
    SELECT 
        CONCAT(
            COALESCE(CAST(sku AS STRING), ''), '#',
            COALESCE(CAST(ad_id AS STRING), ''), '#',
            COALESCE(CAST(dimension_elc_brand AS STRING), ''), '#',
            COALESCE(headline_1, ''), '#',
            COALESCE(title, ''), '#',
            COALESCE(cast(day as STRING), '')
        ) AS sponsored_products_key,
        channel,
        ad,
        profile_name,
        campaign_name,
        ad_group_name,
        dimension_elc_brand,
        dimension_retailer,
        ad_id,
        headline_1,
        title,
        sku,
        imp,
        clicks,
        rev,
        cost,
        conv,
        day,
        upload_timestamp,
        file_date,
        ROW_NUMBER() OVER (PARTITION BY sku, ad_id,day,dimension_elc_brand,headline_1,title ORDER BY file_date DESC,upload_timestamp DESC) AS rn
    FROM int_operation
) b
ON a.sponsored_products_key = b.sponsored_products_key  
WHEN MATCHED AND b.rn = 1 THEN
    UPDATE SET
        a.channel = b.channel,
        a.ad = b.ad,
        a.profile_name = b.profile_name,
        a.campaign_name = b.campaign_name,
        a.ad_group_name = b.ad_group_name,
        a.dimension_elc_brand = b.dimension_elc_brand,
        a.dimension_retailer = b.dimension_retailer,
        a.ad_id = b.ad_id,
        a.headline_1 = b.headline_1,
        a.title = b.title,
        a.sku = b.sku,
        a.imp = b.imp,
        a.clicks = b.clicks,
        a.rev = b.rev,
        a.cost = b.cost,
        a.conv = b.conv,
        a.day = b.day,
        a.file_date = b.file_date,
        a.upload_timestamp = b.upload_timestamp,
        a.updated_date = CURRENT_TIMESTAMP()
WHEN NOT MATCHED BY TARGET AND b.rn = 1 THEN
    INSERT (
        channel,
        ad,
        profile_name,
        campaign_name,
        ad_group_name,
        dimension_elc_brand,
        dimension_retailer,
        ad_id,
        headline_1,
        title,
        sku,
        imp,
        clicks,
        rev,
        cost,
        conv,
        day,
        file_date,
        upload_timestamp,
        sponsored_products_key, 
        inserted_date
    )
    VALUES (
        b.channel,
        b.ad,
        b.profile_name,
        b.campaign_name,
        b.ad_group_name,
        b.dimension_elc_brand,
        b.dimension_retailer,
        b.ad_id,
        b.headline_1,
        b.title,
        b.sku,
        b.imp,
        b.clicks,
        b.rev,
        b.cost,
        b.conv,
        b.day,
        b.file_date,
        b.upload_timestamp,
        b.sponsored_products_key,  
        CURRENT_TIMESTAMP()
);