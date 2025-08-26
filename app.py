import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import time
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# Import custom modules
from sector_rotation import render_sector_rotation
from market_cover import render_market_cover
from trending_news import render_trending_news
from data_sources import DataManager
from utils import setup_scheduler, manual_refresh

# Page configuration
st.set_page_config(
    page_title="Indian Stock Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data manager
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()

# Initialize scheduler
if 'scheduler_initialized' not in st.session_state:
    setup_scheduler()
    st.session_state.scheduler_initialized = True

# Main title and refresh button
col1, col2 = st.columns([4, 1])
with col1:
    st.title("SWING-LEOFY MARKET DOMINATION")
    st.caption("Real-time NSE data feeds with sector analysis and financial news")

with col2:
    st.write("")  # Add some spacing
    if st.button("🔄 Refresh Data", key="manual_refresh"):
        manual_refresh()
        st.success("Data refreshed successfully!")
        st.rerun()

# Display last update time
if 'last_update' in st.session_state:
    ist = pytz.timezone('Asia/Kolkata')
    last_update = st.session_state.last_update.astimezone(ist)
    st.info(f"Last Updated: {last_update.strftime('%Y-%m-%d %I:%M:%S %p IST')}")

# Sidebar navigation  
st.sidebar.title("Navigation")

# Advanced CSS for animated navigation buttons
st.sidebar.markdown("""
<style>
div.stButton > button {
    width: 100%;
    height: 70px;
    font-size: 14px;
    font-weight: bold;
    border-radius: 15px;
    border: none;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin: 10px 0;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}

div.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
}

div.stButton > button:hover::before {
    left: 100%;
}

div.stButton > button:active {
    background: linear-gradient(135deg, #5a67d8 0%, #667eea 100%);
    transform: translateY(-2px) scale(1.02);
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
    100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
}

@keyframes slideInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.stApp {
    background-color: #f0f2f6; /* Light gray background */
}

.stMarkdown h1 {
    text-align: center;
    color: #333;
    animation: slideInUp 0.8s ease-out;
}

.stMarkdown h3 {
    color: #555;
}

.stMarkdown p {
    color: #666;
}

.stButton {
    animation: slideInUp 0.5s ease-out;
}

.stAlert {
    animation: fadeIn 0.5s ease-out;
}

.stSpinner {
    animation: pulse 1.5s infinite;
}

.nav-container {
    padding: 10px 0;
}

/* Custom scrollbar for better aesthetics */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}
</style>
""", unsafe_allow_html=True)

# Vertical navigation buttons
st.sidebar.markdown('<div class="nav-container">', unsafe_allow_html=True)

if st.sidebar.button("🔄 Sector Rotation", key="sector_btn", use_container_width=True):
    st.session_state.current_page = "🔄 Sector Rotation"

if st.sidebar.button("📊 Market Cover", key="market_btn", use_container_width=True):
    st.session_state.current_page = "📊 Market Cover"

if st.sidebar.button("📰 Trending News", key="news_btn", use_container_width=True):
    st.session_state.current_page = "📰 Trending News"

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Initialize page if not set
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🔄 Sector Rotation"

page = st.session_state.current_page

# Auto-refresh indicator
next_refresh = datetime.now(pytz.timezone('Asia/Kolkata')).replace(hour=16, minute=0, second=0, microsecond=0)
if next_refresh <= datetime.now(pytz.timezone('Asia/Kolkata')):
    next_refresh = next_refresh.replace(day=next_refresh.day + 1)

st.sidebar.info(f"⏰ Next auto-refresh: {next_refresh.strftime('%I:%M %p IST')}")

# Market status indicator
market_status = st.session_state.data_manager.get_market_status()
if market_status == "OPEN":
    st.sidebar.success("🟢 Market is OPEN")
elif market_status == "CLOSED":
    st.sidebar.error("🔴 Market is CLOSED")
else:
    st.sidebar.warning("🟡 Market status unknown")

# Render selected page
if page == "🔄 Sector Rotation":
    render_sector_rotation()
elif page == "📊 Market Cover":
    render_market_cover()
elif page == "📰 Trending News":
    render_trending_news()

# Clean footer without revealing sources
st.sidebar.markdown("---")
st.sidebar.markdown("*Premium Market Intelligence*")
st.sidebar.markdown("*Auto-refresh: Daily at 4:00 PM IST*")
