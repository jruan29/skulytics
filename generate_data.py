import pandas as pd
import random
import datetime
import os
import uuid

# Configuration
OUTPUT_DIR = 'data'
NUM_RECORDS = 1000  # Adjust as needed
START_DATE = datetime.date(2023, 1, 1)
END_DATE = datetime.date(2023, 12, 31)

# Helper Functions
def random_date(start, end):
    return start + datetime.timedelta(days=random.randint(0, (end - start).days))

def random_float(low, high, precision=2):
    return round(random.uniform(low, high), precision)

# 1. Setup Dimensions (Master Data)
regions = [101, 102, 103, 104, 105]
retailers = [201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
brands = [301, 302, 303, 304, 305]
products = [f'PROD_{i}' for i in range(1000, 1050)]
dates = [START_DATE + datetime.timedelta(days=x) for x in range((END_DATE - START_DATE).days + 1)]

print("Generating data...")

# ---------------------------------------------------------
# 2. Generate fact_retail_retailer_mob_tbl
# ---------------------------------------------------------
print("Generating fact_retail_retailer_mob_tbl...")
data_retailer_mob = []
for _ in range(NUM_RECORDS):
    date_val = random.choice(dates)
    gross_sales_ty = random_float(1000, 50000)
    
    row = {
        'retailer_mob_key': str(uuid.uuid4()),
        'region_key': random.choice(regions),
        'retailer_key': random.choice(retailers),
        'date_key': date_val,
        'gross_sales_ty': gross_sales_ty,
        'gross_sales_fisc_ly': random_float(gross_sales_ty * 0.8, gross_sales_ty * 1.2),
        'gross_sales_greg_ly': random_float(gross_sales_ty * 0.8, gross_sales_ty * 1.2),
        'record_created_date': datetime.datetime.now(),
        'record_updated_date': datetime.datetime.now()
    }
    data_retailer_mob.append(row)

df_retailer_mob = pd.DataFrame(data_retailer_mob)
df_retailer_mob.to_csv(os.path.join(OUTPUT_DIR, 'fact_retail_retailer_mob_tbl.csv'), index=False)


# ---------------------------------------------------------
# 3. Generate fact_retail_product_mob_tbl
# ---------------------------------------------------------
print("Generating fact_retail_product_mob_tbl...")
data_product_mob = []
for _ in range(NUM_RECORDS):
    date_val = random.choice(dates)
    gross_sales_ty = random_float(100, 5000)
    
    row = {
        'sku_mob_key': str(uuid.uuid4()),
        'retailer_product_key': str(uuid.uuid4()),
        'region_key': random.choice(regions),
        'retailer_key': random.choice(retailers),
        'brand_key': random.choice(brands),
        'product_key': random.choice(products),
        'date_key': date_val,
        'gross_sales_ty': gross_sales_ty,
        'gross_sales_fisc_ly': random_float(gross_sales_ty * 0.8, gross_sales_ty * 1.2),
        'gross_sales_greg_ly': random_float(gross_sales_ty * 0.8, gross_sales_ty * 1.2),
        'record_created_date': datetime.datetime.now(),
        'record_updated_date': datetime.datetime.now()
    }
    data_product_mob.append(row)

df_product_mob = pd.DataFrame(data_product_mob)
df_product_mob.to_csv(os.path.join(OUTPUT_DIR, 'fact_retail_product_mob_tbl.csv'), index=False)


# ---------------------------------------------------------
# 4. Generate fact_retail_search_rank_tbl
# ---------------------------------------------------------
print("Generating fact_retail_search_rank_tbl...")
data_search_rank = []
search_types = ['Organic', 'Paid', 'Sponsored']
keywords = ['shampoo', 'conditioner', 'soap', 'body wash', 'lotion']

for _ in range(NUM_RECORDS):
    date_val = random.choice(dates)
    ly_date = date_val - datetime.timedelta(days=365)
    
    row = {
        'search_rank_key': str(uuid.uuid4()),
        'retailer_product_key': str(uuid.uuid4()),
        'region_key': random.choice(regions),
        'brand_key': random.choice(brands),
        'date_key': date_val,
        'ly_date': ly_date,
        'fisc_ly_date': ly_date, # Simplified
        'greg_ly_date': ly_date,
        'retailer_key': random.choice(retailers),
        'product_key': random.choice(products),
        'search_result_type': random.choice(search_types),
        'search_keyword': random.choice(keywords),
        'hero_product_flag': random.choice([0, 1]),
        'top_search_keyword_flag': random.choice([0, 1]),
        'search_rank_ty': random.randint(1, 50),
        'search_rank_ly': random.randint(1, 50),
        'search_rank_fisc_ly': random.randint(1, 50),
        'search_rank_greg_ly': random.randint(1, 50),
        'search_rank_record_count_ty': 1,
        'search_rank_record_count_ly': 1,
        'search_rank_record_count_fisc_ly': 1,
        'search_rank_record_count_greg_ly': 1,
        'record_created_date': datetime.datetime.now(),
        'record_updated_date': datetime.datetime.now()
    }
    data_search_rank.append(row)

df_search_rank = pd.DataFrame(data_search_rank)
df_search_rank.to_csv(os.path.join(OUTPUT_DIR, 'fact_retail_search_rank_tbl.csv'), index=False)


# ---------------------------------------------------------
# 5. Generate fact_retail_media_tbl
# ---------------------------------------------------------
print("Generating fact_retail_media_tbl...")
data_media = []
media_types = ['Display', 'Search', 'Social']
placement_types = ['Banner', 'Sidebar', 'Feed']
campaigns = ['Summer Sale', 'Back to School', 'Holiday Special', 'New Year New You']

for _ in range(NUM_RECORDS):
    date_val = random.choice(dates)
    ly_date = date_val - datetime.timedelta(days=365)
    impressions = random.randint(1000, 100000)
    clicks = int(impressions * random.uniform(0.01, 0.05))
    spend = clicks * random.uniform(0.5, 2.0)
    sales = clicks * random.uniform(0.1, 0.5) * random.uniform(10, 50)
    
    row = {
        'retailer_media_key': str(uuid.uuid4()),
        'region_key': random.choice(regions),
        'campaign_name': random.choice(campaigns),
        'date_key': date_val,
        'ly_date': ly_date,
        'greg_ly_date': ly_date,
        'fisc_ly_date': ly_date,
        'brand_key': random.choice(brands),
        'retailer_key': random.choice(retailers),
        'media_type': random.choice(media_types),
        'placement_type': random.choice(placement_types),
        'line_item': f'LI_{random.randint(1000, 9999)}',
        'spend_bucket': random.choice(['Low', 'Medium', 'High']),
        
        'click_sales_ty': sales,
        'click_sales_ly': sales * random.uniform(0.8, 1.2),
        'click_sales_fisc_ly': sales * random.uniform(0.8, 1.2),
        'click_sales_greg_ly': sales * random.uniform(0.8, 1.2),
        
        'spend_ty': spend,
        'spend_ly': spend * random.uniform(0.8, 1.2),
        'spend_fisc_ly': spend * random.uniform(0.8, 1.2),
        'spend_greg_ly': spend * random.uniform(0.8, 1.2),
        
        'cost_per_mille_ty': (spend / impressions) * 1000 if impressions > 0 else 0,
        'cost_per_mille_ly': random.uniform(5, 20),
        'cost_per_mille_fisc_ly': random.uniform(5, 20),
        'cost_per_mille_greg_ly': random.uniform(5, 20),
        
        'click_roas_ty': sales / spend if spend > 0 else 0,
        'click_roas_ly': random.uniform(2, 10),
        'click_roas_fisc_ly': random.uniform(2, 10),
        'click_roas_greg_ly': random.uniform(2, 10),
        
        'impressions_ty': impressions,
        'impressions_ly': int(impressions * random.uniform(0.8, 1.2)),
        'impressions_fisc_ly': int(impressions * random.uniform(0.8, 1.2)),
        'impressions_greg_ly': int(impressions * random.uniform(0.8, 1.2)),
        
        'clicks_ty': clicks,
        'clicks_ly': int(clicks * random.uniform(0.8, 1.2)),
        'clicks_fisc_ly': int(clicks * random.uniform(0.8, 1.2)),
        'clicks_greg_ly': int(clicks * random.uniform(0.8, 1.2)),
        
        'click_through_rate_ty': clicks / impressions if impressions > 0 else 0,
        'click_through_rate_ly': random.uniform(0.01, 0.05),
        'click_through_rate_fisc_ly': random.uniform(0.01, 0.05),
        'click_through_rate_greg_ly': random.uniform(0.01, 0.05),
        
        'cost_per_click_ty': spend / clicks if clicks > 0 else 0,
        'cost_per_click_ly': random.uniform(0.5, 2.0),
        'cost_per_click_fisc_ly': random.uniform(0.5, 2.0),
        'cost_per_click_greg_ly': random.uniform(0.5, 2.0),
        
        'new_buyer_ty': int(clicks * 0.1),
        'new_buyer_ly': int(clicks * 0.1),
        'new_buyer_fisc_ly': int(clicks * 0.1),
        'new_buyer_greg_ly': int(clicks * 0.1),
        
        'total_buyer_ty': clicks * 0.2,
        'total_buyer_ly': clicks * 0.2,
        'total_buyer_fisc_ly': clicks * 0.2,
        'total_buyer_greg_ly': clicks * 0.2,
        
        'aov_ty': random.uniform(20, 100),
        'aov_ly': random.uniform(20, 100),
        'aov_fisc_ly': random.uniform(20, 100),
        'aov_greg_ly': random.uniform(20, 100),
        
        'cvr_ty': random.uniform(0.01, 0.05),
        'cvr_ly': random.uniform(0.01, 0.05),
        'cvr_fisc_ly': random.uniform(0.01, 0.05),
        'cvr_greg_ly': random.uniform(0.01, 0.05),
        
        'campaign_repeat_count_ty': 1,
        'campaign_repeat_count_ly': 1,
        'campaign_repeat_count_fisc_ly': 1,
        'campaign_repeat_count_greg_ly': 1,
        
        'record_created_date': datetime.datetime.now(),
        'record_updated_date': datetime.datetime.now()
    }
    data_media.append(row)

df_media = pd.DataFrame(data_media)
df_media.to_csv(os.path.join(OUTPUT_DIR, 'fact_retail_media_tbl.csv'), index=False)


# ---------------------------------------------------------
# 6. Generate fact_retail_brand_mob_tbl
# ---------------------------------------------------------
print("Generating fact_retail_brand_mob_tbl...")
data_brand_mob = []
for _ in range(NUM_RECORDS):
    date_val = random.choice(dates)
    gross_sales_ty = random_float(5000, 100000)
    
    row = {
        'retailer_mob_key': str(uuid.uuid4()), # Assuming this is the PK despite name
        'region_key': random.choice(regions),
        'retailer_key': random.choice(retailers),
        'date_key': date_val,
        'gross_sales_ty': gross_sales_ty,
        'gross_sales_fisc_ly': random_float(gross_sales_ty * 0.8, gross_sales_ty * 1.2),
        'gross_sales_greg_ly': random_float(gross_sales_ty * 0.8, gross_sales_ty * 1.2),
        'record_created_date': datetime.datetime.now(),
        'record_updated_date': datetime.datetime.now()
    }
    data_brand_mob.append(row)

df_brand_mob = pd.DataFrame(data_brand_mob)
df_brand_mob.to_csv(os.path.join(OUTPUT_DIR, 'fact_retail_brand_mob_tbl.csv'), index=False)


# ---------------------------------------------------------
# 7. Generate fact_retail_summary_tbl
# ---------------------------------------------------------
print("Generating fact_retail_summary_tbl...")
data_summary = []
for _ in range(NUM_RECORDS):
    date_val = random.choice(dates)
    ly_date = date_val - datetime.timedelta(days=365)
    gross_sales = random_float(100, 1000)
    units = int(gross_sales / random.uniform(10, 50))
    
    row = {
        'retail_summary_key': str(uuid.uuid4()),
        'retailer_product_key': str(uuid.uuid4()),
        'brand_key': random.choice(brands),
        'region_key': random.choice(regions),
        'retailer_key': random.choice(retailers),
        'product_key': random.choice(products),
        'week_end_date': date_val + datetime.timedelta(days=(4 - date_val.weekday() + 7) % 7), # Next Friday
        'month_start_date': date_val.replace(day=1),
        'date_key': date_val,
        'last_year_date': ly_date,
        'fisc_ly_date': ly_date,
        'greg_ly_date': ly_date,
        
        'gross_sales_ty': gross_sales,
        'gross_sales_ly': gross_sales * random.uniform(0.8, 1.2),
        'gross_sales_fisc_ly': gross_sales * random.uniform(0.8, 1.2),
        'gross_sales_greg_ly': gross_sales * random.uniform(0.8, 1.2),
        
        'full_size_units_sold_ty': units,
        'full_size_units_sold_ly': int(units * random.uniform(0.8, 1.2)),
        'full_size_units_sold_fisc_ly': int(units * random.uniform(0.8, 1.2)),
        'full_size_units_sold_greg_ly': int(units * random.uniform(0.8, 1.2)),
        
        'oos_within_month_ty': random.randint(0, 5),
        'oos_within_month_ly': random.randint(0, 5),
        'oos_within_month_fisc_ly': random.randint(0, 5),
        'oos_within_month_greg_ly': random.randint(0, 5),
        
        'oos_percent_month_ty': random.uniform(0, 0.1),
        'oos_percent_month_ly': random.uniform(0, 0.1),
        'oos_percent_month_fisc_ly': random.uniform(0, 0.1),
        'oos_percent_month_greg_ly': random.uniform(0, 0.1),
        
        'oos_within_retail_month_ty': random.randint(0, 5),
        'oos_within_retail_month_ly': random.randint(0, 5),
        'oos_within_retail_month_fisc_ly': random.randint(0, 5),
        'oos_within_retail_month_greg_ly': random.randint(0, 5),
        
        'oos_percent_retail_month_ty': random.uniform(0, 0.1),
        'oos_percent_retail_month_ly': random.uniform(0, 0.1),
        'oos_percent_retail_month_fisc_ly': random.uniform(0, 0.1),
        'oos_percent_retail_month_greg_ly': random.uniform(0, 0.1),
        
        'unit_price_ty': random.uniform(10, 50),
        'unit_price_ly': random.uniform(10, 50),
        'unit_price_fisc_ly': random.uniform(10, 50),
        'unit_price_greg_ly': random.uniform(10, 50),
        
        'selling_price_ty': random.uniform(10, 50),
        'selling_price_ly': random.uniform(10, 50),
        'selling_price_fisc_ly': random.uniform(10, 50),
        'selling_price_greg_ly': random.uniform(10, 50),
        
        'health_score_ty': random.randint(50, 100),
        'health_score_ly': random.randint(50, 100),
        'health_score_fisc_ly': random.randint(50, 100),
        'health_score_greg_ly': random.randint(50, 100),
        
        'product_title_score_ty': random.randint(50, 100),
        'product_title_score_ly': random.randint(50, 100),
        'product_title_score_fisc_ly': random.randint(50, 100),
        'product_title_score_greg_ly': random.randint(50, 100),
        
        'product_description_score_ty': random.randint(50, 100),
        'product_description_score_ly': random.randint(50, 100),
        'product_description_score_fisc_ly': random.randint(50, 100),
        'product_description_score_greg_ly': random.randint(50, 100),
        
        'gallery_image_score_ty': random.randint(50, 100),
        'gallery_image_score_ly': random.randint(50, 100),
        'gallery_image_score_fisc_ly': random.randint(50, 100),
        'gallery_image_score_greg_ly': random.randint(50, 100),
        
        'keyword_analysis_score_ty': random.randint(50, 100),
        'keyword_analysis_score_ly': random.randint(50, 100),
        'keyword_analysis_score_fisc_ly': random.randint(50, 100),
        'keyword_analysis_score_greg_ly': random.randint(50, 100),
        
        'rating_score_ty': random.randint(50, 100),
        'rating_score_ly': random.randint(50, 100),
        'rating_score_fisc_ly': random.randint(50, 100),
        'rating_score_greg_ly': random.randint(50, 100),
        
        'review_score_ty': random.randint(50, 100),
        'review_score_ly': random.randint(50, 100),
        'review_score_fisc_ly': random.randint(50, 100),
        'review_score_greg_ly': random.randint(50, 100),
        
        'emerch_record_count_ty': 1,
        'emerch_record_count_ly': 1,
        'emerch_record_count_fisc_ly': 1,
        'emerch_record_count_greg_ly': 1,
        
        'sponsored_product_spend_ty': random.uniform(0, 100),
        'sponsored_product_spend_ly': random.uniform(0, 100),
        'sponsored_product_spend_fisc_ly': random.uniform(0, 100),
        'sponsored_product_spend_greg_ly': random.uniform(0, 100),
        
        'sponsored_product_sales_revenue_ty': random.uniform(0, 500),
        'sponsored_product_sales_revenue_ly': random.uniform(0, 500),
        'sponsored_product_sales_revenue_fisc_ly': random.uniform(0, 500),
        'sponsored_product_sales_revenue_greg_ly': random.uniform(0, 500),
        
        'sponsored_product_number_of_impressions_ty': random.randint(0, 1000),
        'sponsored_product_number_of_impressions_ly': random.randint(0, 1000),
        'sponsored_product_number_of_impressions_fisc_ly': random.randint(0, 1000),
        'sponsored_product_number_of_impressions_greg_ly': random.randint(0, 1000),
        
        'sponsored_product_number_of_clicks_ty': random.randint(0, 100),
        'sponsored_product_number_of_clicks_ly': random.randint(0, 100),
        'sponsored_product_number_of_clicks_fisc_ly': random.randint(0, 100),
        'sponsored_product_number_of_clicks_greg_ly': random.randint(0, 100),
        
        'sponsored_product_units_ty': random.uniform(0, 50),
        'sponsored_product_units_ly': random.uniform(0, 50),
        'sponsored_product_units_fisc_ly': random.uniform(0, 50),
        'sponsored_product_units_greg_ly': random.uniform(0, 50),
        
        'revenue_ty': gross_sales,
        'revenue_ly': gross_sales * random.uniform(0.8, 1.2),
        'revenue_fisc_ly': gross_sales * random.uniform(0.8, 1.2),
        'revenue_greg_ly': gross_sales * random.uniform(0.8, 1.2),
        
        'units_ty': units,
        'units_ly': int(units * random.uniform(0.8, 1.2)),
        'units_fisc_ly': int(units * random.uniform(0.8, 1.2)),
        'units_greg_ly': int(units * random.uniform(0.8, 1.2)),
        
        'unit_conversion_ty': random.uniform(0.01, 0.1),
        'unit_conversion_ly': random.uniform(0.01, 0.1),
        'unit_conversion_fisc_ly': random.uniform(0.01, 0.1),
        'unit_conversion_greg_ly': random.uniform(0.01, 0.1),
        
        'traffic_conversion_rate_ty': random.uniform(0.01, 0.1),
        'traffic_conversion_rate_ly': random.uniform(0.01, 0.1),
        'traffic_conversion_rate_fisc_ly': random.uniform(0.01, 0.1),
        'traffic_conversion_rate_greg_ly': random.uniform(0.01, 0.1),
        
        'browse_traffic_ty': random.uniform(0, 100),
        'browse_traffic_ly': random.uniform(0, 100),
        'browse_traffic_fisc_ly': random.uniform(0, 100),
        'browse_traffic_greg_ly': random.uniform(0, 100),
        
        'pptraffic_ty': random.uniform(100, 1000),
        'pptraffic_ly': random.uniform(100, 1000),
        'pptraffic_fisc_ly': random.uniform(100, 1000),
        'pptraffic_greg_ly': random.uniform(100, 1000),
        
        'record_created_date': datetime.datetime.now(),
        'record_updated_date': datetime.datetime.now()
    }
    data_summary.append(row)

df_summary = pd.DataFrame(data_summary)
df_summary.to_csv(os.path.join(OUTPUT_DIR, 'fact_retail_summary_tbl.csv'), index=False)

print("Data generation complete.")
