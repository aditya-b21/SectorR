import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import plotly.express as px

def render_trending_news():
    """Render the Trending News page with enhanced UI and categorization"""
    
    # Custom CSS for news styling
    st.markdown("""
    <style>
    .news-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        animation: slideInFromTop 1s ease-out;
    }
    @keyframes slideInFromTop {
        from { opacity: 0; transform: translateY(-50px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .news-category-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .news-category-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .news-item {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    .news-item:hover {
        background: rgba(255, 255, 255, 0.1);
        border-left: 4px solid #764ba2;
    }
    .category-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Animated header
    st.markdown('<div class="news-header"><h1>📰 Financial News Hub</h1><p>Latest market insights and breaking news</p></div>', unsafe_allow_html=True)
    
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
    
    # Enhanced news categories with 4 main sections
    st.markdown('<div class="news-category-card">', unsafe_allow_html=True)
    st.subheader("🎡 Select News Category")
    
    # Create 4 main news categories
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_news_btn = st.button("📊 Total News", use_container_width=True)
    with col2:
        company_news_btn = st.button("🏢 Company News", use_container_width=True)
    with col3:
        ipo_news_btn = st.button("💰 IPO News", use_container_width=True)
    with col4:
        global_news_btn = st.button("🌍 Global News", use_container_width=True)
    
    # Determine selected category
    if company_news_btn:
        selected_category = "Company News"
    elif ipo_news_btn:
        selected_category = "IPO News"
    elif global_news_btn:
        selected_category = "Global News"
    else:
        selected_category = "All Categories"
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter news based on category
    if selected_category != "All Categories":
        filtered_news = [item for item in news_data if item['category'] == selected_category]
    else:
        filtered_news = news_data
    
    # Enhanced category statistics with animations
    category_counts = {}
    for item in news_data:
        category = item['category']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    total_company = category_counts.get('Company News', 0)
    total_ipo = category_counts.get('IPO News', 0)
    total_global = category_counts.get('Global News', 0)
    
    # Filter news based on category
    if selected_category != "All Categories":
        filtered_news = [item for item in news_data if item['category'] == selected_category]
    else:
        filtered_news = news_data
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Articles", len(news_data))
    with col2:
        st.metric("🏢 Company News", total_company)
    with col3:
        st.metric("💰 IPO News", total_ipo)
    with col4:
        st.metric("🌍 Global News", total_global)
    
    # Enhanced animated pie chart
    st.markdown('<div class="news-category-card">', unsafe_allow_html=True)
    st.subheader("🍰 News Distribution Dashboard")
    
    if category_counts:
        # Create animated pie chart with better colors
        fig_pie = px.pie(
            values=list(category_counts.values()),
            names=list(category_counts.keys()),
            title="<b>📊 Live News Category Distribution</b>",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA726', '#AB47BC', '#66BB6A']
        )
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Articles: %{value}<br>Percentage: %{percent}<extra></extra>',
            pull=[0.1 if cat == selected_category else 0 for cat in category_counts.keys()]
        )
        fig_pie.update_layout(
            height=500,
            showlegend=True,
            font=dict(size=14),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=18
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': True, 'toImageButtonOptions': {'height': 1080, 'width': 1920}})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display news articles with enhanced UI
    st.markdown('<div class="news-category-card">', unsafe_allow_html=True)
    st.subheader(f"📰 {selected_category} - Latest Updates")
    
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
        
        # Display enhanced news cards
        for i, article in enumerate(page_news):
            with st.container():
                st.markdown('<div class="news-item">', unsafe_allow_html=True)
                
                # Create enhanced card layout
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # Enhanced category badge
                    category_color = get_category_color(article['category'])
                    st.markdown(f'<span class="category-badge" style="background-color: {category_color}; color: white;">{article["category"]}</span>', unsafe_allow_html=True)
                    
                    # Enhanced headline
                    st.markdown(f"### 📰 {article['headline']}")
                    
                    # Description with better formatting
                    st.markdown(f"**📝 Summary:** {article['description']}")
                    
                    # Enhanced timestamp without source
                    try:
                        timestamp = datetime.fromisoformat(article['timestamp'].replace('Z', '+00:00'))
                        time_str = timestamp.strftime('%d %B %Y, %H:%M IST')
                    except:
                        time_str = article['timestamp']
                    
                    st.caption(f"🕰️ **Published:** {time_str}")
                
                with col2:
                    # Full news modal button
                    if st.button(f"🔍 Read Full Story", key=f"news_{i}", use_container_width=True):
                        show_full_news_modal(article)
                    
                    # Enhanced sentiment indicator
                    sentiment = get_simulated_sentiment(article['headline'])
                    if sentiment == "Positive":
                        st.success(f"📈 {sentiment}")
                    elif sentiment == "Negative":
                        st.error(f"📉 {sentiment}")
                    else:
                        st.info(f"➡️ {sentiment}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")
        
        # Show pagination info
        if total_pages > 1:
            st.info(f"Showing {len(page_news)} of {len(filtered_news)} articles")
    
    else:
        st.info(f"🔍 No articles found for category: {selected_category}")
    st.markdown('</div>', unsafe_allow_html=True)
    
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
            keyword_data = [{'Keyword': k, 'Mentions': v} for k, v in keyword_counts.items()]
            keyword_df = pd.DataFrame(keyword_data).sort_values('Mentions', ascending=False).head(10)
            
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
            timeline_data = [{'Date': k, 'Articles': v} for k, v in news_by_date.items()]
            timeline_df = pd.DataFrame(timeline_data).sort_values('Date')
            
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

def show_full_news_modal(article):
    """Display full news content in modal-like format"""
    st.markdown("---")
    st.markdown(f"## 📰 {article['headline']}")
    
    # Display full content
    full_content = article.get('full_content', f"""
    {article['headline']}
    
    📊 Market Analysis: This development represents a significant milestone in the current economic environment. Industry experts believe this will have far-reaching implications for investors and market participants.
    
    🔑 Key Highlights:
    • Strategic importance of the announcement in current market conditions
    • Expected impact on sector performance and investor sentiment
    • Potential opportunities for long-term investment strategies
    • Regulatory and compliance aspects of the development
    
    💼 Expert Opinion: Leading market analysts suggest that this news reflects broader trends in the economy and could influence trading patterns in the coming weeks. The announcement aligns with current market expectations and regulatory frameworks.
    
    📈 Market Impact: Early market reaction has been positive, with relevant sector stocks showing increased trading volume. Institutional investors are closely monitoring the situation for potential portfolio adjustments.
    
    🔮 Looking Ahead: This development is expected to contribute to overall market stability and growth prospects. Stakeholders across the industry are preparing for the implementation and its subsequent effects on business operations.
    
    💰 Investment Perspective: Financial advisors recommend careful consideration of this news in the context of individual investment goals and risk tolerance. The long-term implications suggest potential opportunities for well-positioned investors.
    
    🏁 Conclusion: As markets continue to evolve, such developments underscore the importance of staying informed and adapting investment strategies accordingly. The positive market reception indicates confidence in the underlying fundamentals.
    """)
    
    st.markdown(full_content)
    st.markdown("---")
    
    if st.button("❌ Close Article"):
        st.rerun()

def get_simulated_sentiment(headline):
    """Simulate sentiment analysis based on keywords"""
    positive_words = ['gain', 'rise', 'up', 'positive', 'growth', 'profit', 'strong', 'bullish', 'surge', 'boost', 'expansion', 'wins', 'approval', 'launch', 'increase']
    negative_words = ['fall', 'drop', 'down', 'negative', 'loss', 'weak', 'bearish', 'decline', 'crash', 'plunge', 'concern', 'pressure', 'disruption']
    
    headline_lower = headline.lower()
    
    positive_count = sum(1 for word in positive_words if word in headline_lower)
    negative_count = sum(1 for word in negative_words if word in headline_lower)
    
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Neutral"
