import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests

def render_trending_news():
    """Render the Trending News page"""
    st.header("📰 Trending News - Market News & Analysis")
    
    # Get data manager
    data_manager = st.session_state.data_manager
    
    # Fetch news data with caching
    if 'news_data' not in st.session_state:
        with st.spinner("Loading financial news..."):
            st.session_state.news_data = data_manager.get_financial_news(limit=50)
    
    news_data = st.session_state.news_data
    
    if not news_data:
        st.error("Unable to load news data. Please check your internet connection and try refreshing.")
        return
    
    # News categories filter
    st.subheader("📂 News Categories")
    
    # Get unique categories
    categories = list(set([item['category'] for item in news_data]))
    categories.insert(0, "All Categories")
    
    selected_category = st.selectbox(
        "Filter by category:",
        categories,
        key="news_category_filter"
    )
    
    # Filter news based on category
    if selected_category != "All Categories":
        filtered_news = [item for item in news_data if item['category'] == selected_category]
    else:
        filtered_news = news_data
    
    # Category statistics
    col1, col2, col3, col4 = st.columns(4)
    
    category_counts = {}
    for item in news_data:
        category = item['category']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    with col1:
        st.metric("Total Articles", len(news_data))
    with col2:
        st.metric("Categories", len(categories) - 1)  # Subtract "All Categories"
    with col3:
        most_active = max(category_counts.items(), key=lambda x: x[1]) if category_counts else ("None", 0)
        st.metric("Most Active", most_active[0][:15] + "..." if len(most_active[0]) > 15 else most_active[0])
    with col4:
        st.metric("Filtered Results", len(filtered_news))
    
    # Category breakdown
    st.subheader("📊 Category Breakdown")
    
    if category_counts:
        category_df = pd.DataFrame(
            list(category_counts.items()),
            columns=['Category', 'Count']
        ).sort_values('Count', ascending=False)
        
        import plotly.express as px
        fig_categories = px.bar(
            category_df,
            x='Category',
            y='Count',
            title="News Articles by Category",
            color='Count',
            color_continuous_scale='Blues'
        )
        fig_categories.update_layout(
            height=400,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_categories, use_container_width=True)
    
    # Display news articles
    st.subheader(f"📖 {selected_category} Articles")
    
    if filtered_news:
        # Search functionality
        search_term = st.text_input("🔍 Search articles:", key="news_search")
        
        if search_term:
            filtered_news = [
                item for item in filtered_news 
                if search_term.lower() in item['headline'].lower() or 
                   search_term.lower() in item['description'].lower()
            ]
        
        # Sort options
        sort_option = st.selectbox(
            "Sort by:",
            ["Latest First", "Oldest First", "Category"],
            key="news_sort"
        )
        
        if sort_option == "Latest First":
            filtered_news.sort(key=lambda x: x['timestamp'], reverse=True)
        elif sort_option == "Oldest First":
            filtered_news.sort(key=lambda x: x['timestamp'])
        elif sort_option == "Category":
            filtered_news.sort(key=lambda x: x['category'])
        
        # Pagination
        items_per_page = st.selectbox("Articles per page:", [10, 20, 30, 50], index=1)
        total_pages = len(filtered_news) // items_per_page + (1 if len(filtered_news) % items_per_page > 0 else 0)
        
        if total_pages > 1:
            page = st.selectbox(f"Page (1-{total_pages}):", range(1, total_pages + 1))
            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_news = filtered_news[start_idx:end_idx]
        else:
            page_news = filtered_news[:items_per_page]
        
        # Display news cards
        for i, article in enumerate(page_news):
            with st.container():
                # Create card-like layout
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Category badge
                    category_color = get_category_color(article['category'])
                    st.markdown(f"<span style='background-color: {category_color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;'>{article['category']}</span>", unsafe_allow_html=True)
                    
                    # Headline
                    st.markdown(f"### {article['headline']}")
                    
                    # Description
                    st.write(article['description'])
                    
                    # Source and timestamp
                    try:
                        timestamp = datetime.fromisoformat(article['timestamp'].replace('Z', '+00:00'))
                        time_str = timestamp.strftime('%Y-%m-%d %H:%M UTC')
                    except:
                        time_str = article['timestamp']
                    
                    st.caption(f"**Source:** {article['source']} | **Published:** {time_str}")
                
                with col2:
                    st.write("")  # Spacing
                    if article['url']:
                        st.link_button("Read Full Article", article['url'], use_container_width=True)
                    
                    # News sentiment indicator (simulated)
                    sentiment = get_simulated_sentiment(article['headline'])
                    sentiment_color = "green" if sentiment == "Positive" else "red" if sentiment == "Negative" else "gray"
                    st.markdown(f"**Sentiment:** <span style='color: {sentiment_color};'>{sentiment}</span>", unsafe_allow_html=True)
                
                st.divider()
        
        # Show pagination info
        if total_pages > 1:
            st.info(f"Showing {len(page_news)} of {len(filtered_news)} articles")
    
    else:
        st.info(f"No articles found for category: {selected_category}")
    
    # News insights
    st.subheader("📈 News Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏷️ Most Mentioned Topics")
        # Extract common keywords from headlines
        all_headlines = " ".join([item['headline'] for item in news_data])
        
        # Common financial keywords to look for
        keywords = ['stock', 'market', 'nifty', 'sensex', 'earnings', 'profit', 'revenue', 'growth', 'ipo', 'bank', 'sector']
        keyword_counts = {}
        
        for keyword in keywords:
            count = all_headlines.lower().count(keyword)
            if count > 0:
                keyword_counts[keyword.title()] = count
        
        if keyword_counts:
            keyword_df = pd.DataFrame(
                list(keyword_counts.items()),
                columns=['Keyword', 'Mentions']
            ).sort_values('Mentions', ascending=False).head(10)
            
            fig_keywords = px.bar(
                keyword_df,
                x='Mentions',
                y='Keyword',
                orientation='h',
                title="Most Mentioned Keywords",
                color='Mentions',
                color_continuous_scale='Viridis'
            )
            fig_keywords.update_layout(height=400)
            st.plotly_chart(fig_keywords, use_container_width=True)
        else:
            st.info("No common keywords found in headlines")
    
    with col2:
        st.subheader("📅 News Timeline")
        
        # Group news by date
        news_by_date = {}
        for article in news_data:
            try:
                date = datetime.fromisoformat(article['timestamp'].replace('Z', '+00:00')).date()
                date_str = date.strftime('%Y-%m-%d')
                news_by_date[date_str] = news_by_date.get(date_str, 0) + 1
            except:
                continue
        
        if news_by_date:
            timeline_df = pd.DataFrame(
                list(news_by_date.items()),
                columns=['Date', 'Articles']
            ).sort_values('Date')
            
            fig_timeline = px.line(
                timeline_df,
                x='Date',
                y='Articles',
                title="News Volume Over Time",
                markers=True
            )
            fig_timeline.update_layout(height=400)
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("Timeline data not available")
    
    # News sources analysis
    st.subheader("📡 News Sources")
    
    source_counts = {}
    for item in news_data:
        source = item['source']
        source_counts[source] = source_counts.get(source, 0) + 1
    
    if source_counts:
        source_df = pd.DataFrame(
            list(source_counts.items()),
            columns=['Source', 'Articles']
        ).sort_values('Articles', ascending=False).head(10)
        
        st.dataframe(
            source_df,
            column_config={
                "Source": "News Source",
                "Articles": st.column_config.NumberColumn("Article Count")
            },
            use_container_width=True,
            hide_index=True
        )

def get_category_color(category):
    """Return color for category badge"""
    colors = {
        'Company News': '#3498db',
        'Company Earnings': '#2ecc71', 
        'Economy Market Pulse': '#e74c3c',
        'Industry & Market': '#f39c12',
        'Economy Inflation': '#9b59b6',
        'IPO Analysis': '#1abc9c',
        'IPO News': '#34495e',
        'Global Equity News': '#e67e22'
    }
    return colors.get(category, '#95a5a6')

def get_simulated_sentiment(headline):
    """Simulate sentiment analysis based on keywords"""
    positive_words = ['gain', 'rise', 'up', 'positive', 'growth', 'profit', 'strong', 'bullish', 'surge', 'boost']
    negative_words = ['fall', 'drop', 'down', 'negative', 'loss', 'weak', 'bearish', 'decline', 'crash', 'plunge']
    
    headline_lower = headline.lower()
    
    positive_count = sum(1 for word in positive_words if word in headline_lower)
    negative_count = sum(1 for word in negative_words if word in headline_lower)
    
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Neutral"
