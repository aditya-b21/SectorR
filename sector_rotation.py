import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

def render_sector_rotation():
    """Render the Sector Rotation page"""
    st.header("🔄 Sector Rotation Analysis")
    
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
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    total_sectors = len(sector_df)
    gainers = len(sector_df[sector_df['Percent_Change'] > 0])
    losers = len(sector_df[sector_df['Percent_Change'] < 0])
    neutral = total_sectors - gainers - losers
    
    with col1:
        st.metric("Total Sectors", total_sectors)
    with col2:
        st.metric("Gainers", gainers, delta=f"+{gainers}")
    with col3:
        st.metric("Losers", losers, delta=f"-{losers}")
    with col4:
        st.metric("Neutral", neutral)
    
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
    
    # Industry Performance Overview Chart
    st.subheader("📊 Industry Performance Overview")
    
    if not filtered_df.empty:
        # Create interactive bar chart
        fig_bar = px.bar(
            filtered_df.head(15),  # Show top 15 sectors
            x='Percent_Change',
            y='Industry',
            orientation='h',
            color='Percent_Change',
            color_continuous_scale=['red', 'yellow', 'green'],
            title="Sector Performance (% Change)",
            labels={'Percent_Change': 'Percentage Change (%)', 'Industry': 'Sector'},
            text='Percent_Change'
        )
        
        fig_bar.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig_bar.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Industry Data Table
    st.subheader("📋 Industry Data Table")
    
    if not filtered_df.empty:
        # Format the dataframe for display
        display_df = filtered_df.copy()
        display_df['Avg_Open'] = display_df['Avg_Open'].round(2)
        display_df['Avg_Close'] = display_df['Avg_Close'].round(2)
        display_df['Avg_High'] = display_df['Avg_High'].round(2)
        display_df['Avg_Low'] = display_df['Avg_Low'].round(2)
        display_df['Percent_Change'] = display_df['Percent_Change'].round(2)
        
        # Display table with styling
        st.dataframe(
            display_df,
            column_config={
                "Industry": "Industry Name",
                "Avg_Open": st.column_config.NumberColumn("Avg. Open", format="₹%.2f"),
                "Avg_Close": st.column_config.NumberColumn("Avg. Close", format="₹%.2f"),
                "Avg_High": st.column_config.NumberColumn("Avg. High", format="₹%.2f"),
                "Avg_Low": st.column_config.NumberColumn("Avg. Low", format="₹%.2f"),
                "Percent_Change": st.column_config.NumberColumn("% Change", format="%.2f%%"),
                "Trend": "Trend"
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(f"No sectors found for filter: {filter_option}")
    
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
    
    # Market Heatmap
    st.subheader("🗺️ Market Heatmap")
    
    # Fetch heatmap data
    if 'heatmap_data' not in st.session_state:
        with st.spinner("Loading heatmap data..."):
            st.session_state.heatmap_data = data_manager.get_market_heatmap_data()
    
    heatmap_df = st.session_state.heatmap_data
    
    if not heatmap_df.empty:
        # Create treemap for heatmap visualization
        fig_heatmap = px.treemap(
            heatmap_df.head(20),  # Top 20 stocks
            path=['Symbol'],
            values='Volume',
            color='Change',
            color_continuous_scale=['red', 'yellow', 'green'],
            title="Stock Performance Heatmap (Size: Volume, Color: % Change)"
        )
        fig_heatmap.update_layout(height=500)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.info("Heatmap data temporarily unavailable")
    
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
