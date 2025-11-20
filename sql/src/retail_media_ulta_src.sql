DECLARE VAR1 TIMESTAMP;

SET VAR1 = (
    SELECT IFNULL(MAX(upload_timestamp), CAST("1900-01-01 00:00:00" AS TIMESTAMP))
    FROM `{{params.source_project}}.skulytics.sh_ulta_retail_media_tbl`
);

DELETE FROM `{{params.source_project}}.skulytics.sh_ulta_retail_media_tbl` t
WHERE EXISTS (
    SELECT 1 
    FROM `{{params.landing_project}}.skulytics.sh_ulta_retail_media_tbl` l
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

MERGE INTO `{{params.source_project}}.skulytics.sh_ulta_retail_media_tbl` AS a
USING (
    -- we are getting multpile values like imperssions,clicks etc.. for same campaign, so we are adding them
    WITH int_operation AS (
    SELECT 
        CAST(elc_brand AS STRING) AS elc_brand,
        CAST(single_vs_multi_branded AS STRING) AS single_vs_multi_branded,
        CAST(fiscal_year AS STRING) AS fiscal_year,
        CAST(quarter AS STRING) AS quarter,
        CAST(`1h_or_2h` AS STRING) AS `1h_or_2h`,
        CAST(onsite_v_offsite AS STRING) AS onsite_v_offsite,
        CAST(digital_media_type AS STRING) AS digital_media_type,
        CAST(spend_bucket AS STRING) AS spend_bucket,
        CAST(campaign_name AS STRING) AS campaign_name,
        CAST(month AS STRING) AS month,
        SAFE.PARSE_DATE('%Y-%m-%d', CAST(campaign_start_date AS STRING)) AS campaign_start_date,
        SAFE.PARSE_DATE('%Y-%m-%d', CAST(campaign_end_date AS STRING)) AS campaign_end_date,
        SAFE_CAST(days_in_month AS INT64) AS days_in_month,
        SAFE_CAST(total_days_in_campaign AS INT64) AS total_days_in_campaign,
        SAFE_CAST(campaign_window_percentage AS FLOAT64) AS campaign_window_percentage,
        CAST(featured_product_subbrand_or_promo AS STRING) AS featured_product_subbrand_or_promo,
        SAFE_CAST(REGEXP_REPLACE(elc_investment_actual, r'[$,]', '') AS FLOAT64) AS elc_investment_actual,
        CAST(retailer_co_investment AS STRING) AS retailer_co_investment,
        CAST(funnel_position AS STRING) AS funnel_position,
        CAST(digital_media_type_select_from_list AS STRING) AS digital_media_type_select_from_list,
        CAST(targeting_segments AS STRING) AS targeting_segments,
        SAFE_CAST(REGEXP_REPLACE(impressions, r'[$,]', '') AS INT64) AS impressions,
        SAFE_CAST(
            CASE 
                WHEN total_uniques = 'N/A' THEN NULL 
                ELSE REGEXP_REPLACE(total_uniques, r'[$,]', '') 
            END AS INT64
        ) AS total_uniques,
        SAFE_CAST(REGEXP_REPLACE(uniques, r'[$,]', '') AS INT64) AS uniques,
        SAFE_CAST(REGEXP_REPLACE(clicks, r'[$,]', '') AS INT64) AS clicks,
        SAFE_CAST(REGEXP_REPLACE(ctr, r'[%]', '') AS FLOAT64)  AS ctr,
        SAFE_CAST(
            CASE 
                WHEN total_video_views = 'N/A' THEN NULL 
                ELSE REGEXP_REPLACE(total_video_views, r'[$,]', '') 
            END AS INT64
        ) AS total_video_views,
        SAFE_CAST(REGEXP_REPLACE(video_views, r'[$,]', '') AS INT64) AS video_views,
        SAFE_CAST(video_completions AS FLOAT64) AS video_completions,
        SAFE_CAST(REGEXP_REPLACE(video_completion_rate, r'[%]', '') AS FLOAT64)  AS video_completion_rate,
        SAFE_CAST(REGEXP_REPLACE(elc_cpm, r'[$,]', '') AS FLOAT64) AS elc_cpm,
        SAFE_CAST(REGEXP_REPLACE(elc_cpc, r'[$,]', '') AS FLOAT64) AS elc_cpc,
        CAST(sales_reporting_basket_level_or_brand AS STRING) AS sales_reporting_basket_level_or_brand,
        SAFE_CAST(REGEXP_REPLACE(omni_attrib_sales, r'[$,]', '') AS FLOAT64) AS omni_attrib_sales,
        SAFE_CAST(REGEXP_REPLACE(store_attrib_sales, r'[$,]', '') AS FLOAT64) AS store_attrib_sales,
        SAFE_CAST(REGEXP_REPLACE(online_attrib_sales, r'[$,]', '') AS FLOAT64) AS online_attrib_sales,
        SAFE_CAST(REGEXP_REPLACE(omni_roas, r'[$,]', '') AS FLOAT64) AS omni_roas,
        SAFE_CAST(REGEXP_REPLACE(store_roas, r'[$,]', '') AS FLOAT64) AS store_roas,
        SAFE_CAST(REGEXP_REPLACE(online_roas, r'[$,]', '') AS FLOAT64) AS online_roas,
        SAFE_CAST(REGEXP_REPLACE(new_buyers, r'[$,]', '') AS INT64) AS new_buyers,
        SAFE_CAST(REGEXP_REPLACE(new_buyer_percentage, r'[%]', '') AS FLOAT64)  AS new_buyer_percentage,
        SAFE_CAST(REGEXP_REPLACE(cost_per_acquisition, r'[$,]', '') AS FLOAT64) AS cost_per_acquisition,
        SAFE_CAST(REGEXP_REPLACE(omni_avg_order_value, r'[$,]', '') AS FLOAT64) AS omni_avg_order_value,
        SAFE_CAST(REGEXP_REPLACE(store_avg_order_value, r'[$,]', '') AS FLOAT64) AS store_avg_order_value,
        SAFE_CAST(REGEXP_REPLACE(conversions, r'[$,]', '') AS FLOAT64) AS conversions,
        CASE
            WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') THEN SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', upload_timestamp)
            WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{14}$') THEN SAFE.PARSE_TIMESTAMP('%Y%m%d%H%M%S', upload_timestamp)
            ELSE NULL  
        END AS upload_timestamp,
        CASE
            WHEN REGEXP_CONTAINS(CAST(file_date AS STRING), r'^\d{4}-\d{2}-\d{2}$') THEN SAFE.PARSE_DATE('%Y-%m-%d', CAST(file_date AS STRING))
            WHEN REGEXP_CONTAINS(CAST(file_date AS STRING), r'^\d{8}$') THEN SAFE.PARSE_DATE('%Y%m%d', CAST(file_date AS STRING))
            ELSE NULL  
        END AS file_date,
        DENSE_RANK() OVER(PARTITION BY file_date ORDER BY CASE WHEN reload_required = 'True' THEN 1 ELSE 2 END,
            TIMESTAMP_TRUNC(PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', upload_timestamp),MINUTE) DESC) AS priority_rank
    FROM `{{params.landing_project}}.skulytics.sh_ulta_retail_media_tbl`
    WHERE 
        CASE
            WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') THEN SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', upload_timestamp)
            WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{14}$') THEN SAFE.PARSE_TIMESTAMP('%Y%m%d%H%M%S', upload_timestamp)
            ELSE NULL  
        END > VAR1
    QUALIFY priority_rank = 1
),
int_operation_2 as (
SELECT *,
    SAFE_DIVIDE ( new_buyers, SAFE_DIVIDE (new_buyer_percentage, 100) ) AS total_buyer,
    SAFE_DIVIDE (online_attrib_sales, COALESCE(conversions, 0)) AS aov,
    SAFE_DIVIDE (conversions, COALESCE(impressions, 0)) AS cvr
FROM int_operation),

aggregated_data AS (
SELECT
    elc_brand,
    campaign_name,
    month,
    fiscal_year,
    digital_media_type,
    targeting_segments,
    MAX(single_vs_multi_branded) AS single_vs_multi_branded,
    MAX(quarter) AS quarter,
    MAX(`1h_or_2h`) AS `1h_or_2h`,
    MAX(onsite_v_offsite) AS onsite_v_offsite,
    MAX(spend_bucket) AS spend_bucket,
    MAX(campaign_start_date) AS campaign_start_date,
    MAX(campaign_end_date) AS campaign_end_date,
    MAX(featured_product_subbrand_or_promo) AS featured_product_subbrand_or_promo,
    MAX(retailer_co_investment) AS retailer_co_investment,
    MAX(funnel_position) AS funnel_position,
    MAX(digital_media_type_select_from_list) AS digital_media_type_select_from_list,
    MAX(sales_reporting_basket_level_or_brand) AS sales_reporting_basket_level_or_brand,
    MAX(file_date) AS file_date,
    MAX(days_in_month) AS days_in_month,
    MAX(total_days_in_campaign) AS total_days_in_campaign,
    MAX(campaign_window_percentage) AS campaign_window_percentage,
    SUM(elc_investment_actual) AS elc_investment_actual,
    SUM(impressions) AS impressions,
    SUM(total_uniques) AS total_uniques,
    SUM(uniques) AS uniques,
    SUM(clicks) AS clicks,
    AVG(ctr) AS ctr,
    SUM(total_video_views) AS total_video_views,
    SUM(video_views) AS video_views,
    AVG(video_completions) AS video_completions,
    AVG(video_completion_rate) AS video_completion_rate,
    AVG(elc_cpm) AS elc_cpm,
    AVG(elc_cpc) AS elc_cpc,
    SUM(omni_attrib_sales) AS omni_attrib_sales,
    SUM(store_attrib_sales) AS store_attrib_sales,
    SUM(online_attrib_sales) AS online_attrib_sales,
    AVG(omni_roas) AS omni_roas,
    AVG(store_roas) AS store_roas,
    AVG(online_roas) AS online_roas,
    SUM(new_buyers) AS new_buyers,
    AVG(new_buyer_percentage) AS new_buyer_percentage,
    AVG(cost_per_acquisition) AS cost_per_acquisition,
    AVG(omni_avg_order_value) AS omni_avg_order_value,
    AVG(store_avg_order_value) AS store_avg_order_value,
    SUM(conversions) AS conversions,
    SUM(total_buyer) AS total_buyer,
    AVG(aov) as aov,
    AVG(cvr) AS cvr,
    count(campaign_name) as campaign_repeat_count,
FROM int_operation_2
GROUP BY
    elc_brand,
    campaign_name,
    month,
    fiscal_year,
    digital_media_type,
    targeting_segments

)
SELECT
CONCAT(
COALESCE(elc_brand, ''), '#',
COALESCE(campaign_name, ''), '#',
COALESCE(month, ''), '#',
COALESCE(fiscal_year, ''),'#',
COALESCE(digital_media_type, ''),'#',
COALESCE(targeting_segments, '')
) AS retail_media_ulta_key,
*
FROM aggregated_data
) b
ON a.retail_media_ulta_key = b.retail_media_ulta_key  
WHEN MATCHED THEN
    UPDATE SET
        a.single_vs_multi_branded = b.single_vs_multi_branded,
        a.quarter = b.quarter,
        a.`1h_or_2h` = b.`1h_or_2h`,
        a.onsite_v_offsite = b.onsite_v_offsite,
        a.digital_media_type = b.digital_media_type,
        a.spend_bucket = b.spend_bucket,
        a.campaign_start_date = b.campaign_start_date,
        a.campaign_end_date = b.campaign_end_date,
        a.days_in_month = b.days_in_month,
        a.total_days_in_campaign = b.total_days_in_campaign,
        a.campaign_window_percentage = b.campaign_window_percentage,
        a.featured_product_subbrand_or_promo = b.featured_product_subbrand_or_promo,
        a.elc_investment_actual = b.elc_investment_actual,
        a.retailer_co_investment = b.retailer_co_investment,
        a.funnel_position = b.funnel_position,
        a.digital_media_type_select_from_list = b.digital_media_type_select_from_list,
        a.targeting_segments = b.targeting_segments,
        a.impressions = b.impressions,
        a.total_uniques = b.total_uniques,
        a.uniques = b.uniques,
        a.clicks = b.clicks,
        a.ctr = b.ctr,
        a.total_video_views = b.total_video_views,
        a.video_views = b.video_views,
        a.video_completions = b.video_completions,
        a.video_completion_rate = b.video_completion_rate,
        a.elc_cpm = b.elc_cpm,
        a.elc_cpc = b.elc_cpc,
        a.sales_reporting_basket_level_or_brand = b.sales_reporting_basket_level_or_brand,
        a.omni_attrib_sales = b.omni_attrib_sales,
        a.store_attrib_sales = b.store_attrib_sales,
        a.online_attrib_sales = b.online_attrib_sales,
        a.omni_roas = b.omni_roas,
        a.store_roas = b.store_roas,
        a.online_roas = b.online_roas,
        a.new_buyers = b.new_buyers,
        a.new_buyer_percentage = b.new_buyer_percentage,
        a.cost_per_acquisition = b.cost_per_acquisition,
        a.omni_avg_order_value = b.omni_avg_order_value,
        a.store_avg_order_value = b.store_avg_order_value,
        a.conversions = b.conversions,
        a.total_buyer = b.total_buyer,
        a.aov = b.aov,
        a.cvr = b.cvr,
        a.campaign_repeat_count = b.campaign_repeat_count,
        a.file_date = b.file_date,
        a.upload_timestamp = CURRENT_TIMESTAMP(),
        a.updated_date = CURRENT_TIMESTAMP()
WHEN NOT MATCHED BY TARGET  THEN
    INSERT (
        elc_brand,
        single_vs_multi_branded,
        fiscal_year,
        quarter,
        `1h_or_2h`,
        onsite_v_offsite,
        digital_media_type,
        spend_bucket,
        campaign_name,
        month,
        campaign_start_date,
        campaign_end_date,
        days_in_month,
        total_days_in_campaign,
        campaign_window_percentage,
        featured_product_subbrand_or_promo,
        elc_investment_actual,
        retailer_co_investment,
        funnel_position,
        digital_media_type_select_from_list,
        targeting_segments,
        impressions,
        total_uniques,
        uniques,
        clicks,
        ctr,
        total_video_views,
        video_views,
        video_completions,
        video_completion_rate,
        elc_cpm,
        elc_cpc,
        sales_reporting_basket_level_or_brand,
        omni_attrib_sales,
        store_attrib_sales,
        online_attrib_sales,
        omni_roas,
        store_roas,
        online_roas,
        new_buyers,
        new_buyer_percentage,
        cost_per_acquisition,
        omni_avg_order_value,
        store_avg_order_value,
        conversions,
        total_buyer,
        aov,
        cvr,
        campaign_repeat_count,
        file_date,
        upload_timestamp,
        retail_media_ulta_key, 
        inserted_date
    )
    VALUES (
        b.elc_brand,
        b.single_vs_multi_branded,
        b.fiscal_year,
        b.quarter,
        b.`1h_or_2h`,
        b.onsite_v_offsite,
        b.digital_media_type,
        b.spend_bucket,
        b.campaign_name,
        b.month,
        b.campaign_start_date,
        b.campaign_end_date,
        b.days_in_month,
        b.total_days_in_campaign,
        b.campaign_window_percentage,
        b.featured_product_subbrand_or_promo,
        b.elc_investment_actual,
        b.retailer_co_investment,
        b.funnel_position,
        b.digital_media_type_select_from_list,
        b.targeting_segments,
        b.impressions,
        b.total_uniques,
        b.uniques,
        b.clicks,
        b.ctr,
        b.total_video_views,
        b.video_views,
        b.video_completions,
        b.video_completion_rate,
        b.elc_cpm,
        b.elc_cpc,
        b.sales_reporting_basket_level_or_brand,
        b.omni_attrib_sales,
        b.store_attrib_sales,
        b.online_attrib_sales,
        b.omni_roas,
        b.store_roas,
        b.online_roas,
        b.new_buyers,
        b.new_buyer_percentage,
        b.cost_per_acquisition,
        b.omni_avg_order_value,
        b.store_avg_order_value,
        b.conversions,
        b.total_buyer,
        b.aov,
        b.cvr,
        b.campaign_repeat_count,
        b.file_date,
        CURRENT_TIMESTAMP(),
        b.retail_media_ulta_key,  
        CURRENT_TIMESTAMP()
    );