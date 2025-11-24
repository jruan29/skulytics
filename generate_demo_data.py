import pandas as pd
import numpy as np
import datetime
import os
import uuid
import random

# Configuration
OUTPUT_DIR = 'data'
START_DATE = datetime.date(2023, 1, 1)
END_DATE = datetime.date(2026, 3, 1)
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

ensure_dir(OUTPUT_DIR)

print("Generating Dimensions...")

# ---------------------------------------------------------
# 1. Dimensions
# ---------------------------------------------------------

# --- dim_region ---
regions = [
    {'region_key': 0, 'region_name': 'Global', 'region_code': 'GLB', 'country': 'Multiple', 'currency': 'USD', 'timezone': 'UTC'},
    {'region_key': 1, 'region_name': 'North America', 'region_code': 'NAM', 'country': 'United States', 'currency': 'USD', 'timezone': 'America/New_York'},
    {'region_key': 2, 'region_name': 'Europe', 'region_code': 'EUR', 'country': 'United Kingdom', 'currency': 'EUR', 'timezone': 'Europe/London'},
    {'region_key': 3, 'region_name': 'Asia Pacific', 'region_code': 'APAC', 'country': 'Australia', 'currency': 'AUD', 'timezone': 'Australia/Sydney'}
]
df_region = pd.DataFrame(regions)
df_region.to_csv(os.path.join(OUTPUT_DIR, 'dim_region.csv'), index=False)

# --- dim_brand ---
brands = [
    {'brand_key': 1, 'brand_name': 'TechNova', 'category': 'Electronics', 'subcategory': 'Audio', 'brand_tier': 'Premium', 'brand_description': 'Premium wireless audio devices'},
    {'brand_key': 2, 'brand_name': 'SmartHome Pro', 'category': 'Electronics', 'subcategory': 'Smart Home', 'brand_tier': 'Standard', 'brand_description': 'Affordable smart home automation'},
    {'brand_key': 3, 'brand_name': 'FitLife', 'category': 'Health & Beauty', 'subcategory': 'Fitness', 'brand_tier': 'Standard', 'brand_description': 'Everyday fitness and wellness products'},
    {'brand_key': 4, 'brand_name': 'HomeEssentials', 'category': 'Home & Kitchen', 'subcategory': 'Kitchen Appliances', 'brand_tier': 'Value', 'brand_description': 'Budget-friendly kitchen solutions'},
    {'brand_key': 5, 'brand_name': 'PureGlow', 'category': 'Health & Beauty', 'subcategory': 'Skincare', 'brand_tier': 'Premium', 'brand_description': 'Luxury organic skincare line'},
    {'brand_key': 6, 'brand_name': 'GadgetMaster', 'category': 'Electronics', 'subcategory': 'Accessories', 'brand_tier': 'Standard', 'brand_description': 'Tech accessories and peripherals'},
    {'brand_key': 7, 'brand_name': 'EcoLiving', 'category': 'Home & Kitchen', 'subcategory': 'Sustainability', 'brand_tier': 'Premium', 'brand_description': 'Eco-friendly home products'}
]
df_brand = pd.DataFrame(brands)
df_brand.to_csv(os.path.join(OUTPUT_DIR, 'dim_brand.csv'), index=False)

# --- dim_retailer ---
retailers = [
    {'retailer_key': 1, 'retailer_name': 'Amazon', 'retailer_type': 'Marketplace', 'region_key': 1, 'market_share_pct': 38.7},
    {'retailer_key': 2, 'retailer_name': 'Walmart.com', 'retailer_type': 'Omnichannel', 'region_key': 1, 'market_share_pct': 6.3},
    {'retailer_key': 3, 'retailer_name': 'Target.com', 'retailer_type': 'Omnichannel', 'region_key': 1, 'market_share_pct': 3.9},
    {'retailer_key': 4, 'retailer_name': 'Best Buy', 'retailer_type': 'Omnichannel', 'region_key': 1, 'market_share_pct': 2.1},
    {'retailer_key': 5, 'retailer_name': 'Company DTC Site', 'retailer_type': 'DTC', 'region_key': 1, 'market_share_pct': 1.5}
]
df_retailer = pd.DataFrame(retailers)
df_retailer.to_csv(os.path.join(OUTPUT_DIR, 'dim_retailer.csv'), index=False)

# --- dim_product ---
# Specific products
specific_products = [
    {'productkey': 'SKU001', 'product_name': 'TechNova Wireless Earbuds Pro', 'brand_key': 1, 'category': 'Electronics', 'price_tier': 'Premium', 'base_price': 149.99, 'is_hero_product': True, 'launch_date': '2023-03-15'},
    {'productkey': 'SKU003', 'product_name': 'SmartHome WiFi Camera 360', 'brand_key': 2, 'category': 'Electronics', 'price_tier': 'Mid', 'base_price': 79.99, 'is_hero_product': False, 'launch_date': '2023-06-01'},
    {'productkey': 'SKU007', 'product_name': 'FitLife Yoga Mat Premium', 'brand_key': 3, 'category': 'Health & Beauty', 'price_tier': 'Mid', 'base_price': 49.99, 'is_hero_product': False, 'launch_date': '2023-01-10'},
    {'productkey': 'SKU009', 'product_name': 'SmartHome Smart Thermostat', 'brand_key': 2, 'category': 'Electronics', 'price_tier': 'Mid', 'base_price': 129.99, 'is_hero_product': True, 'launch_date': '2022-11-01'},
    {'productkey': 'SKU012', 'product_name': 'TechNova Wireless Charging Pad', 'brand_key': 1, 'category': 'Electronics', 'price_tier': 'Premium', 'base_price': 59.99, 'is_hero_product': True, 'launch_date': '2023-05-20'},
    {'productkey': 'SKU015', 'product_name': 'HomeEssentials Coffee Maker Deluxe', 'brand_key': 4, 'category': 'Home & Kitchen', 'price_tier': 'Budget', 'base_price': 39.99, 'is_hero_product': False, 'launch_date': '2022-08-15'},
    {'productkey': 'SKU018', 'product_name': 'GadgetMaster USB-C Hub 7-in-1', 'brand_key': 6, 'category': 'Electronics', 'price_tier': 'Mid', 'base_price': 34.99, 'is_hero_product': False, 'launch_date': '2023-09-01'},
    {'productkey': 'SKU022', 'product_name': 'PureGlow Vitamin C Serum', 'brand_key': 5, 'category': 'Health & Beauty', 'price_tier': 'Premium', 'base_price': 79.99, 'is_hero_product': False, 'launch_date': '2023-02-28'}
]

products = []
# Add specific products
for p in specific_products:
    brand = next(b for b in brands if b['brand_key'] == p['brand_key'])
    p['subcategory'] = brand['subcategory']
    p['upc_code'] = str(random.randint(100000000000, 999999999999))
    p['product_status'] = 'Active'
    products.append(p)

# Generate remaining products to reach 50
existing_skus = set(p['productkey'] for p in products)
sku_counter = 1
while len(products) < 50:
    sku = f'SKU{sku_counter:03d}'
    if sku in existing_skus:
        sku_counter += 1
        continue
    
    brand = random.choice(brands)
    price_tier = random.choice(['Budget', 'Mid', 'Premium'])
    base_price = random.uniform(10, 30) if price_tier == 'Budget' else random.uniform(30, 100) if price_tier == 'Mid' else random.uniform(100, 500)
    is_hero = random.random() < 0.2
    
    products.append({
        'productkey': sku,
        'product_name': f'{brand["brand_name"]} {brand["subcategory"]} {sku}',
        'brand_key': brand['brand_key'],
        'category': brand['category'],
        'subcategory': brand['subcategory'],
        'upc_code': str(random.randint(100000000000, 999999999999)),
        'price_tier': price_tier,
        'base_price': round(base_price, 2),
        'is_hero_product': is_hero,
        'launch_date': datetime.date(2022, 1, 1) + datetime.timedelta(days=random.randint(0, 700)),
        'product_status': 'Active'
    })
    sku_counter += 1

df_product = pd.DataFrame(products)
df_product.to_csv(os.path.join(OUTPUT_DIR, 'dim_product.csv'), index=False)

# --- dim_date ---
date_list = [START_DATE + datetime.timedelta(days=x) for x in range((END_DATE - START_DATE).days + 1)]
dim_date_data = []
for d in date_list:
    is_weekend = d.weekday() >= 5
    # Simple holiday logic
    is_holiday = False
    holiday_name = None
    if d.month == 1 and d.day == 1: is_holiday, holiday_name = True, "New Year's Day"
    elif d.month == 12 and d.day == 25: is_holiday, holiday_name = True, "Christmas Day"
    elif d.month == 11 and d.day == 29 and d.year == 2024: is_holiday, holiday_name = True, "Black Friday" # Simplified
    
    dim_date_data.append({
        'datekey': d,
        'full_date': d,
        'year': d.year,
        'month': d.month,
        'month_name': d.strftime('%B'),
        'month_abbr': d.strftime('%b'),
        'week': int(d.strftime('%V')),
        'week_start_date': d - datetime.timedelta(days=d.weekday()),
        'week_end_date': d + datetime.timedelta(days=4 - d.weekday() + 7) if d.weekday() <= 4 else d + datetime.timedelta(days=4 - d.weekday()), # Simplified Friday logic
        'month_start_date': d.replace(day=1),
        'day_of_month': d.day,
        'day_of_week': d.weekday() + 1,
        'day_name': d.strftime('%A'),
        'day_abbr': d.strftime('%a'),
        'quarter': (d.month - 1) // 3 + 1,
        'quarter_name': f'Q{(d.month - 1) // 3 + 1}',
        'is_weekend': is_weekend,
        'is_holiday': is_holiday,
        'holiday_name': holiday_name,
        'fiscal_year': d.year if d.month >= 2 else d.year - 1,
        'fiscal_quarter': ((d.month - 2) // 3 + 1) if d.month >= 2 else 4,
        'fiscal_period': d.month - 1 if d.month >= 2 else 12,
        'ly_date': d - datetime.timedelta(days=365), # Simplified leap year
        'fiscly_date': d - datetime.timedelta(days=364), # Simplified 52 weeks
        'gregly_date': d - datetime.timedelta(days=365)
    })
df_date = pd.DataFrame(dim_date_data)
df_date.to_csv(os.path.join(OUTPUT_DIR, 'dim_date.csv'), index=False)


# ---------------------------------------------------------
# 2. Fact Retail Summary Generation
# ---------------------------------------------------------
print("Generating Fact Retail Summary...")

# Create skeleton: Date x Product x Retailer
# To reduce size, we'll assume not every product is at every retailer every day.
# But for simplicity and to ensure we hit the stories, we'll do full cross join for key products/retailers and sample for others.
# Actually, 2.5M rows is manageable.
# 50 products * 5 retailers = 250 combos.
# 1155 days.
# 250 * 1155 = 288,750 rows. Wait, the plan said 2.5M rows?
# "50 products x 5 retailers x 3 years x 365 days = ~273,750 theoretical max"
# Ah, the plan said "Row Count Target: ~2.5 million rows".
# But the math 50*5*3*365 is only ~273k.
# Maybe the user meant 500 products? Or more retailers?
# Or maybe the user math was wrong in the plan?
# "50 products x 5 retailers x 3 years x 365 days = ~273,750" -> This math is correct.
# If the target is 2.5M, we need 10x more data.
# I will stick to the 50 products and 5 retailers defined in dimensions.
# The "2.5 million" might be a typo in the plan or I should generate more products.
# The plan explicitly lists 50 products.
# I will generate ~273k rows. It's enough for a demo.

# Cross join
df_cross = pd.merge(pd.DataFrame({'key': 1, 'date_key': df_date['datekey']}), 
                    pd.DataFrame({'key': 1, 'product_key': df_product['productkey']}), on='key')
df_cross = pd.merge(df_cross, pd.DataFrame({'key': 1, 'retailer_key': df_retailer['retailer_key']}), on='key').drop('key', axis=1)

# Merge attributes
df_fact = df_cross.merge(df_product[['productkey', 'base_price', 'price_tier', 'brand_key', 'is_hero_product']], left_on='product_key', right_on='productkey')
df_fact = df_fact.merge(df_retailer[['retailer_key', 'region_key', 'retailer_name']], on='retailer_key')
df_fact = df_fact.merge(df_date[['datekey', 'month', 'day_of_week', 'is_holiday', 'week_end_date', 'month_start_date', 'ly_date', 'fiscly_date', 'gregly_date']], left_on='date_key', right_on='datekey')

# Initialize columns
n_rows = len(df_fact)
df_fact['gross_sales_usd_ty'] = 0.0
df_fact['gross_units_sold_ty'] = 0
df_fact['is_out_of_stock'] = False
df_fact['oos_days_ty'] = 0
df_fact['oos_percent_ty'] = 0.0
df_fact['content_score'] = np.random.randint(65, 90, n_rows)
df_fact['title_score'] = np.random.randint(65, 90, n_rows)
df_fact['desc_score'] = np.random.randint(65, 90, n_rows)
df_fact['image_score'] = np.random.randint(65, 90, n_rows)
df_fact['keyword_score'] = np.random.randint(65, 90, n_rows)
df_fact['rating_score'] = np.random.randint(70, 95, n_rows)
df_fact['review_score'] = np.random.randint(60, 90, n_rows)
df_fact['review_rating'] = np.round(np.random.uniform(3.8, 4.6, n_rows), 1)
df_fact['review_count'] = np.random.randint(50, 3000, n_rows)
df_fact['organic_rank_ty'] = np.random.randint(10, 40, n_rows)
df_fact['paid_rank_ty'] = np.nan
df_fact['is_sponsored_product'] = False
df_fact['total_visits_ty'] = 0
df_fact['total_orders_ty'] = 0
df_fact['cvr_ty'] = 0.0

# --- Baseline Logic ---
# Vectorized operations for speed
# Base Sales
df_fact['daily_base_sales'] = np.where(df_fact['price_tier'] == 'Budget', np.random.uniform(200, 2000, n_rows),
                              np.where(df_fact['price_tier'] == 'Mid', np.random.uniform(500, 8000, n_rows),
                                       np.random.uniform(300, 5000, n_rows))) # Premium

# Amazon Lift
df_fact.loc[df_fact['retailer_name'] == 'Amazon', 'daily_base_sales'] *= 1.5

# Seasonality
# Holiday (Nov-Dec)
df_fact.loc[df_fact['month'].isin([11, 12]), 'daily_base_sales'] *= 1.4
# Jan
df_fact.loc[df_fact['month'] == 1, 'daily_base_sales'] *= 0.75
# Weekend Lift (Fri-Sun: 5,6,7) - Wait, python weekday 0=Mon, 6=Sun. 
# My dim_date day_of_week is 1=Mon, 7=Sun.
df_fact.loc[df_fact['day_of_week'].isin([5, 6, 7]), 'daily_base_sales'] *= 1.15

# Calculate Unit Price & Selling Price
df_fact['unit_price_ty'] = df_fact['base_price']
df_fact['selling_price_ty'] = df_fact['base_price'] # Simplified

# Calculate Units & Sales
df_fact['gross_sales_usd_ty'] = df_fact['daily_base_sales']
df_fact['gross_units_sold_ty'] = (df_fact['gross_sales_usd_ty'] / df_fact['selling_price_ty']).astype(int)
# Recalculate sales to match units exactly
df_fact['gross_sales_usd_ty'] = df_fact['gross_units_sold_ty'] * df_fact['selling_price_ty']

# CVR
df_fact['cvr_ty'] = np.random.uniform(0.03, 0.07, n_rows)
df_fact.loc[df_fact['price_tier'] == 'Premium', 'cvr_ty'] = np.random.uniform(0.02, 0.04, len(df_fact[df_fact['price_tier'] == 'Premium']))

# Traffic
df_fact['total_orders_ty'] = df_fact['gross_units_sold_ty'] # Simplified 1 unit per order
df_fact['total_visits_ty'] = (df_fact['total_orders_ty'] / df_fact['cvr_ty']).fillna(0).astype(int)

# OOS Baseline
# Random 3% OOS
oos_indices = np.random.choice(df_fact.index, size=int(n_rows * 0.03), replace=False)
df_fact.loc[oos_indices, 'is_out_of_stock'] = True
df_fact.loc[oos_indices, 'oos_days_ty'] = 1
df_fact.loc[oos_indices, 'oos_percent_ty'] = 1.0
df_fact.loc[oos_indices, 'gross_sales_usd_ty'] = 0
df_fact.loc[oos_indices, 'gross_units_sold_ty'] = 0
df_fact.loc[oos_indices, 'total_orders_ty'] = 0


# ---------------------------------------------------------
# 3. Apply Stories
# ---------------------------------------------------------
print("Applying Stories...")

# Story 1: SKU003 Conversion Drop (Oct 15 - Nov 18, 2025)
# Retailer 1 (Amazon)
mask_s1 = (df_fact['product_key'] == 'SKU003') & (df_fact['retailer_key'] == 1) & \
          (df_fact['date_key'] >= datetime.date(2025, 10, 15)) & (df_fact['date_key'] <= datetime.date(2025, 11, 18))

# We need to iterate day by day or apply vectorized logic carefully
# Week 1 (Oct 15-21): Normal (already set by baseline)
# Week 2 (Oct 22-28): OOS 4 days, Review drop, CVR drop
s1_dates = df_fact.loc[mask_s1, 'date_key'].unique()
for d in s1_dates:
    idx = df_fact[(mask_s1) & (df_fact['date_key'] == d)].index
    if len(idx) == 0: continue
    
    if datetime.date(2025, 10, 22) <= d <= datetime.date(2025, 10, 28):
        if d in [datetime.date(2025, 10, 24), datetime.date(2025, 10, 25), datetime.date(2025, 10, 26), datetime.date(2025, 10, 27)]:
            df_fact.loc[idx, 'is_out_of_stock'] = True
            df_fact.loc[idx, 'oos_days_ty'] = 1
            df_fact.loc[idx, 'oos_percent_ty'] = 1.0
            df_fact.loc[idx, 'gross_sales_usd_ty'] = 0
            df_fact.loc[idx, 'gross_units_sold_ty'] = 0
        df_fact.loc[idx, 'review_rating'] = 3.8
        df_fact.loc[idx, 'review_score'] = 65
        df_fact.loc[idx, 'cvr_ty'] = 0.033
        
    elif datetime.date(2025, 10, 29) <= d <= datetime.date(2025, 11, 4):
        if d in [datetime.date(2025, 10, 29), datetime.date(2025, 10, 30), datetime.date(2025, 10, 31)]:
            df_fact.loc[idx, 'is_out_of_stock'] = True
            df_fact.loc[idx, 'oos_days_ty'] = 1
            df_fact.loc[idx, 'oos_percent_ty'] = 1.0
            df_fact.loc[idx, 'gross_sales_usd_ty'] = 0
        df_fact.loc[idx, 'review_rating'] = 3.7
        df_fact.loc[idx, 'review_score'] = 62
        df_fact.loc[idx, 'organic_rank_ty'] = 31
        df_fact.loc[idx, 'cvr_ty'] = 0.026
        
    elif datetime.date(2025, 11, 5) <= d <= datetime.date(2025, 11, 11):
        df_fact.loc[idx, 'is_out_of_stock'] = False
        df_fact.loc[idx, 'review_rating'] = 3.9
        df_fact.loc[idx, 'review_score'] = 68
        df_fact.loc[idx, 'cvr_ty'] = 0.032
        df_fact.loc[idx, 'organic_rank_ty'] = 28
        
    elif datetime.date(2025, 11, 12) <= d <= datetime.date(2025, 11, 18):
        df_fact.loc[idx, 'review_rating'] = 4.0
        df_fact.loc[idx, 'review_score'] = 72
        df_fact.loc[idx, 'cvr_ty'] = 0.039
        df_fact.loc[idx, 'organic_rank_ty'] = 25

# Story 2: Content Health (SKU015 Walmart, SKU022 Amazon)
# Phase 1: Sep 1-15 (Poor)
# Phase 3: Sep 17-30 (Improved)
# Phase 4: Oct 1-31 (Sustained)
for prod, ret in [('SKU015', 2), ('SKU022', 1)]:
    mask_s2 = (df_fact['product_key'] == prod) & (df_fact['retailer_key'] == ret)
    
    # Phase 1
    p1_idx = df_fact[mask_s2 & (df_fact['date_key'] >= datetime.date(2025, 9, 1)) & (df_fact['date_key'] <= datetime.date(2025, 9, 15))].index
    df_fact.loc[p1_idx, 'content_score'] = 48
    df_fact.loc[p1_idx, 'title_score'] = 42
    df_fact.loc[p1_idx, 'desc_score'] = 51
    df_fact.loc[p1_idx, 'keyword_score'] = 38
    df_fact.loc[p1_idx, 'image_score'] = 55
    df_fact.loc[p1_idx, 'cvr_ty'] = 0.028
    df_fact.loc[p1_idx, 'organic_rank_ty'] = 45
    
    # Phase 3
    p3_idx = df_fact[mask_s2 & (df_fact['date_key'] >= datetime.date(2025, 9, 17)) & (df_fact['date_key'] <= datetime.date(2025, 9, 30))].index
    df_fact.loc[p3_idx, 'content_score'] = 85
    df_fact.loc[p3_idx, 'title_score'] = 88
    df_fact.loc[p3_idx, 'desc_score'] = 84
    df_fact.loc[p3_idx, 'keyword_score'] = 82
    df_fact.loc[p3_idx, 'image_score'] = 86
    df_fact.loc[p3_idx, 'cvr_ty'] = 0.032
    df_fact.loc[p3_idx, 'organic_rank_ty'] = 36
    
    # Phase 4
    p4_idx = df_fact[mask_s2 & (df_fact['date_key'] >= datetime.date(2025, 10, 1)) & (df_fact['date_key'] <= datetime.date(2025, 10, 31))].index
    df_fact.loc[p4_idx, 'content_score'] = 87
    df_fact.loc[p4_idx, 'title_score'] = 89
    df_fact.loc[p4_idx, 'desc_score'] = 86
    df_fact.loc[p4_idx, 'keyword_score'] = 84
    df_fact.loc[p4_idx, 'image_score'] = 87
    df_fact.loc[p4_idx, 'cvr_ty'] = 0.036
    df_fact.loc[p4_idx, 'organic_rank_ty'] = 29
    
    # Recalculate sales for these periods based on new CVR and Visits (Visits should change too)
    # Simplified: just boost sales by ratio of CVR improvement + Traffic improvement
    # Phase 1: Low traffic
    df_fact.loc[p1_idx, 'total_visits_ty'] = 800
    # Phase 3: Better traffic
    df_fact.loc[p3_idx, 'total_visits_ty'] = 950
    # Phase 4: Best traffic
    df_fact.loc[p4_idx, 'total_visits_ty'] = 1100
    
    # Recalc orders/sales
    for idx_set in [p1_idx, p3_idx, p4_idx]:
        df_fact.loc[idx_set, 'total_orders_ty'] = (df_fact.loc[idx_set, 'total_visits_ty'] * df_fact.loc[idx_set, 'cvr_ty']).astype(int)
        df_fact.loc[idx_set, 'gross_units_sold_ty'] = df_fact.loc[idx_set, 'total_orders_ty']
        df_fact.loc[idx_set, 'gross_sales_usd_ty'] = df_fact.loc[idx_set, 'gross_units_sold_ty'] * df_fact.loc[idx_set, 'selling_price_ty']


# Story 3: Rank Decline (SKU009 Amazon) Aug 1 - Sep 15
mask_s3 = (df_fact['product_key'] == 'SKU009') & (df_fact['retailer_key'] == 1)
# Phase 1: Aug 1-10 (Baseline)
p1_idx = df_fact[mask_s3 & (df_fact['date_key'] >= datetime.date(2025, 8, 1)) & (df_fact['date_key'] <= datetime.date(2025, 8, 10))].index
df_fact.loc[p1_idx, 'organic_rank_ty'] = 8
df_fact.loc[p1_idx, 'total_visits_ty'] = 2500
df_fact.loc[p1_idx, 'cvr_ty'] = 0.05

# Phase 2: Aug 11-31 (Decline)
# Gradual decline logic... simplified
p2_idx = df_fact[mask_s3 & (df_fact['date_key'] >= datetime.date(2025, 8, 11)) & (df_fact['date_key'] <= datetime.date(2025, 8, 31))].index
df_fact.loc[p2_idx, 'organic_rank_ty'] = np.linspace(10, 16, len(p2_idx)).astype(int)
df_fact.loc[p2_idx, 'total_visits_ty'] = np.linspace(2300, 1850, len(p2_idx)).astype(int)

# Phase 3: Sep 1-15 (Recovery)
p3_idx = df_fact[mask_s3 & (df_fact['date_key'] >= datetime.date(2025, 9, 1)) & (df_fact['date_key'] <= datetime.date(2025, 9, 15))].index
df_fact.loc[p3_idx, 'content_score'] = 89
df_fact.loc[p3_idx, 'is_sponsored_product'] = True
df_fact.loc[p3_idx, 'paid_rank_ty'] = 3
df_fact.loc[p3_idx, 'organic_rank_ty'] = np.linspace(15, 10, len(p3_idx)).astype(int)
df_fact.loc[p3_idx, 'total_visits_ty'] = np.linspace(1900, 2200, len(p3_idx)).astype(int)
df_fact.loc[p3_idx, 'sponsored_product_sales_ty'] = 3500 # Flat for simplicity
df_fact.loc[p3_idx, 'sponsored_product_units_ty'] = int(3500 / 129.99)

# Recalc sales for S3
for idx_set in [p1_idx, p2_idx, p3_idx]:
    df_fact.loc[idx_set, 'total_orders_ty'] = (df_fact.loc[idx_set, 'total_visits_ty'] * df_fact.loc[idx_set, 'cvr_ty']).astype(int)
    df_fact.loc[idx_set, 'gross_units_sold_ty'] = df_fact.loc[idx_set, 'total_orders_ty']
    # Add sponsored units if any
    df_fact.loc[idx_set, 'gross_units_sold_ty'] += df_fact.loc[idx_set, 'sponsored_product_units_ty'].fillna(0)
    df_fact.loc[idx_set, 'gross_sales_usd_ty'] = df_fact.loc[idx_set, 'gross_units_sold_ty'] * df_fact.loc[idx_set, 'selling_price_ty']


# Story 5: Prolonged OOS (SKU012 Amazon) Jun 15 - Jul 31
mask_s5 = (df_fact['product_key'] == 'SKU012') & (df_fact['retailer_key'] == 1)
# Phase 2: Jun 26 - Jul 10 (OOS)
p2_idx = df_fact[mask_s5 & (df_fact['date_key'] >= datetime.date(2025, 6, 26)) & (df_fact['date_key'] <= datetime.date(2025, 7, 10))].index
df_fact.loc[p2_idx, 'is_out_of_stock'] = True
df_fact.loc[p2_idx, 'oos_days_ty'] = 1
df_fact.loc[p2_idx, 'oos_percent_ty'] = 1.0
df_fact.loc[p2_idx, 'gross_sales_usd_ty'] = 0
df_fact.loc[p2_idx, 'gross_units_sold_ty'] = 0
df_fact.loc[p2_idx, 'total_orders_ty'] = 0
df_fact.loc[p2_idx, 'organic_rank_ty'] = np.linspace(7, 12, len(p2_idx)).astype(int)

# Phase 3: Jul 11-25 (Recovery)
p3_idx = df_fact[mask_s5 & (df_fact['date_key'] >= datetime.date(2025, 7, 11)) & (df_fact['date_key'] <= datetime.date(2025, 7, 25))].index
df_fact.loc[p3_idx, 'is_out_of_stock'] = False
df_fact.loc[p3_idx, 'gross_sales_usd_ty'] = 6000
df_fact.loc[p3_idx, 'gross_units_sold_ty'] = 100
df_fact.loc[p3_idx, 'organic_rank_ty'] = np.linspace(10, 8, len(p3_idx)).astype(int)


# ---------------------------------------------------------
# 4. Calculate Last Year Metrics
# ---------------------------------------------------------
print("Calculating LY Metrics...")
# Self join on date - 365 days
# Create a lookup dataframe
df_lookup = df_fact[['date_key', 'product_key', 'retailer_key', 'gross_sales_usd_ty', 'gross_units_sold_ty', 'oos_days_ty', 'oos_percent_ty', 'unit_price_ty', 'selling_price_ty', 'content_score', 'cvr_ty', 'total_orders_ty', 'total_visits_ty', 'organic_rank_ty', 'paid_rank_ty']].copy()
df_lookup['next_year_date'] = df_lookup['date_key'].apply(lambda x: x + datetime.timedelta(days=365))

# Merge
df_fact = df_fact.merge(df_lookup, left_on=['date_key', 'product_key', 'retailer_key'], right_on=['next_year_date', 'product_key', 'retailer_key'], how='left', suffixes=('', '_ly'))

# Rename _ly columns to match schema
ly_cols = {
    'gross_sales_usd_ty_ly': 'gross_sales_usd_ly',
    'gross_units_sold_ty_ly': 'gross_units_sold_ly',
    'oos_days_ty_ly': 'oos_days_ly',
    'oos_percent_ty_ly': 'oos_percent_ly',
    'unit_price_ty_ly': 'unit_price_ly',
    'selling_price_ty_ly': 'selling_price_ly',
    'content_score_ly': 'content_score_ly', # Not in schema but useful? Schema doesn't have content_score_ly.
    'cvr_ty_ly': 'cvr_ly',
    'total_orders_ty_ly': 'total_orders_ly',
    'total_visits_ty_ly': 'total_visits_ly',
    'organic_rank_ty_ly': 'organic_rank_ly',
    'paid_rank_ty_ly': 'paid_rank_ly'
}
df_fact.rename(columns=ly_cols, inplace=True)

# Fill NaNs for LY (first year data)
for col in ly_cols.values():
    if col in df_fact.columns:
        df_fact[col] = df_fact[col].fillna(0) # Or fill with some heuristic if needed

# Fiscly and Gregly - simplified to equal LY for demo
for col in ['gross_sales_usd', 'gross_units_sold']:
    df_fact[f'{col}_fiscly'] = df_fact[f'{col}_ly']
    df_fact[f'{col}_gregly'] = df_fact[f'{col}_ly']

# Generate Keys
df_fact['retail_summary_key'] = [str(uuid.uuid4()) for _ in range(len(df_fact))]
df_fact['retailer_product_key'] = df_fact['retailer_key'].astype(str) + '-' + df_fact['product_key']
df_fact['record_created_date'] = datetime.datetime.now()
df_fact['record_updated_date'] = datetime.datetime.now()

# Select columns matching DDL
summary_cols = [
    'retail_summary_key', 'retailer_product_key', 'brand_key', 'region_key', 'retailer_key', 'product_key',
    'week_end_date', 'month_start_date', 'date_key', 'last_year_date', 'fiscly_date', 'gregly_date',
    'gross_sales_usd_ty', 'gross_units_sold_ty',
    'gross_sales_usd_ly', 'gross_units_sold_ly', 'gross_sales_usd_fiscly', 'gross_units_sold_fiscly', 'gross_sales_usd_gregly', 'gross_units_sold_gregly',
    'is_out_of_stock', 'oos_days_ty', 'oos_percent_ty', 'oos_days_ly', 'oos_percent_ly',
    'unit_price_ty', 'selling_price_ty', 'unit_price_ly', 'selling_price_ly',
    'content_score', 'title_score', 'desc_score', 'image_score', 'keyword_score', 'rating_score', 'review_score',
    'is_sponsored_product', 'sponsored_product_sales_ty', 'sponsored_product_units_ty', 'sponsored_product_sales_ly', 'sponsored_product_units_ly',
    'total_orders_ty', 'total_visits_ty', 'cvr_ty', 'total_orders_ly', 'total_visits_ly', 'cvr_ly',
    'organic_rank_ty', 'paid_rank_ty', 'organic_rank_ly', 'paid_rank_ly',
    'review_rating', 'review_count',
    'record_created_date', 'record_updated_date'
]

# Ensure all columns exist
for c in summary_cols:
    if c not in df_fact.columns:
        df_fact[c] = None # Fill missing with None/NaN

df_fact[summary_cols].to_csv(os.path.join(OUTPUT_DIR, 'fact_retail_summary_tbl.csv'), index=False)


# ---------------------------------------------------------
# 5. Fact Retail Media Generation
# ---------------------------------------------------------
print("Generating Fact Retail Media...")
# Generate campaigns
campaigns = [
    {'campaign_name': 'Summer_Electronics_2025', 'brand_key': 1, 'retailer_key': 1, 'media_type': 'Sponsored Products', 'placement_type': 'Search', 'start': datetime.date(2025, 6, 1), 'end': datetime.date(2025, 8, 31)},
    {'campaign_name': 'Holiday_SmartHome_2024', 'brand_key': 2, 'retailer_key': 1, 'media_type': 'Sponsored Brands', 'placement_type': 'Homepage', 'start': datetime.date(2024, 11, 1), 'end': datetime.date(2024, 12, 31)},
    {'campaign_name': 'Q1_Fitness_Launch_2025', 'brand_key': 3, 'retailer_key': 2, 'media_type': 'Display', 'placement_type': 'Category', 'start': datetime.date(2025, 1, 15), 'end': datetime.date(2025, 3, 31)},
    {'campaign_name': 'Prime_Day_TechNova_2025', 'brand_key': 1, 'retailer_key': 1, 'media_type': 'Sponsored Products', 'placement_type': 'Search', 'start': datetime.date(2025, 7, 15), 'end': datetime.date(2025, 7, 16)},
    {'campaign_name': 'Back_to_School_Gadgets', 'brand_key': 6, 'retailer_key': 3, 'media_type': 'Sponsored Products', 'placement_type': 'Product Detail', 'start': datetime.date(2024, 8, 1), 'end': datetime.date(2024, 9, 15)},
    # Add optimized campaign for Story 4
    {'campaign_name': 'Summer_Electronics_Optimized_Aug', 'brand_key': 1, 'retailer_key': 1, 'media_type': 'Sponsored Products', 'placement_type': 'Product Detail', 'start': datetime.date(2025, 8, 1), 'end': datetime.date(2025, 8, 31)}
]

media_rows = []
for camp in campaigns:
    curr_date = camp['start']
    while curr_date <= camp['end']:
        # Story 4 Logic
        if camp['campaign_name'] == 'Summer_Electronics_2025':
            if datetime.date(2025, 7, 1) <= curr_date <= datetime.date(2025, 7, 15):
                spend = 5000
                impressions = 500000
                clicks = 7500
                sales = 18000
            elif datetime.date(2025, 7, 16) <= curr_date <= datetime.date(2025, 7, 31):
                spend = 5000
                impressions = 650000
                clicks = 8500
                sales = 14000 # ROAS drop
            elif datetime.date(2025, 8, 1) <= curr_date <= datetime.date(2025, 8, 15):
                spend = 2000
                impressions = 250000
                clicks = 3200
                sales = 7200
            else: # Rest of Aug
                spend = 2000
                impressions = 250000
                clicks = 3200
                sales = 7200
        elif camp['campaign_name'] == 'Summer_Electronics_Optimized_Aug':
             spend = 3000
             impressions = 180000
             clicks = 4500
             sales = 12000
        else:
            # Generic logic
            spend = random.uniform(100, 1000)
            impressions = int(spend * random.uniform(50, 200))
            clicks = int(impressions * random.uniform(0.005, 0.02))
            sales = spend * random.uniform(2.5, 5.0)

        media_rows.append({
            'retailer_media_key': str(uuid.uuid4()),
            'region_key': 1, # Simplified
            'brand_key': camp['brand_key'],
            'retailer_key': camp['retailer_key'],
            'date_key': curr_date,
            'campaign_name': camp['campaign_name'],
            'media_type': camp['media_type'],
            'placement_type': camp['placement_type'],
            'spend_ty': spend,
            'impressions_ty': impressions,
            'clicks_ty': clicks,
            'click_sales_ty': sales,
            'click_through_rate_ty': clicks/impressions if impressions > 0 else 0,
            'cost_per_click_ty': spend/clicks if clicks > 0 else 0,
            'click_roas_ty': sales/spend if spend > 0 else 0,
            'cvr_ty': random.uniform(0.03, 0.08),
            'record_created_date': datetime.datetime.now(),
            'record_updated_date': datetime.datetime.now()
        })
        curr_date += datetime.timedelta(days=1)

df_media = pd.DataFrame(media_rows)
# Fill missing columns with defaults
for c in ['ly_date', 'fiscly_date', 'gregly_date', 'spend_ly', 'impressions_ly', 'clicks_ly', 'click_sales_ly', 'click_roas_ly']:
    df_media[c] = None # Simplified
df_media.to_csv(os.path.join(OUTPUT_DIR, 'fact_retail_media_tbl.csv'), index=False)


# ---------------------------------------------------------
# 6. Fact Retail Search Rank Generation
# ---------------------------------------------------------
print("Generating Fact Retail Search Rank...")
# Generate based on summary data to ensure consistency
# We'll sample from summary where organic_rank_ty is not null
df_rank_source = df_fact[df_fact['organic_rank_ty'].notna()].sample(frac=0.2) # 20% of rows
rank_rows = []
keywords_map = {
    'SKU001': ['technova earbuds', 'wireless earbuds', 'bluetooth headphones'],
    'SKU003': ['360 wifi camera indoor', 'smart security camera', 'home camera'],
    'SKU009': ['smart thermostat', 'wifi thermostat', 'energy saving thermostat']
}

for _, row in df_rank_source.iterrows():
    prod = row['product_key']
    kws = keywords_map.get(prod, [f'keyword {prod} 1', f'keyword {prod} 2'])
    
    for kw in kws:
        rank = row['organic_rank_ty']
        # Adjust rank based on keyword type
        if 'technova' in kw or '360' in kw: # Branded/Specific
            rank = max(1, rank - 10)
        else:
            rank = rank + random.randint(0, 20)
            
        rank_rows.append({
            'search_rank_key': str(uuid.uuid4()),
            'retailer_product_key': row['retailer_product_key'],
            'region_key': row['region_key'],
            'brand_key': row['brand_key'],
            'retailer_key': row['retailer_key'],
            'product_key': prod,
            'date_key': row['date_key'],
            'search_result_type': 'Organic',
            'keyword': kw,
            'keyword_position': rank,
            'is_hero': row['is_hero_product'], # Wait, is_hero_product is in df_fact? Yes merged.
            'record_created_date': datetime.datetime.now(),
            'record_updated_date': datetime.datetime.now()
        })

df_rank = pd.DataFrame(rank_rows)
df_rank.to_csv(os.path.join(OUTPUT_DIR, 'fact_retail_search_rank_tbl.csv'), index=False)


# ---------------------------------------------------------
# 7. Mobility Tables
# ---------------------------------------------------------
print("Generating Mobility Tables...")

# Product Mob
df_prod_mob = df_fact.groupby(['region_key', 'retailer_key', 'brand_key', 'product_key', 'date_key']).agg({
    'gross_sales_usd_ty': 'sum',
    'gross_sales_usd_fiscly': 'sum',
    'gross_sales_usd_gregly': 'sum'
}).reset_index()
df_prod_mob.rename(columns={'gross_sales_usd_ty': 'gross_sales_ty', 'gross_sales_usd_fiscly': 'gross_sales_fiscly', 'gross_sales_usd_gregly': 'gross_sales_gregly'}, inplace=True)
df_prod_mob['sku_mob_key'] = df_prod_mob.apply(lambda x: f"{x['retailer_key']}-{x['product_key']}-{x['date_key']}", axis=1)
df_prod_mob['retailer_product_key'] = df_prod_mob['retailer_key'].astype(str) + '-' + df_prod_mob['product_key']
df_prod_mob['record_created_date'] = datetime.datetime.now()
df_prod_mob['record_updated_date'] = datetime.datetime.now()
df_prod_mob.to_csv(os.path.join(OUTPUT_DIR, 'fact_retail_product_mob_tbl.csv'), index=False)

# Retailer Mob
df_ret_mob = df_fact.groupby(['region_key', 'retailer_key', 'date_key']).agg({
    'gross_sales_usd_ty': 'sum',
    'gross_sales_usd_fiscly': 'sum',
    'gross_sales_usd_gregly': 'sum'
}).reset_index()
df_ret_mob.rename(columns={'gross_sales_usd_ty': 'gross_sales_ty', 'gross_sales_usd_fiscly': 'gross_sales_fiscly', 'gross_sales_usd_gregly': 'gross_sales_gregly'}, inplace=True)
df_ret_mob['retailer_mob_key'] = df_ret_mob.apply(lambda x: f"{x['retailer_key']}-{x['date_key']}", axis=1)
df_ret_mob['record_created_date'] = datetime.datetime.now()
df_ret_mob['record_updated_date'] = datetime.datetime.now()
df_ret_mob.to_csv(os.path.join(OUTPUT_DIR, 'fact_retail_retailer_mob_tbl.csv'), index=False)

# Brand Mob
df_brand_mob = df_fact.groupby(['region_key', 'brand_key', 'date_key']).agg({
    'gross_sales_usd_ty': 'sum',
    'gross_sales_usd_fiscly': 'sum',
    'gross_sales_usd_gregly': 'sum'
}).reset_index()
df_brand_mob.rename(columns={'gross_sales_usd_ty': 'gross_sales_ty', 'gross_sales_usd_fiscly': 'gross_sales_fiscly', 'gross_sales_usd_gregly': 'gross_sales_gregly'}, inplace=True)
df_brand_mob['brand_mob_key'] = df_brand_mob.apply(lambda x: f"{x['brand_key']}-{x['date_key']}", axis=1)
df_brand_mob['record_created_date'] = datetime.datetime.now()
df_brand_mob['record_updated_date'] = datetime.datetime.now()
df_brand_mob.to_csv(os.path.join(OUTPUT_DIR, 'fact_retail_brand_mob_tbl.csv'), index=False)

print("Data Generation Complete.")
