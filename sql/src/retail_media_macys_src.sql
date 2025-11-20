DECLARE VAR1 TIMESTAMP;

SET VAR1 = (
    SELECT IFNULL(MAX(upload_timestamp), CAST("1900-01-01 00:00:00" AS TIMESTAMP))
    FROM `{{params.source_project}}.skulytics.sh_macys_retail_media_tbl`
);

DELETE FROM `{{params.source_project}}.skulytics.sh_macys_retail_media_tbl` t
WHERE EXISTS (
    SELECT 1 
    FROM `{{params.landing_project}}.skulytics.sh_macys_retail_media_tbl` l
    WHERE 
        l.reload_required = 'True'
        AND (
            CASE
                WHEN REGEXP_CONTAINS(l.upload_timestamp, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') THEN SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', l.upload_timestamp)
                WHEN REGEXP_CONTAINS(l.upload_timestamp, r'^\d{14}$') THEN SAFE.PARSE_TIMESTAMP('%Y%m%d%H%M%S', l.upload_timestamp)
                ELSE NULL
            END > VAR1
        )
        AND t.month = l.month
        AND t.fiscal_year = l.fiscal_year
);

MERGE INTO `{{params.source_project}}.skulytics.sh_macys_retail_media_tbl` AS a
USING (
     WITH int_operation AS (
    SELECT 
        CAST(retailer AS STRING) AS retailer,
        CAST(digital_media_type AS STRING) AS digital_media_type,
        CAST(campaign_name AS STRING) AS campaign_name,
        CAST(brand AS STRING) AS brand,
        CAST(attribution AS STRING) AS attribution,
        CAST(placement_type AS STRING) AS placement_type,
        CAST(line_item AS STRING) AS line_item,
        CAST(spend_bucket AS STRING) AS spend_bucket,
        CAST(tactic AS STRING) AS tactic,
        CAST(month AS STRING) AS month,
        CAST(fiscal_year AS STRING) AS fiscal_year,
        CAST(quarter AS STRING) AS quarter,
        SAFE_CAST(REGEXP_REPLACE(spend, r'[$,]', '') AS FLOAT64) AS spend,
        -- ROUND impressions to nearest integer, then cast to INT64 --
        SAFE_CAST(ROUND(SAFE_CAST(REGEXP_REPLACE(impressions, r'[,]', '') AS FLOAT64)) AS INT64) AS impressions,
        SAFE_CAST(REGEXP_REPLACE(clicks, r'[,]', '') AS INT64) AS clicks,
        SAFE_CAST(REGEXP_REPLACE(ctr, r'[%]', '') AS FLOAT64) / 100 AS ctr,
        SAFE_CAST(REGEXP_REPLACE(cpm, r'[$,]', '') AS FLOAT64) AS cpm,
        SAFE_CAST(REGEXP_REPLACE(cpc, r'[$,]', '') AS FLOAT64) AS cpc,
        SAFE_CAST(REGEXP_REPLACE(aov, r'[$,]', '') AS FLOAT64) AS aov,
        SAFE_CAST(REGEXP_REPLACE(cvr, r'[%]', '') AS FLOAT64) / 100 AS cvr,
        SAFE_CAST(REGEXP_REPLACE(online_sales_last_click, r'[$,]', '') AS FLOAT64) AS online_sales_last_click,
        SAFE_CAST(REGEXP_REPLACE(online_roas_last_click, r'[$,]', '') AS FLOAT64) AS online_roas_last_click,
        SAFE_CAST(REGEXP_REPLACE(new_buyers, r'[,]', '') AS INT64) AS new_buyers,
        SAFE_CAST(REGEXP_REPLACE(total_buyers, r'[,]', '') AS INT64) AS total_buyers,
        SAFE_CAST(REGEXP_REPLACE(new_buyer_percentage, r'[%]', '') AS FLOAT64) / 100 AS new_buyer_percentage,
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
    FROM `{{params.landing_project}}.skulytics.sh_macys_retail_media_tbl`
        WHERE
            CASE
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') THEN SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', upload_timestamp)
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{14}$') THEN SAFE.PARSE_TIMESTAMP('%Y%m%d%H%M%S', upload_timestamp)
                ELSE NULL
            END > VAR1
    QUALIFY priority_rank = 1
)
, finding_distinct AS (
    SELECT 
        DISTINCT 
            CONCAT(
                COALESCE(retailer, ''), '#',
                COALESCE(digital_media_type, ''), '#',
                COALESCE(campaign_name, ''), '#',
                COALESCE(brand, ''), '#',
                COALESCE(attribution, ''), '#',
                COALESCE(placement_type, ''), '#',
                COALESCE(spend_bucket, ''), '#',
                COALESCE(line_item, ''), '#',
                COALESCE(tactic, ''), '#',
                COALESCE(month, ''), '#',
                COALESCE(fiscal_year, ''),'#',
                COALESCE(quarter, '')
            ) AS retail_media_macys_key,
            retailer,
            digital_media_type,
            campaign_name,
            brand,
            attribution,
            placement_type,
            spend_bucket,
            line_item,
            tactic,
            month,
            fiscal_year,
            quarter,
            spend,
            impressions,
            clicks,
            ctr,
            cpm,
            cpc,
            aov,
            cvr,
            online_sales_last_click,
            online_roas_last_click,
            new_buyers,
            total_buyers,
            new_buyer_percentage,
            file_date
    FROM int_operation
)
SELECT 
    retail_media_macys_key,
    retailer,
    digital_media_type,
    campaign_name,
    brand,
    attribution,
    placement_type,
    spend_bucket,
    line_item,
    tactic,
    month,
    fiscal_year,
    quarter,
    file_date,
    SUM(spend) AS spend,
    SUM(impressions) AS impressions,
    SUM(clicks) AS clicks,
    AVG(ctr) AS ctr,
    AVG(cpm) AS cpm,
    AVG(cpc) AS cpc,
    AVG(aov) AS aov,
    AVG(cvr) AS cvr,
    SUM(online_sales_last_click) AS online_sales_last_click,
    AVG(online_roas_last_click) AS online_roas_last_click,
    SUM(new_buyers) AS new_buyers,
    SUM(total_buyers) AS total_buyers,
    AVG(new_buyer_percentage) AS new_buyer_percentage,
    COUNT(campaign_name) as campaign_repeat_count
FROM finding_distinct
GROUP BY 
    retail_media_macys_key, 
    retailer, 
    digital_media_type, 
    campaign_name, 
    brand, 
    attribution, 
    placement_type, 
    spend_bucket, 
    line_item, 
    tactic, 
    month, 
    fiscal_year,
    quarter,
    file_date
) b
ON a.retail_media_macys_key = b.retail_media_macys_key  
WHEN MATCHED THEN
    UPDATE SET
        a.digital_media_type = b.digital_media_type,
        a.attribution = b.attribution,
        a.spend_bucket = b.spend_bucket,
        a.tactic = b.tactic,
        a.quarter = b.quarter,
        a.spend = b.spend,
        a.impressions = b.impressions,
        a.clicks = b.clicks,
        a.ctr = b.ctr,
        a.cpm = b.cpm,
        a.cpc = b.cpc,
        a.aov = b.aov,
        a.cvr = b.cvr,
        a.online_sales_last_click = b.online_sales_last_click,
        a.online_roas_last_click = b.online_roas_last_click,
        a.new_buyers = b.new_buyers,
        a.total_buyers = b.total_buyers,
        a.new_buyer_percentage = b.new_buyer_percentage,
        a.campaign_repeat_count = b.campaign_repeat_count,
        a.file_date = b.file_date,
        a.upload_timestamp = CURRENT_TIMESTAMP(),
        a.updated_date = CURRENT_TIMESTAMP()
WHEN NOT MATCHED BY TARGET  THEN
    INSERT (
        retailer,
        digital_media_type,
        campaign_name,
        brand,
        attribution,
        placement_type,
        line_item,
        spend_bucket,
        tactic,
        month,
        fiscal_year,
        quarter,
        spend,
        impressions,
        clicks,
        ctr,
        cpm,
        cpc,
        aov,
        cvr,
        online_sales_last_click,
        online_roas_last_click,
        new_buyers,
        total_buyers,
        new_buyer_percentage,
        campaign_repeat_count,
        file_date,
        upload_timestamp,
        retail_media_macys_key,  
        inserted_date
    )
    VALUES (
        b.retailer,
        b.digital_media_type,
        b.campaign_name,
        b.brand,
        b.attribution,
        b.placement_type,
        b.line_item,
        b.spend_bucket,
        b.tactic,
        b.month,
        b.fiscal_year,
        b.quarter,
        b.spend,
        b.impressions,
        b.clicks,
        b.ctr,
        b.cpm,
        b.cpc,
        b.aov,
        b.cvr,
        b.online_sales_last_click,
        b.online_roas_last_click,
        b.new_buyers,
        b.total_buyers,
        b.new_buyer_percentage,
        b.campaign_repeat_count,
        b.file_date,
        CURRENT_TIMESTAMP(),
        b.retail_media_macys_key,  
        CURRENT_TIMESTAMP()
    );