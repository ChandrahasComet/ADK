import yfinance as yf
import datetime
from google.adk.agents import Agent

def get_stock_price(company_name: str) -> dict:
    """
    Get the current stock price for a company using yfinance.
    The company_name should be the ticker symbol (e.g., 'AAPL' for Apple).
    Input args: company_name: str, time: str
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        ticker = yf.Ticker(company_name)
        data = ticker.history(period="1d", interval="1m")
        
        if data.empty:
            return {
                "company": company_name,
                "time": now,
                "error": "No data available for the specified company."
            }
        
        latest_price = data['Close'].iloc[-1]
        return {
            "company": company_name,
            "time": now,
            "stock_price": round(latest_price, 2)
        }
        
    except Exception as e:
        return {
            "company": company_name,
            "time": now,
            "error": str(e)
        }
    
stock_analyst = Agent(
    name = "stock_analyst",
    model = "gemini-2.0-flash",
    description = "Stock analyst agent that can provide the stock price for the given ticker symbol",
    instruction = """
    You are a helpful AI assistant that can provide the stock price for the given ticker symbol.

    For the query you must first get the current time and then use the get_stock_price tool to get the stock price.

    Output format must be
    GOOG: $170.00 (2023-07-17 10:30:00)
    APPLE: $270.00 (2023-07-17 10:30:00)
""",
    tools = [get_stock_price]
)