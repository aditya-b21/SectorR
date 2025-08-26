import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tradingview_charts import render_tradingview_widget, render_indices_overview

def render_market_cover():
    """Render the Market Cover page with enhanced UI"""
    
    # Custom CSS for market cover styling
    st.markdown("""
    <style>
    .market-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .index-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .index-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    .metric-enhanced {
        background: linear-gradient(45deg, #667eea, #764ba2);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        animation: pulse 2s infinite;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Animated header
    st.markdown('<div class="market-header"><h1>📊 Live Market Dashboard</h1><p>Real-time Indian market indices with advanced analytics</p></div>', unsafe_allow_html=True)
    
    # Get data manager
    data_manager = st.session_state.data_manager
    
    # Fetch index data with caching
    if 'index_data' not in st.session_state:
        with st.spinner("Loading market indices data..."):
            st.session_state.index_data = data_manager.get_index_data()
    
    index_df = st.session_state.index_data
    
    if index_df.empty:
        st.error("Unable to load index data. Please try refreshing.")
        return
    
    # Enhanced Market Overview Cards
    st.markdown('<div class="index-card">', unsafe_allow_html=True)
    st.subheader("🔥 Live Index Performance Dashboard")
    
    # Create cards for each major index
    indices_per_row = 3
    num_indices = len(index_df)
    
    for i in range(0, num_indices, indices_per_row):
        cols = st.columns(indices_per_row)
        
        for j, col in enumerate(cols):
            if i + j < num_indices:
                index_data = index_df.iloc[i + j]
                
                with col:
                    # Enhanced trend visualization
                    trend_color = "green" if index_data['Percent_Change'] > 0 else "red" if index_data['Percent_Change'] < 0 else "gray"
                    trend_icon = "📈" if index_data['Percent_Change'] > 0 else "📉" if index_data['Percent_Change'] < 0 else "➡️"
                    
                    st.markdown('<div class="metric-enhanced">', unsafe_allow_html=True)
                    st.metric(
                        label=f"{trend_icon} {index_data['Index']}",
                        value=f"₹{index_data['Last_Price']:,.2f}",
                        delta=f"{index_data['Change']:+.2f} ({index_data['Percent_Change']:+.2f}%)"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Additional details in expander with TradingView chart
                    with st.expander(f"📈 Live Chart & Details - {index_data['Index']}"):
                        st.write(f"**Open:** ₹{index_data['Open']:,.2f}")
                        st.write(f"**High:** ₹{index_data['High']:,.2f}")
                        st.write(f"**Low:** ₹{index_data['Low']:,.2f}")
                        st.write(f"**Volume:** {index_data['Volume']:,.0f}")
                        st.write(f"**Trend:** {trend_icon}")
                        
                        # Show TradingView chart
                        if 'Symbol' in index_data:
                            chart_symbol = index_data['Symbol'].replace('^', '')
                            render_tradingview_widget(chart_symbol, height=350)
    
    # TradingView Live Charts Section
    st.subheader("📊 Live TradingView Charts - Real-Time Data")
    
    # Major Indices TradingView Charts
    st.markdown("#### 🚀 Major Indices - Live Professional Charts")
    render_indices_overview()
    
    # Individual Index Selection with Real TradingView Chart
    st.markdown("#### 🎯 Detailed Index Analysis")
    selected_index = st.selectbox(
        "Select index for detailed live analysis:",
        index_df['Index'].tolist(),
        key="selected_index_chart"
    )
    
    if selected_index:
        selected_row = index_df[index_df['Index'] == selected_index].iloc[0]
        
        # Show current metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Price", f"₹{selected_row['Last_Price']:,.2f}")
        with col2:
            st.metric("Change", f"{selected_row['Change']:+.2f}")
        with col3:
            st.metric("% Change", f"{selected_row['Percent_Change']:+.2f}%")
        with col4:
            st.metric("Volume", f"{selected_row['Volume']:,.0f}")
        
        # Show live TradingView chart
        st.markdown(f"### 📈 {selected_index} - Live Professional Chart")
        if 'Symbol' in selected_row:
            chart_symbol = selected_row['Symbol'].replace('^', '')
            render_tradingview_widget(chart_symbol, height=600)
        
        # Additional analysis section
        with st.expander("📊 Technical Analysis Summary"):
            st.markdown(f"""
            **{selected_index} Analysis:**
            - **Current Trend:** {'Bullish' if selected_row['Percent_Change'] > 0 else 'Bearish' if selected_row['Percent_Change'] < 0 else 'Neutral'}
            - **Day Range:** ₹{selected_row['Low']:,.2f} - ₹{selected_row['High']:,.2f}
            - **Opening Price:** ₹{selected_row['Open']:,.2f}
            - **Price Movement:** {abs(selected_row['Percent_Change']):.2f}% {'upward' if selected_row['Percent_Change'] > 0 else 'downward' if selected_row['Percent_Change'] < 0 else 'sideways'}
            - **Trading Volume:** {selected_row['Volume']:,.0f} shares
            """)
            
            # Risk indicator
            risk_level = "High" if abs(selected_row['Percent_Change']) > 2 else "Medium" if abs(selected_row['Percent_Change']) > 1 else "Low"
            risk_color = "🔴" if risk_level == "High" else "🟡" if risk_level == "Medium" else "🟢"
            st.markdown(f"**Volatility Risk:** {risk_color} {risk_level}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced Comparative Performance Chart
    st.markdown('<div class="index-card">', unsafe_allow_html=True)
    st.subheader("🏆 Comparative Index Performance Arena")
    
    # Multi-select for comparison
    comparison_indices = st.multiselect(
        "Select indices for comparison:",
        index_df['Index'].tolist(),
        default=index_df['Index'].tolist()[:4],  # Default to first 4 indices
        key="comparison_indices"
    )
    
    if comparison_indices:
        # Create normalized comparison chart
        comparison_df = index_df[index_df['Index'].isin(comparison_indices)]
        
        fig_comparison = px.bar(
            comparison_df,
            x='Index',
            y='Percent_Change',
            color='Percent_Change',
            color_continuous_scale=['#FF4757', '#FFA502', '#2ED573', '#1E90FF'],
            title="<b>🏁 Live Index Performance Battle</b>",
            text='Percent_Change'
        )
        
        fig_comparison.update_traces(
            texttemplate='%{text:.2f}%',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Performance: %{y:.2f}%<extra></extra>'
        )
        fig_comparison.update_layout(
            height=500,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=18,
            xaxis=dict(tickangle=45)
        )
        
        fig_comparison.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig_comparison.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Performance summary table
        st.subheader("📋 Performance Summary")
        summary_df = comparison_df[['Index', 'Price', 'Change', 'Percent_Change', 'Volume']].copy()
        summary_df['Price'] = summary_df['Price'].round(2)
        summary_df['Change'] = summary_df['Change'].round(2)
        summary_df['Percent_Change'] = summary_df['Percent_Change'].round(2)
        
        st.dataframe(
            summary_df,
            column_config={
                "Index": "Index Name",
                "Price": st.column_config.NumberColumn("Current Price", format="₹%.2f"),
                "Change": st.column_config.NumberColumn("Change", format="₹%.2f"),
                "Percent_Change": st.column_config.NumberColumn("% Change", format="%.2f%%"),
                "Volume": st.column_config.NumberColumn("Volume", format="%d")
            },
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced Market Breadth Analysis
    st.markdown('<div class="index-card">', unsafe_allow_html=True)
    st.subheader("🏀 Market Sentiment & Breadth Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Advancing vs Declining")
        advancing = len(index_df[index_df['Percent_Change'] > 0])
        declining = len(index_df[index_df['Percent_Change'] < 0])
        unchanged = len(index_df[index_df['Percent_Change'] == 0])
        
        breadth_data = pd.DataFrame({
            'Status': ['Advancing', 'Declining', 'Unchanged'],
            'Count': [advancing, declining, unchanged]
        })
        
        fig_breadth = px.pie(
            breadth_data,
            values='Count',
            names='Status',
            title="<b>🎯 Market Breadth Overview</b>",
            color_discrete_map={
                'Advancing': '#2ED573',
                'Declining': '#FF4757',
                'Unchanged': '#747D8C'
            }
        )
        fig_breadth.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
            pull=[0.1, 0, 0]
        )
        fig_breadth.update_layout(
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=16
        )
        fig_breadth.update_layout(height=300)
        st.plotly_chart(fig_breadth, use_container_width=True)
    
    with col2:
        st.subheader("Index Strength")
        avg_change = index_df['Percent_Change'].mean()
        total_volume = index_df['Volume'].sum()
        
        st.metric("Average % Change", f"{avg_change:.2f}%")
        st.metric("Total Volume", f"{total_volume:,.0f}")
        st.metric("Market Sentiment", 
                 "Bullish" if avg_change > 0 else "Bearish" if avg_change < 0 else "Neutral")
    
    with col3:
        st.subheader("Top Movers")
        
        # Best performer
        best_performer = index_df.loc[index_df['Percent_Change'].idxmax()]
        st.success(f"🏆 Best: {best_performer['Index']}")
        st.write(f"Change: +{best_performer['Percent_Change']:.2f}%")
        
        # Worst performer
        worst_performer = index_df.loc[index_df['Percent_Change'].idxmin()]
        st.error(f"📉 Worst: {worst_performer['Index']}")
        st.write(f"Change: {worst_performer['Percent_Change']:.2f}%")
    
    # Historical correlation analysis
    st.subheader("🔗 Index Correlation Analysis")
    
    # Generate sample correlation matrix for demonstration
    correlation_indices = ['NIFTY 50', 'NIFTY BANK', 'NIFTY IT', 'NIFTY PHARMA']
    available_indices = [idx for idx in correlation_indices if idx in index_df['Index'].values]
    
    if len(available_indices) >= 2:
        # Create sample correlation matrix
        np.random.seed(42)
        n = len(available_indices)
        correlation_matrix = np.random.uniform(0.3, 0.9, (n, n))
        np.fill_diagonal(correlation_matrix, 1.0)
        
        # Make matrix symmetric
        correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2
        
        correlation_df = pd.DataFrame(
            correlation_matrix
        )
        correlation_df.index = available_indices
        correlation_df.columns = available_indices
        
        fig_corr = px.imshow(
            correlation_df,
            color_continuous_scale='RdBu',
            aspect='auto',
            title="<b>🔗 Index Correlation Heat Matrix</b>"
        )
        fig_corr.update_layout(
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=16
        )
        fig_corr.update_layout(height=400)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.info("📊 Correlation values closer to 1.0 indicate indices move together, while values closer to 0 indicate independent movement.")
    st.markdown('</div>', unsafe_allow_html=True)
