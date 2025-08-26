import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
from streamlit_option_menu import option_menu
import time

def render_sector_rotation():
    """Render the Sector Rotation page with enhanced UI"""
    # Custom CSS for animations and styling
    st.markdown("""
    <style>
    .metric-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    .sector-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInDown 1s ease-out;
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .sector-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    .sector-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Animated header
    st.markdown('<div class="sector-header"><h1>🔄 Sector Rotation Analysis</h1><p>Real-time sector performance with 100+ sectors</p></div>', unsafe_allow_html=True)
    
    # Get data manager
    data_manager = st.session_state.data_manager
    
    # Fetch sector data with caching
    if 'sector_data' not in st.session_state:
        with st.spinner("Loading sector data..."):
            st.session_state.sector_data = data_manager.get_sector_data()
    
    sector_df = st.session_state.sector_data
    
    if sector_df.empty:
        st.error("Unable to load sector data. Please try refreshing.")
        return
    
    # Enhanced metrics with animations
    col1, col2, col3, col4 = st.columns(4)
    
    total_sectors = len(sector_df)
    gainers = len(sector_df[sector_df['Percent_Change'] > 0])
    losers = len(sector_df[sector_df['Percent_Change'] < 0])
    neutral = total_sectors - gainers - losers
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📊 Total Sectors", total_sectors)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📈 Gainers", gainers, delta=f"+{gainers}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📉 Losers", losers, delta=f"-{losers}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("➡️ Neutral", neutral)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter options
    st.subheader("Filter Options")
    filter_option = st.selectbox(
        "Show sectors:",
        ["All", "Gainers", "Losers", "Neutral"],
        key="sector_filter"
    )
    
    # Apply filter
    if filter_option == "Gainers":
        filtered_df = sector_df[sector_df['Percent_Change'] > 0]
    elif filter_option == "Losers":
        filtered_df = sector_df[sector_df['Percent_Change'] < 0]
    elif filter_option == "Neutral":
        filtered_df = sector_df[sector_df['Percent_Change'] == 0]
    else:
        filtered_df = sector_df
    
    # Top Performance Changes Section (like in your image)
    st.markdown('<div class="sector-card">', unsafe_allow_html=True)
    st.subheader("📈 Top Performance Changes")
    
    # Get top performing sectors
    top_performers = filtered_df.nlargest(10, 'Percent_Change')
    
    if not top_performers.empty:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🚀 Top Gainers")
            for _, sector in top_performers.head(5).iterrows():
                st.markdown(f"**{sector['Industry']}** - {sector['Percent_Change']:.2f}%", 
                          help=f"Open: ₹{sector['Avg_Open']:.2f} | Close: ₹{sector['Avg_Close']:.2f}")
        
        with col2:
            # Create top performance bar chart
            fig_top = px.bar(
                top_performers.head(8),
                x='Percent_Change',
                y='Industry',
                orientation='h',
                color='Percent_Change',
                color_continuous_scale=['#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'],
                title="<b>🏆 Top 8 Sector Performance</b>",
                text='Percent_Change'
            )
            fig_top.update_traces(
                texttemplate='%{text:.2f}%',
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Performance: %{x:.2f}%<extra></extra>'
            )
            fig_top.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=10),
                title_font_size=16,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_top, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced Industry Performance Overview Chart
    st.markdown('<div class="sector-card">', unsafe_allow_html=True)
    st.subheader("📊 Complete Industry Performance Overview")
    
    if not filtered_df.empty:
        # Create enhanced interactive bar chart with animations
        display_count = min(25, len(filtered_df))  # Show up to 25 sectors
        fig_bar = px.bar(
            filtered_df.head(display_count),
            x='Percent_Change',
            y='Industry',
            orientation='h',
            color='Percent_Change',
            color_continuous_scale=['#FF4757', '#FFA502', '#2ED573', '#1E90FF', '#5F27CD'],
            title=f"<b>📊 Sector Performance Dashboard ({display_count} Sectors)</b>",
            labels={'Percent_Change': 'Percentage Change (%)', 'Industry': 'Sector'},
            text='Percent_Change'
        )
        
        fig_bar.update_traces(
            texttemplate='%{text:.2f}%', 
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Change: %{x:.2f}%<extra></extra>'
        )
        fig_bar.update_layout(
            height=700, 
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=20,
            xaxis=dict(gridcolor='rgba(255,255,255,0.2)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.2)')
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced Clickable Industry Data Table
    st.markdown('<div class="sector-card">', unsafe_allow_html=True)
    st.subheader("📋 Interactive Sector Explorer")
    st.caption("Click on any sector to view its constituent stocks")
    
    if not filtered_df.empty:
        # Format the dataframe for display
        display_df = filtered_df.copy().reset_index(drop=True)
        display_df['Avg_Open'] = display_df['Avg_Open'].round(2)
        display_df['Avg_Close'] = display_df['Avg_Close'].round(2)
        display_df['Avg_High'] = display_df['Avg_High'].round(2)
        display_df['Avg_Low'] = display_df['Avg_Low'].round(2)
        display_df['Percent_Change'] = display_df['Percent_Change'].round(2)
        
        # Create interactive table with sector selection
        selected_sector = st.selectbox(
            "🎯 Select a sector to view its stocks:",
            options=display_df['Industry'].tolist(),
            key="sector_selector"
        )
        
        # Display sector table
        st.dataframe(
            display_df,
            column_config={
                "Industry": "🏭 Sector Name",
                "Avg_Open": st.column_config.NumberColumn("📊 Avg. Open", format="₹%.2f"),
                "Avg_Close": st.column_config.NumberColumn("💰 Avg. Close", format="₹%.2f"),
                "Avg_High": st.column_config.NumberColumn("⬆️ Avg. High", format="₹%.2f"),
                "Avg_Low": st.column_config.NumberColumn("⬇️ Avg. Low", format="₹%.2f"),
                "Percent_Change": st.column_config.NumberColumn("📈 % Change", format="%.2f%%"),
                "Trend": "📊 Trend"
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Display stocks in selected sector
        if selected_sector:
            st.markdown(f'### 🔍 Stocks in {selected_sector}')
            
            # Fetch sector stocks
            sector_stocks = data_manager.get_sector_stocks(selected_sector)
            
            if not sector_stocks.empty:
                # Format stock data
                sector_stocks['Current_Price'] = sector_stocks['Current_Price'].round(2)
                sector_stocks['Change'] = sector_stocks['Change'].round(2)
                sector_stocks['Percent_Change'] = sector_stocks['Percent_Change'].round(2)
                
                # Display stocks table
                st.dataframe(
                    sector_stocks,
                    column_config={
                        "Symbol": "🏷️ Stock Symbol",
                        "Current_Price": st.column_config.NumberColumn("💵 Current Price", format="₹%.2f"),
                        "Change": st.column_config.NumberColumn("📊 Change", format="₹%.2f"),
                        "Percent_Change": st.column_config.NumberColumn("📈 % Change", format="%.2f%%"),
                        "Volume": st.column_config.NumberColumn("📊 Volume", format="%d"),
                        "High": st.column_config.NumberColumn("⬆️ Day High", format="₹%.2f"),
                        "Low": st.column_config.NumberColumn("⬇️ Day Low", format="₹%.2f")
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                # Stock performance chart for selected sector
                stock_fig = px.bar(
                    sector_stocks.head(10),
                    x='Symbol',
                    y='Percent_Change',
                    color='Percent_Change',
                    color_continuous_scale=['#FF6B6B', '#FFE66D', '#4ECDC4'],
                    title=f"📊 Top 10 Stocks Performance in {selected_sector}",
                    text='Percent_Change'
                )
                stock_fig.update_traces(
                    texttemplate='%{text:.1f}%',
                    textposition='outside'
                )
                stock_fig.update_layout(
                    height=400,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(stock_fig, use_container_width=True)
            else:
                st.info(f"No stock data available for {selected_sector}")
    else:
        st.info(f"No sectors found for filter: {filter_option}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Top Performance Changes
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🟢 Top 5 Gainers")
        if not sector_df.empty:
            top_gainers = sector_df.nlargest(5, 'Percent_Change')[['Industry', 'Percent_Change']]
            for _, row in top_gainers.iterrows():
                st.success(f"{row['Industry']}: +{row['Percent_Change']:.2f}%")
        else:
            st.info("No gainer data available")
    
    with col2:
        st.subheader("🔴 Top 5 Losers")
        if not sector_df.empty:
            top_losers = sector_df.nsmallest(5, 'Percent_Change')[['Industry', 'Percent_Change']]
            for _, row in top_losers.iterrows():
                st.error(f"{row['Industry']}: {row['Percent_Change']:.2f}%")
        else:
            st.info("No loser data available")
    
    # Enhanced Market Heatmap with 4K quality
    st.markdown('<div class="sector-card">', unsafe_allow_html=True)
    st.subheader("🗺️ Market Heatmap - Live Performance")
    
    # Fetch heatmap data
    if 'heatmap_data' not in st.session_state:
        with st.spinner("🔄 Loading high-resolution heatmap data..."):
            st.session_state.heatmap_data = data_manager.get_market_heatmap_data()
    
    heatmap_df = st.session_state.heatmap_data
    
    if not heatmap_df.empty:
        # Create enhanced treemap for heatmap visualization
        fig_heatmap = px.treemap(
            heatmap_df.head(25),  # Top 25 stocks
            path=['Symbol'],
            values='Volume',
            color='Change',
            color_continuous_scale=['#FF4757', '#FFA502', '#2ED573', '#1E90FF', '#5F27CD'],
            title="<b>🎯 Live Market Heatmap</b><br><sub>Size: Trading Volume | Color: Performance %</sub>"
        )
        fig_heatmap.update_traces(
            textinfo='label+value',
            hovertemplate='<b>%{label}</b><br>Change: %{color:.2f}%<br>Volume: %{value:,.0f}<extra></extra>'
        )
        fig_heatmap.update_layout(
            height=600,
            font=dict(size=14),
            title_font_size=18,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True, config={'displayModeBar': True, 'toImageButtonOptions': {'height': 1080, 'width': 1920}})
    else:
        st.info("🔄 Heatmap data is being updated...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Price Chart with toggles
    st.subheader("📈 Price Chart Analysis")
    
    chart_options = st.multiselect(
        "Select chart elements:",
        ["Price", "Volume", "MA20", "MA50"],
        default=["Price"],
        key="chart_toggles"
    )
    
    if chart_options and not sector_df.empty:
        # Generate sample time series data for demonstration
        dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
        sample_data = pd.DataFrame({
            'Date': dates,
            'Price': np.random.randn(len(dates)).cumsum() + 100,
            'Volume': np.random.randint(1000000, 5000000, len(dates))
        })
        
        # Calculate moving averages
        sample_data['MA20'] = sample_data['Price'].rolling(20).mean()
        sample_data['MA50'] = sample_data['Price'].rolling(50).mean()
        
        # Create subplot
        fig_chart = go.Figure()
        
        if "Price" in chart_options:
            fig_chart.add_trace(go.Scatter(
                x=sample_data['Date'], 
                y=sample_data['Price'],
                mode='lines',
                name='Price',
                line=dict(color='blue')
            ))
        
        if "MA20" in chart_options:
            fig_chart.add_trace(go.Scatter(
                x=sample_data['Date'], 
                y=sample_data['MA20'],
                mode='lines',
                name='MA20',
                line=dict(color='orange')
            ))
        
        if "MA50" in chart_options:
            fig_chart.add_trace(go.Scatter(
                x=sample_data['Date'], 
                y=sample_data['MA50'],
                mode='lines',
                name='MA50',
                line=dict(color='red')
            ))
        
        fig_chart.update_layout(
            title="Market Index Price Chart",
            xaxis_title="Date",
            yaxis_title="Price",
            height=400
        )
        
        st.plotly_chart(fig_chart, use_container_width=True)
        
        if "Volume" in chart_options:
            fig_volume = px.bar(
                sample_data.tail(30), 
                x='Date', 
                y='Volume',
                title="Volume Chart (Last 30 Days)"
            )
            fig_volume.update_layout(height=300)
            st.plotly_chart(fig_volume, use_container_width=True)
    
    # FII/DII Net Flow
    st.subheader("💰 FII/DII Net Flow")
    
    # Fetch FII/DII data
    if 'fii_dii_data' not in st.session_state:
        with st.spinner("Loading FII/DII data..."):
            st.session_state.fii_dii_data = data_manager.get_fii_dii_data()
    
    fii_dii = st.session_state.fii_dii_data
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("FII Flow")
        fii_net = fii_dii['FII_Inflow'] - fii_dii['FII_Outflow']
        st.metric(
            "Net FII Flow",
            f"₹{fii_net:,.0f} Cr",
            delta=f"{'Positive' if fii_net > 0 else 'Negative'} Impact"
        )
        st.write(f"Inflow: ₹{fii_dii['FII_Inflow']:,.0f} Cr")
        st.write(f"Outflow: ₹{fii_dii['FII_Outflow']:,.0f} Cr")
    
    with col2:
        st.subheader("DII Flow")
        dii_net = fii_dii['DII_Inflow'] - fii_dii['DII_Outflow']
        st.metric(
            "Net DII Flow",
            f"₹{dii_net:,.0f} Cr",
            delta=f"{'Positive' if dii_net > 0 else 'Negative'} Impact"
        )
        st.write(f"Inflow: ₹{fii_dii['DII_Inflow']:,.0f} Cr")
        st.write(f"Outflow: ₹{fii_dii['DII_Outflow']:,.0f} Cr")
    
    with col3:
        st.subheader("Net Impact")
        total_net = fii_net + dii_net
        impact_color = "green" if total_net > 0 else "red"
        st.metric(
            "Combined Flow",
            f"₹{total_net:,.0f} Cr",
            delta=f"{'Bullish' if total_net > 0 else 'Bearish'}"
        )
        st.markdown(f"**Overall Impact:** {'🟢 Positive' if total_net > 0 else '🔴 Negative'}")
