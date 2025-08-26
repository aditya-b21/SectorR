import streamlit as st
import streamlit.components.v1 as components

def render_tradingview_widget(symbol, height=500, theme="dark"):
    """Render TradingView widget for a specific symbol"""
    
    # Convert Indian stock symbols to TradingView format
    if symbol.endswith('.NS'):
        tv_symbol = f"NSE:{symbol.replace('.NS', '')}"
    elif symbol.startswith('^'):
        tv_symbol = f"NSE:{symbol.replace('^', '')}"
    else:
        tv_symbol = f"NSE:{symbol}"
    
    tradingview_html = f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container" style="height:{height}px;width:100%;border-radius:12px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.15);">
      <div class="tradingview-widget-container__widget" style="height:calc({height}px - 32px);width:100%"></div>
      <div class="tradingview-widget-copyright" style="display:none;">
        <span class="blue-text">Professional Chart View</span>
      </div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
      {{
        "autosize": true,
        "symbol": "{tv_symbol}",
        "interval": "D",
        "timezone": "Asia/Kolkata",
        "theme": "{theme}",
        "style": "1",
        "locale": "en",
        "enable_publishing": false,
        "withdateranges": true,
        "range": "YTD",
        "hide_side_toolbar": false,
        "allow_symbol_change": false,
        "details": true,
        "hotlist": false,
        "calendar": false,
        "studies": [
          "STD;SMA",
          "STD;MACD"
        ],
        "container_id": "tradingview_{symbol.replace('.', '_').replace('^', '_')}",
        "hide_legend": false,
        "save_image": false,
        "hide_volume": false,
        "support_host": "https://www.tradingview.com"
      }}
      </script>
    </div>
    <!-- TradingView Widget END -->
    """
    
    components.html(tradingview_html, height=height)

def render_tradingview_modal(symbol, stock_name):
    """Render TradingView chart in a modal"""
    
    modal_key = f"modal_{symbol.replace('.', '_').replace('^', '_')}"
    
    if st.button(f"📈 {stock_name}", key=f"btn_{symbol}", help=f"View {stock_name} chart"):
        st.session_state[modal_key] = True
    
    if st.session_state.get(modal_key, False):
        # Custom CSS for modal
        st.markdown("""
        <style>
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.8);
            z-index: 1000;
            display: flex;
            justify-content: center;
            align-items: center;
            animation: fadeIn 0.3s ease-out;
        }
        
        .modal-content {
            background: white;
            border-radius: 20px;
            width: 90vw;
            height: 80vh;
            max-width: 1200px;
            position: relative;
            animation: slideIn 0.3s ease-out;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        }
        
        .modal-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 20px 20px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .modal-close {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        .modal-close:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.1);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideIn {
            from { 
                opacity: 0; 
                transform: scale(0.8) translateY(-50px); 
            }
            to { 
                opacity: 1; 
                transform: scale(1) translateY(0); 
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            col1, col2, col3 = st.columns([1, 10, 1])
            
            with col2:
                st.markdown(f"""
                <div class="modal-overlay">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h2>📈 {stock_name} Live Chart</h2>
                            <button class="modal-close" onclick="closeModal()">×</button>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Close modal button
                if st.button("✕ Close Chart", key=f"close_{modal_key}"):
                    st.session_state[modal_key] = False
                    st.rerun()
                
                # Render the TradingView chart
                render_tradingview_widget(symbol, height=600, theme="dark")

def render_indices_overview():
    """Render overview of major Indian indices"""
    
    major_indices = [
        ("NIFTY 50", "NIFTY"),
        ("SENSEX", "SENSEX"), 
        ("NIFTY BANK", "BANKNIFTY"),
        ("NIFTY IT", "CNXIT"),
        ("NIFTY PHARMA", "CNXPHARMA"),
        ("NIFTY FMCG", "CNXFMCG"),
        ("NIFTY AUTO", "CNXAUTO"),
        ("NIFTY METAL", "CNXMETAL")
    ]
    
    st.subheader("📊 Major Indian Indices - Live Charts")
    
    # Display indices in tabs
    tabs = st.tabs([name for name, _ in major_indices])
    
    for i, (name, symbol) in enumerate(major_indices):
        with tabs[i]:
            st.markdown(f"### {name} Live Chart")
            render_tradingview_widget(symbol, height=400)

def render_sector_chart(sector_name, symbol):
    """Render sector-specific chart"""
    
    st.markdown(f"### 📈 {sector_name} Performance")
    render_tradingview_widget(symbol, height=450)

def render_stock_modal_button(stock_symbol, stock_name):
    """Render a button that opens stock chart in modal"""
    
    # Create unique key for the stock
    modal_key = f"stock_modal_{stock_symbol.replace('.', '_').replace('-', '_')}"
    button_key = f"stock_btn_{stock_symbol.replace('.', '_').replace('-', '_')}"
    
    # Stock button with professional styling
    if st.button(
        f"📊 {stock_name}", 
        key=button_key,
        help=f"Click to view live chart for {stock_name}",
        use_container_width=True
    ):
        st.session_state[modal_key] = True
    
    # Modal logic with bigger size
    if st.session_state.get(modal_key, False):
        # Add custom CSS for full-width modal
        st.markdown("""
        <style>
        .chart-modal {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            margin: 20px 0;
        }
        .chart-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 20px 20px 0 0;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create full-width expander for chart
        with st.expander(f"📈 {stock_name} - Live Professional Chart", expanded=True):
            # Header with close button
            col1, col2 = st.columns([6, 1])
            
            with col1:
                st.markdown(f"""
                <div class="chart-header">
                    <h2>📊 {stock_name} - Live Market Analysis</h2>
                    <p>Professional TradingView Chart with Technical Indicators</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("✕ Close Chart", key=f"close_{button_key}", type="secondary"):
                    st.session_state[modal_key] = False
                    st.rerun()
            
            # Render the bigger chart
            st.markdown('<div class="chart-modal">', unsafe_allow_html=True)
            render_tradingview_widget(stock_symbol, height=700)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Additional info
            st.info("💡 Use the chart tools above for technical analysis. This is a live professional chart with real-time data.")