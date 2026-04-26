from fastapi import FastAPI, HTTPException, Query
from vnstock import Vnstock
import pandas as pd
from typing import Optional, List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Vnstock API", 
    description="API wrapper for vnstock library to be used in Flutter",
    version="1.0.0"
)

# Initialize Vnstock
v = Vnstock()

def get_stock_instance(symbol: str, source: str = "KBS"):
    try:
        return v.stock(symbol=symbol, source=source)
    except Exception as e:
        logger.error(f"Error initializing stock {symbol} from {source}: {e}")
        return None

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Vnstock API is running"}

@app.get("/stock/price")
def get_stock_price(symbol: str = Query(..., description="Stock ticker symbol, e.g., VNM")):
    """
    Get current stock price, change, and volume info.
    """
    stock = get_stock_instance(symbol)
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found or source unavailable")
    
    try:
        # KBS price_board returns a list of symbols
        df = stock.trading.price_board([symbol])
        if df.empty:
            return {"data": {}}
        
        data = df.iloc[0].to_dict()
        # Ensure we return common fields for Flutter
        result = {
            "symbol": data.get("symbol"),
            "price": data.get("price"),
            "change": data.get("change_amount"),
            "change_percent": data.get("change_percent"),
            "volume": data.get("total_volume"),
            "high": data.get("high"),
            "low": data.get("low"),
            "time": data.get("time"),
            "raw": data # Include raw data just in case
        }
        return {"data": result}
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock/overview")
def get_stock_overview(symbol: str = Query(..., description="Stock ticker symbol")):
    """
    Get company information and overview.
    """
    stock = get_stock_instance(symbol)
    if not stock or not stock.company:
        raise HTTPException(status_code=404, detail=f"Company info for {symbol} not available")
    
    try:
        overview = stock.company.overview()
        profile = stock.company.profile()
        
        return {
            "symbol": symbol,
            "overview": overview.to_dict(orient="records") if not overview.empty else [],
            "profile": profile.to_dict(orient="records") if not profile.empty else []
        }
    except Exception as e:
        logger.error(f"Error fetching overview for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock/historical")
def get_historical(
    symbol: str = Query(...),
    start_date: str = Query("2024-01-01"),
    end_date: Optional[str] = None,
    resolution: str = "1D"
):
    """
    Get historical price data.
    Note: Historical data source might vary; using a fallback mechanism.
    """
    # Try different sources for historical data
    for source in ["VCI", "KBS"]:
        try:
            stock = v.stock(symbol=symbol, source=source)
            # Some sources use .trading.historical_data, others .quote.history
            if hasattr(stock.trading, 'historical_data'):
                df = stock.trading.historical_data(start_date=start_date, end_date=end_date, resolution=resolution)
            elif hasattr(stock.quote, 'history'):
                df = stock.quote.history(start=start_date, end=end_date, interval=resolution)
            else:
                continue
                
            if not df.empty:
                return {"symbol": symbol, "source": source, "data": df.to_dict(orient="records")}
        except Exception as e:
            logger.warning(f"Source {source} failed for historical data: {e}")
            continue
            
    raise HTTPException(status_code=500, detail="Unable to fetch historical data from any source")

@app.get("/stock/all")
def get_all_info(symbol: str = Query(...)):
    """
    Get all information (price, overview) in one call for Flutter dashboard.
    """
    try:
        price = get_stock_price(symbol)
        overview = get_stock_overview(symbol)
        return {
            "price": price["data"],
            "company": overview
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
