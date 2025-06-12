import datetime
import yfinance as yf

def get_current_time(format: str)->dict:
    """
    Get the current time in the mentioned format.
    """
    return {
        "current_time": datetime.datetime.now().strftime(format) if format else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

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