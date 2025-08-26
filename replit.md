# Overview

This is an Indian Stock Market Dashboard built with Streamlit that provides real-time NSE (National Stock Exchange) data visualization and financial news. The application features three main sections: Market Cover for index performance, Sector Rotation Analysis for sector-wise market movements, and Trending News for financial market updates. The dashboard automatically refreshes data daily and provides manual refresh capabilities for users to get the latest market information.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Framework
- **Streamlit**: Chosen as the primary web framework for rapid development and built-in data visualization capabilities
- **Multi-page Architecture**: Organized into separate modules (market_cover.py, sector_rotation.py, trending_news.py) for maintainability
- **Session State Management**: Uses Streamlit's session state to cache data and maintain application state across user interactions

## Data Management
- **Centralized DataManager Class**: Single point of data access in data_sources.py that handles all external API calls
- **Request Session Management**: Maintains persistent HTTP sessions with proper headers for NSE API compliance
- **Error Handling**: Implements retry logic and graceful fallbacks for API failures
- **Data Caching Strategy**: Uses session state to cache fetched data and minimize API calls

## Visualization Layer
- **Plotly Integration**: Leverages Plotly Express and Graph Objects for interactive charts and metrics
- **Responsive Layout**: Uses Streamlit's column system for responsive grid layouts
- **Real-time Metrics**: Displays live market data with trend indicators and color-coded performance metrics

## Scheduling System
- **APScheduler**: Background scheduler for automated daily data refresh at 4 PM IST
- **Manual Refresh**: User-triggered refresh capability with immediate data updates
- **Timezone Handling**: Proper IST timezone management for scheduling and display

## Data Sources Integration
- **NSE API**: Primary data source for Indian stock market indices and sector information
- **Custom Headers**: Implements browser-like headers to avoid bot detection
- **Rate Limiting**: Built-in delays and retry mechanisms to respect API limitations

# External Dependencies

## APIs and Data Sources
- **NSE India API** (www.nseindia.com/api): Primary source for real-time Indian stock market data including indices and sector performance
- **MarketAux API**: Secondary news data source with API key authentication for financial news aggregation

## Python Libraries
- **streamlit**: Web application framework for dashboard interface
- **plotly**: Interactive data visualization library for charts and graphs
- **pandas**: Data manipulation and analysis framework
- **requests**: HTTP library for API communications
- **apscheduler**: Background task scheduling for automated data refresh
- **pytz**: Timezone handling for IST scheduling and display
- **numpy**: Numerical computing support for data processing

## Environment Configuration
- **MarketAux API Key**: Requires MARKETAUX_API_KEY environment variable for news data access
- **Session Management**: Maintains HTTP sessions with custom headers for NSE API compatibility