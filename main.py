from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from vnstock import Vnstock
import pandas as pd
from typing import Optional, List, Dict, Any
import logging
from vnstock.common import indices
from vnstock.explorer.misc import gold_price

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Vnstock API", 
    description="API wrapper for vnstock library to be used in Flutter. Hosted at: vnstock.finance.duylong.art",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize Vnstock
v = Vnstock()

def clean_data(data: Any) -> Any:
    """Convert NaN values to None for JSON compliance."""
    if isinstance(data, pd.DataFrame):
        return data.where(pd.notnull(data), None).to_dict(orient="records")
    if isinstance(data, list):
        return [clean_data(i) for i in data]
    if isinstance(data, dict):
        return {k: clean_data(v) for k, v in data.items()}
    return data

def get_stock_instance(symbol: str, source: str = "KBS"):
    try:
        return v.stock(symbol=symbol, source=source)
    except Exception as e:
        logger.error(f"Error initializing stock {symbol} from {source}: {e}")
        return None

def get_msn_instance(symbol: str, asset_type: str = "world_index"):
    try:
        if asset_type == "crypto":
            return v.crypto(symbol=symbol, source="MSN")
        elif asset_type == "fx":
            return v.fx(symbol=symbol, source="MSN")
        else:
            return v.world_index(symbol=symbol, source="MSN")
    except Exception as e:
        logger.error(f"Error initializing MSN asset {symbol} ({asset_type}): {e}")
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
        # Ensure we return common fields for Flutter based on raw data observed
        result = {
            "symbol": data.get("symbol"),
            "price": data.get("close_price") or data.get("price"),
            "change": data.get("price_change") or data.get("change_amount"),
            "change_percent": data.get("percent_change") or data.get("change_percent"),
            "volume": data.get("volume_accumulated") or data.get("total_volume"),
            "high": data.get("high_price") or data.get("high"),
            "low": data.get("low_price") or data.get("low"),
            "time": data.get("time"),
            "raw": data 
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
        # profile = stock.company.profile() # This might fail for some sources
        
        return {
            "symbol": symbol,
            "overview": clean_data(overview),
            # "profile": clean_data(profile)
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
                return {"symbol": symbol, "source": source, "data": clean_data(df)}
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

# --- Market & Indices ---

@app.get("/market/indices")
def list_indices():
    """List all supported indices metadata."""
    try:
        df = indices.get_all_indices()
        return {"data": clean_data(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market/index/historical")
def get_index_historical(
    symbol: str = Query(..., description="Index symbol, e.g., VNINDEX, VN30, DJI"),
    start_date: str = Query("2024-01-01"),
    end_date: Optional[str] = None,
    resolution: str = "1D"
):
    """Get historical data for domestic or international indices."""
    # Check if it's a domestic index first
    if indices.is_valid_index(symbol):
        # Use existing stock historical logic but specifically for indices
        return get_historical(symbol=symbol, start_date=start_date, end_date=end_date, resolution=resolution)
    
    asset = get_msn_instance(symbol, asset_type="world_index")
    if asset:
        try:
            df = asset.quote.history(start=start_date, end=end_date, interval=resolution)
            return {"symbol": symbol, "source": "MSN", "data": clean_data(df)}
        except Exception as e:
            logger.error(f"MSN Index history failed for {symbol}: {e}")
    
    raise HTTPException(status_code=404, detail=f"Index {symbol} not found or data unavailable")

@app.get("/market/gold")
def get_gold_prices(date: Optional[str] = None):
    """Get SJC and BTMC gold prices."""
    try:
        sjc = gold_price.sjc_gold_price(date=date)
        btmc = gold_price.btmc_goldprice()
        return {
            "sjc": clean_data(sjc),
            "btmc": clean_data(btmc)
        }
    except Exception as e:
        logger.error(f"Error fetching gold prices: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Derivatives & Assets ---

@app.get("/assets/futures")
def list_futures():
    """List all available futures contracts."""
    try:
        # We can use any valid stock instance to access listing
        stock = get_stock_instance("VN30F1M")
        df = stock.listing.all_future_indices()
        return {"data": clean_data(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/assets/warrants")
def list_warrants():
    """List all covered warrants."""
    try:
        stock = get_stock_instance("ACB")
        df = stock.listing.all_covered_warrant()
        return {"data": clean_data(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/assets/bonds")
def list_bonds(corp: bool = True):
    """List corporate or government bonds."""
    try:
        stock = get_stock_instance("ACB")
        if corp:
            df = stock.listing.all_bonds()
        else:
            df = stock.listing.all_government_bonds()
        return {"data": clean_data(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Funds ---

@app.get("/funds/listing")
def list_funds():
    """List all open funds from FMarket."""
    try:
        f = v.fund(source="FMARKET")
        df = f.listing()
        return {"data": clean_data(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/funds/details/{symbol}")
def get_fund_details(symbol: str):
    """Get detailed information for a fund."""
    try:
        f = v.fund(source="FMARKET")
        details = f.details(symbol=symbol)
        return {"symbol": symbol, "details": details}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Forex & Crypto ---

@app.get("/forex/historical")
def get_fx_historical(symbol: str = "EURUSD", start_date: str = "2024-01-01", end_date: Optional[str] = None):
    """Get historical exchange rate data from MSN."""
    asset = get_msn_instance(symbol, asset_type="fx")
    if not asset:
        raise HTTPException(status_code=404, detail=f"Forex pair {symbol} not found")
    try:
        df = asset.quote.history(start=start_date, end=end_date)
        return {"symbol": symbol, "data": clean_data(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/crypto/historical")
def get_crypto_historical(symbol: str = "BTC", start_date: str = "2024-01-01", end_date: Optional[str] = None):
    """Get historical cryptocurrency price data from MSN."""
    asset = get_msn_instance(symbol, asset_type="crypto")
    if not asset:
        raise HTTPException(status_code=404, detail=f"Crypto asset {symbol} not found")
    try:
        df = asset.quote.history(start=start_date, end=end_date)
        return {"symbol": symbol, "data": clean_data(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- News & Events ---

@app.get("/stock/news")
def get_stock_news(symbol: str = Query(...)):
    """Get company news for a ticker."""
    stock = get_stock_instance(symbol)
    if not stock or not stock.company:
        raise HTTPException(status_code=404, detail="Company news unavailable")
    try:
        df = stock.company.news()
        return {"symbol": symbol, "data": clean_data(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock/events")
def get_stock_events(symbol: str = Query(...)):
    """Get corporate events for a ticker."""
    stock = get_stock_instance(symbol)
    if not stock or not stock.company:
        raise HTTPException(status_code=404, detail="Company events unavailable")
    try:
        df = stock.company.events()
        return {"symbol": symbol, "data": clean_data(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
