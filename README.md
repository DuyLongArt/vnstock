# Vnstock API Service

A FastAPI wrapper for the [vnstock](https://github.com/thinh-vu/vnstock) library, optimized for Flutter applications.

## Live API
The service is hosted at: **[vnstock.finance.duylong.art](https://vnstock.finance.duylong.art)**

## Features
- **Comprehensive Stock Data**: Prices, historical data, and company overviews.
- **Market Indices**: VNIndex, VN30, HNX, and international world indices (DJI, etc.).
- **Derivatives & Assets**: Futures (VN30F1M), Covered Warrants, and Bonds.
- **Investment Funds**: Mutual funds and ETFs data via FMarket.
- **International Markets**: Real-time/historical Forex (USDVND) and Crypto (BTC, ETH) via MSN.
- **Market Indicators**: Domestic gold prices (SJC, BTMC).
- **Corporate Intelligence**: Company news and corporate events.
- **CORS Enabled**: Ready for Flutter Web and cross-origin mobile apps.
- **Dockerized**: Easy deployment via Northbank or any cloud provider.

## Documentation
For detailed information on endpoints, parameters, and Flutter integration, see:
- **[Full API Documentation](API_DOCS.md)**
- Interactive Swagger UI: `/docs`

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Running the Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Docker Deployment
```bash
docker build -t vnstock-api .
docker run -p 8000:8000 vnstock-api
```
