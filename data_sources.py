import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import streamlit as st
import time
import json
import os

class DataManager:
    def __init__(self):
        self.nse_base_url = "https://www.nseindia.com/api"
        self.marketaux_api_key = os.getenv("MARKETAUX_API_KEY", "demo_key")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })
        
    def get_nse_data(self, endpoint, retries=3):
        """Fetch data from NSE with error handling and retries"""
        for attempt in range(retries):
            try:
                response = self.session.get(f"{self.nse_base_url}/{endpoint}", timeout=10)
                if response.status_code == 200:
                    return response.json()
                else:
                    time.sleep(1)  # Wait before retry
            except Exception as e:
                if attempt == retries - 1:
                    st.error(f"Failed to fetch NSE data from {endpoint}: {str(e)}")
                time.sleep(1)
        return None

    def get_market_status(self):
        """Get current market status"""
        try:
            data = self.get_nse_data("marketStatus")
            if data and 'marketState' in data:
                for market in data['marketState']:
                    if market['market'] == 'Capital Market':
                        return market['marketStatus']
            return "UNKNOWN"
        except:
            return "UNKNOWN"

    def get_sector_data(self):
        """Fetch sector-wise performance data"""
        try:
            # Get sector indices data
            sector_data = self.get_nse_data("equity-stockIndices?index=SECTORAL%20INDICES")
            
            if not sector_data or 'data' not in sector_data:
                return pd.DataFrame()
            
            sectors_list = []
            for sector in sector_data['data']:
                sectors_list.append({
                    'Industry': sector.get('index', 'N/A'),
                    'Avg_Open': sector.get('open', 0),
                    'Avg_Close': sector.get('last', 0),
                    'Avg_High': sector.get('high', 0),
                    'Avg_Low': sector.get('low', 0),
                    'Change': sector.get('change', 0),
                    'Percent_Change': sector.get('pChange', 0),
                    'Volume': sector.get('totalTradedVolume', 0)
                })
            
            df = pd.DataFrame(sectors_list)
            df['Trend'] = df['Percent_Change'].apply(lambda x: '↑' if x > 0 else '↓' if x < 0 else '→')
            return df
            
        except Exception as e:
            st.error(f"Error fetching sector data: {str(e)}")
            return pd.DataFrame()

    def get_top_gainers_losers(self):
        """Get top gainers and losers"""
        try:
            gainers = self.get_nse_data("equity-stockIndices?index=SECURITIES%20IN%20F%26O")
            
            if not gainers or 'data' not in gainers:
                return pd.DataFrame(), pd.DataFrame()
            
            # Process data for top gainers and losers
            stocks = gainers['data'][:50]  # Take first 50 stocks
            df = pd.DataFrame(stocks)
            
            if df.empty:
                return pd.DataFrame(), pd.DataFrame()
            
            # Sort by percentage change
            df = df.sort_values('pChange', ascending=False)
            
            top_gainers = df.head(10)[['symbol', 'lastPrice', 'change', 'pChange']]
            top_losers = df.tail(10)[['symbol', 'lastPrice', 'change', 'pChange']]
            
            return top_gainers, top_losers
            
        except Exception as e:
            st.error(f"Error fetching gainers/losers: {str(e)}")
            return pd.DataFrame(), pd.DataFrame()

    def get_index_data(self):
        """Fetch major indices data"""
        indices = [
            "NIFTY 50", "NIFTY BANK", "NIFTY IT", "NIFTY PHARMA", 
            "NIFTY FMCG", "NIFTY AUTO", "NIFTY METAL", "NIFTY ENERGY"
        ]
        
        indices_data = []
        
        for index in indices:
            try:
                data = self.get_nse_data(f"equity-stockIndices?index={index.replace(' ', '%20')}")
                
                if data and 'data' in data and len(data['data']) > 0:
                    index_info = data['data'][0]
                    indices_data.append({
                        'Index': index,
                        'Price': index_info.get('last', 0),
                        'Change': index_info.get('change', 0),
                        'Percent_Change': index_info.get('pChange', 0),
                        'Open': index_info.get('open', 0),
                        'High': index_info.get('high', 0),
                        'Low': index_info.get('low', 0),
                        'Volume': index_info.get('totalTradedVolume', 0)
                    })
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                st.warning(f"Could not fetch data for {index}: {str(e)}")
                
        return pd.DataFrame(indices_data)

    def get_market_heatmap_data(self):
        """Generate heatmap data for top stocks"""
        try:
            data = self.get_nse_data("equity-stockIndices?index=SECURITIES%20IN%20F%26O")
            
            if not data or 'data' not in data:
                return pd.DataFrame()
            
            stocks = data['data'][:30]  # Top 30 stocks for heatmap
            heatmap_data = []
            
            for stock in stocks:
                heatmap_data.append({
                    'Symbol': stock.get('symbol', 'N/A'),
                    'Price': stock.get('lastPrice', 0),
                    'Change': stock.get('pChange', 0),
                    'Volume': stock.get('totalTradedVolume', 0),
                    'Market_Cap': stock.get('lastPrice', 0) * 1000000  # Approximate
                })
            
            return pd.DataFrame(heatmap_data)
            
        except Exception as e:
            st.error(f"Error fetching heatmap data: {str(e)}")
            return pd.DataFrame()

    def get_fii_dii_data(self):
        """Fetch FII/DII flow data"""
        try:
            # Try to get FII/DII data from NSE
            data = self.get_nse_data("fiidiiTradeReact")
            
            if data:
                return {
                    'FII_Inflow': data.get('fiiInflow', 0),
                    'FII_Outflow': data.get('fiiOutflow', 0),
                    'DII_Inflow': data.get('diiInflow', 0),
                    'DII_Outflow': data.get('diiOutflow', 0),
                    'Date': datetime.now().strftime('%Y-%m-%d')
                }
            else:
                # Return dummy structure if API fails
                return {
                    'FII_Inflow': 0,
                    'FII_Outflow': 0,
                    'DII_Inflow': 0,
                    'DII_Outflow': 0,
                    'Date': datetime.now().strftime('%Y-%m-%d')
                }
                
        except Exception as e:
            st.warning(f"FII/DII data temporarily unavailable: {str(e)}")
            return {
                'FII_Inflow': 0,
                'FII_Outflow': 0,
                'DII_Inflow': 0,
                'DII_Outflow': 0,
                'Date': datetime.now().strftime('%Y-%m-%d')
            }

    def get_financial_news(self, limit=20):
        """Fetch Indian financial news from MarketAux"""
        try:
            url = "https://api.marketaux.com/v1/news/all"
            params = {
                'api_token': self.marketaux_api_key,
                'countries': 'in',
                'filter_entities': 'true',
                'limit': limit,
                'published_after': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                news_items = []
                
                for article in data.get('data', []):
                    # Categorize news based on keywords
                    title = article.get('title', '').lower()
                    description = article.get('description', '').lower()
                    
                    category = self._categorize_news(title + ' ' + description)
                    
                    news_items.append({
                        'headline': article.get('title', 'No title'),
                        'category': category,
                        'timestamp': article.get('published_at', ''),
                        'source': article.get('source', 'Unknown'),
                        'url': article.get('url', ''),
                        'description': article.get('description', '')[:200] + '...'
                    })
                
                return news_items
            else:
                st.warning(f"News API returned status code: {response.status_code}")
                return []
                
        except Exception as e:
            st.error(f"Error fetching news: {str(e)}")
            return []

    def _categorize_news(self, text):
        """Categorize news based on keywords"""
        categories = {
            'Company Earnings': ['earnings', 'profit', 'revenue', 'quarterly', 'results'],
            'IPO Analysis': ['ipo', 'listing', 'public offering', 'debut'],
            'Economy Market Pulse': ['gdp', 'inflation', 'policy', 'rbi', 'interest rate'],
            'Industry & Market': ['sector', 'industry', 'market', 'nifty', 'sensex'],
            'Global Equity News': ['global', 'international', 'foreign', 'overseas'],
            'Company News': ['company', 'corporate', 'merger', 'acquisition']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'Company News'  # Default category

    def refresh_all_data(self):
        """Refresh all data sources"""
        try:
            # Update timestamp
            st.session_state.last_update = datetime.now(pytz.timezone('Asia/Kolkata'))
            
            # Refresh cached data
            if 'sector_data' in st.session_state:
                del st.session_state.sector_data
            if 'index_data' in st.session_state:
                del st.session_state.index_data
            if 'news_data' in st.session_state:
                del st.session_state.news_data
            if 'heatmap_data' in st.session_state:
                del st.session_state.heatmap_data
            if 'fii_dii_data' in st.session_state:
                del st.session_state.fii_dii_data
            
            return True
            
        except Exception as e:
            st.error(f"Error refreshing data: {str(e)}")
            return False
