import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Skulytics - eCommerce Performance Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# ENTERPRISE-GRADE CSS STYLING (NO EMOJIS - PROFESSIONAL ICONS ONLY)
# =============================================================================
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Professional Font Stack */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Main Container */
    .main {
        background-color: #F5F7FA;
        padding: 0;
    }
    
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 2rem;
        max-width: 100% !important;
    }
    
    /* Navigation Bar */
    .nav-container {
        background-color: #11377C;
        padding: 1rem 2rem;
        margin: -5rem -5rem 2rem -5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .nav-logo {
        color: white;
        font-size: 20px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Professional Alert Card */
    .alert-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        transition: all 0.2s ease;
    }
    
    .alert-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .alert-card-urgent {
        border-left: 4px solid #DC3545;
    }
    
    .alert-card-monitor {
        border-left: 4px solid #FF8300;
    }
    
    .alert-card-opportunity {
        border-left: 4px solid #1CB192;
    }
    
    .alert-card-info {
        border-left: 4px solid #0075FF;
    }
    
    .alert-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .alert-icon {
        font-size: 16px;
        margin-right: 0.5rem;
    }
    
    .alert-badge {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 4px 8px;
        border-radius: 12px;
        color: white;
    }
    
    .badge-urgent { background: #DC3545; }
    .badge-monitor { background: #FF8300; }
    .badge-opportunity { background: #1CB192; }
    .badge-info { background: #0075FF; }
    
    .alert-title {
        font-size: 14px;
        font-weight: 600;
        color: #2D3748;
        margin: 0.5rem 0;
    }
    
    .alert-details {
        font-size: 13px;
        color: #6C757D;
        margin: 0.25rem 0;
    }
    
    .alert-timestamp {
        font-size: 11px;
        color: #A0AEC0;
        margin-top: 0.5rem;
    }
    
    /* Professional KPI Tile */
    .kpi-tile {
        background: white;
        border: 1px solid #E2E8F0;
        border-left: 3px solid #1CB192;
        border-radius: 6px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        height: 100%;
    }
    
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    
    .kpi-icon {
        font-size: 18px;
        color: #1CB192;
    }
    
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #6C757D;
    }
    
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #11377C;
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    .kpi-change {
        font-size: 14px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .kpi-change-positive {
        color: #28A745;
    }
    
    .kpi-change-negative {
        color: #DC3545;
    }
    
    .kpi-change-neutral {
        color: #6C757D;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }
    
    .status-green { background: #28A745; }
    .status-orange { background: #FF8300; }
    .status-red { background: #DC3545; }
    
    /* Filter Bar */
    .filter-bar {
        background: #F5F7FA;
        border-bottom: 1px solid #E2E8F0;
        padding: 1rem 2rem;
        margin: -1rem -5rem 2rem -5rem;
    }
    
    /* Active Filter Badge */
    .active-filter {
        background: #FFF3E0;
        border: 1px solid #FF8300;
        border-left: 4px solid #FF8300;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .active-filter-text {
        font-weight: 600;
        color: #2D3748;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Commerce Journey Funnel */
    .funnel-stage {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
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
    
    .funnel-icon {
        font-size: 28px;
        margin-bottom: 0.75rem;
        color: #6C757D;
    }
    
    .funnel-title {
        font-size: 16px;
        font-weight: 600;
        color: #11377C;
        margin-bottom: 0.75rem;
    }
    
    .funnel-metric-primary {
        font-size: 22px;
        font-weight: 700;
        color: #2D3748;
        margin-bottom: 0.25rem;
    }
    
    .funnel-metric-secondary {
        font-size: 13px;
        color: #6C757D;
        margin-bottom: 0.75rem;
    }
    
    .funnel-status {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        padding: 4px 10px;
        border-radius: 12px;
        display: inline-block;
    }
    
    .status-healthy {
        background: #D4EDDA;
        color: #28A745;
    }
    
    .status-needs-work {
        background: #FFF3CD;
        color: #856404;
    }
    
    .status-critical {
        background: #F8D7DA;
        color: #721C24;
    }
    
    /* Professional Buttons */
    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        padding: 0.5rem 1.25rem;
        font-size: 14px;
        border: none;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Banner Styles */
    .banner {
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: start;
        gap: 1rem;
    }
    
    .banner-warning {
        background: #FFF3E0;
        border: 1px solid #FF8300;
        border-left: 4px solid #FF8300;
    }
    
    .banner-success {
        background: #E0F7F4;
        border: 1px solid #1CB192;
        border-left: 4px solid #1CB192;
    }
    
    .banner-icon {
        font-size: 20px;
        flex-shrink: 0;
    }
    
    .banner-content h4 {
        margin: 0 0 0.5rem 0;
        color: #2D3748;
        font-size: 16px;
    }
    
    .banner-content p {
        margin: 0;
        color: #6C757D;
        font-size: 14px;
    }
    
    /* Professional Table */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        overflow: hidden;
    }
    
    .dataframe th {
        background: #F9FAFB;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #6C757D;
        padding: 0.75rem 1rem;
        border-bottom: 2px solid #E2E8F0;
        text-align: left;
    }
    
    .dataframe td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #F1F3F5;
        font-size: 14px;
        color: #2D3748;
    }
    
    .dataframe tr:hover {
        background: #F9FAFB;
    }
    
    /* Content Columns */
    .content-column {
        border-radius: 6px;
        padding: 1.25rem;
        height: 100%;
    }
    
    .content-existing {
        background: #F9FAFB;
        border: 1px solid #E2E8F0;
    }
    
    .content-improved {
        background: white;
        border: 2px solid #1CB192;
    }
    
    .content-impact {
        background: #EBF8FF;
        border: 1px solid #0075FF;
    }
    
    .content-header {
        font-size: 16px;
        font-weight: 600;
        color: #11377C;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .content-subheader {
        font-size: 12px;
        color: #6C757D;
        margin-bottom: 1rem;
    }
    
    .content-section {
        margin-bottom: 1.5rem;
    }
    
    .content-label {
        font-size: 13px;
        font-weight: 600;
        color: #2D3748;
        margin-bottom: 0.5rem;
    }
    
    .content-text {
        font-size: 13px;
        color: #2D3748;
        line-height: 1.5;
        background: white;
        padding: 0.75rem;
        border-radius: 4px;
        border: 1px solid #E2E8F0;
    }
    
    .content-meta {
        font-size: 11px;
        color: #6C757D;
        margin-top: 0.25rem;
    }
    
    .content-issue {
        font-size: 12px;
        color: #DC3545;
        margin-top: 0.5rem;
        display: flex;
        align-items: start;
        gap: 0.5rem;
    }
    
    .content-improvement {
        font-size: 12px;
        color: #28A745;
        margin-top: 0.5rem;
        display: flex;
        align-items: start;
        gap: 0.5rem;
    }
    
    .improvement-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .improvement-list li {
        padding: 0.5rem 0;
        border-bottom: 1px solid #E2E8F0;
        font-size: 13px;
        display: flex;
        align-items: start;
        gap: 0.5rem;
    }
    
    /* Impact Box */
    .impact-box {
        background: #E8F5E9;
        border: 2px solid #28A745;
        border-radius: 8px;
        padding: 1.25rem;
        margin-top: 1.5rem;
    }
    
    .impact-title {
        font-size: 16px;
        font-weight: 600;
        color: #28A745;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Score Badges */
    .score-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 14px;
        text-align: center;
    }
    
    .score-red {
        background: #DC3545;
        color: white;
    }
    
    .score-yellow {
        background: #FF8300;
        color: white;
    }
    
    .score-green {
        background: #28A745;
        color: white;
    }
    
    /* Success Notification */
    .success-notification {
        background: #D4EDDA;
        border: 1px solid #C3E6CB;
        border-left: 4px solid #28A745;
        color: #155724;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* Hide Streamlit Default Elements */
    div[data-testid="stToolbar"] {
        display: none;
    }
    
    /* Adjust Streamlit Columns */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Chart Containers */
    .chart-container {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .chart-title {
        font-size: 16px;
        font-weight: 600;
        color: #11377C;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
if 'selected_module' not in st.session_state:
    st.session_state.selected_module = "Main Dashboard"
if 'alert_clicked' not in st.session_state:
    st.session_state.alert_clicked = None
if 'filters_visible' not in st.session_state:
    st.session_state.filters_visible = True
if 'simulate_modal_open' not in st.session_state:
    st.session_state.simulate_modal_open = False
if 'content_deployed' not in st.session_state:
    st.session_state.content_deployed = False
if 'show_impact_tracking' not in st.session_state:
    st.session_state.show_impact_tracking = False
if 'filter_sku' not in st.session_state:
    st.session_state.filter_sku = "All SKUs"
if 'filter_retailer' not in st.session_state:
    st.session_state.filter_retailer = "All Retailers"

# =============================================================================
# LOAD DATA
# =============================================================================
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

# =============================================================================
# NAVIGATION BAR
# =============================================================================
st.markdown("""
<div class="nav-container">
    <div class="nav-logo">
        <i class="fas fa-chart-line"></i>
        Skulytics
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns([2, 2, 2, 2, 2, 2])

with nav_col1:
    if st.button("Main Dashboard", key="nav_main", use_container_width=True):
        st.session_state.selected_module = "Main Dashboard"
        st.rerun()

with nav_col2:
    if st.button("Product Performance", key="nav_product", use_container_width=True):
        st.session_state.selected_module = "Product Performance"
        st.rerun()

with nav_col3:
    if st.button("Content Crafter", key="nav_content", use_container_width=True):
        st.session_state.selected_module = "Content Crafter"
        st.rerun()

with nav_col4:
    st.button("Demand Forecasting*", key="nav_demand", disabled=True, use_container_width=True)

with nav_col5:
    st.button("Media Spend*", key="nav_media", disabled=True, use_container_width=True)

with nav_col6:
    st.button("Competitor Intel*", key="nav_competitor", disabled=True, use_container_width=True)

# =============================================================================
# FILTER BAR
# =============================================================================
if st.session_state.filters_visible:
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    filter_cols = st.columns([2, 2, 2, 2, 2, 1])
    
    with filter_cols[0]:
        month_filter = st.selectbox("Month/Year", ["November 2025", "October 2025", "September 2025"], key="month_select")
    
    with filter_cols[1]:
        st.session_state.filter_retailer = st.selectbox(
            "Channel Partner",
            ["All Retailers", "Walmart", "Target", "Amazon", "Kroger", "Costco"],
            key="retailer_select"
        )
    
    with filter_cols[2]:
        category_filter = st.selectbox(
            "Product Category",
            ["All Categories", "Snacks", "Beverages", "Household", "Personal Care", "Health", "Pet Care"],
            key="category_select"
        )
    
    with filter_cols[3]:
        sku_options = ["All SKUs"] + [f"{row['sku_id']} ({row['sku_name']})" for _, row in sku_data.iterrows()]
        st.session_state.filter_sku = st.selectbox("SKU", sku_options, key="sku_select")
    
    with filter_cols[4]:
        brand_filter = st.selectbox(
            "Brand",
            ["All Brands", "CleanHome", "PureVitality", "EcoFresh", "BrewMasters", "SnackSmart", "PetWellness"],
            key="brand_select"
        )
    
    with filter_cols[5]:
        st.write("")
        st.write("")
        if st.button("Hide", key="hide_filters"):
            st.session_state.filters_visible = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="text-align: center; padding: 0.5rem;">', unsafe_allow_html=True)
    if st.button("Show Filters", key="show_filters"):
        st.session_state.filters_visible = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# MODULE 1: MAIN DASHBOARD
# =============================================================================
def render_main_dashboard():
    st.markdown("## <i class='fas fa-tachometer-alt'></i> Commerce Journey Hub", unsafe_allow_html=True)
    st.markdown("---")
    
    # Alert Panel
    st.markdown("### <i class='fas fa-bell'></i> Active Alerts", unsafe_allow_html=True)
    
    alert_cols = st.columns(5)
    
    # Alert 1: URGENT
    with alert_cols[0]:
        st.markdown("""
        <div class="alert-card alert-card-urgent">
            <div class="alert-header">
                <span><i class="fas fa-exclamation-triangle alert-icon" style="color: #DC3545;"></i></span>
                <span class="alert-badge badge-urgent">URGENT</span>
            </div>
            <div class="alert-title">SKU003 - Conversion Down 22%</div>
            <div class="alert-details">OOS Days ↑150%, Rating ↓0.4 stars at Target</div>
            <div class="alert-timestamp">2 hours ago</div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Investigate", key="alert1_investigate", use_container_width=True):
                st.session_state.alert_clicked = "alert_1"
                st.session_state.filter_sku = "SKU003 (Multi-Purpose Cleaner)"
                st.session_state.filter_retailer = "Target"
                st.rerun()
        with btn_col2:
            st.button("Ask in Chat", key="alert1_chat", use_container_width=True)
    
    # Alert 2: MONITOR
    with alert_cols[1]:
        st.markdown("""
        <div class="alert-card alert-card-monitor">
            <div class="alert-header">
                <span><i class="fas fa-chart-line alert-icon" style="color: #FF8300;"></i></span>
                <span class="alert-badge badge-monitor">MONITOR</span>
            </div>
            <div class="alert-title">SKU002 - Views Down 15%</div>
            <div class="alert-details">Organic rank dropped #4 → #8 at Walmart</div>
            <div class="alert-timestamp">5 hours ago</div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.button("Investigate", key="alert2_investigate", use_container_width=True)
        with btn_col2:
            st.button("Ask in Chat", key="alert2_chat", use_container_width=True)
    
    # Alert 3: OPPORTUNITY
    with alert_cols[2]:
        st.markdown("""
        <div class="alert-card alert-card-opportunity">
            <div class="alert-header">
                <span><i class="fas fa-bullseye alert-icon" style="color: #1CB192;"></i></span>
                <span class="alert-badge badge-opportunity">OPPORTUNITY</span>
            </div>
            <div class="alert-title">SKU001 - ROAS Up 45%</div>
            <div class="alert-details">Paid media efficiency up. Consider budget increase</div>
            <div class="alert-timestamp">1 day ago</div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.button("View Details", key="alert3_view", use_container_width=True)
        with btn_col2:
            st.button("Ask in Chat", key="alert3_chat", use_container_width=True)
    
    # Alert 4: MONITOR
    with alert_cols[3]:
        st.markdown("""
        <div class="alert-card alert-card-monitor">
            <div class="alert-header">
                <span><i class="fas fa-warehouse alert-icon" style="color: #FF8300;"></i></span>
                <span class="alert-badge badge-monitor">MONITOR</span>
            </div>
            <div class="alert-title">SKU007 - Low Stock</div>
            <div class="alert-details">3 days supply at Kroger. Restock recommended</div>
            <div class="alert-timestamp">6 hours ago</div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.button("Investigate", key="alert4_investigate", use_container_width=True)
        with btn_col2:
            st.button("Ask in Chat", key="alert4_chat", use_container_width=True)
    
    # Alert 5: INFO
    with alert_cols[4]:
        st.markdown("""
        <div class="alert-card alert-card-info">
            <div class="alert-header">
                <span><i class="fas fa-info-circle alert-icon" style="color: #0075FF;"></i></span>
                <span class="alert-badge badge-info">INFO</span>
            </div>
            <div class="alert-title">SKU005 - Content Updated</div>
            <div class="alert-details">Deployed at Costco. Impact tracking enabled</div>
            <div class="alert-timestamp">3 days ago</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.button("Track Impact", key="alert5_track", use_container_width=True)
    
    st.markdown("---")
    
    # Active Filter Badge
    if st.session_state.alert_clicked:
        st.markdown("""
        <div class="active-filter">
            <div class="active-filter-text">
                <i class="fas fa-search"></i>
                <span>Active Filter: SKU003 | Target</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Full Product Analysis", key="view_analysis", use_container_width=False):
            st.session_state.selected_module = "Product Performance"
            st.rerun()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Clear Filters", key="clear_filters", use_container_width=True):
                st.session_state.alert_clicked = None
                st.session_state.filter_sku = "All SKUs"
                st.session_state.filter_retailer = "All Retailers"
                st.rerun()
        
        st.markdown("---")
    
    # Determine if filtered
    is_filtered = st.session_state.alert_clicked is not None
    
    # KPI Tiles
    st.markdown("### <i class='fas fa-chart-bar'></i> Key Performance Indicators", unsafe_allow_html=True)
    
    # Row 1
    kpi_row1 = st.columns(3)
    
    with kpi_row1[0]:
        value = "$12,400" if is_filtered else "$1,247,890"
        change = "↓ 18% vs LW" if is_filtered else "↑ 12.4% vs LM"
        change_class = "negative" if is_filtered else "positive"
        st.markdown(f"""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">Gross Sales</div>
                <i class="fas fa-dollar-sign kpi-icon"></i>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-change kpi-change-{change_class}">{change}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_row1[1]:
        value = "890" if is_filtered else "18,432"
        change = "↓ 3.3% vs LW" if is_filtered else "↑ 8.2% vs LM"
        change_class = "negative" if is_filtered else "positive"
        st.markdown(f"""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">Units Sold</div>
                <i class="fas fa-box kpi-icon"></i>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-change kpi-change-{change_class}">{change}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_row1[2]:
        value = "2.8%" if is_filtered else "3.4%"
        change = "↓ 22% vs LW" if is_filtered else "↓ 2.1% vs LM"
        st.markdown(f"""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">Average CVR</div>
                <i class="fas fa-percentage kpi-icon"></i>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-change kpi-change-negative">{change}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Row 2
    kpi_row2 = st.columns(3)
    
    with kpi_row2[0]:
        value = "#3" if is_filtered else "#6.2"
        change = "Stable"
        st.markdown(f"""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">Avg Organic Rank</div>
                <i class="fas fa-trophy kpi-icon"></i>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-change kpi-change-neutral">{change}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_row2[1]:
        value = "8.5%" if is_filtered else "4.2%"
        change = "↑ 8.5pts vs LW" if is_filtered else "↑ 1.8% vs LM"
        warning = "<i class='fas fa-exclamation-triangle' style='color: #DC3545; margin-right: 0.5rem;'></i>" if is_filtered else ""
        st.markdown(f"""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">OOS %</div>
                <i class="fas fa-warehouse kpi-icon"></i>
            </div>
            <div class="kpi-value">{warning}{value}</div>
            <div class="kpi-change kpi-change-negative">{change}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_row2[2]:
        value = "58/100" if is_filtered else "72/100"
        change = "↓ 33% vs LM" if is_filtered else "↓ 8pts vs LM"
        st.markdown(f"""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">Content Health Score</div>
                <i class="fas fa-file-alt kpi-icon"></i>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-change kpi-change-negative">{change}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Row 3
    kpi_row3 = st.columns(3)
    
    with kpi_row3[0]:
        st.markdown("""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">Total Media Spend</div>
                <i class="fas fa-bullhorn kpi-icon"></i>
            </div>
            <div class="kpi-value">$124,500</div>
            <div class="kpi-change kpi-change-positive">↑ 15% vs LM</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_row3[1]:
        st.markdown("""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">ROAS</div>
                <i class="fas fa-chart-line kpi-icon"></i>
            </div>
            <div class="kpi-value">3.8x</div>
            <div class="kpi-change kpi-change-positive">↑ 0.4x vs LM</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_row3[2]:
        st.markdown("""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">Avg Paid Rank</div>
                <i class="fas fa-ad kpi-icon"></i>
            </div>
            <div class="kpi-value">#4.1</div>
            <div class="kpi-change kpi-change-positive">↑ 2 spots vs LM</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Section
    st.markdown("### <i class='fas fa-chart-area'></i> Performance Analytics", unsafe_allow_html=True)
    
    chart_cols = st.columns(2)
    
    with chart_cols[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Monthly Sales Trend</div>', unsafe_allow_html=True)
        
        if is_filtered:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=sku003_monthly['month'],
                y=sku003_monthly['sales'],
                mode='lines+markers',
                line=dict(color='#FF8300', width=3),
                marker=dict(color='#FF8300', size=10),
                name='SKU003 Sales'
            ))
        else:
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
            font=dict(family='Inter, sans-serif', size=12, color='#2D3748'),
            hovermode='x unified',
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        fig.update_yaxis(gridcolor='#E2E8F0', gridwidth=1)
        fig.update_xaxis(showgrid=False)
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_cols[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Top Products by Sales - November 2025</div>', unsafe_allow_html=True)
        
        colors = ['#DC3545' if sku == 'SKU003' and is_filtered else '#1CB192' for sku in top_products['sku_id']]
        
        fig = go.Figure(go.Bar(
            x=top_products['sales'],
            y=top_products['sku_name'],
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
            font=dict(family='Inter, sans-serif', size=11, color='#2D3748'),
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        fig.update_xaxis(gridcolor='#E2E8F0', gridwidth=1)
        fig.update_yaxis(showgrid=False)
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Commerce Journey Funnel
    st.markdown("### <i class='fas fa-filter'></i> Commerce Journey Performance", unsafe_allow_html=True)
    
    funnel_cols = st.columns(4)
    
    with funnel_cols[0]:
        views = "48K Views" if is_filtered else "245K Views"
        rank = "Avg Rank #3" if is_filtered else "Avg Rank #6.2"
        st.markdown(f"""
        <div class="funnel-stage funnel-stage-healthy">
            <div class="funnel-icon"><i class="fas fa-eye"></i></div>
            <div class="funnel-title">Discovery</div>
            <div class="funnel-metric-primary">{views}</div>
            <div class="funnel-metric-secondary">{rank}</div>
            <div class="funnel-status status-healthy">Healthy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with funnel_cols[1]:
        traffic = "16.8K Traffic" if is_filtered else "89K Traffic"
        score = "Content Score 58/100" if is_filtered else "Content Score 72/100"
        st.markdown(f"""
        <div class="funnel-stage funnel-stage-warning">
            <div class="funnel-icon"><i class="fas fa-hand-pointer"></i></div>
            <div class="funnel-title">Engagement</div>
            <div class="funnel-metric-primary">{traffic}</div>
            <div class="funnel-metric-secondary">{score}</div>
            <div class="funnel-status status-needs-work">Needs Work</div>
        </div>
        """, unsafe_allow_html=True)
    
    with funnel_cols[2]:
        cvr = "CVR 2.8%" if is_filtered else "CVR 3.4%"
        atc = "5.2K Add-to-Cart" if is_filtered else "28.5K Add-to-Cart"
        stage_class = "critical" if is_filtered else "warning"
        status_class = "status-critical" if is_filtered else "status-needs-work"
        status_text = "Critical" if is_filtered else "Needs Work"
        st.markdown(f"""
        <div class="funnel-stage funnel-stage-{stage_class}">
            <div class="funnel-icon"><i class="fas fa-shopping-cart"></i></div>
            <div class="funnel-title">Conversion</div>
            <div class="funnel-metric-primary">{cvr}</div>
            <div class="funnel-metric-secondary">{atc}</div>
            <div class="funnel-status {status_class}">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with funnel_cols[3]:
        sales = "$12.4K" if is_filtered else "$1.24M"
        units = "890 Units" if is_filtered else "18.4K Units"
        stage_class = "warning" if is_filtered else "healthy"
        status_class = "status-needs-work" if is_filtered else "status-healthy"
        status_text = "Below Target" if is_filtered else "Healthy"
        st.markdown(f"""
        <div class="funnel-stage funnel-stage-{stage_class}">
            <div class="funnel-icon"><i class="fas fa-money-bill-wave"></i></div>
            <div class="funnel-title">Sales</div>
            <div class="funnel-metric-primary">{sales}</div>
            <div class="funnel-metric-secondary">{units}</div>
            <div class="funnel-status {status_class}">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# MODULE 2: PRODUCT PERFORMANCE
# =============================================================================
def render_product_performance():
    st.markdown("## <i class='fas fa-chart-line'></i> Product Performance Analysis", unsafe_allow_html=True)
    
    # Alert Context Banner
    if st.session_state.alert_clicked:
        st.markdown("""
        <div class="banner banner-warning">
            <i class="fas fa-exclamation-triangle banner-icon" style="color: #FF8300;"></i>
            <div class="banner-content">
                <h4>SKU003 — Conversion Down 22%</h4>
                <p>Contributing Factors: OOS Days ↑150%, Rating ↓0.4 stars, Competitor Price Cut 15%</p>
                <p style="font-style: italic; margin-top: 0.5rem;"><i class="fas fa-lightbulb" style="margin-right: 0.5rem;"></i>AI Suggestion: Investigate root causes. Potential factors: out-of-stock for 3 days, negative review spike, competitor action.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI Metadata Tiles
    st.markdown("### <i class='fas fa-crosshairs'></i> SKU003 Performance Snapshot", unsafe_allow_html=True)
    
    meta_row1 = st.columns(3)
    
    with meta_row1[0]:
        st.markdown("""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">Avg Organic Rank</div>
                <span class="status-dot status-green"></span>
            </div>
            <div class="kpi-value">#3</div>
            <div class="kpi-change kpi-change-neutral">Stable</div>
            <div style="font-size: 12px; color: #6C757D; margin-top: 0.5rem;">No change vs. last week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with meta_row1[1]:
        st.markdown("""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">Avg Paid Rank</div>
                <span class="status-dot status-orange"></span>
            </div>
            <div class="kpi-value">#7</div>
            <div class="kpi-change kpi-change-negative">↓2 spots</div>
            <div style="font-size: 12px; color: #6C757D; margin-top: 0.5rem;">Declined from #5</div>
        </div>
        """, unsafe_allow_html=True)
    
    with meta_row1[2]:
        st.markdown("""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">Sales (Current Month)</div>
                <span class="status-dot status-red"></span>
            </div>
            <div class="kpi-value">$12,400</div>
            <div class="kpi-change kpi-change-negative">↓18% WoW</div>
            <div style="font-size: 12px; color: #6C757D; margin-top: 0.5rem;">Down from $15,100</div>
        </div>
        """, unsafe_allow_html=True)
    
    meta_row2 = st.columns(3)
    
    with meta_row2[0]:
        st.markdown("""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">Stock Status</div>
                <span class="status-dot status-red"></span>
            </div>
            <div class="kpi-value"><i class="fas fa-exclamation-triangle" style="color: #DC3545; margin-right: 0.5rem;"></i>OOS 3 Days</div>
            <div class="kpi-change kpi-change-negative">Nov 10-12</div>
            <div style="font-size: 12px; color: #6C757D; margin-top: 0.5rem;">Restock Alert Sent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with meta_row2[1]:
        st.markdown("""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">P-Page Traffic</div>
                <span class="status-dot status-orange"></span>
            </div>
            <div class="kpi-value">8,200</div>
            <div class="kpi-change kpi-change-negative">↓8% WoW</div>
            <div style="font-size: 12px; color: #6C757D; margin-top: 0.5rem;">Down from 8,900</div>
        </div>
        """, unsafe_allow_html=True)
    
    with meta_row2[2]:
        st.markdown("""
        <div class="kpi-tile">
            <div class="kpi-header">
                <div class="kpi-label">CVR (Conversion Rate)</div>
                <span class="status-dot status-red"></span>
            </div>
            <div class="kpi-value">2.8%</div>
            <div class="kpi-change kpi-change-negative">↓22% WoW</div>
            <div style="font-size: 12px; color: #DC3545; margin-top: 0.5rem; font-weight: 600;">
                <i class="fas fa-exclamation-triangle"></i> Primary Problem
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    st.markdown("### <i class='fas fa-chart-bar'></i> Comparative Analytics", unsafe_allow_html=True)
    
    chart_cols = st.columns(2)
    
    with chart_cols[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">SKU Performance Comparison - Household Category at Target</div>', unsafe_allow_html=True)
        
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
            font=dict(family='Inter, sans-serif', size=11, color='#2D3748'),
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        fig.update_xaxis(gridcolor='#E2E8F0', gridwidth=1)
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_cols[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">SKU003 CVR Trend - Last 30 Days</div>', unsafe_allow_html=True)
        
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
            x0='2025-11-09', x1='2025-11-12',
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
            font=dict(family='Inter, sans-serif', size=12, color='#2D3748'),
            hovermode='x unified',
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        fig.update_yaxis(gridcolor='#E2E8F0', gridwidth=1)
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Opportunity Table
    st.markdown("### <i class='fas fa-lightbulb'></i> Opportunity Analysis & Recommendations", unsafe_allow_html=True)
    
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
            'Image Score: 42/100 (only 3 images), Description Score: 45/100'
        ],
        'Recommended Action': [
            'Restock immediately, prevent future OOS',
            'Launch review response campaign',
            'Test price match ($8.99) or bundle',
            'Add 2 lifestyle images, expand description by 150 chars'
        ],
        'Forecasted Impact': [
            'CVR +1.1pts, Sales +$1,800',
            'Stabilize rating',
            'Maintain market share',
            'Rank #3→#1, CVR +0.8pts, Sales +$1,200'
        ]
    })
    
    st.dataframe(opp_data, use_container_width=True, hide_index=True)
    
    st.write("")
    
    action_cols = st.columns(4)
    
    with action_cols[0]:
        st.button("View Details", key="opp1", use_container_width=True)
    
    with action_cols[1]:
        st.button("View Reviews", key="opp2", use_container_width=True)
    
    with action_cols[2]:
        st.button("Simulate Price", key="opp3", use_container_width=True)
    
    with action_cols[3]:
        if st.button("Simulate Fix", key="opp4", use_container_width=True, type="primary"):
            st.session_state.simulate_modal_open = True
            st.rerun()
    
    # Scenario Simulator Modal
    if st.session_state.simulate_modal_open:
        st.markdown("---")
        st.markdown("### <i class='fas fa-chart-area'></i> Scenario Simulator: Content Score Improvement", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; border: 2px solid #FF8300; border-radius: 8px; padding: 1.5rem; margin: 1rem 0;">
            <h4 style="color: #11377C; margin-bottom: 1rem;"><i class="fas fa-chart-line"></i> Impact Forecast</h4>
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
        
        st.write("")
        
        btn_cols = st.columns([3, 1, 1])
        
        with btn_cols[1]:
            if st.button("Cancel", key="sim_cancel", use_container_width=True):
                st.session_state.simulate_modal_open = False
                st.rerun()
        
        with btn_cols[2]:
            if st.button("Apply Changes", key="sim_apply", use_container_width=True, type="primary"):
                with st.spinner("Applying changes..."):
                    time.sleep(2)
                st.success("Content update queued. Routing to Content Crafter for deployment.")
                time.sleep(1)
                st.session_state.simulate_modal_open = False
                st.session_state.selected_module = "Content Crafter"
                st.rerun()

# =============================================================================
# MODULE 3: CONTENT CRAFTER
# =============================================================================
def render_content_crafter():
    st.markdown("## <i class='fas fa-pen-nib'></i> Content Crafter", unsafe_allow_html=True)
    
    # AI Suggestion Banner
    st.markdown("""
    <div class="banner banner-success">
        <i class="fas fa-lightbulb banner-icon" style="color: #1CB192;"></i>
        <div class="banner-content">
            <h4>SKU003 — Content Score has dropped 33% at Target</h4>
            <p style="font-style: italic;">AI Recommendation: Add lifestyle images and optimize description to improve SEO.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Score Tiles
    st.markdown("### <i class='fas fa-chart-pie'></i> Content Health Scores", unsafe_allow_html=True)
    
    score_cols = st.columns(7)
    
    scores = [
        ("Overall", 58, "red"),
        ("Title", 72, "yellow"),
        ("Description", 45, "red"),
        ("Image", 42, "red"),
        ("Keyword", 55, "red"),
        ("Rating", "4.2/5", "yellow"),
        ("Review", 68, "yellow")
    ]
    
    for i, (label, score, color) in enumerate(scores):
        with score_cols[i]:
            score_class = f"score-{color}"
            highlight = 'style="border: 3px solid #FF8300; box-shadow: 0 0 15px rgba(255,131,0,0.3);"' if label == "Image" else ''
            
            st.markdown(f"""
            <div {highlight} style="background: white; padding: 1rem; border-radius: 6px; text-align: center; border: 1px solid #E2E8F0;">
                <div style="font-size: 11px; color: #6C757D; font-weight: 600; text-transform: uppercase; margin-bottom: 0.5rem;">{label}</div>
                <div class="score-badge {score_class}">{score}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 3-Column Layout
    st.markdown("### <i class='fas fa-columns'></i> Content Optimization", unsafe_allow_html=True)
    
    content_cols = st.columns(3)
    
    # Column 1: Existing Content
    with content_cols[0]:
        st.markdown("""
        <div class="content-column content-existing">
            <div class="content-header">
                <i class="fas fa-file-alt"></i>
                Existing Content
            </div>
            <div class="content-subheader">Current state at Target</div>
            
            <div class="content-section">
                <div class="content-label">Product Title</div>
                <div class="content-text">Multi-Purpose Cleaner</div>
                <div class="content-meta">22 characters</div>
                <div class="content-issue">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>Missing keywords: 'eco-friendly', 'antibacterial', 'non-toxic'</span>
                </div>
                <div class="content-issue">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>No brand mention</span>
                </div>
            </div>
            
            <div class="content-section">
                <div class="content-label">Product Description</div>
                <div class="content-text">Effective cleaning solution for multiple surfaces.</div>
                <div class="content-meta">7 words | 54 characters</div>
                <div class="content-issue">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>75% shorter than competitors (avg 215 chars)</span>
                </div>
                <div class="content-issue">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>Missing ingredient information</span>
                </div>
                <div class="content-issue">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>No benefit statements</span>
                </div>
            </div>
            
            <div class="content-section">
                <div class="content-label">Images</div>
                <div style="font-size: 12px; color: #6C757D; margin: 0.5rem 0;">
                    <i class="fas fa-image"></i> Product Image 1<br>
                    <i class="fas fa-image"></i> Product Image 2<br>
                    <i class="fas fa-image"></i> Product Image 3
                </div>
                <div class="content-issue">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>Only 3 images. Competitors average 8</span>
                </div>
                <div class="content-issue">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>Missing lifestyle images</span>
                </div>
            </div>
            
            <div class="content-section">
                <div class="content-label">Keywords Present</div>
                <div style="font-size: 12px; color: #6C757D;">cleaner, multi-purpose, cleaning</div>
                <div class="content-meta">3 keywords</div>
                <div class="content-issue">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>Missing 9 high-value keywords</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Column 2: AI-Generated Improvements
    with content_cols[1]:
        st.markdown("""
        <div class="content-column content-improved">
            <div class="content-header">
                <i class="fas fa-magic"></i>
                AI-Generated Improvements
            </div>
            <div class="content-subheader">Optimized content recommendations</div>
            
            <div class="content-section">
                <div class="content-label">New Title</div>
                <div class="content-text">CleanHome Eco-Friendly Multi-Purpose Cleaner | Antibacterial, Non-Toxic Formula</div>
                <div class="content-meta">82 characters</div>
                <div class="content-improvement">
                    <i class="fas fa-check-circle"></i>
                    <span>Added brand name</span>
                </div>
                <div class="content-improvement">
                    <i class="fas fa-check-circle"></i>
                    <span>Included 3 high-value keywords</span>
                </div>
                <div class="content-improvement">
                    <i class="fas fa-check-circle"></i>
                    <span>SEO-optimized length</span>
                </div>
            </div>
            
            <div class="content-section">
                <div class="content-label">New Description</div>
                <div class="content-text">CleanHome's powerful multi-purpose cleaner tackles tough messes on kitchen counters, bathroom tiles, glass, and more. Our eco-friendly, antibacterial formula is non-toxic, biodegradable, and safe for families and pets. No harsh chemicals—just effective cleaning with a fresh lemon scent. Perfect for daily use.</div>
                <div class="content-meta">46 words | 285 characters</div>
                <div class="content-improvement">
                    <i class="fas fa-check-circle"></i>
                    <span>Matches competitor length benchmark</span>
                </div>
                <div class="content-improvement">
                    <i class="fas fa-check-circle"></i>
                    <span>Includes benefit statements</span>
                </div>
                <div class="content-improvement">
                    <i class="fas fa-check-circle"></i>
                    <span>Lists use cases</span>
                </div>
            </div>
            
            <div class="content-section">
                <div class="content-label">New Images</div>
                <div style="font-size: 12px; color: #6C757D; margin: 0.5rem 0;">
                    <i class="fas fa-image"></i> Lifestyle Image 1: Person cleaning kitchen<br>
                    <i class="fas fa-image"></i> Lifestyle Image 2: Product on counter<br>
                    <i class="fas fa-image"></i> Ingredient flat lay<br>
                    <i class="fas fa-image"></i> Before/After: Clean surface<br>
                    <i class="fas fa-image"></i> Product Image 5: Family pack
                </div>
                <div class="content-meta">Total: 8 images (3 existing + 5 new)</div>
                <div class="content-improvement">
                    <i class="fas fa-check-circle"></i>
                    <span>Added 5 new images (meets 8-image benchmark)</span>
                </div>
                <div class="content-improvement">
                    <i class="fas fa-check-circle"></i>
                    <span>Includes lifestyle and in-use shots</span>
                </div>
            </div>
            
            <div class="content-section">
                <div class="content-label">Keywords Added</div>
                <div style="font-size: 12px; color: #6C757D;">eco-friendly, antibacterial, non-toxic, biodegradable, family-safe, pet-safe, lemon scent, kitchen cleaner, bathroom cleaner</div>
                <div class="content-meta">Total: 12 keywords (+9)</div>
                <div class="content-improvement">
                    <i class="fas fa-check-circle"></i>
                    <span>Added 9 high-value keywords</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Column 3: Improvements & Impact
    with content_cols[2]:
        st.markdown("""
        <div class="content-column content-impact">
            <div class="content-header">
                <i class="fas fa-chart-line"></i>
                Summary & Impact
            </div>
            
            <div class="content-section">
                <div class="content-label">Improvements Checklist</div>
                <ul class="improvement-list">
                    <li><i class="fas fa-check-circle" style="color: #28A745;"></i> Added 9 high-value keywords</li>
                    <li><i class="fas fa-check-circle" style="color: #28A745;"></i> Expanded description by 231 characters (+427%)</li>
                    <li><i class="fas fa-check-circle" style="color: #28A745;"></i> Added benefit-driven copy structure</li>
                    <li><i class="fas fa-check-circle" style="color: #28A745;"></i> Included ingredient/safety callouts</li>
                    <li><i class="fas fa-check-circle" style="color: #28A745;"></i> Added 5 lifestyle images</li>
                    <li><i class="fas fa-check-circle" style="color: #28A745;"></i> Optimized title for SEO (82 chars vs. 22)</li>
                    <li><i class="fas fa-check-circle" style="color: #28A745;"></i> Added sensory details (lemon scent)</li>
                    <li><i class="fas fa-check-circle" style="color: #28A745;"></i> Listed specific use cases</li>
                </ul>
            </div>
            
            <div class="impact-box">
                <div class="impact-title">
                    <i class="fas fa-bullseye"></i>
                    Predicted Performance Lift
                </div>
        """, unsafe_allow_html=True)
        
        impact_metric_cols = st.columns(2)
        with impact_metric_cols[0]:
            st.metric("Content Score", "88/100", "+30pts (+52%)")
            st.metric("CVR", "3.7%", "+0.9pts (+32%)")
        with impact_metric_cols[1]:
            st.metric("Organic Rank", "#1", "+2 spots")
            st.metric("Sales Lift", "$2,400", "over 2 weeks")
        
        st.progress(0.87, text="Confidence: 87%")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action Buttons
    if not st.session_state.content_deployed:
        btn_cols = st.columns([2, 1, 1, 1, 1])
        
        with btn_cols[1]:
            st.button("Generate Alternative", key="generate_alt", use_container_width=True)
        
        with btn_cols[2]:
            st.button("Edit Manually", key="edit_manual", use_container_width=True)
        
        with btn_cols[3]:
            if st.button("Cancel", key="content_cancel", use_container_width=True):
                st.session_state.selected_module = "Product Performance"
                st.rerun()
        
        with btn_cols[4]:
            if st.button("Deploy Changes", key="deploy_content", use_container_width=True, type="primary"):
                with st.spinner("Deploying content..."):
                    time.sleep(2)
                st.session_state.content_deployed = True
                st.balloons()
                st.rerun()
    else:
        # Show deployment status
        st.markdown("""
        <div class="success-notification">
            <i class="fas fa-check-circle" style="font-size: 20px;"></i>
            <span>Content deployed successfully to Target. Impact tracking enabled.</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Track Impact (Simulated - 2 Weeks Later)", key="track_impact_btn", use_container_width=False):
            st.session_state.show_impact_tracking = True
            st.rerun()
        
        if st.session_state.show_impact_tracking:
            st.markdown("---")
            st.markdown("### <i class='fas fa-chart-area'></i> Impact Tracking: SKU003 Content Update", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: #E8F5E9; border: 2px solid #28A745; border-radius: 8px; padding: 1.25rem; margin: 1.25rem 0;">
                <h4 style="color: #11377C; margin-bottom: 1rem;">Deployment Summary</h4>
                <p style="margin: 0.5rem 0;"><strong>Deployment Date:</strong> November 18, 2025</p>
                <p style="margin: 0.5rem 0;"><strong>Status:</strong> <span style="background: #28A745; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 700;">LIVE</span></p>
                <p style="margin: 0.5rem 0;"><strong>Time Since Deployment:</strong> 14 days</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Before/After Comparison**")
            
            comparison_data = pd.DataFrame({
                'Metric': ['Content Score', 'Organic Rank', 'CVR', 'Sales (2 weeks)', 'P-Page Traffic'],
                'Before (Pre-Fix)': ['58/100', '#3', '2.8%', '$12,400', '8,200'],
                'After (Post-Fix)': ['88/100', '#1', '3.9%', '$15,050', '11,500'],
                'Change': ['+30pts (+52%)', '+2 spots', '+1.1pts (+39%)', '+$2,650 (+21%)', '+3,300 (+40%)'],
                'Status': ['Exceeded forecast', 'Met forecast', 'Exceeded forecast', 'Exceeded forecast', 'Additional benefit']
            })
            
            st.dataframe(comparison_data, use_container_width=True, hide_index=True)
            
            st.markdown("""
            <div style="background: #E8F5E9; border-left: 4px solid #28A745; padding: 1rem; border-radius: 6px; margin: 1.25rem 0;">
                <p style="margin: 0.5rem 0;"><i class="fas fa-check-circle" style="color: #28A745; font-size: 20px; margin-right: 0.5rem;"></i></p>
                <p style="margin: 0.5rem 0;"><strong>AI Summary:</strong></p>
                <p style="margin: 0.5rem 0;">Your content update for SKU003 <strong>exceeded forecasted impact</strong>. Actual sales lift: <strong>$2,650</strong> (vs. forecast $2,400). Organic rank improved to <strong>#1</strong> as predicted. CVR recovery outpaced forecast by <strong>0.2pts</strong>.</p>
                <p style="margin-top: 1rem; color: #1CB192; font-weight: 600;">
                    <i class="fas fa-lightbulb" style="margin-right: 0.5rem;"></i>
                    Recommendation: Apply similar content strategy to SKU002 and SKU004.
                </p>
            </div>
            """, unsafe_allow_html=True)

# =============================================================================
# MAIN APP ROUTING
# =============================================================================
if st.session_state.selected_module == "Main Dashboard":
    render_main_dashboard()
elif st.session_state.selected_module == "Product Performance":
    render_product_performance()
elif st.session_state.selected_module == "Content Crafter":
    render_content_crafter()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6C757D; padding: 1.25rem;">
    <p style="margin: 0.5rem 0;">Skulytics eCommerce Performance Intelligence Platform | Demo Version | © 2025</p>
    <p style="font-size: 12px; margin: 0.5rem 0;">Production-ready analytics for CPG brands across all retail channels</p>
</div>
""", unsafe_allow_html=True)
