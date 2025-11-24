CREATE OR REPLACE TABLE
  `{{params.transform_project}}.skulytics_NA.union_retail_media_tbl` AS
WITH
  macys_retail AS (
  SELECT
    0 AS region_key,
    CASE
      WHEN MONTH='January' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+2000, 1, 1 )
      WHEN MONTH='February' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+2000, 2, 1 )
      WHEN MONTH='March' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+2000, 3, 1 )
      WHEN MONTH='April' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+2000, 4, 1 )
      WHEN MONTH='May' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+2000, 5, 1 )
      WHEN MONTH='June' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+2000, 6, 1 )
      WHEN MONTH='July' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+1999, 7, 1 )
      WHEN MONTH='August' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+1999, 8, 1 )
      WHEN MONTH='September' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+1999, 9, 1 )
      WHEN MONTH='October' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+1999, 10, 1 )
      WHEN MONTH='November' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+1999, 11, 1 )
      WHEN MONTH='December' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+1999, 12, 1 )
  END
    AS date_key,
    brd_tbl.brand_id AS brand_key,
    1 AS retailer_key,
    campaign_name,
    digital_media_type AS media_type,
    placement_type,
    line_item,
    spend_bucket,
    tactic,
    quarter,
    MONTH,
    fiscal_year,
    spend,
    cpm AS cost_per_mille,
    impressions,
    clicks,
    ctr AS click_through_rate,
    cpc AS cost_per_click,
    new_buyers AS new_buyer,
    total_buyers AS total_buyer,
    aov,
    cvr,
    campaign_repeat_count
  FROM
    `{{params.source_project}}.skulytics.sh_macys_retail_media_tbl` macys_rtl_tbl
  LEFT JOIN
    `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd_tbl
  ON
    LOWER(
      CASE
        WHEN LOWER(macys_tactic_tbl.brand)="prettypink" THEN 'Pretty Pink'
        WHEN LOWER(macys_tactic_tbl.brand)="monster" THEN 'Monster Makeup'
        ELSE macys_rtl_tbl.brand
    END
      )=LOWER(brd_tbl.brand_name)
  WHERE
    brd_tbl.brand_id IN (1,
      2,
      4,
      5,
      10,
      27) ),
  ulta_retail AS (
  SELECT
    0 AS region_key,
    CASE
      WHEN MONTH='January' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+2000, 1, 1 )
      WHEN MONTH='February' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+2000, 2, 1 )
      WHEN MONTH='March' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+2000, 3, 1 )
      WHEN MONTH='April' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+2000, 4, 1 )
      WHEN MONTH='May' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+2000, 5, 1 )
      WHEN MONTH='June' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+2000, 6, 1 )
      WHEN MONTH='July' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+1999, 7, 1 )
      WHEN MONTH='August' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+1999, 8, 1 )
      WHEN MONTH='September' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+1999, 9, 1 )
      WHEN MONTH='October' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+1999, 10, 1 )
      WHEN MONTH='November' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+1999, 11, 1 )
      WHEN MONTH='December' THEN DATE ( CAST(SUBSTR (fiscal_year, 3, 2) AS INT64)+1999, 12, 1 )
  END
    AS date_key,
    brd_tbl.brand_id AS brand_key,
    2 AS retailer_key,
    campaign_name,
    digital_media_type_select_from_list AS media_type,
    CAST(NULL AS STRING) AS placement_type,
    CAST(targeting_segments AS STRING) AS line_item,
    CAST(spend_bucket AS STRING),
    online_attrib_sales AS click_sales,
    quarter,
    MONTH,
    fiscal_year,
    elc_investment_actual AS spend,
    elc_cpm AS cost_per_mille,
    online_roas AS click_roas,
    impressions,
    clicks,
    ctr AS click_through_rate,
    elc_cpc AS cost_per_click,
    new_buyers AS new_buyer,
    total_buyer,
    aov,
    cvr,
    campaign_repeat_count
  FROM
    `{{params.source_project}}.skulytics.sh_ulta_retail_media_tbl` ulta_rtl_tbl
  LEFT JOIN
    `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd_tbl
  ON
    LOWER(
      CASE
        WHEN LOWER(macys_tactic_tbl.brand)="prettypink" THEN 'Pretty Pink'
        WHEN LOWER(macys_tactic_tbl.brand)="monster" THEN 'Monster Makeup'
        ELSE ulta_rtl_tbl.elc_brand
    END
      )=LOWER(brd_tbl.brand_name)
  WHERE
    brd_tbl.brand_id IN (1,
      2,
      4,
      5,
      10,
      27) ),
  macys_tactics AS (
  SELECT
    brd_tbl.brand_id AS brand_key,
    CASE
      WHEN tactic IN ("Direct Load", "Organic Search") THEN "Onsite"
      WHEN tactic="Paid Social Lower Funnel" THEN "Social"
      WHEN tactic="Display" THEN "Offsite"
      ELSE tactic
  END
    AS tactic,
    DATE_TRUNC (file_date, MONTH) AS date_key,
    AVG(aov_ty) AS average_order_value,
    AVG(unit_conv_ty) AS conversion_rate
  FROM
    `{{params.source_project}}.skulytics.sh_macys_tactics_tbl` macys_tactic_tbl
  LEFT JOIN
    `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd_tbl
  ON
    LOWER(
      CASE
        WHEN LOWER(macys_tactic_tbl.brand)="prettypink" THEN 'Pretty Pink'
        WHEN LOWER(macys_tactic_tbl.brand)="monster" THEN 'Monster Makeup'
        ELSE macys_tactic_tbl.brand
    END
      )=LOWER(brd_tbl.brand_name)
  WHERE
    brd_tbl.brand_id IN (1,
      2,
      4,
      5,
      10,
      27)
    AND tactic IN ( "Direct Load",
      "Organic Search",
      "Paid Social Lower Funnel",
      "Display",
      "Email",
      "Social" )
  GROUP BY
    brand_key,
    tactic,
    date_key
  UNION ALL
  SELECT
    brd_tbl.brand_id AS brand_key,
    CASE
      WHEN tactic IN ("Direct Load", "Organic Search") THEN "Onsite"
      WHEN tactic="Paid Social Lower Funnel" THEN "Social"
      WHEN tactic="Display" THEN "Offsite"
      ELSE tactic
  END
    AS tactic,
    DATE_SUB (DATE_TRUNC (file_date, MONTH), INTERVAL 1 YEAR) AS date_key,
    AVG(aov_ly) AS average_order_value,
    AVG(unit_conv_ly) AS conversion_rate
  FROM
    `{{params.source_project}}.skulytics.sh_macys_tactics_tbl` macys_tactic_tbl
  LEFT JOIN
    `{{params.dwh_project}}.COMMON_DMART.dim_brand_tbl` brd_tbl
  ON
    LOWER(
      CASE
        WHEN LOWER(macys_tactic_tbl.brand)="prettypink" THEN 'Pretty Pink'
        WHEN LOWER(macys_tactic_tbl.brand)="monster" THEN 'Monster Makeup'
        ELSE macys_tactic_tbl.brand
    END
      )=LOWER(brd_tbl.brand_name)
  WHERE
    brd_tbl.brand_id IN (1,
      2,
      4,
      5,
      10,
      27)
    AND tactic IN ( "Direct Load",
      "Organic Search",
      "Paid Social Lower Funnel",
      "Display",
      "Email",
      "Social" )
    AND DATE_SUB (DATE_TRUNC (file_date, MONTH), INTERVAL 1 YEAR) NOT IN (
    SELECT
      DISTINCT DATE_TRUNC (file_date, MONTH)
    FROM
      `{{params.source_project}}.skulytics.sh_macys_tactics_tbl` )
  GROUP BY
    brand_key,
    tactic,
    date_key ),
  macys_retail_final AS (
  SELECT
    r.region_key,
    r.date_key,
    r.brand_key,
    r.retailer_key,
    r.campaign_name,
    r.media_type,
    r.placement_type,
    r.line_item,
    r.spend_bucket,
    (t.average_order_value*t.conversion_rate*r.clicks) AS click_sales,
    r.quarter,
    r.month,
    r.fiscal_year,
    r.spend,
    r.cost_per_mille,
    SAFE_DIVIDE ( t.average_order_value*t.conversion_rate*r.clicks, r.spend ) AS click_roas,
    r.impressions,
    r.clicks,
    r.click_through_rate,
    r.cost_per_click,
    r.new_buyer,
    r.total_buyer,
    t.average_order_value AS aov,
    t.conversion_rate AS cvr,
    r.campaign_repeat_count
  FROM
    macys_retail r
  LEFT JOIN
    macys_tactics t
  ON
    r.brand_key=t.brand_key
    AND r.date_key=t.date_key
    AND
    CASE
      WHEN r.tactic="Brand Showcase" THEN "Onsite"
      WHEN r.tactic="CTV/OLV" THEN "Offsite"
      ELSE r.tactic
  END
    =t.tactic ),
  retail_tbl_final AS (
  SELECT
    *
  FROM
    macys_retail_final
  UNION ALL
  SELECT
    *
  FROM
    ulta_retail )
SELECT
  CONCAT ( CAST(region_key AS STRING), '#', date_key, '#', CAST(brand_key AS STRING), '#', CAST(retailer_key AS STRING), '#', COALESCE(campaign_name, ''), '#', COALESCE(media_type, ''), '#', COALESCE(line_item, '') ) AS retail_media_key,
  *,
  CURRENT_TIMESTAMP() AS record_created_date,
  CURRENT_TIMESTAMP() AS record_updated_date
FROM
  retail_tbl_final;