import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Skulytics - eCommerce Performance Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
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
        padding: 1rem;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem;
        max-width: 100% !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #11377C;
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    /* Floating Chat Button */
    .chat-fab {
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 60px;
        height: 60px;
        background: #FF8300;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(255,131,0,0.4);
        z-index: 9999;
        transition: all 0.3s ease;
        color: white;
        font-size: 24px;
    }
    
    .chat-fab:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(255,131,0,0.6);
    }
    
    /* Chat Panel Expanded */
    .chat-panel-expanded {
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 450px;
        max-height: 600px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        z-index: 9999;
        overflow-y: auto;
        border: 1px solid #E2E8F0;
    }
    
    .chat-header-fab {
        background: #11377C;
        color: white;
        padding: 1rem;
        border-radius: 12px 12px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 1;
    }
    
    .chat-close-btn {
        background: transparent;
        border: none;
        color: white;
        font-size: 20px;
        cursor: pointer;
        padding: 0.25rem 0.5rem;
    }
    
    .chat-content-fab {
        padding: 1.5rem;
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
        border-radius: 6px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        height: 100%;
    }
    
    .kpi-tile-positive {
        border-left: 3px solid #28A745;
    }
    
    .kpi-tile-negative {
        border-left: 3px solid #DC3545;
    }
    
    .kpi-tile-neutral {
        border-left: 3px solid #6C757D;
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
    
    /* Score Badges */
    .score-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 14px;
        text-align: center;
        min-width: 60px;
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
    
    /* Message Bubbles */
    .message-user {
        background: #EBF8FF;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        margin-left: 10%;
        font-size: 14px;
    }
    
    .message-ai {
        background: #F5F7FA;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        margin-right: 10%;
        font-size: 14px;
        line-height: 1.6;
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
    
    /* Hide Streamlit Default Elements */
    div[data-testid="stToolbar"] {
        display: none;
    }
    
    /* Adjust Streamlit Columns */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
if 'selected_module' not in st.session_state:
    st.session_state.selected_module = "Skulytics Performance"
if 'alert_clicked' not in st.session_state:
    st.session_state.alert_clicked = None
if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False
if 'chat_context' not in st.session_state:
    st.session_state.chat_context = ""
if 'chat_stage' not in st.session_state:
    st.session_state.chat_stage = "initial"  # initial, scenario, apply
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
if 'category_drilldown' not in st.session_state:
    st.session_state.category_drilldown = None

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
# FLOATING CHAT BUTTON (Bottom-Right, Always Visible)
# =============================================================================
def render_floating_chat_button():
    """Render persistent floating chat button"""
    if not st.session_state.show_chat:
        # Show floating button
        if st.button("💬", key="open_chat_fab", help="Open AI Assistant"):
            st.session_state.show_chat = True
            if not st.session_state.chat_context:
                st.session_state.chat_context = "General"
            st.rerun()
        
        # Add CSS positioning
        st.markdown("""
        <style>
        [data-testid="baseButton-secondary"][kind="secondary"]:has([title="Open AI Assistant"]) {
            position: fixed !important;
            bottom: 24px !important;
            right: 24px !important;
            width: 60px !important;
            height: 60px !important;
            border-radius: 50% !important;
            background: #FF8300 !important;
            color: white !important;
            font-size: 24px !important;
            box-shadow: 0 4px 12px rgba(255,131,0,0.4) !important;
            z-index: 9999 !important;
            padding: 0 !important;
            border: none !important;
        }
        [data-testid="baseButton-secondary"][kind="secondary"]:has([title="Open AI Assistant"]):hover {
            transform: scale(1.1) !important;
            box-shadow: 0 6px 20px rgba(255,131,0,0.6) !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Show expanded chat panel
        render_chat_panel_fab()

def render_chat_panel_fab():
    """Render full chat panel (expanded from FAB)"""
    
    # Container for chat panel
    st.markdown('<div class="chat-panel-expanded">', unsafe_allow_html=True)
    
    # Header with close button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<div class="chat-header-fab"><i class="fas fa-comments"></i> AI Assistant</div>', unsafe_allow_html=True)
    with col2:
        if st.button("✕", key="close_chat_fab"):
            st.session_state.show_chat = False
            st.rerun()
    
    # Chat content
    st.markdown('<div class="chat-content-fab">', unsafe_allow_html=True)
    
    context = st.session_state.chat_context
    stage = st.session_state.chat_stage
    
    if "SKU003" in context:
        # Initial Question
        st.markdown("""
        <div class="message-user">
            Why did conversion rate drop for SKU003 at Target, and what should I do?
        </div>
        """, unsafe_allow_html=True)
        
        # AI Response - 3 Factors
        st.markdown('''
        <div class="message-ai">
            <strong> Three factors contributed to the 22% CVR drop for SKU003 at Target: </strong> <br><br>
            
            <strong> 1. Primary Driver: </strong> Product was out-of-stock for 3 days (Nov 10-12), causing traffic to convert elsewhere <br><br>
            
            <strong> 2. Rating Impact: </strong> Rating dropped from 4.6 to 4.2 stars due to 3 recent 1-star reviews mentioning 'ineffective cleaning' <br><br>
            
            <strong> 3. Competitive Pressure:</strong> Competitor EcoClean cut price by 15% on similar product (now $8.99 vs. your $10.49) <br><br>
            
            <strong> Recommended Actions: </strong> <br>
            • <strong> Immediate:</strong> Ensure restock and implement inventory alerts <br>
            • <strong> Short-term:</strong> Address review concerns with response campaign <br>
            • <strong> Strategic:</strong> Improve content (add lifestyle images, expand description) <br><br>
            
            Would you like me to simulate recovery scenarios or route you to specific actions?
        </div>
        ''', unsafe_allow_html=True)
        
        if stage == "initial":
            # Quick Reply Buttons
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                if st.button("🎯 Simulate scenarios", key="chat_sim", use_container_width=True):
                    st.session_state.chat_stage = "scenario"
                    st.rerun()
            with btn_col2:
                if st.button("✍️ Show improvements", key="chat_content", use_container_width=True):
                    st.session_state.selected_module = "Content Crafter"
                    st.session_state.show_chat = False
                    st.rerun()
            with btn_col3:
                if st.button("❓ Fix stock + images?", key="chat_combined", use_container_width=True):
                    st.session_state.chat_stage = "scenario"
                    st.rerun()
        
        elif stage == "scenario":
            # User clicked on combined fix
            st.markdown("""
            <div class="message-user">
                What if we fix stock and images?
            </div>
            """, unsafe_allow_html=True)
            
            # AI Response - Combined Scenario
            st.markdown("""
            <div class="message-ai">
                <strong> Scenario: Combined Fixes (Restock + Content) </strong> <br><br>
                
                <strong> Actions: </strong> <br>
                • Eliminate OOS (maintain 100% stock availability) <br>
                • Add 2 lifestyle images (3 → 5 total) <br>
                • Expand description (+150 chars with keywords) <br><br>
                
                <strong> Forecasted Impact: </strong> <br>
                • Content Score: 58 → 85 (+27pts)<br>
                • Organic Rank: #3 → #1 (+2 spots)<br>
                • CVR: 2.8% → 4.1% (+1.3pts, +46%)<br>
                • Sales Lift: +$3,200 over next 2 weeks<br>
                • Confidence: 89% <br><br>
                
                <strong> Why This Works:</strong> The combination addresses both availability and appeal, maximizing conversion recovery while defending against competitor pricing. <br><br>
                
                Would you like to apply these changes?
            </div>
            """, unsafe_allow_html=True)
            
            # Action Buttons
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("✅ Apply Changes", key="chat_apply", use_container_width=True, type="primary"):
                    st.session_state.selected_module = "Content Crafter"
                    st.session_state.show_chat = False
                    st.rerun()
            with btn_col2:
                if st.button("🔄 Compare Scenarios", key="chat_compare", use_container_width=True):
                    st.session_state.selected_module = "Product Performance"
                    st.session_state.show_chat = False
                    st.rerun()
    
    else:
        # Generic chat for other contexts
        st.markdown(f"""
        <div class="message-user">
            Tell me more about: {context}
        </div>
        <div class="message-ai">
            I can help you understand this issue. Would you like me to: <br><br>
            • Show detailed analysis<br>
            • Recommend specific actions<br>
            • Simulate potential solutions<br><br>
            Click a button below to proceed.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Close Chat", key="chat_close_generic"):
            st.session_state.show_chat = False
            st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: white; margin: 0;"><i class="fas fa-chart-line"></i> Skulytics</h2>
        <p style="color: rgba(255,255,255,0.7); font-size: 12px; margin-top: 0.5rem;">eCommerce Performance Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Skulytics Performance", key="nav_main", use_container_width=True):
        st.session_state.selected_module = "Skulytics Performance"
        st.rerun()
    
    if st.button("Product Performance", key="nav_product", use_container_width=True):
        st.session_state.selected_module = "Product Performance"
        st.rerun()
    
    if st.button("✍️ Content Crafter", key="nav_content", use_container_width=True):
        st.session_state.selected_module = "Content Crafter"
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Coming Soon:**")
    st.button("Demand Forecasting", key="nav_demand", disabled=True, use_container_width=True)
    st.button("Media Spend", key="nav_media", disabled=True, use_container_width=True)
    st.button("Competitor Intel", key="nav_competitor", disabled=True, use_container_width=True)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def show_chat_panel(context_text):
    """Open chat panel with context"""
    st.session_state.show_chat = True
    st.session_state.chat_context = context_text
    st.session_state.chat_stage = "initial"
    st.rerun()

def render_kpi_tile(label, value, change, change_type, icon_class):
    """Render a KPI tile with proper styling based on change type"""
    border_class = f"kpi-tile-{change_type}"
    change_class = f"kpi-change-{change_type}"
    
    st.markdown(f"""
    <div class="kpi-tile {border_class}">
        <div class="kpi-header">
            <div class="kpi-label">{label}</div>
            <i class="{icon_class} kpi-icon"></i>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-change {change_class}">{change}</div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# MODULE 1: SKULYTICS PERFORMANCE (Main Dashboard)
# =============================================================================
def render_main_dashboard():
    st.markdown("## Skulytics Performance", unsafe_allow_html=True)
    st.markdown("---")
    
    # Alert Panel
    st.markdown("### Active Alerts", unsafe_allow_html=True)
    
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
            if st.button("Ask in Chat", key="alert1_chat", use_container_width=True):
                show_chat_panel("SKU003 Conversion Drop")
    
    # Alert 2-5
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
            if st.button("Ask in Chat", key="alert2_chat", use_container_width=True):
                show_chat_panel("SKU002 Views Decline")
    
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
            if st.button("Ask in Chat", key="alert3_chat", use_container_width=True):
                show_chat_panel("SKU001 ROAS Opportunity")
    
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
            if st.button("Ask in Chat", key="alert4_chat", use_container_width=True):
                show_chat_panel("SKU007 Stock Issue")
    
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
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("View Full Product Analysis", key="view_analysis", use_container_width=True):
                st.session_state.selected_module = "Product Performance"
                st.rerun()
            if st.button("Clear Filters", key="clear_filters", use_container_width=True):
                st.session_state.alert_clicked = None
                st.session_state.filter_sku = "All SKUs"
                st.session_state.filter_retailer = "All Retailers"
                st.rerun()
        
        st.markdown("---")
    
    # Determine if filtered
    is_filtered = st.session_state.alert_clicked is not None
    
    # TOP 6 MOST IMPORTANT KPIs IN ONE ROW
    st.markdown("### Key Performance Indicators", unsafe_allow_html=True)
    
    kpi_row = st.columns(6)
    
    with kpi_row[0]:
        value = "$12,400" if is_filtered else "$1,247,890"
        change = "↓ 18% vs LW" if is_filtered else "↑ 12.4% vs LM"
        change_type = "negative" if is_filtered else "positive"
        render_kpi_tile("Gross Sales", value, change, change_type, "fas fa-dollar-sign")
    
    with kpi_row[1]:
        value = "2.8%" if is_filtered else "3.4%"
        change = "↓ 22% vs LW" if is_filtered else "↓ 2.1% vs LM"
        render_kpi_tile("CVR (Conversion)", value, change, "negative", "fas fa-percentage")
    
    with kpi_row[2]:
        value = "58/100" if is_filtered else "72/100"
        change = "↓ 33% vs LM" if is_filtered else "↓ 8pts vs LM"
        render_kpi_tile("Content Health", value, change, "negative", "fas fa-file-alt")
    
    with kpi_row[3]:
        value = "#3" if is_filtered else "#6.2"
        change = "Stable"
        render_kpi_tile("Avg Organic Rank", value, change, "neutral", "fas fa-trophy")
    
    with kpi_row[4]:
        value = "8.5%" if is_filtered else "4.2%"
        change = "↑ 8.5pts vs LW" if is_filtered else "↑ 1.8% vs LM"
        render_kpi_tile("Out of Stock %", value, change, "negative", "fas fa-warehouse")
    
    with kpi_row[5]:
        st.markdown("""
        <div class="kpi-tile kpi-tile-neutral">
            <div class="kpi-header">
                <div class="kpi-label">Total Media Spend</div>
                <i class="fas fa-bullhorn kpi-icon"></i>
            </div>
            <div class="kpi-value">$124,500</div>
            <div class="kpi-change kpi-change-neutral">↑ 15% vs LM</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Section
    st.markdown("### Performance Analytics", unsafe_allow_html=True)
    
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
        fig.update_yaxes(gridcolor='#E2E8F0', gridwidth=1)
        fig.update_xaxes(showgrid=False)
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_cols[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        if st.session_state.category_drilldown:
            st.markdown(f'<div class="chart-title">Products in {st.session_state.category_drilldown} Category</div>', unsafe_allow_html=True)
            
            category_skus = sku_data[sku_data['category'] == st.session_state.category_drilldown]
            category_sales = top_products[top_products['sku_id'].isin(category_skus['sku_id'].values)]
            
            colors = ['#DC3545' if sku == 'SKU003' and is_filtered else '#1CB192' for sku in category_sales['sku_id']]
            
            fig = go.Figure(go.Bar(
                x=category_sales['sales'],
                y=category_sales['sku_name'],
                orientation='h',
                marker=dict(color=colors),
                text=category_sales['sales'].apply(lambda x: f'${x:,.0f}'),
                textposition='outside'
            ))
            
            if st.button("← Back to Categories", key="back_to_categories"):
                st.session_state.category_drilldown = None
                st.rerun()
        else:
            st.markdown('<div class="chart-title">Sales by Category - November 2025</div>', unsafe_allow_html=True)
            
            category_sales = sku_data.merge(top_products, on='sku_id').groupby('category')['sales'].sum().reset_index()
            category_sales = category_sales.sort_values('sales', ascending=True)
            
            fig = go.Figure(go.Bar(
                x=category_sales['sales'],
                y=category_sales['category'],
                orientation='h',
                marker=dict(color='#1CB192'),
                text=category_sales['sales'].apply(lambda x: f'${x:,.0f}'),
                textposition='outside'
            ))
            
            st.markdown("<p style='font-size: 12px; color: #6C757D;'>Click a category to drill down into products</p>", unsafe_allow_html=True)
        
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
        fig.update_xaxes(gridcolor='#E2E8F0', gridwidth=1)
        fig.update_yaxes(showgrid=False)
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        if not st.session_state.category_drilldown:
            drill_cols = st.columns(len(category_sales))
            for i, (idx, row) in enumerate(category_sales.iterrows()):
                with drill_cols[i]:
                    if st.button(row['category'], key=f"drill_{row['category']}", use_container_width=True):
                        st.session_state.category_drilldown = row['category']
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Commerce Journey - Bar Trends + Heatmap
    st.markdown("### Commerce Journey Performance", unsafe_allow_html=True)
    
    journey_cols = st.columns(2)
    
    with journey_cols[0]:
        st.markdown("**Journey Stage Trends (Last 30 Days)**")
        
        stages = ['Discovery', 'Engagement', 'Conversion', 'Sales']
        values_filtered = [48, 16.8, 2.8, 12.4] if is_filtered else [245, 89, 3.4, 1247.89]
        values_prev = [52, 18.5, 3.6, 15.1] if is_filtered else [235, 92, 3.5, 1180]
        
        for stage, val, prev_val in zip(stages, values_filtered, values_prev):
            pct_change = ((val - prev_val) / prev_val * 100)
            color = '#28A745' if pct_change > 0 else '#DC3545'
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[prev_val, val],
                y=['Previous', 'Current'],
                orientation='h',
                marker=dict(color=['#E2E8F0', color]),
                text=[f'{prev_val:.1f}', f'{val:.1f}'],
                textposition='inside'
            ))
            
            fig.update_layout(
                title=stage,
                height=120,
                showlegend=False,
                margin=dict(l=0, r=0, t=30, b=0),
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            fig.update_xaxes(showticklabels=False, showgrid=False)
            fig.update_yaxes(showticklabels=False)
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with journey_cols[1]:
        st.markdown("**Top 10 Products Heatmap - Key Metrics**")
        
        top10 = top_products.head(10).copy()
        top10 = top10.merge(sku_data[['sku_id', 'sku_name']], on='sku_id')
        
        heatmap_data = []
        for sku_id in top10['sku_id']:
            perf = performance_data[performance_data['sku_id'] == sku_id].iloc[0] if len(performance_data[performance_data['sku_id'] == sku_id]) > 0 else None
            content = content_data[content_data['sku_id'] == sku_id].iloc[0] if len(content_data[content_data['sku_id'] == sku_id]) > 0 else None
            
            if perf is not None and content is not None:
                heatmap_data.append({
                    'SKU': sku_id,
                    'CVR': perf['cvr'],
                    'Rank': 11 - perf['organic_rank'],
                    'Content': content['overall_health'],
                    'OOS': 100 - perf['oos_pct']
                })
        
        heatmap_df = pd.DataFrame(heatmap_data)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_df[['CVR', 'Rank', 'Content', 'OOS']].values.T,
            x=heatmap_df['SKU'],
            y=['CVR', 'Rank', 'Content', 'Stock'],
            colorscale='RdYlGn',
            text=heatmap_df[['CVR', 'Rank', 'Content', 'OOS']].values.T,
            texttemplate='%{text:.1f}',
            textfont={"size": 10},
            colorbar=dict(title="Score")
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# =============================================================================
# MODULE 2: PRODUCT PERFORMANCE
# =============================================================================
def render_product_performance():
    st.markdown("## Product Performance Analysis", unsafe_allow_html=True)
    
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
    
    st.markdown("### SKU003 Performance Snapshot", unsafe_allow_html=True)
    
    meta_row1 = st.columns(3)
    
    with meta_row1[0]:
        st.markdown("""
        <div class="kpi-tile kpi-tile-neutral">
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
        <div class="kpi-tile kpi-tile-negative">
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
        <div class="kpi-tile kpi-tile-negative">
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
        <div class="kpi-tile kpi-tile-negative">
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
        <div class="kpi-tile kpi-tile-negative">
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
        <div class="kpi-tile kpi-tile-negative">
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
    
    st.markdown("### Comparative Analytics", unsafe_allow_html=True)
    
    chart_cols = st.columns(2)
    
    with chart_cols[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">SKU Performance Comparison - Household Category at Target</div>', unsafe_allow_html=True)
        
        peer_skus = ['SKU006', 'SKU015', 'SKU018', 'SKU012', 'SKU009', 'SKU003', 'SKU021', 'SKU024']
        peer_names = ['Laundry Detergent', 'Dish Soap', 'Wipes', 'Glass Cleaner', 'Floor Cleaner', 'Multi-Purpose', 'Bathroom Cleaner', 'Kitchen Spray']
        peer_sales = [22000, 19000, 17000, 16000, 15000, 12400, 11000, 10000]
        colors = ['#DC3545' if sku == 'SKU003' else '#1CB192' for sku in peer_skus]
        
        fig = go.Figure(go.Bar(
            x=peer_sales,
            y=peer_names,
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
        fig.update_xaxes(gridcolor='#E2E8F0', gridwidth=1)
        
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
        fig.update_yaxes(gridcolor='#E2E8F0', gridwidth=1)
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Opportunity Analysis & Recommendations", unsafe_allow_html=True)
    
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
    
    if st.session_state.simulate_modal_open:
        st.markdown("---")
        st.markdown("### Scenario Simulator: Content Score Improvement", unsafe_allow_html=True)
        
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
                    time.sleep(1)
                st.success("Content update queued. Routing to Content Crafter for deployment.")
                time.sleep(1)
                st.session_state.simulate_modal_open = False
                st.session_state.selected_module = "Content Crafter"
                st.rerun()

# =============================================================================
# MODULE 3: CONTENT CRAFTER
# =============================================================================
def render_content_crafter():
    st.markdown("## Content Crafter", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="banner banner-success">
        <i class="fas fa-lightbulb banner-icon" style="color: #1CB192;"></i>
        <div class="banner-content">
            <h4>SKU003 — Content Score has dropped 33% at Target</h4>
            <p style="font-style: italic;">AI Recommendation: Add lifestyle images and optimize description to improve SEO.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Content Health Scores", unsafe_allow_html=True)
    
    score_cols = st.columns(7)
    
    scores = [
        ("Overall", "58", "red"),
        ("Title", "72", "yellow"),
        ("Description", "45", "red"),
        ("Image", "42", "red"),
        ("Keyword", "55", "red"),
        ("Rating", "4.2/5", "yellow"),
        ("Review", "68", "yellow")
    ]
    
    for i, (label, score, color) in enumerate(scores):
        with score_cols[i]:
            score_class = f"score-{color}"
            highlight = 'border: 3px solid #FF8300; box-shadow: 0 0 15px rgba(255,131,0,0.3);' if label == "Image" else 'border: 1px solid #E2E8F0;'
            
            st.markdown(f"""
            <div style="{highlight} background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                <div style="font-size: 11px; color: #6C757D; font-weight: 600; text-transform: uppercase; margin-bottom: 0.5rem;">{label}</div>
                <div class="score-badge {score_class}">{score}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Content Optimization", unsafe_allow_html=True)
    
    content_cols = st.columns(3)
    
    with content_cols[0]:
        st.markdown("#### Existing Content")
        st.caption("Current state at Target")
        
        st.markdown("**Product Title**")
        st.info("Multi-Purpose Cleaner")
        st.caption("22 characters")
        st.error("⚠️ Missing keywords: 'eco-friendly', 'antibacterial', 'non-toxic'")
        st.error("⚠️ No brand mention")
        
        st.markdown("**Product Description**")
        st.info("Effective cleaning solution for multiple surfaces.")
        st.caption("7 words | 54 characters")
        st.error("⚠️ 75% shorter than competitors (avg 215 chars)")
        st.error("⚠️ Missing ingredient information")
        st.error("⚠️ No benefit statements")
        
        st.markdown("**Images**")
        st.caption("• Product Image 1")
        st.caption("• Product Image 2")
        st.caption("• Product Image 3")
        st.error("⚠️ Only 3 images. Competitors average 8")
        st.error("⚠️ Missing lifestyle images")
        
        st.markdown("**Keywords Present**")
        st.caption("cleaner, multi-purpose, cleaning")
        st.caption("3 keywords")
        st.error("⚠️ Missing 9 high-value keywords")
    
    with content_cols[1]:
        st.markdown("#### AI-Generated Improvements ✨")
        st.caption("Optimized content recommendations")
        
        st.markdown("**New Title**")
        st.success("CleanHome Eco-Friendly Multi-Purpose Cleaner | Antibacterial, Non-Toxic Formula")
        st.caption("82 characters")
        st.success("✓ Added brand name")
        st.success("✓ Included 3 high-value keywords")
        st.success("✓ SEO-optimized length")
        
        st.markdown("**New Description**")
        st.success("CleanHome's powerful multi-purpose cleaner tackles tough messes on kitchen counters, bathroom tiles, glass, and more. Our eco-friendly, antibacterial formula is non-toxic, biodegradable, and safe for families and pets. No harsh chemicals—just effective cleaning with a fresh lemon scent. Perfect for daily use.")
        st.caption("46 words | 285 characters")
        st.success("✓ Matches competitor length benchmark")
        st.success("✓ Includes benefit statements")
        st.success("✓ Lists use cases")
        
        st.markdown("**New Images**")
        st.caption("• Lifestyle Image 1: Person cleaning kitchen")
        st.caption("• Lifestyle Image 2: Product on counter")
        st.caption("• Ingredient flat lay")
        st.caption("• Before/After: Clean surface")
        st.caption("• Product Image 5: Family pack")
        st.caption("Total: 8 images (3 existing + 5 new)")
        st.success("✓ Added 5 new images (meets 8-image benchmark)")
        st.success("✓ Includes lifestyle and in-use shots")
        
        st.markdown("**Keywords Added**")
        st.caption("eco-friendly, antibacterial, non-toxic, biodegradable, family-safe, pet-safe, lemon scent, kitchen cleaner, bathroom cleaner")
        st.caption("Total: 12 keywords (+9)")
        st.success("✓ Added 9 high-value keywords")
    
    with content_cols[2]:
        st.markdown("#### Summary & Impact")
        
        st.markdown("**Improvements Checklist**")
        st.success("✓ Added 9 high-value keywords")
        st.success("✓ Expanded description by 231 characters (+427%)")
        st.success("✓ Added benefit-driven copy structure")
        st.success("✓ Included ingredient/safety callouts")
        st.success("✓ Added 5 lifestyle images")
        st.success("✓ Optimized title for SEO (82 chars vs. 22)")
        st.success("✓ Added sensory details (lemon scent)")
        st.success("✓ Listed specific use cases")
        
        st.markdown("**Predicted Performance Lift**")
        
        impact_cols = st.columns(2)
        with impact_cols[0]:
            st.metric("Content Score", "88/100", "+30pts (+52%)")
            st.metric("CVR", "3.7%", "+0.9pts (+32%)")
        with impact_cols[1]:
            st.metric("Organic Rank", "#1", "+2 spots")
            st.metric("Sales Lift", "$2,400", "over 2 weeks")
        
        st.progress(0.87, text="Confidence: 87%")
    
    st.markdown("---")
    
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
            st.markdown("### Impact Tracking: SKU003 Content Update", unsafe_allow_html=True)
            
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
                'Status': ['✓ Exceeded forecast', '✓ Met forecast', '✓ Exceeded forecast', '✓ Exceeded forecast', '✓ Additional benefit']
            })
            
            st.dataframe(comparison_data, use_container_width=True, hide_index=True)
            
            st.success("""
            **AI Summary:** Your content update for SKU003 **exceeded forecasted impact**. Actual sales lift: **$2,650** (vs. forecast $2,400). 
            Organic rank improved to **#1** as predicted. CVR recovery outpaced forecast by **0.2pts**.
            
            💡 **Recommendation:** Apply similar content strategy to SKU002 and SKU004.
            """)

# =============================================================================
# MAIN APP ROUTING
# =============================================================================
if st.session_state.selected_module == "Skulytics Performance":
    render_main_dashboard()
elif st.session_state.selected_module == "Product Performance":
    render_product_performance()
elif st.session_state.selected_module == "Content Crafter":
    render_content_crafter()

# Render Floating Chat Button (Always visible)
render_floating_chat_button()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6C757D; padding: 1.25rem;">
    <p style="margin: 0.5rem 0;">Skulytics eCommerce Performance Intelligence Platform | Demo Version | © 2025</p>
    <p style="font-size: 12px; margin: 0.5rem 0;">Production-ready analytics for CPG brands across all retail channels</p>
</div>
""", unsafe_allow_html=True)
