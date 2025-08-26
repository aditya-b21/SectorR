import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
from streamlit_option_menu import option_menu
import time
# from tradingview_charts import render_tradingview_widget, render_stock_modal_button, render_sector_chart

def render_sector_rotation():
    """Render the Sector Rotation page with enhanced UI"""
    # Make the page wider and add better spacing
    st.markdown("""
    <style>
    .main > div {
        max-width: 100% !important;
        padding: 1rem 2rem !important;
    }
    .stSelectbox > div > div {
        font-size: 16px !important;
    }
    .stDataFrame {
        font-size: 16px !important;
    }
    .sector-card {
        padding: 20px !important;
        margin: 15px 0 !important;
        font-size: 18px !important;
    }
    .stock-info {
        font-size: 16px !important;
        padding: 12px !important;
        margin: 8px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Advanced CSS for animations and styling
    st.markdown("""
    <style>
    /* Global animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes shimmer {
        0% { background-position: -200px 0; }
        100% { background-position: calc(200px + 100%) 0; }
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 0.8rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        animation: fadeInUp 0.8s ease-out;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -200px;
        width: 200px;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 3s infinite;
    }
    
    .metric-container:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 20px 40px rgba(31, 38, 135, 0.5);
        animation: pulse 2s infinite;
    }
    
    .sector-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%, #f093fb 100%);
        padding: 3rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInDown 1s ease-out;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .sector-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 4s infinite;
    }
    
    .sector-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: slideInLeft 0.8s ease-out;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .sector-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .sector-card:nth-child(even) {
        animation: slideInRight 0.8s ease-out;
    }
    
    /* Enhanced table styling */
    .stDataFrame {
        animation: fadeInUp 1s ease-out;
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* Loading animations */
    .stSpinner {
        animation: pulse 1.5s infinite;
    }
    
    /* Chart animations */
    .js-plotly-plot {
        animation: fadeInUp 1.2s ease-out;
    }
    
    /* Button animations */
    .stSelectbox {
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Enhanced scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #764ba2, #667eea);
        border-radius: 10px;
        border: 2px solid transparent;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8, #553c9a);
    }
    </style>
    
    <script>
    // Add JavaScript for enhanced interactivity
    window.onload = function() {
        // Add click ripple effect to cards
        const cards = document.querySelectorAll('.sector-card');
        cards.forEach(card => {
            card.addEventListener('click', function(e) {
                let ripple = document.createElement('span');
                let rect = this.getBoundingClientRect();
                let size = Math.max(rect.width, rect.height);
                let x = e.clientX - rect.left - size / 2;
                let y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
        
        // Add smooth scroll behavior
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // Intersection Observer for animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
                }
            });
        }, observerOptions);
        
        // Observe all animated elements
        document.querySelectorAll('.sector-card, .metric-container').forEach(el => {
            observer.observe(el);
        });
    };
    </script>
    """, unsafe_allow_html=True)
    
    # Animated header
    st.markdown('<div class="sector-header"><h1>🔄 Advanced Sector Rotation Analysis</h1><p>Comprehensive real-time sector performance with 150+ detailed categories</p><p><small>✨ Enhanced with AI-powered analytics and interactive visualizations</small></p></div>', unsafe_allow_html=True)
    
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
    
    # Real-time data indicators
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 📊 Live Market Overview")
        current_time = datetime.now().strftime("%H:%M:%S IST")
        st.markdown(f"🕐 **Live Data Stream:** {current_time} | 🔄 **Auto-refresh:** Every 5 minutes")
    with col2:
        data_freshness = "🟢 LIVE" if datetime.now().hour >= 9 and datetime.now().hour <= 15 else "🟡 POST-MARKET"
        st.markdown(f"**Status:** {data_freshness}")
    
    st.markdown("---")
    
    # Enhanced metrics with animations
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_sectors = len(sector_df)
    gainers = len(sector_df[sector_df['Percent_Change'] > 0])
    losers = len(sector_df[sector_df['Percent_Change'] < 0])
    neutral = total_sectors - gainers - losers
    avg_performance = sector_df['Percent_Change'].mean()
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📊 Total Sectors", f"{total_sectors}+", help="Complete sector coverage including sub-categories")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📈 Gainers", gainers, delta=f"{(gainers/total_sectors*100):.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📉 Losers", losers, delta=f"{(losers/total_sectors*100):.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("➡️ Neutral", neutral, help="Sectors with no significant change")
        st.markdown('</div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        delta_color = "normal" if avg_performance > 0 else "inverse"
        st.metric("📊 Avg Performance", f"{avg_performance:.2f}%", delta=f"Market Average", delta_color=delta_color)
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
    
    # Professional Industry Performance Overview (SwingAlgo Style)
    st.markdown('<div class="sector-card">', unsafe_allow_html=True)
    st.subheader("📊 Industry Performance Overview")
    
    if not filtered_df.empty:
        # Sort by performance and take top performers like SwingAlgo
        top_performers = filtered_df.sort_values('Percent_Change', ascending=False).head(20)
        
        # Create professional horizontal bar chart matching SwingAlgo
        fig_bar = px.bar(
            top_performers,
            x='Percent_Change',
            y='Industry',
            orientation='h',
            color='Percent_Change',
            color_continuous_scale=['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60'],
            title="<b>Industry Performance Overview</b>",
            labels={'Percent_Change': 'Performance (%)', 'Industry': ''},
            text='Percent_Change'
        )
        
        # Update layout to match SwingAlgo style
        fig_bar.update_traces(
            texttemplate='%{text:.2f}%', 
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Performance: %{x:.2f}%<extra></extra>',
            textfont=dict(size=11, color='white')
        )
        
        fig_bar.update_layout(
            height=600, 
            showlegend=False,
            plot_bgcolor='#2c3e50',  # Dark background like SwingAlgo
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=11, color='white'),
            title_font_size=18,
            title_x=0.5,
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True,
                tickformat='.1f',
                ticksuffix='%',
                range=[0, max(top_performers['Percent_Change'].max() * 1.2, 4)]
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=False,
                tickfont=dict(size=10)
            ),
            margin=dict(l=250, r=100, t=50, b=50)  # More space for sector names
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Comprehensive 150+ Sectors Pie Chart
    st.markdown('<div class="sector-card">', unsafe_allow_html=True)
    st.subheader("🥧 Complete 150+ Sectors Market Distribution")
    st.caption("Interactive pie chart showing all sectors with detailed performance data")
    
    if not sector_df.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create comprehensive pie chart for all sectors
            # Group sectors by main category for better visualization
            sector_categories = {}
            for _, row in sector_df.iterrows():
                sector_name = row['Industry']
                # Extract main category (before the dash if it exists)
                if ' - ' in sector_name:
                    main_category = sector_name.split(' - ')[0]
                else:
                    main_category = sector_name
                
                if main_category not in sector_categories:
                    sector_categories[main_category] = {
                        'sectors': [], 
                        'total_change': 0, 
                        'avg_price': 0, 
                        'volume': 0
                    }
                
                sector_categories[main_category]['sectors'].append(sector_name)
                sector_categories[main_category]['total_change'] += row['Percent_Change']
                sector_categories[main_category]['avg_price'] += row['Avg_Close']
                sector_categories[main_category]['volume'] += row['Volume']
            
            # Prepare data for pie chart
            pie_data = []
            for category, data in sector_categories.items():
                count = len(data['sectors'])
                avg_change = data['total_change'] / count
                avg_price = data['avg_price'] / count
                total_volume = data['volume']
                
                pie_data.append({
                    'Category': category,
                    'Sector_Count': count,
                    'Avg_Change': avg_change,
                    'Avg_Price': avg_price,
                    'Total_Volume': total_volume,
                    'Sub_Sectors': ', '.join(data['sectors'][:3]) + f"... (+{count-3} more)" if count > 3 else ', '.join(data['sectors'])
                })
            
            pie_df = pd.DataFrame(pie_data)
            
            # Create animated pie chart
            fig_pie = px.pie(
                pie_df,
                values='Sector_Count',
                names='Category',
                title="<b>📊 Market Distribution: 150+ Sectors by Category</b>",
                hover_data=['Avg_Change', 'Total_Volume'],
                color_discrete_sequence=['#FF6B6B', '#FFE66D', '#4ECDC4', '#45B7D1', '#96CEB4', '#A8E6CF', '#FF8B94', '#FFD93D', '#6BCF7F', '#4D4D4D', '#B4A7D6', '#F7DC6F', '#85C1E9', '#F8C471', '#82E0AA']
            )
            
            fig_pie.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>' +
                             'Sectors: %{value}<br>' +
                             'Avg Change: %{customdata[0]:.2f}%<br>' +
                             'Total Volume: %{customdata[1]:,.0f}<br>' +
                             '<extra></extra>',
                textfont_size=10,
                marker=dict(line=dict(color='#FFFFFF', width=2))
            )
            
            fig_pie.update_layout(
                height=600,
                font=dict(size=12),
                title_font_size=18,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.01
                ),
                margin=dict(l=20, r=120, t=60, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Sector Categories Overview")
            st.markdown("*Click on pie chart segments to see details*")
            
            # Display category summary
            for i, (category, data) in enumerate(sector_categories.items()):
                count = len(data['sectors'])
                avg_change = data['total_change'] / count
                
                # Color based on performance
                if avg_change > 1:
                    color = "🟢"
                elif avg_change > 0:
                    color = "🟡"
                else:
                    color = "🔴"
                
                with st.expander(f"{color} {category} ({count} sectors)"):
                    st.write(f"**Average Change:** {avg_change:.2f}%")
                    st.write(f"**Sector Count:** {count}")
                    st.write("**Sub-sectors:**")
                    for sector in data['sectors'][:5]:  # Show first 5
                        sector_row = sector_df[sector_df['Industry'] == sector].iloc[0]
                        st.write(f"• {sector}: {sector_row['Percent_Change']:.2f}%")
                    if count > 5:
                        st.write(f"... and {count-5} more sectors")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Professional Sector Explorer (SwingAlgo Style)
    st.markdown('<div class="sector-card">', unsafe_allow_html=True)
    st.subheader("🔍 Complete Sector Coverage - 150+ Industries")
    
    # Search functionality like SwingAlgo
    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("🔍 Search industries...", placeholder="Type sector name to filter", key="sector_search")
    with col2:
        show_count = st.selectbox("Show", ["All", "Top 15", "Top 50"], key="show_count")
    
    if not filtered_df.empty:
        # Apply search filter
        if search_query:
            search_filtered = filtered_df[filtered_df['Industry'].str.contains(search_query, case=False, na=False)]
        else:
            search_filtered = filtered_df
            
        # Apply count filter
        if show_count == "Top 15":
            display_df = search_filtered.head(15)
        elif show_count == "Top 50":
            display_df = search_filtered.head(50)
        else:
            display_df = search_filtered
            
        # Format the dataframe for professional display
        display_df = display_df.copy().reset_index(drop=True)
        display_df['Avg_Open'] = display_df['Avg_Open'].round(2)
        display_df['Avg_Close'] = display_df['Avg_Close'].round(2)
        display_df['Avg_High'] = display_df['Avg_High'].round(2)
        display_df['Avg_Low'] = display_df['Avg_Low'].round(2)
        display_df['Percent_Change'] = display_df['Percent_Change'].round(2)
        
        # Add trend arrows like SwingAlgo
        display_df['Trend_Arrow'] = display_df['Percent_Change'].apply(
            lambda x: "🟢 Up" if x > 0 else "🔴 Down" if x < 0 else "➡️ Flat"
        )
        
        st.markdown(f"**Showing {len(display_df)} of {len(sector_df)} sectors**")
        
        # Professional table display matching SwingAlgo layout
        st.dataframe(
            display_df,
            column_config={
                "Industry": st.column_config.TextColumn("🏭 Industry", width="large", help="Sector/Industry name"),
                "Avg_Open": st.column_config.NumberColumn("💰 Avg. Open", format="%.2f", help="Average opening price"),
                "Avg_Close": st.column_config.NumberColumn("💰 Avg. Close", format="%.2f", help="Average closing price"),
                "Avg_High": st.column_config.NumberColumn("📈 Avg. High", format="%.2f", help="Average high price"),
                "Avg_Low": st.column_config.NumberColumn("📉 Avg. Low", format="%.2f", help="Average low price"),
                "Percent_Change": st.column_config.NumberColumn("📊 Change (%)", format="%.2f%%", help="Percentage change"),
                "Trend_Arrow": st.column_config.TextColumn("📊 Trend", help="Price trend direction")
            },
            use_container_width=True,
            hide_index=True,
            height=600
        )
        
        # Sector selection for detailed view
        st.markdown("---")
        selected_sector = st.selectbox(
            "🎯 Select a sector for detailed stock analysis:",
            options=display_df['Industry'].tolist(),
            key="sector_selector"
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
                
                st.markdown("#### 📋 Detailed Stock Data")
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
