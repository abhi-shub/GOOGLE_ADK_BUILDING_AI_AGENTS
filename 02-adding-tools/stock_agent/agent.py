import yfinance as yf
from google.adk import Agent
from google.adk.tools import FunctionTool

def get_stock_price(ticker: str) -> dict:
    """
    Retrieves the current stock price for a given ticker symbol.

    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'GOOGL', 'MSFT')

    Returns:
        Dictionary containing stock information including current price,
        daily high/low, and company name.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price_data = stock.history(period="1d")

        return {
            "company_name": info.get('shortName', 'Unknown'),
            "current_price": float(price_data['Close'].iloc[-1]),
            "daily_high": float(price_data['High'].iloc[-1]),
            "daily_low": float(price_data['Low'].iloc[-1]),
            "currency": info.get('currency', 'USD'),
            "ticker": ticker
        }
    except Exception as e:
        return {
            "error": f"Failed to retrieve stock information: {str(e)}",
            "ticker": ticker
        }

stock_agent = Agent(
    name="stock_agent",
    model="gemini-2.5-flash",
    description="An agent that provides stock market information",
    instruction="You are a helpful financial assistant that provides stock market information. When asked about stock prices, use the get_stock_price tool to retrieve current information. Explain the data in a clear, concise manner.",
    tools=[FunctionTool(get_stock_price)]
)

root_agent = stock_agent

