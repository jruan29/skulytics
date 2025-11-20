import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Skulytics - eCommerce Performance Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for production-quality styling
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background-color: #FFFFFF;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Navigation Bar */
    .nav-container {
        background-color: #11377C;
        padding: 15px 30px;
        margin: -70px -70px 30px -70px;
        border-radius: 0;
    }
    
    .nav-title {
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin: 0;
    }
    
    /* Filter Bar Styles */
    .filter-bar {
        background-color: #EFEFEF;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Alert Cards */
    .alert-card {
        background: white;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .alert-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .alert-urgent {
        border-left: 4px solid #DC3545;
    }
    
    .alert-monitor {
        border-left: 4px solid #FF8300;
    }
    
    .alert-opportunity {
        border-left: 4px solid #1CB192;
    }
    
    .alert-info {
        border-left: 4px solid #0075FF;
    }
    
    /* KPI Tiles */
    .kpi-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #1CB192;
        height: 100%;
    }
    
    .kpi-label {
        color: #6C757D;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        color: #000000;
        font-size: 28px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .kpi-change-positive {
        color: #28A745;
        font-size: 14px;
        font-weight: 600;
    }
    
    .kpi-change-negative {
        color: #DC3545;
        font-size: 14px;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Primary Button (Orange) */
    .primary-btn {
        background-color: #FF8300 !important;
        color: white !important;
    }
    
    /* Secondary Button (Teal) */
    .secondary-btn {
        background-color: #1CB192 !important;
        color: white !important;
    }
    
    /* Active Filter Badge */
    .active-filter {
        background-color: #FFF3E0;
        border: 1px solid #FF8300;
        border-left: 4px solid #FF8300;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    /* Commerce Journey Funnel */
    .funnel-stage {
        background: white;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .funnel-stage-healthy {
        border-left: 4px solid #1CB192;
    }
    
    .funnel-stage-warning {
        border-left: 4px solid #FF8300;
    }
    
    .funnel-stage-critical {
        border-left: 4px solid #DC3545;
    }
    
    /* Modal/Dialog Styles */
    .modal-content {
        background: white;
        border: 2px solid #FF8300;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    /* Chat Panel */
    .chat-panel {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    .chat-message-user {
        background: #E3F2FD;
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
        margin-left: 20%;
    }
    
    .chat-message-ai {
        background: #F8F9FA;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
        margin-right: 20%;
    }
    
    /* Content Crafter Columns */
    .content-column-existing {
        background: #F8F9FA;
        border: 1px solid #6C757D;
        border-radius: 8px;
        padding: 16px;
    }
    
    .content-column-improved {
        background: white;
        border: 2px solid #1CB192;
        border-radius: 8px;
        padding: 16px;
    }
    
    .content-column-impact {
        background: #E3F2FD;
        border: 1px solid #0075FF;
        border-radius: 8px;
        padding: 16px;
    }
    
    /* Score Badges */
    .score-badge-red {
        background: #DC3545;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    
    .score-badge-yellow {
        background: #FF8300;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    
    .score-badge-green {
        background: #28A745;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    
    /* Impact Box */
    .impact-box {
        background: #E8F5E9;
        border: 2px solid #28A745;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
    }
    
    /* Improvements Checklist */
    .improvement-item {
        padding: 8px 0;
        border-bottom: 1px solid #E0E0E0;
    }
    
    /* Custom Metric Cards */
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #F8F9FA;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_module' not in st.session_state:
    st.session_state.selected_module = "Main Dashboard"
if 'filter_month' not in st.session_state:
    st.session_state.filter_month = "November 2025"
if 'filter_retailer' not in st.session_state:
    st.session_state.filter_retailer = "All Retailers"
if 'filter_category' not in st.session_state:
    st.session_state.filter_category = "All Categories"
if 'filter_sku' not in st.session_state:
    st.session_state.filter_sku = "All SKUs"
if 'filter_brand' not in st.session_state:
    st.session_state.filter_brand = "All Brands"
if 'filters_visible' not in st.session_state:
    st.session_state.filters_visible = True
if 'alert_clicked' not in st.session_state:
    st.session_state.alert_clicked = None
if 'simulate_modal_open' not in st.session_state:
    st.session_state.simulate_modal_open = False
if 'chat_open' not in st.session_state:
    st.session_state.chat_open = False
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'content_deployed' not in st.session_state:
    st.session_state.content_deployed = False
if 'show_impact_tracking' not in st.session_state:
    st.session_state.show_impact_tracking = False

# Load data
@st.cache_data
def load_data():
    sku_data = pd.read_csv('sku_data.csv')
    performance_data = pd.read_csv('performance_data.csv')
    content_data = pd.read_csv('content_data.csv')
    timeseries_data = pd.read_csv('timeseries_data.csv')
    monthly_sales = pd.read_csv('monthly_sales.csv')
    sku003_monthly = pd.read_csv('sku003_monthly.csv')
    top_products = pd.read_csv('top_products.csv')
    
    return sku_data, performance_data, content_data, timeseries_data, monthly_sales, sku003_monthly, top_products

sku_data, performance_data, content_data, timeseries_data, monthly_sales, sku003_monthly, top_products = load_data()

# Navigation Bar
def render_navigation():
    st.markdown('<div class="nav-container"><h1 class="nav-title">📊 Skulytics - eCommerce Performance Intelligence</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])
    
    with col1:
        if st.button("🏠 Main Dashboard", key="nav_main", use_container_width=True):
            st.session_state.selected_module = "Main Dashboard"
            st.rerun()
    
    with col2:
        if st.button("📈 Product Performance", key="nav_product", use_container_width=True):
            st.session_state.selected_module = "Product Performance"
            st.rerun()
    
    with col3:
        if st.button("✍️ Content Crafter", key="nav_content", use_container_width=True):
            st.session_state.selected_module = "Content Crafter"
            st.rerun()
    
    with col4:
        st.button("📊 Demand Forecasting*", key="nav_demand", disabled=True, use_container_width=True)
    
    with col5:
        st.button("💰 Media Spend*", key="nav_media", disabled=True, use_container_width=True)
    
    with col6:
        st.button("🔍 Competitor Intel*", key="nav_competitor", disabled=True, use_container_width=True)

# Filter Bar
def render_filters():
    if st.session_state.filters_visible:
        st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
        
        with col1:
            st.session_state.filter_month = st.selectbox(
                "Month/Year",
                ["November 2025", "October 2025", "September 2025"],
                key="month_filter"
            )
        
        with col2:
            st.session_state.filter_retailer = st.selectbox(
                "Channel Partner",
                ["All Retailers", "Walmart", "Target", "Amazon", "Kroger", "Costco"],
                key="retailer_filter"
            )
        
        with col3:
            st.session_state.filter_category = st.selectbox(
                "Product Category",
                ["All Categories", "Snacks", "Beverages", "Household", "Personal Care", "Health", "Pet Care"],
                key="category_filter"
            )
        
        with col4:
            sku_options = ["All SKUs"] + [f"{row['sku_id']} ({row['sku_name']})" for _, row in sku_data.iterrows()]
            st.session_state.filter_sku = st.selectbox(
                "SKU",
                sku_options,
                key="sku_filter"
            )
        
        with col5:
            st.session_state.filter_brand = st.selectbox(
                "Brand",
                ["All Brands", "CleanHome", "PureVitality", "EcoFresh", "BrewMasters", "SnackSmart", "PetWellness"],
                key="brand_filter"
            )
        
        with col6:
            st.write("")
            st.write("")
            if st.button("🔽 Hide", key="hide_filters"):
                st.session_state.filters_visible = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        col1, col2, col3 = st.columns([5, 2, 5])
        with col2:
            if st.button("🔼 Show Filters", key="show_filters"):
                st.session_state.filters_visible = True
                st.rerun()

# Main Dashboard Module
def render_main_dashboard():
    st.markdown("## 🎯 Commerce Journey Hub")
    
    # Alert Panel
    st.markdown("### 🔔 Active Alerts")
    
    alert_cols = st.columns(5)
    
    # Alert 1: URGENT (SKU003)
    with alert_cols[0]:
        st.markdown("""
        <div class="alert-card alert-urgent">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 20px;">⚠️</span>
                <span style="background: #DC3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold;">URGENT</span>
            </div>
            <h4 style="margin: 10px 0; font-size: 14px;">SKU003 - Conversion Down 22%</h4>
            <p style="font-size: 11px; color: #6C757D; margin: 5px 0;">OOS Days ↑150%, Rating ↓0.4 stars at Target</p>
            <p style="font-size: 10px; color: #999;">2 hours ago</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔍 Investigate", key="alert1_investigate", use_container_width=True):
                st.session_state.alert_clicked = "alert_1"
                st.session_state.filter_sku = "SKU003 (Multi-Purpose Cleaner)"
                st.session_state.filter_retailer = "Target"
                st.rerun()
        with col_btn2:
            if st.button("💬 Ask Chat", key="alert1_chat", use_container_width=True):
                st.session_state.chat_open = True
                st.session_state.chat_messages = [
                    {"role": "user", "content": "Why did conversion rate drop for SKU003 at Target, and what should I do?"}
                ]
                st.rerun()
    
    # Alert 2: MONITOR
    with alert_cols[1]:
        st.markdown("""
        <div class="alert-card alert-monitor">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 20px;">⚡</span>
                <span style="background: #FF8300; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold;">MONITOR</span>
            </div>
            <h4 style="margin: 10px 0; font-size: 14px;">SKU002 - Views Down 15%</h4>
            <p style="font-size: 11px; color: #6C757D; margin: 5px 0;">Organic rank dropped #4 → #8 at Walmart</p>
            <p style="font-size: 10px; color: #999;">5 hours ago</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.button("🔍 Investigate", key="alert2_investigate", use_container_width=True)
        with col_btn2:
            st.button("💬 Ask Chat", key="alert2_chat", use_container_width=True)
    
    # Alert 3: OPPORTUNITY
    with alert_cols[2]:
        st.markdown("""
        <div class="alert-card alert-opportunity">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 20px;">🎯</span>
                <span style="background: #1CB192; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold;">OPPORTUNITY</span>
            </div>
            <h4 style="margin: 10px 0; font-size: 14px;">SKU001 - ROAS Up 45%</h4>
            <p style="font-size: 11px; color: #6C757D; margin: 5px 0;">Paid media efficiency up. Consider budget increase</p>
            <p style="font-size: 10px; color: #999;">1 day ago</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.button("📊 View Details", key="alert3_view", use_container_width=True)
        with col_btn2:
            st.button("💬 Ask Chat", key="alert3_chat", use_container_width=True)
    
    # Alert 4: MONITOR
    with alert_cols[3]:
        st.markdown("""
        <div class="alert-card alert-monitor">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 20px;">📦</span>
                <span style="background: #FF8300; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold;">MONITOR</span>
            </div>
            <h4 style="margin: 10px 0; font-size: 14px;">SKU007 - Low Stock</h4>
            <p style="font-size: 11px; color: #6C757D; margin: 5px 0;">3 days supply at Kroger. Restock recommended</p>
            <p style="font-size: 10px; color: #999;">6 hours ago</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.button("🔍 Investigate", key="alert4_investigate", use_container_width=True)
        with col_btn2:
            st.button("💬 Ask Chat", key="alert4_chat", use_container_width=True)
    
    # Alert 5: INFO
    with alert_cols[4]:
        st.markdown("""
        <div class="alert-card alert-info">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 20px;">ℹ️</span>
                <span style="background: #0075FF; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold;">INFO</span>
            </div>
            <h4 style="margin: 10px 0; font-size: 14px;">SKU005 - Content Updated</h4>
            <p style="font-size: 11px; color: #6C757D; margin: 5px 0;">Deployed at Costco. Impact tracking enabled</p>
            <p style="font-size: 10px; color: #999;">3 days ago</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.button("📈 Track Impact", key="alert5_track", use_container_width=True)
    
    st.markdown("---")
    
    # Active Filter Badge (conditional)
    if st.session_state.alert_clicked:
        st.markdown(f"""
        <div class="active-filter">
            <span style="font-size: 18px;">🔍</span>
            <span style="font-weight: bold; margin-left: 10px;">Active Filter: SKU003 | Target</span>
            <span style="float: right; cursor: pointer;">
        """, unsafe_allow_html=True)
        
        if st.button("✕ Clear Filters", key="clear_filters"):
            st.session_state.alert_clicked = None
            st.session_state.filter_sku = "All SKUs"
            st.session_state.filter_retailer = "All Retailers"
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("📊 View Full Product Analysis", key="view_product_analysis", use_container_width=False):
            st.session_state.selected_module = "Product Performance"
            st.rerun()
        
        st.markdown("---")
    
    # KPI Tile Grid
    st.markdown("### 📊 Key Performance Indicators")
    
    # Determine if filtered
    is_filtered = st.session_state.alert_clicked is not None
    
    # Row 1
    kpi_cols1 = st.columns(3)
    
    with kpi_cols1[0]:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-label">Gross Sales</div>', unsafe_allow_html=True)
        if is_filtered:
            st.markdown('<div class="kpi-value">$12,400</div>', unsafe_allow_html=True)
            st.markdown('<div class="kpi-change-negative">↓ 18% vs LW</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="kpi-value">$1,247,890</div>', unsafe_allow_html=True)
            st.markdown('<div class="kpi-change-positive">↑ 12.4% vs LM</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with kpi_cols1[1]:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-label">Units Sold</div>', unsafe_allow_html=True)
        if is_filtered:
            st.markdown('<div class="kpi-value">890</div>', unsafe_allow_html=True)
            st.markdown('<div class="kpi-change-negative">↓ 3.3% vs LW</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="kpi-value">18,432</div>', unsafe_allow_html=True)
            st.markdown('<div class="kpi-change-positive">↑ 8.2% vs LM</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with kpi_cols1[2]:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-label">Average CVR</div>', unsafe_allow_html=True)
        if is_filtered:
            st.markdown('<div class="kpi-value">2.8%</div>', unsafe_allow_html=True)
            st.markdown('<div class="kpi-change-negative">↓ 22% vs LW</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="kpi-value">3.4%</div>', unsafe_allow_html=True)
            st.markdown('<div class="kpi-change-negative">↓ 2.1% vs LM</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2
    kpi_cols2 = st.columns(3)
    
    with kpi_cols2[0]:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-label">Avg Organic Rank</div>', unsafe_allow_html=True)
        if is_filtered:
            st.markdown('<div class="kpi-value">#3</div>', unsafe_allow_html=True)
            st.markdown('<div style="color: #6C757D; font-size: 14px;">Stable</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="kpi-value">#6.2</div>', unsafe_allow_html=True)
            st.markdown('<div style="color: #6C757D; font-size: 14px;">Stable</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with kpi_cols2[1]:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-label">OOS %</div>', unsafe_allow_html=True)
        if is_filtered:
            st.markdown('<div class="kpi-value">⚠️ 8.5%</div>', unsafe_allow_html=True)
            st.markdown('<div class="kpi-change-negative">↑ 8.5pts vs LW</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="kpi-value">4.2%</div>', unsafe_allow_html=True)
            st.markdown('<div class="kpi-change-negative">↑ 1.8% vs LM</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with kpi_cols2[2]:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-label">Content Health Score</div>', unsafe_allow_html=True)
        if is_filtered:
            st.markdown('<div class="kpi-value">58/100</div>', unsafe_allow_html=True)
            st.markdown('<div class="kpi-change-negative">↓ 33% vs LM</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="kpi-value">72/100</div>', unsafe_allow_html=True)
            st.markdown('<div class="kpi-change-negative">↓ 8pts vs LM</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3
    kpi_cols3 = st.columns(3)
    
    with kpi_cols3[0]:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-label">Total Media Spend</div>', unsafe_allow_html=True)
        st.markdown('<div class="kpi-value">$124,500</div>', unsafe_allow_html=True)
        st.markdown('<div style="color: #0075FF; font-size: 14px;">↑ 15% vs LM</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with kpi_cols3[1]:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-label">ROAS</div>', unsafe_allow_html=True)
        st.markdown('<div class="kpi-value">3.8x</div>', unsafe_allow_html=True)
        st.markdown('<div class="kpi-change-positive">↑ 0.4x vs LM</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with kpi_cols3[2]:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-label">Avg Paid Rank</div>', unsafe_allow_html=True)
        st.markdown('<div class="kpi-value">#4.1</div>', unsafe_allow_html=True)
        st.markdown('<div class="kpi-change-positive">↑ 2 spots vs LM</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Section
    st.markdown("### 📈 Performance Analytics")
    
    chart_cols = st.columns(2)
    
    with chart_cols[0]:
        st.markdown("**Monthly Sales Trend**")
        
        if is_filtered:
            # SKU003 filtered data
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=sku003_monthly['month'],
                y=sku003_monthly['sales'],
                mode='lines+markers',
                line=dict(color='#FF8300', width=3),
                marker=dict(color='#FF8300', size=10),
                name='SKU003 Sales'
            ))
            fig.update_layout(
                height=350,
                xaxis_title="Month",
                yaxis_title="Sales ($)",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Arial', size=12, color='#000000'),
                hovermode='x unified',
                showlegend=False
            )
            fig.update_yaxis(gridcolor='#E0E0E0', gridwidth=1)
        else:
            # Aggregate data
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=monthly_sales['month'],
                y=monthly_sales['total_sales'],
                mode='lines+markers',
                line=dict(color='#FF8300', width=3),
                marker=dict(color='#FF8300', size=10),
                name='Total Sales'
            ))
            fig.update_layout(
                height=350,
                xaxis_title="Month",
                yaxis_title="Sales ($)",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Arial', size=12, color='#000000'),
                hovermode='x unified',
                showlegend=False
            )
            fig.update_yaxis(gridcolor='#E0E0E0', gridwidth=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_cols[1]:
        st.markdown("**Top Products by Sales - November 2025**")
        
        # Determine colors
        if is_filtered:
            colors = ['#DC3545' if sku == 'SKU003' else '#1CB192' for sku in top_products['sku_id']]
        else:
            colors = ['#1CB192'] * len(top_products)
        
        fig = go.Figure(go.Bar(
            x=top_products['sales'],
            y=[f"{row['sku_id']}<br>{row['sku_name']}" for _, row in top_products.iterrows()],
            orientation='h',
            marker=dict(color=colors),
            text=top_products['sales'].apply(lambda x: f'${x:,.0f}'),
            textposition='outside'
        ))
        fig.update_layout(
            height=350,
            xaxis_title="Sales ($)",
            yaxis_title="",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial', size=11, color='#000000'),
            showlegend=False
        )
        fig.update_xaxis(gridcolor='#E0E0E0', gridwidth=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Commerce Journey Funnel
    st.markdown("### 🔄 Commerce Journey Performance")
    
    funnel_cols = st.columns(4)
    
    with funnel_cols[0]:
        if is_filtered:
            st.markdown("""
            <div class="funnel-stage funnel-stage-healthy">
                <div style="font-size: 40px; margin-bottom: 10px;">👁️</div>
                <h4 style="color: #11377C; margin: 10px 0;">Discovery</h4>
                <div style="font-size: 24px; font-weight: bold; color: #000;">48K Views</div>
                <div style="font-size: 14px; color: #6C757D; margin-top: 5px;">Avg Rank #3</div>
                <div style="margin-top: 10px; padding: 4px 12px; background: #28A745; color: white; border-radius: 12px; display: inline-block; font-size: 11px;">Healthy</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="funnel-stage funnel-stage-healthy">
                <div style="font-size: 40px; margin-bottom: 10px;">👁️</div>
                <h4 style="color: #11377C; margin: 10px 0;">Discovery</h4>
                <div style="font-size: 24px; font-weight: bold; color: #000;">245K Views</div>
                <div style="font-size: 14px; color: #6C757D; margin-top: 5px;">Avg Rank #6.2</div>
                <div style="margin-top: 10px; padding: 4px 12px; background: #28A745; color: white; border-radius: 12px; display: inline-block; font-size: 11px;">Healthy</div>
            </div>
            """, unsafe_allow_html=True)
    
    with funnel_cols[1]:
        if is_filtered:
            st.markdown("""
            <div class="funnel-stage funnel-stage-warning">
                <div style="font-size: 40px; margin-bottom: 10px;">👆</div>
                <h4 style="color: #11377C; margin: 10px 0;">Engagement</h4>
                <div style="font-size: 24px; font-weight: bold; color: #000;">16.8K Traffic</div>
                <div style="font-size: 14px; color: #6C757D; margin-top: 5px;">Content Score 58/100</div>
                <div style="margin-top: 10px; padding: 4px 12px; background: #FF8300; color: white; border-radius: 12px; display: inline-block; font-size: 11px;">Needs Work</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="funnel-stage funnel-stage-warning">
                <div style="font-size: 40px; margin-bottom: 10px;">👆</div>
                <h4 style="color: #11377C; margin: 10px 0;">Engagement</h4>
                <div style="font-size: 24px; font-weight: bold; color: #000;">89K Traffic</div>
                <div style="font-size: 14px; color: #6C757D; margin-top: 5px;">Content Score 72/100</div>
                <div style="margin-top: 10px; padding: 4px 12px; background: #FF8300; color: white; border-radius: 12px; display: inline-block; font-size: 11px;">Needs Work</div>
            </div>
            """, unsafe_allow_html=True)
    
    with funnel_cols[2]:
        if is_filtered:
            st.markdown("""
            <div class="funnel-stage funnel-stage-critical">
                <div style="font-size: 40px; margin-bottom: 10px;">🛒</div>
                <h4 style="color: #11377C; margin: 10px 0;">Conversion</h4>
                <div style="font-size: 24px; font-weight: bold; color: #000;">CVR 2.8%</div>
                <div style="font-size: 14px; color: #6C757D; margin-top: 5px;">5.2K Add-to-Cart</div>
                <div style="margin-top: 10px; padding: 4px 12px; background: #DC3545; color: white; border-radius: 12px; display: inline-block; font-size: 11px;">Critical</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="funnel-stage funnel-stage-warning">
                <div style="font-size: 40px; margin-bottom: 10px;">🛒</div>
                <h4 style="color: #11377C; margin: 10px 0;">Conversion</h4>
                <div style="font-size: 24px; font-weight: bold; color: #000;">CVR 3.4%</div>
                <div style="font-size: 14px; color: #6C757D; margin-top: 5px;">28.5K Add-to-Cart</div>
                <div style="margin-top: 10px; padding: 4px 12px; background: #FF8300; color: white; border-radius: 12px; display: inline-block; font-size: 11px;">Needs Work</div>
            </div>
            """, unsafe_allow_html=True)
    
    with funnel_cols[3]:
        if is_filtered:
            st.markdown("""
            <div class="funnel-stage funnel-stage-warning">
                <div style="font-size: 40px; margin-bottom: 10px;">💰</div>
                <h4 style="color: #11377C; margin: 10px 0;">Sales</h4>
                <div style="font-size: 24px; font-weight: bold; color: #000;">$12.4K</div>
                <div style="font-size: 14px; color: #6C757D; margin-top: 5px;">890 Units</div>
                <div style="margin-top: 10px; padding: 4px 12px; background: #FF8300; color: white; border-radius: 12px; display: inline-block; font-size: 11px;">Below Target</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="funnel-stage funnel-stage-healthy">
                <div style="font-size: 40px; margin-bottom: 10px;">💰</div>
                <h4 style="color: #11377C; margin: 10px 0;">Sales</h4>
                <div style="font-size: 24px; font-weight: bold; color: #000;">$1.24M</div>
                <div style="font-size: 14px; color: #6C757D; margin-top: 5px;">18.4K Units</div>
                <div style="margin-top: 10px; padding: 4px 12px; background: #28A745; color: white; border-radius: 12px; display: inline-block; font-size: 11px;">Healthy</div>
            </div>
            """, unsafe_allow_html=True)

# Product Performance Module
def render_product_performance():
    st.markdown("## 📈 Product Performance Analysis")
    
    # Alert Context Banner
    if st.session_state.alert_clicked:
        st.markdown("""
        <div style="background: #FFF3E0; border: 1px solid #FF8300; border-left: 4px solid #FF8300; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 24px; margin-right: 15px;">⚠️</span>
                <div>
                    <h4 style="margin: 0; color: #000;">SKU003 — Conversion Down 22%</h4>
                    <p style="margin: 5px 0 0 0; color: #6C757D;">Contributing Factors: OOS Days ↑150%, Rating ↓0.4 stars, Competitor Price Cut 15%</p>
                    <p style="margin: 5px 0 0 0; color: #6C757D; font-size: 13px;"><em>💡 AI Suggestion: Investigate root causes. Potential factors: out-of-stock for 3 days, negative review spike, competitor action.</em></p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI Metadata Tiles
    st.markdown("### 🎯 SKU003 Performance Snapshot")
    
    meta_row1 = st.columns(3)
    
    with meta_row1[0]:
        st.markdown("""
        <div class="kpi-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="kpi-label">Avg Organic Rank</div>
                <div style="width: 12px; height: 12px; background: #28A745; border-radius: 50%;"></div>
            </div>
            <div class="kpi-value">#3</div>
            <div style="color: #6C757D; font-size: 14px;">Stable</div>
            <div style="font-size: 12px; color: #999; margin-top: 5px;">No change vs. last week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with meta_row1[1]:
        st.markdown("""
        <div class="kpi-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="kpi-label">Avg Paid Rank</div>
                <div style="width: 12px; height: 12px; background: #FF8300; border-radius: 50%;"></div>
            </div>
            <div class="kpi-value">#7</div>
            <div class="kpi-change-negative">↓2 spots</div>
            <div style="font-size: 12px; color: #999; margin-top: 5px;">Declined from #5</div>
        </div>
        """, unsafe_allow_html=True)
    
    with meta_row1[2]:
        st.markdown("""
        <div class="kpi-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="kpi-label">Sales (Current Month)</div>
                <div style="width: 12px; height: 12px; background: #DC3545; border-radius: 50%;"></div>
            </div>
            <div class="kpi-value">$12,400</div>
            <div class="kpi-change-negative">↓18% WoW</div>
            <div style="font-size: 12px; color: #999; margin-top: 5px;">Down from $15,100</div>
        </div>
        """, unsafe_allow_html=True)
    
    meta_row2 = st.columns(3)
    
    with meta_row2[0]:
        st.markdown("""
        <div class="kpi-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="kpi-label">Stock Status</div>
                <div style="width: 12px; height: 12px; background: #DC3545; border-radius: 50%;"></div>
            </div>
            <div class="kpi-value">⚠️ OOS 3 Days</div>
            <div class="kpi-change-negative">Nov 10-12</div>
            <div style="font-size: 12px; color: #999; margin-top: 5px;">Restock Alert Sent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with meta_row2[1]:
        st.markdown("""
        <div class="kpi-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="kpi-label">P-Page Traffic</div>
                <div style="width: 12px; height: 12px; background: #FF8300; border-radius: 50%;"></div>
            </div>
            <div class="kpi-value">8,200</div>
            <div class="kpi-change-negative">↓8% WoW</div>
            <div style="font-size: 12px; color: #999; margin-top: 5px;">Down from 8,900</div>
        </div>
        """, unsafe_allow_html=True)
    
    with meta_row2[2]:
        st.markdown("""
        <div class="kpi-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="kpi-label">CVR (Conversion Rate)</div>
                <div style="width: 12px; height: 12px; background: #DC3545; border-radius: 50%;"></div>
            </div>
            <div class="kpi-value">2.8%</div>
            <div class="kpi-change-negative">↓22% WoW</div>
            <div style="font-size: 12px; color: #DC3545; margin-top: 5px; font-weight: 600;">⚠️ Primary Problem</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    st.markdown("### 📊 Comparative Analytics")
    
    chart_cols = st.columns(2)
    
    with chart_cols[0]:
        st.markdown("**SKU003 vs. Peer SKUs - Household Category at Target**")
        
        peer_skus = ['SKU006\nLaundry Detergent', 'SKU015\nDish Soap', 'SKU018\nWipes', 'SKU012\nGlass Cleaner', 
                     'SKU009\nFloor Cleaner', 'SKU003\nMulti-Purpose', 'SKU021\nBathroom Cleaner', 'SKU024\nKitchen Spray']
        peer_sales = [22000, 19000, 17000, 16000, 15000, 12400, 11000, 10000]
        colors = ['#DC3545' if 'SKU003' in sku else '#1CB192' for sku in peer_skus]
        
        fig = go.Figure(go.Bar(
            x=peer_sales,
            y=peer_skus,
            orientation='h',
            marker=dict(color=colors),
            text=[f'${s:,.0f}' for s in peer_sales],
            textposition='outside'
        ))
        fig.update_layout(
            height=350,
            xaxis_title="Sales ($)",
            yaxis_title="",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial', size=11, color='#000000'),
            showlegend=False
        )
        fig.update_xaxis(gridcolor='#E0E0E0', gridwidth=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_cols[1]:
        st.markdown("**SKU003 CVR Trend - Last 30 Days**")
        
        # Filter timeseries data
        ts_data = timeseries_data[timeseries_data['metric_name'] == 'cvr'].copy()
        ts_data['date'] = pd.to_datetime(ts_data['date'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ts_data['date'],
            y=ts_data['metric_value'],
            mode='lines+markers',
            line=dict(color='#0075FF', width=2),
            marker=dict(color='#0075FF', size=6),
            name='CVR'
        ))
        
        # Add OOS period shading
        fig.add_vrect(
            x0='2025-11-05', x1='2025-11-08',
            fillcolor='red', opacity=0.2,
            annotation_text="OOS Period", annotation_position="top left",
            annotation=dict(font_size=10, font_color="red")
        )
        
        fig.update_layout(
            height=350,
            xaxis_title="Date",
            yaxis_title="CVR (%)",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial', size=12, color='#000000'),
            hovermode='x unified',
            showlegend=False
        )
        fig.update_yaxis(gridcolor='#E0E0E0', gridwidth=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Opportunity Table
    st.markdown("### 🎯 Opportunity Analysis & Recommendations")
    
    opp_data = pd.DataFrame({
        'Issue Detected': [
            'CVR Drop 22%',
            'Rating Decline (4.6→4.2)',
            'Competitive Pressure',
            'Low Content Score (58/100)'
        ],
        'Root Cause': [
            '3-day stockout (Nov 10-12)',
            '3 new 1-star reviews mentioning "ineffective cleaning"',
            'Competitor EcoClean cut price by 15% (now $8.99 vs. $10.49)',
            'Image Score: 42/100 (only 3 images, no lifestyle), Description Score: 45/100'
        ],
        'Recommended Action': [
            'Restock immediately, prevent future OOS',
            'Launch review response campaign, address product concerns',
            'Test price match ($8.99) or promotional bundle',
            'Add 2 lifestyle images, expand description by 150 chars'
        ],
        'Forecasted Impact': [
            'CVR +1.1pts, Sales +$1,800',
            'Stabilize rating, prevent further decline',
            'Maintain market share, prevent further losses',
            'Organic Rank +2 spots (#3→#1), CVR +0.8pts, Sales +$1,200'
        ]
    })
    
    st.dataframe(opp_data, use_container_width=True, hide_index=True)
    
    st.markdown("")
    
    # Action buttons for each row
    action_cols = st.columns(4)
    
    with action_cols[0]:
        st.button("📊 View Details", key="opp1_btn", use_container_width=True)
    
    with action_cols[1]:
        st.button("👁️ View Reviews", key="opp2_btn", use_container_width=True)
    
    with action_cols[2]:
        st.button("💰 Simulate Price", key="opp3_btn", use_container_width=True)
    
    with action_cols[3]:
        if st.button("🔧 Simulate Fix", key="opp4_btn", use_container_width=True, type="primary"):
            st.session_state.simulate_modal_open = True
            st.rerun()
    
    # Scenario Simulator Modal
    if st.session_state.simulate_modal_open:
        st.markdown("---")
        st.markdown("### 🎯 Scenario Simulator: Content Score Improvement")
        
        sim_container = st.container()
        with sim_container:
            st.markdown("""
            <div class="modal-content">
                <h4 style="color: #11377C; margin-bottom: 20px;">📈 Impact Forecast</h4>
            </div>
            """, unsafe_allow_html=True)
            
            sim_cols = st.columns(2)
            
            with sim_cols[0]:
                st.markdown("**Current State**")
                st.metric("Image Score", "42/100", delta=None, delta_color="off")
                st.caption("3 product images only")
                st.metric("Description Score", "45/100", delta=None, delta_color="off")
                st.caption("120 characters (too short)")
            
            with sim_cols[1]:
                st.markdown("**After Improvements**")
                st.metric("Image Score", "85/100", delta="+43", delta_color="normal")
                st.caption("5 images (added 2 lifestyle shots)")
                st.metric("Description Score", "88/100", delta="+43", delta_color="normal")
                st.caption("270 characters (optimized)")
            
            st.markdown("**Forecasted Business Impact**")
            
            impact_cols = st.columns(4)
            
            with impact_cols[0]:
                st.metric("Content Score", "88/100", "+30pts (+52%)")
            
            with impact_cols[1]:
                st.metric("Organic Rank", "#1", "+2 spots")
            
            with impact_cols[2]:
                st.metric("CVR", "3.6%", "+0.8pts (+29%)")
            
            with impact_cols[3]:
                st.metric("Sales Lift", "$1,200", "over 2 weeks")
            
            st.progress(0.85, text="Confidence Level: 85%")
            
            st.markdown("")
            
            btn_cols = st.columns([3, 1, 1])
            
            with btn_cols[1]:
                if st.button("❌ Cancel", key="sim_cancel", use_container_width=True):
                    st.session_state.simulate_modal_open = False
                    st.rerun()
            
            with btn_cols[2]:
                if st.button("✅ Apply Changes", key="sim_apply", use_container_width=True, type="primary"):
                    with st.spinner("Applying changes..."):
                        time.sleep(2)
                    st.success("✅ Content update queued. Routing to Content Crafter for deployment.")
                    time.sleep(1)
                    st.session_state.simulate_modal_open = False
                    st.session_state.selected_module = "Content Crafter"
                    st.rerun()

# Content Crafter Module
def render_content_crafter():
    st.markdown("## ✍️ Content Crafter")
    
    # AI Suggestion Banner
    st.markdown("""
    <div style="background: #E0F7F4; border: 1px solid #1CB192; border-left: 4px solid #1CB192; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 24px; margin-right: 15px;">💡</span>
            <div>
                <h4 style="margin: 0; color: #000;">SKU003 — Content Score has dropped 33% at Target</h4>
                <p style="margin: 5px 0 0 0; color: #6C757D;"><em>AI Recommendation: Add lifestyle images and optimize description to improve SEO.</em></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Score Tiles
    st.markdown("### 📊 Content Health Scores")
    
    score_cols = st.columns(7)
    
    scores = [
        ("Overall", 58, "red"),
        ("Title", 72, "yellow"),
        ("Description", 45, "red"),
        ("Image", 42, "red"),
        ("Keyword", 55, "red"),
        ("Rating", 4.2, "yellow"),
        ("Review", 68, "yellow")
    ]
    
    for i, (label, score, color) in enumerate(scores):
        with score_cols[i]:
            if color == "red":
                bg_color = "#DC3545"
            elif color == "yellow":
                bg_color = "#FF8300"
            else:
                bg_color = "#28A745"
            
            # Highlight Image score
            border_style = "border: 3px solid #FF8300; box-shadow: 0 0 15px rgba(255,131,0,0.3);" if label == "Image" else ""
            
            if label == "Rating":
                st.markdown(f"""
                <div style="background: white; padding: 15px; border-radius: 8px; text-align: center; {border_style}">
                    <div style="font-size: 11px; color: #6C757D; font-weight: 600; text-transform: uppercase;">{label}</div>
                    <div style="font-size: 24px; font-weight: bold; color: {bg_color}; margin: 8px 0;">{score}/5</div>
                    <div style="padding: 3px 8px; background: {bg_color}; color: white; border-radius: 12px; font-size: 10px; display: inline-block;">⭐</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: white; padding: 15px; border-radius: 8px; text-align: center; {border_style}">
                    <div style="font-size: 11px; color: #6C757D; font-weight: 600; text-transform: uppercase;">{label}</div>
                    <div style="font-size: 24px; font-weight: bold; color: {bg_color}; margin: 8px 0;">{score}/100</div>
                    <div style="padding: 3px 8px; background: {bg_color}; color: white; border-radius: 12px; font-size: 10px; display: inline-block;">{color.upper()}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main Content Section: 3-Column Layout
    st.markdown("### 📝 Content Optimization")
    
    content_cols = st.columns(3)
    
    # Column 1: Existing Content
    with content_cols[0]:
        st.markdown('<div class="content-column-existing">', unsafe_allow_html=True)
        st.markdown("**Existing Content**")
        st.caption("Current state at Target")
        
        st.markdown("---")
        
        st.markdown("**Product Title**")
        st.text("Multi-Purpose Cleaner")
        st.caption("22 characters")
        st.error("⚠️ Missing keywords: 'eco-friendly', 'antibacterial', 'non-toxic'")
        st.error("⚠️ No brand mention")
        
        st.markdown("---")
        
        st.markdown("**Product Description**")
        st.text_area("", "Effective cleaning solution for multiple surfaces.", height=100, disabled=True, label_visibility="collapsed")
        st.caption("7 words | 54 characters")
        st.error("⚠️ 75% shorter than competitors (avg 215 chars)")
        st.error("⚠️ Missing ingredient information")
        st.error("⚠️ No benefit statements")
        
        st.markdown("---")
        
        st.markdown("**Images**")
        st.caption("📷 Product Image 1")
        st.caption("📷 Product Image 2")
        st.caption("📷 Product Image 3")
        st.error("⚠️ Only 3 images. Competitors average 8")
        st.error("⚠️ Missing lifestyle images")
        
        st.markdown("---")
        
        st.markdown("**Keywords Present**")
        st.caption("cleaner, multi-purpose, cleaning")
        st.caption("3 keywords")
        st.error("⚠️ Missing 9 high-value keywords")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Column 2: AI-Generated Improvements
    with content_cols[1]:
        st.markdown('<div class="content-column-improved">', unsafe_allow_html=True)
        st.markdown("**AI-Generated Improvements ✨**")
        st.caption("Optimized content recommendations")
        
        st.markdown("---")
        
        st.markdown("**New Title**")
        st.text("CleanHome Eco-Friendly Multi-Purpose Cleaner | Antibacterial, Non-Toxic Formula")
        st.caption("82 characters")
        st.success("✓ Added brand name")
        st.success("✓ Included 3 high-value keywords")
        st.success("✓ SEO-optimized length")
        
        st.markdown("---")
        
        st.markdown("**New Description**")
        st.text_area("", "CleanHome's powerful multi-purpose cleaner tackles tough messes on kitchen counters, bathroom tiles, glass, and more. Our eco-friendly, antibacterial formula is non-toxic, biodegradable, and safe for families and pets. No harsh chemicals—just effective cleaning with a fresh lemon scent. Perfect for daily use.", height=150, disabled=True, label_visibility="collapsed")
        st.caption("46 words | 285 characters")
        st.success("✓ Matches competitor length benchmark")
        st.success("✓ Includes benefit statements")
        st.success("✓ Lists use cases")
        
        st.markdown("---")
        
        st.markdown("**New Images**")
        st.caption("🖼️ Lifestyle Image 1: Person cleaning kitchen")
        st.caption("🖼️ Lifestyle Image 2: Product on counter")
        st.caption("🖼️ Ingredient flat lay")
        st.caption("🖼️ Before/After: Clean surface")
        st.caption("🖼️ Product Image 5: Family pack")
        st.caption("**Total: 8 images** (3 existing + 5 new)")
        st.success("✓ Added 5 new images (meets 8-image benchmark)")
        st.success("✓ Includes lifestyle and in-use shots")
        
        st.markdown("---")
        
        st.markdown("**Keywords Added**")
        st.caption("eco-friendly, antibacterial, non-toxic, biodegradable, family-safe, pet-safe, lemon scent, kitchen cleaner, bathroom cleaner")
        st.caption("**Total: 12 keywords** (+9 from original 3)")
        st.success("✓ Added 9 high-value keywords")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Column 3: Improvements & Impact
    with content_cols[2]:
        st.markdown('<div class="content-column-impact">', unsafe_allow_html=True)
        st.markdown("**Summary & Impact**")
        
        st.markdown("---")
        
        st.markdown("**Improvements Checklist**")
        improvements = [
            "Added 9 high-value keywords",
            "Expanded description by 231 characters (+427%)",
            "Added benefit-driven copy structure",
            "Included ingredient/safety callouts",
            "Added 5 lifestyle images",
            "Optimized title for SEO (82 chars vs. 22)",
            "Added sensory details (lemon scent)",
            "Listed specific use cases"
        ]
        
        for imp in improvements:
            st.markdown(f"<div class='improvement-item'>✅ {imp}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown('<div class="impact-box">', unsafe_allow_html=True)
        st.markdown("**🎯 Predicted Performance Lift**")
        st.markdown("")
        
        st.metric("Content Score", "88/100", "+30pts (+52%)")
        st.metric("Organic Rank", "#1", "+2 spots")
        st.metric("CVR", "3.7%", "+0.9pts (+32%)")
        st.metric("Sales Lift", "$2,400", "over 2 weeks")
        
        st.progress(0.87, text="Confidence: 87%")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action Buttons
    if not st.session_state.content_deployed:
        btn_cols = st.columns([2, 1, 1, 1, 1])
        
        with btn_cols[1]:
            st.button("🔄 Generate Alternative", key="generate_alt", use_container_width=True)
        
        with btn_cols[2]:
            st.button("✏️ Edit Manually", key="edit_manual", use_container_width=True)
        
        with btn_cols[3]:
            if st.button("❌ Cancel", key="content_cancel", use_container_width=True):
                st.session_state.selected_module = "Product Performance"
                st.rerun()
        
        with btn_cols[4]:
            if st.button("🚀 Deploy Changes", key="deploy_content", use_container_width=True, type="primary"):
                with st.spinner("Deploying content..."):
                    time.sleep(2)
                st.success("✅ Content deployed successfully to Target. Impact tracking enabled.")
                st.session_state.content_deployed = True
                st.balloons()
                time.sleep(1)
                st.rerun()
    else:
        # Show deployment status
        st.info("✅ Content successfully deployed! Changes are live at Target.")
        
        if st.button("📊 Track Impact (Simulated - 2 Weeks Later)", key="track_impact_btn", use_container_width=False):
            st.session_state.show_impact_tracking = True
            st.rerun()
        
        if st.session_state.show_impact_tracking:
            st.markdown("---")
            st.markdown("### 📈 Impact Tracking: SKU003 Content Update")
            
            st.markdown("""
            <div style="background: #E8F5E9; border: 2px solid #28A745; border-radius: 8px; padding: 20px; margin: 20px 0;">
                <h4 style="color: #11377C;">Deployment Summary</h4>
                <p><strong>Deployment Date:</strong> November 13, 2025</p>
                <p><strong>Status:</strong> <span style="background: #28A745; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px;">LIVE</span></p>
                <p><strong>Time Since Deployment:</strong> 14 days</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Before/After Comparison**")
            
            comparison_data = pd.DataFrame({
                'Metric': ['Content Score', 'Organic Rank', 'CVR', 'Sales (2 weeks)', 'P-Page Traffic'],
                'Before (Pre-Fix)': ['58/100', '#3', '2.8%', '$12,400', '8,200'],
                'After (Post-Fix)': ['88/100', '#1', '3.9%', '$15,050', '11,500'],
                'Change': ['+30pts (+52%)', '+2 spots', '+1.1pts (+39%)', '+$2,650 (+21%)', '+3,300 (+40%)'],
                'Status': ['✅ Exceeded forecast', '✅ Met forecast', '✅ Exceeded forecast', '✅ Exceeded forecast', '✅ Additional benefit']
            })
            
            st.dataframe(comparison_data, use_container_width=True, hide_index=True)
            
            st.markdown("""
            <div style="background: #E8F5E9; border-left: 4px solid #28A745; padding: 16px; border-radius: 8px; margin: 20px 0;">
                <span style="font-size: 24px;">🎉</span>
                <p style="margin: 10px 0;"><strong>AI Summary:</strong></p>
                <p>Your content update for SKU003 <strong>exceeded forecasted impact</strong>. Actual sales lift: <strong>$2,650</strong> (vs. forecast $2,400). Organic rank improved to <strong>#1</strong> as predicted. CVR recovery outpaced forecast by <strong>0.2pts</strong>.</p>
                <p style="margin-top: 15px; color: #1CB192; font-weight: 600;">💡 Recommendation: Apply similar content strategy to SKU002 and SKU004.</p>
            </div>
            """, unsafe_allow_html=True)

# Chat Panel
def render_chat_panel():
    if st.session_state.chat_open:
        with st.sidebar:
            st.markdown("### 💬 AI Copilot Assistant")
            
            if st.button("✕ Close", key="close_chat"):
                st.session_state.chat_open = False
                st.session_state.chat_messages = []
                st.rerun()
            
            st.markdown("---")
            
            # Display chat messages
            for msg in st.session_state.chat_messages:
                if msg['role'] == 'user':
                    st.markdown(f"""
                    <div class="chat-message-user">
                        {msg['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message-ai">
                        🤖 {msg['content']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Initial AI response if just opened
            if len(st.session_state.chat_messages) == 1:
                ai_response = """**Three factors contributed to the 22% CVR drop for SKU003 at Target:**

1. **Primary Driver:** Product was out-of-stock for 3 days (Nov 10-12), causing traffic to convert elsewhere

2. **Rating Impact:** Rating dropped from 4.6 to 4.2 stars due to 3 recent 1-star reviews mentioning 'ineffective cleaning'

3. **Competitive Pressure:** Competitor EcoClean cut price by 15% (now $8.99 vs. $10.49)

**Recommended Actions:**
- **Immediate:** Ensure restock and implement inventory alerts
- **Short-term:** Address review concerns with response campaign
- **Strategic:** Improve content (add lifestyle images, expand description)

Would you like me to simulate recovery scenarios?"""
                
                st.session_state.chat_messages.append({"role": "ai", "content": ai_response})
                st.rerun()
            
            st.markdown("---")
            
            # Quick reply buttons
            if len(st.session_state.chat_messages) >= 2:
                st.markdown("**Quick Actions:**")
                if st.button("🎯 Simulate recovery scenarios", key="chat_sim"):
                    follow_up = """**Scenario: Combined Fixes (Restock + Content)**

**Actions:**
- Eliminate OOS (maintain 100% stock availability)
- Add 2 lifestyle images (3 → 5 total)
- Expand description (+150 chars with keywords)

**Forecasted Impact:**
- Content Score: 58 → 85 (+27pts)
- Organic Rank: #3 → #1 (+2 spots)
- CVR: 2.8% → 4.1% (+1.3pts, +46%)
- Sales Lift: +$3,200 over 2 weeks
- Confidence: 89%

**Why This Works:** The combination addresses both availability and appeal, maximizing conversion recovery while defending against competitor pricing.

Would you like to apply these changes?"""
                    
                    st.session_state.chat_messages.append({"role": "user", "content": "Simulate recovery scenarios"})
                    st.session_state.chat_messages.append({"role": "ai", "content": follow_up})
                    st.rerun()
                
                if st.button("✍️ Show content improvements", key="chat_content"):
                    st.session_state.selected_module = "Content Crafter"
                    st.rerun()

# Main App Logic
render_navigation()
render_filters()

if st.session_state.selected_module == "Main Dashboard":
    render_main_dashboard()
elif st.session_state.selected_module == "Product Performance":
    render_product_performance()
elif st.session_state.selected_module == "Content Crafter":
    render_content_crafter()

# Render chat panel if open
render_chat_panel()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6C757D; padding: 20px;">
    <p>Skulytics eCommerce Performance Intelligence Platform | Demo Version | © 2025</p>
    <p style="font-size: 12px;">Production-ready analytics for CPG brands across all retail channels</p>
</div>
""", unsafe_allow_html=True)
