import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def render_market_cover():
    """Render the Market Cover page"""
    st.header("📊 Market Cover - Indian Indices")
    
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
    
    # Market Overview Cards
    st.subheader("📈 Live Index Performance")
    
    # Create cards for each major index
    indices_per_row = 3
    num_indices = len(index_df)
    
    for i in range(0, num_indices, indices_per_row):
        cols = st.columns(indices_per_row)
        
        for j, col in enumerate(cols):
            if i + j < num_indices:
                index_data = index_df.iloc[i + j]
                
                with col:
                    # Determine trend color
                    trend_color = "green" if index_data['Percent_Change'] > 0 else "red" if index_data['Percent_Change'] < 0 else "gray"
                    trend_icon = "↑" if index_data['Percent_Change'] > 0 else "↓" if index_data['Percent_Change'] < 0 else "→"
                    
                    st.metric(
                        label=index_data['Index'],
                        value=f"₹{index_data['Price']:,.2f}",
                        delta=f"{index_data['Change']:+.2f} ({index_data['Percent_Change']:+.2f}%)"
                    )
                    
                    # Additional details in expander
                    with st.expander(f"Details for {index_data['Index']}"):
                        st.write(f"**Open:** ₹{index_data['Open']:,.2f}")
                        st.write(f"**High:** ₹{index_data['High']:,.2f}")
                        st.write(f"**Low:** ₹{index_data['Low']:,.2f}")
                        st.write(f"**Volume:** {index_data['Volume']:,.0f}")
                        st.write(f"**Trend:** {trend_icon}")
    
    # Interactive Charts Section
    st.subheader("📊 Interactive Index Charts")
    
    # Index selection for detailed chart
    selected_index = st.selectbox(
        "Select index for detailed analysis:",
        index_df['Index'].tolist(),
        key="selected_index_chart"
    )
    
    # Time period selection
    time_period = st.selectbox(
        "Select time period:",
        ["1W", "1M", "6M", "1Y"],
        index=1,
        key="time_period"
    )
    
    # Generate sample historical data for the selected index
    if selected_index:
        selected_row = index_df[index_df['Index'] == selected_index].iloc[0]
        
        # Calculate number of days based on period
        days_map = {"1W": 7, "1M": 30, "6M": 180, "1Y": 365}
        num_days = days_map[time_period]
        
        # Generate sample historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=num_days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Simulate price movement starting from current price
        np.random.seed(42)  # For consistent demo data
        price_changes = np.random.randn(len(dates)) * 0.02  # 2% daily volatility
        current_price = selected_row['Price']
        
        # Create realistic price series
        prices = [current_price]
        for change in price_changes[1:]:
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)
        
        historical_data = pd.DataFrame({
            'Date': dates,
            'Price': prices,
            'Volume': np.random.randint(1000000, 10000000, len(dates))
        })
        
        # Create candlestick-style data
        historical_data['Open'] = historical_data['Price'].shift(1).fillna(historical_data['Price'])
        historical_data['High'] = historical_data[['Price', 'Open']].max(axis=1) * (1 + np.random.uniform(0, 0.02, len(dates)))
        historical_data['Low'] = historical_data[['Price', 'Open']].min(axis=1) * (1 - np.random.uniform(0, 0.02, len(dates)))
        historical_data['Close'] = historical_data['Price']
        
        # Create the main price chart
        fig = go.Figure()
        
        fig.add_trace(go.Candlestick(
            x=historical_data['Date'],
            open=historical_data['Open'],
            high=historical_data['High'],
            low=historical_data['Low'],
            close=historical_data['Close'],
            name=selected_index
        ))
        
        fig.update_layout(
            title=f"{selected_index} - {time_period} Performance",
            xaxis_title="Date",
            yaxis_title="Price (₹)",
            height=500,
            xaxis_rangeslider_visible=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Volume chart
        fig_volume = px.bar(
            historical_data,
            x='Date',
            y='Volume',
            title=f"{selected_index} - Trading Volume ({time_period})"
        )
        fig_volume.update_layout(height=300)
        st.plotly_chart(fig_volume, use_container_width=True)
    
    # Comparative Performance Chart
    st.subheader("🔄 Comparative Index Performance")
    
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
            color_continuous_scale=['red', 'yellow', 'green'],
            title="Index Performance Comparison (% Change)",
            text='Percent_Change'
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
    
    # Market Breadth Analysis
    st.subheader("🎯 Market Breadth Analysis")
    
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
            color_discrete_map={
                'Advancing': 'green',
                'Declining': 'red',
                'Unchanged': 'gray'
            }
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
            correlation_matrix,
            index=available_indices,
            columns=available_indices
        )
        
        fig_corr = px.imshow(
            correlation_df,
            color_continuous_scale='RdBu',
            aspect='auto',
            title="Index Correlation Matrix"
        )
        fig_corr.update_layout(height=400)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.info("📊 Correlation values closer to 1.0 indicate indices move together, while values closer to 0 indicate independent movement.")
