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
    st.title("🇮🇳 Indian Stock Market Dashboard")
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
page = st.sidebar.selectbox(
    "Select Page",
    ["🔄 Sector Rotation", "📊 Market Cover", "📰 Trending News"],
    key="navigation"
)

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
