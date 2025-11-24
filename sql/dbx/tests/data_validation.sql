-- TEST 1: Date Range Coverage
SELECT 'Date Range Test' as test_name,
       MIN(date_key) as min_date,
       MAX(date_key) as max_date,
       COUNT(DISTINCT date_key) as distinct_dates,
       CASE 
           WHEN MIN(date_key) = '2023-01-01' 
            AND MAX(date_key) = '2026-03-01' 
            AND COUNT(DISTINCT date_key) >= 1155 
           THEN 'PASS' 
           ELSE 'FAIL' 
       END as result
FROM skulytics_dev.default.fact_retail_summary_tbl;

-- TEST 2: No Orphaned Keys (Product)
SELECT 'Product Key Integrity' as test_name,
       COUNT(*) as orphaned_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl f
LEFT JOIN skulytics_dev.default.dim_product p ON f.product_key = p.productkey
WHERE p.productkey IS NULL;

-- TEST 3: No Orphaned Keys (Brand)
SELECT 'Brand Key Integrity' as test_name,
       COUNT(*) as orphaned_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl f
LEFT JOIN skulytics_dev.default.dim_brand b ON f.brand_key = b.brand_key
WHERE b.brand_key IS NULL;

-- TEST 4: No Orphaned Keys (Retailer)
SELECT 'Retailer Key Integrity' as test_name,
       COUNT(*) as orphaned_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl f
LEFT JOIN skulytics_dev.default.dim_retailer r ON f.retailer_key = r.retailer_key
WHERE r.retailer_key IS NULL;

-- TEST 5: No Orphaned Keys (Region)
SELECT 'Region Key Integrity' as test_name,
       COUNT(*) as orphaned_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl f
LEFT JOIN skulytics_dev.default.dim_region r ON f.region_key = r.region_key
WHERE r.region_key IS NULL;

-- TEST 6: No Orphaned Keys (Date)
SELECT 'Date Key Integrity' as test_name,
       COUNT(*) as orphaned_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl f
LEFT JOIN skulytics_dev.default.dim_date d ON f.date_key = d.datekey
WHERE d.datekey IS NULL;

-- TEST 7: Content Scores in Valid Range (0-100)
SELECT 'Content Score Range' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE content_score < 0 OR content_score > 100
   OR title_score < 0 OR title_score > 100
   OR desc_score < 0 OR desc_score > 100
   OR image_score < 0 OR image_score > 100
   OR keyword_score < 0 OR keyword_score > 100;

-- TEST 8: CVR in Valid Range (0-100%)
SELECT 'CVR Range' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE cvr_ty < 0 OR cvr_ty > 100;

-- TEST 9: Review Rating in Valid Range (1.0-5.0)
SELECT 'Review Rating Range' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE review_rating < 1.0 OR review_rating > 5.0;

-- TEST 10: No Negative Sales
SELECT 'No Negative Sales' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE gross_sales_usd_ty < 0;

-- TEST 11: No Negative Units
SELECT 'No Negative Units' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE gross_units_sold_ty < 0;

-- TEST 12: Price Consistency (sales = units * price, with tolerance)
SELECT 'Price Consistency' as test_name,
       COUNT(*) as inconsistent_count,
       CASE WHEN COUNT(*) < 100 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE gross_units_sold_ty > 0
  AND ABS(gross_sales_usd_ty - (gross_units_sold_ty * selling_price_ty)) > (selling_price_ty * 2);
  -- Allow for some rounding/bundling variance

-- TEST 13: CVR Math Check (orders/visits)
SELECT 'CVR Calculation' as test_name,
       COUNT(*) as inconsistent_count,
       CASE WHEN COUNT(*) < 50 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE total_visits_ty > 0
  AND ABS(cvr_ty - ((total_orders_ty * 1.0) / total_visits_ty)) > 0.5;
  -- Allow small rounding tolerance

-- TEST 14: OOS Days Don't Exceed Date Range
SELECT 'OOS Days Logic' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE oos_days_ty > 365;  -- Can't have more OOS days than a year

-- TEST 15: Sales Should Be Zero When OOS (for single-day records)
SELECT 'OOS Sales Check' as test_name,
       COUNT(*) as invalid_count,
       CASE WHEN COUNT(*) < 100 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE is_out_of_stock = TRUE
  AND gross_sales_usd_ty > 0;
  -- Some tolerance for partial-day OOS

-- TEST 16: Story 1 - Conversion Drop Exists (SKU003)
SELECT 'Story 1: Conversion Drop' as test_name,
       COUNT(*) as matching_rows,
       CASE WHEN COUNT(*) >= 7 THEN 'PASS' ELSE 'FAIL' END as result
FROM (
    SELECT 
        date_key,
        cvr_ty,
        LAG(cvr_ty, 7) OVER (PARTITION BY product_key, retailer_key ORDER BY date_key) as cvr_1w_ago
    FROM skulytics_dev.default.fact_retail_summary_tbl
    WHERE product_key = 'SKU003'
      AND retailer_key = 1
      AND date_key BETWEEN '2025-10-15' AND '2025-11-05'
) subq
WHERE ((cvr_ty - cvr_1w_ago) / cvr_1w_ago) < -0.15;

-- TEST 17: Story 2 - Content Improvement Exists (SKU015)
SELECT 'Story 2: Content Improvement' as test_name,
       MAX(content_score) - MIN(content_score) as score_delta,
       CASE WHEN (MAX(content_score) - MIN(content_score)) >= 30 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE product_key = 'SKU015'
  AND retailer_key = 2
  AND date_key BETWEEN '2025-09-01' AND '2025-10-31';

-- TEST 18: Story 3 - Rank Decline Exists (SKU009)
SELECT 'Story 3: Rank Decline' as test_name,
       MAX(organic_rank_ty) - MIN(organic_rank_ty) as rank_change,
       CASE WHEN (MAX(organic_rank_ty) - MIN(organic_rank_ty)) >= 5 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE product_key = 'SKU009'
  AND retailer_key = 1
  AND date_key BETWEEN '2025-08-01' AND '2025-08-31';

-- TEST 19: Story 4 - ROAS Decline Exists (Media Table)
SELECT 'Story 4: ROAS Decline' as test_name,
       MIN(click_roas_ty) as min_roas,
       CASE WHEN MIN(click_roas_ty) < 3.0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_media_tbl
WHERE campaign_name = 'Summer_Electronics_2025'
  AND date_key BETWEEN '2025-07-16' AND '2025-07-31';

-- TEST 20: Story 5 - Extended OOS Exists (SKU012)
SELECT 'Story 5: Extended OOS' as test_name,
       SUM(CASE WHEN is_out_of_stock = TRUE THEN 1 ELSE 0 END) as oos_days,
       CASE WHEN SUM(CASE WHEN is_out_of_stock = TRUE THEN 1 ELSE 0 END) >= 15 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE product_key = 'SKU012'
  AND retailer_key = 1
  AND date_key BETWEEN '2025-06-26' AND '2025-07-10';

-- TEST 21: Seasonality Check - Holiday Lift Exists
SELECT 'Seasonality: Holiday Lift' as test_name,
       AVG(CASE WHEN MONTH(date_key) IN (11,12) THEN gross_sales_usd_ty END) / 
       AVG(CASE WHEN MONTH(date_key) NOT IN (11,12) THEN gross_sales_usd_ty END) as holiday_multiplier,
       CASE WHEN (AVG(CASE WHEN MONTH(date_key) IN (11,12) THEN gross_sales_usd_ty END) / 
                  AVG(CASE WHEN MONTH(date_key) NOT IN (11,12) THEN gross_sales_usd_ty END)) > 1.2 
            THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE YEAR(date_key) = 2024;

-- TEST 22: Data Volume Check
SELECT 'Data Volume Check' as test_name,
       COUNT(*) as total_rows,
       CASE WHEN COUNT(*) BETWEEN 200000 AND 3000000 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl;

-- TEST 23: Product Coverage Check
SELECT 'Product Coverage' as test_name,
       COUNT(DISTINCT product_key) as distinct_products,
       CASE WHEN COUNT(DISTINCT product_key) = 50 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl;

-- TEST 24: Retailer Coverage Check
SELECT 'Retailer Coverage' as test_name,
       COUNT(DISTINCT retailer_key) as distinct_retailers,
       CASE WHEN COUNT(DISTINCT retailer_key) = 5 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl;

-- TEST 25: No Future Dates
SELECT 'No Future Dates' as test_name,
       COUNT(*) as future_count,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as result
FROM skulytics_dev.default.fact_retail_summary_tbl
WHERE date_key > CURRENT_DATE();
