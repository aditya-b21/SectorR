import streamlit as st
from datetime import datetime, time
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

def setup_scheduler():
    """Setup the auto-refresh scheduler for 4 PM IST daily"""
    try:
        scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Kolkata'))
        
        # Schedule daily refresh at 4 PM IST (after market closes)
        scheduler.add_job(
            func=scheduled_refresh,
            trigger="cron",
            hour=16,
            minute=0,
            second=0,
            timezone=pytz.timezone('Asia/Kolkata'),
            id='daily_market_refresh',
            replace_existing=True
        )
        
        if not scheduler.running:
            scheduler.start()
            print("✅ Auto-refresh scheduler started successfully - Daily refresh at 4:00 PM IST")
        
        st.session_state.scheduler = scheduler
        
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown() if scheduler.running else None)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to start scheduler: {str(e)}")
        return False

def scheduled_refresh():
    """Function called by scheduler for auto-refresh"""
    try:
        # Clear all cached data
        clear_cached_data()
        
        # Update last refresh time
        st.session_state.last_update = datetime.now(pytz.timezone('Asia/Kolkata'))
        
        # Log the refresh
        print(f"Auto-refresh completed at {st.session_state.last_update}")
        
    except Exception as e:
        print(f"Error during scheduled refresh: {str(e)}")

def manual_refresh():
    """Manual refresh function triggered by button"""
    try:
        # Clear all cached data
        clear_cached_data()
        
        # Refresh data manager
        if hasattr(st.session_state, 'data_manager'):
            st.session_state.data_manager.refresh_all_data()
        
        # Update last refresh time
        st.session_state.last_update = datetime.now(pytz.timezone('Asia/Kolkata'))
        
        return True
        
    except Exception as e:
        st.error(f"Error during manual refresh: {str(e)}")
        return False

def clear_cached_data():
    """Clear all cached data from session state"""
    cached_keys = [
        'sector_data',
        'index_data', 
        'news_data',
        'heatmap_data',
        'fii_dii_data',
        'gainers_losers_data'
    ]
    
    for key in cached_keys:
        if key in st.session_state:
            del st.session_state[key]

def format_indian_currency(amount):
    """Format amount in Indian currency format"""
    if amount >= 10000000:  # 1 crore
        return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000:  # 1 lakh
        return f"₹{amount/100000:.2f} L"
    elif amount >= 1000:  # 1 thousand
        return f"₹{amount/1000:.2f} K"
    else:
        return f"₹{amount:.2f}"

def get_market_timing():
    """Get Indian market timing information"""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    
    # Market hours: 9:15 AM to 3:30 PM IST
    market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
    market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
    
    if market_open <= now <= market_close:
        # Check if it's a weekday (Monday = 0, Sunday = 6)
        if now.weekday() < 5:  # Monday to Friday
            return "OPEN"
    
    return "CLOSED"

def calculate_percentage_change(current, previous):
    """Calculate percentage change between two values"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def validate_api_response(response):
    """Validate API response and return cleaned data"""
    if not response:
        return None
    
    if isinstance(response, dict):
        if 'error' in response:
            st.warning(f"API Error: {response['error']}")
            return None
        return response
    
    return response

def get_trend_indicator(change):
    """Get trend indicator based on change value"""
    if change > 0:
        return "↑", "green"
    elif change < 0:
        return "↓", "red"
    else:
        return "→", "gray"

def format_volume(volume):
    """Format volume in readable format"""
    if volume >= 10000000:  # 1 crore
        return f"{volume/10000000:.2f}Cr"
    elif volume >= 100000:  # 1 lakh
        return f"{volume/100000:.2f}L"
    elif volume >= 1000:  # 1 thousand
        return f"{volume/1000:.2f}K"
    else:
        return str(int(volume))

def check_internet_connection():
    """Check if internet connection is available"""
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def handle_api_error(error, api_name):
    """Handle API errors gracefully"""
    error_messages = {
        'connection': f"Connection error with {api_name}. Please check your internet connection.",
        'timeout': f"Request to {api_name} timed out. Please try again later.",
        'rate_limit': f"Rate limit exceeded for {api_name}. Please wait before making more requests.",
        'authentication': f"Authentication failed for {api_name}. Please check your API key.",
        'not_found': f"Requested data not found on {api_name}.",
        'server_error': f"Server error on {api_name}. Please try again later."
    }
    
    return error_messages.get(error, f"Unknown error occurred with {api_name}")

def log_data_fetch(source, status, message=""):
    """Log data fetch attempts for debugging"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {source}: {status}"
    if message:
        log_entry += f" - {message}"
    
    # In a production environment, you might want to write to a file
    print(log_entry)

def get_cache_key(prefix, params=None):
    """Generate cache key for data storage"""
    key = prefix
    if params:
        key += "_" + "_".join([str(v) for v in params.values()])
    return key

def is_cache_valid(cache_key, validity_minutes=5):
    """Check if cached data is still valid"""
    if cache_key not in st.session_state:
        return False
    
    cached_time = st.session_state.get(f"{cache_key}_timestamp")
    if not cached_time:
        return False
    
    now = datetime.now()
    if (now - cached_time).total_seconds() > validity_minutes * 60:
        return False
    
    return True

def set_cache(cache_key, data):
    """Set data in cache with timestamp"""
    st.session_state[cache_key] = data
    st.session_state[f"{cache_key}_timestamp"] = datetime.now()

def get_cache(cache_key):
    """Get data from cache"""
    return st.session_state.get(cache_key)
