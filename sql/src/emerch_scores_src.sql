DECLARE var1 TIMESTAMP;

SET var1 = (
    SELECT IFNULL(MAX(upload_timestamp), CAST('1900-01-01 00:00:00' AS TIMESTAMP))
    FROM `{{params.source_project}}.skulytics.sh_emerch_scores_tbl`
);

MERGE INTO `{{params.source_project}}.skulytics.sh_emerch_scores_tbl` AS a
USING (
    WITH int_operation AS (
        SELECT 
            CAST(brand AS STRING) AS brand,
            CAST(retailer AS STRING) AS retailer,
            CAST(title AS STRING) AS title,
            CASE
                WHEN REGEXP_CONTAINS(CAST(date AS STRING), r'^\d{4}-\d{2}-\d{2}$') THEN SAFE.PARSE_DATE('%Y-%m-%d', CAST(date AS STRING))
                WHEN REGEXP_CONTAINS(CAST(date AS STRING), r'^[A-Za-z]{3} \d{4}$') THEN SAFE.PARSE_DATE('%b %Y', CAST(date AS STRING))
                WHEN REGEXP_CONTAINS(CAST(date AS STRING), r'^[A-Za-z]{3}-\d{2}$') THEN 
                    SAFE.PARSE_DATE('%Y-%m-%d', 
                        CONCAT(
                            20,
                            SUBSTR(CAST(date AS STRING), -2),
                            '-',
                            FORMAT_DATE('%m', SAFE.PARSE_DATE('%b', SUBSTR(CAST(date AS STRING), 1, 3))),
                            '-01'
                        )
                    )
                ELSE NULL 
            END AS date,
            SAFE_CAST(retailer_id AS INT64) AS retailer_id,
            SAFE_CAST(product_number AS INT64) AS product_number,  
            CAST(CAST(health_score AS FLOAT64) AS INT64) AS health_score,  
            CAST(CAST(title_score AS FLOAT64) AS INT64) AS title_score,  
            CAST(CAST(description_score AS FLOAT64) AS INT64) AS description_score, 
            CAST(CAST(image_score AS FLOAT64) AS INT64) AS image_score,  
            CAST(CAST(rating_score AS FLOAT64) AS INT64) AS rating_score,  
            CAST(CAST(review_score AS FLOAT64) AS INT64) AS review_score,  
            CAST(CAST(keyword_score AS FLOAT64) AS INT64) AS keyword_score,  
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
        FROM `{{params.landing_project}}.skulytics.sh_emerch_scores_tbl`
        WHERE
            CASE
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') THEN SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', upload_timestamp)
                WHEN REGEXP_CONTAINS(upload_timestamp, r'^\d{14}$') THEN SAFE.PARSE_TIMESTAMP('%Y%m%d%H%M%S', upload_timestamp)
                ELSE NULL  
            END > var1
    )
    SELECT 
        CONCAT(
            COALESCE(title, ''), '#',
            COALESCE(cast(date as STRING), ''), '#',
            COALESCE(cast(retailer_id as string), ''), '#',
            COALESCE(brand, ''), '#',
            COALESCE(cast(product_number as string), '')
        ) AS emerch_scores_key,
        brand,
        retailer,
        title,
        date,
        retailer_id,
        product_number,
        health_score,
        title_score,
        description_score,
        image_score,
        rating_score,
        review_score,
        keyword_score,
        upload_timestamp,  
        file_date,  
        ROW_NUMBER() OVER (PARTITION BY product_number, date, title, retailer_id, brand ORDER BY file_date DESC, upload_timestamp DESC) AS rn
    FROM int_operation
) b
ON a.emerch_scores_key = b.emerch_scores_key  
WHEN MATCHED AND b.rn = 1 THEN
       UPDATE SET
        a.brand = b.brand,  
        a.retailer = b.retailer,  
        a.title = b.title,  
        a.date = b.date,  
        a.retailer_id = b.retailer_id,  
        a.product_number = b.product_number,  
        a.health_score = b.health_score,  
        a.title_score = b.title_score,  
        a.description_score = b.description_score,  
        a.image_score = b.image_score,  
        a.rating_score = b.rating_score,  
        a.review_score = b.review_score,  
        a.keyword_score = b.keyword_score,  
        a.upload_timestamp = b.upload_timestamp, 
        a.file_date = b.file_date,  
        a.updated_date = CURRENT_TIMESTAMP()  
WHEN NOT MATCHED BY TARGET AND b.rn = 1 THEN
    INSERT (
        brand,
        retailer,
        title,
        date,
        retailer_id,
        product_number,
        health_score,
        title_score,
        description_score,
        image_score,
        rating_score,
        review_score,
        keyword_score,
        upload_timestamp,
        file_date,
        emerch_scores_key, 
        inserted_date 
    )
    VALUES (
        b.brand,  
        b.retailer,  
        b.title,  
        b.date,  
        b.retailer_id,  
        b.product_number,  
        b.health_score,  
        b.title_score,  
        b.description_score,  
        b.image_score,  
        b.rating_score,  
        b.review_score,  
        b.keyword_score,  
        b.upload_timestamp,  
        b.file_date, 
        b.emerch_scores_key,  
        CURRENT_TIMESTAMP()  
    );