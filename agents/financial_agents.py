import requests
import re

class FinancialAgents:
    API_KEY = 'e3b54dba91347af391b932a2c934f999'

    @staticmethod
    def plot_trend(ticker):
        """Show the latest days of stock trends for a ticker."""
        try:
            url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={FinancialAgents.API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                stock_data = response.json()
                data = stock_data['historical'][:50]
                data.reverse()
                transformed_data = [{"date": record["date"], "price": record["close"]} for record in data]
                return {
                    "type": "stockChart",
                    "content": f"Latest trends for {ticker}",
                    "stockInfo": {
                        "stockName": ticker,
                        "stockSymbol": ticker,
                        "stockData": transformed_data
                    }
                }
            else:
                return {"type": "error", "content": "Data not available"}
        except Exception as error:
            return {"type": "error", "content": f"Network error: {error}, sorry"}

    @staticmethod
    def plot_moving_average(input_text):
        """Calculate and display the moving average for a ticker."""
        try:
            match = re.search(r'(\d+)-day moving average for (\w+)', input_text, re.IGNORECASE)
            if match:
                ma_window = int(match.group(1))
                ticker = match.group(2).upper()
                n_days = 256
            else:
                return {"type": "error", "content": "Invalid input format."}

            url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={FinancialAgents.API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                stock_data = response.json()
                if 'historical' in stock_data:
                    data = stock_data['historical']
                    data.sort(key=lambda x: x['date'])
                    data = data[-n_days:]

                    if len(data) < ma_window:
                        return {"type": "error", "content": f"Not enough data to calculate a {ma_window}-day moving average for {ticker}."}

                    closing_prices = [record['close'] for record in data]

                    ma_data = []
                    for i in range(len(data)):
                        if i >= ma_window - 1:
                            window = closing_prices[i - ma_window + 1:i + 1]
                            moving_average = sum(window) / ma_window
                            ma_data.append({
                                "date": data[i]["date"],
                                "price": data[i]["close"],
                                "ma": moving_average
                            })

                    return {
                        "type": "stockChartWithMA",
                        "content": f"Added {ma_window}-day moving average for {ticker}",
                        "stockInfo": {
                            "stockName": ticker,
                            "stockSymbol": ticker,
                            "stockData": ma_data
                        }
                    }
                else:
                    return {"type": "error", "content": "Data not available"}
            else:
                return {"type": "error", "content": "Data not available"}
        except Exception as error:
            return {"type": "error", "content": f"Network error: {error}, sorry"}

   

    @staticmethod
    def fetch_stock_news(ticker_symbol):
        """Fetch the latest news for a given ticker symbol."""
        try:
            # Fetch news data
            url = f"https://financialmodelingprep.com/api/v3/stock_news?tickers={ticker_symbol}&page=0&apikey={FinancialAgents.API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                news_data = response.json()
                if isinstance(news_data, list) and news_data:
                    formatted_news = [
                        {
                            "publishedDate": news.get("publishedDate", ""),
                            "title": news.get("title", ""),
                            "text": news.get("text", ""),
                            "site": news.get("site", ""),
                            "url": news.get("url", ""),
                            "image": news.get("image", ""),
                        }
                        for news in news_data
                    ]
                    return {
                        "type": "stockNews",
                        "content": f"Here are the latest news articles for {ticker_symbol}:",
                        "newsInfo": {
                            "ticker": ticker_symbol,
                            "articles": formatted_news
                        }
                    }
                else:
                    return {"type": "error", "content": f"No news available for {ticker_symbol}."}
            else:
                return {"type": "error", "content": "Data not available"}
        except Exception as error:
            return {"type": "error", "content": f"An error occurred: {error}"}
