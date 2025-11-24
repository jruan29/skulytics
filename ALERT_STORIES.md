# Skulytics Demo Alert Stories

The following scenarios have been engineered into the dataset to support specific demo flows.

## Story 1: Conversion Drop Crisis
- **Product:** SKU003 (SmartHome WiFi Camera 360)
- **Retailer:** Amazon
- **Timeline:** Oct 15 - Nov 18, 2025
- **Narrative:** A perfect storm of OOS, negative reviews, and rank drop causes a 35% conversion decline.
- **Key Data Points:**
    - CVR drops from 4.0% to 2.6%.
    - Review rating drops from 4.2 to 3.7.
    - OOS for 7 days in late October.

## Story 2: Content Health Transformation
- **Products:** SKU015 (Walmart), SKU022 (Amazon)
- **Timeline:** Sep 1 - Oct 31, 2025
- **Narrative:** Products with poor content scores (40-60) receive an AI overhaul on Sep 16, leading to improved scores (85+) and sales uplift (+82%).
- **Key Data Points:**
    - Content Score jumps from ~48 to ~85 on Sep 16.
    - Sales and Traffic increase significantly in following weeks.

## Story 3: Rank Decline and Recovery
- **Product:** SKU009 (Smart Thermostat)
- **Retailer:** Amazon
- **Timeline:** Aug 1 - Sep 15, 2025
- **Narrative:** Organic rank slips from pos 8 to 16, causing traffic loss. Recovery via paid ads (Sep 3) and content optimization restores rank.
- **Key Data Points:**
    - Organic Rank degrades over August.
    - Paid Ads start Sep 3 (Rank 3).
    - Organic Rank recovers in September.

## Story 4: Media Efficiency Decline
- **Campaign:** Summer_Electronics_2025
- **Timeline:** Jul 1 - Aug 31, 2025
- **Narrative:** ROAS drops below 3.0 due to ad fatigue. Budget is reallocated to a new optimized campaign (`Summer_Electronics_Optimized_Aug`) which achieves ROAS 4.0+.
- **Key Data Points:**
    - `click_roas_ty` drops to ~2.8 in late July.
    - New campaign starts Aug 1 with high ROAS.

## Story 5: Prolonged OOS Impact
- **Product:** SKU012 (TechNova Wireless Charging Pad)
- **Retailer:** Amazon
- **Timeline:** Jun 15 - Jul 31, 2025
- **Narrative:** Hero product goes OOS for 15 days (Jun 26 - Jul 10), losing rank and sales. Recovery is slow.
- **Key Data Points:**
    - `is_out_of_stock` = TRUE for 15 consecutive days.
    - Sales = 0 during OOS.
    - Organic Rank degrades and slowly recovers.
