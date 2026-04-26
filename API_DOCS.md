# Vnstock API Documentation

**Base URL**: `https://vnstock.finance.duylong.art`

## Endpoints

### 1. Market & Indices

#### List All Indices
- **URL**: `/market/indices`
- **Method**: `GET`
- **Description**: Returns metadata for all supported indices.

#### Index Historical Data
- **URL**: `/market/index/historical`
- **Method**: `GET`
- **Params**:
  - `symbol` (required): Index ticker (e.g., `VNINDEX`, `VN30`, `DJI`).
  - `start_date` (optional): `YYYY-MM-DD` (default: `2024-01-01`).
  - `end_date` (optional): `YYYY-MM-DD`.
  - `resolution` (optional): `1D`, `1H`, `5m`.

#### Gold Prices
- **URL**: `/market/gold`
- **Method**: `GET`
- **Description**: Real-time and historical SJC/BTMC gold prices.

### 2. Stocks

#### Stock Price
- **URL**: `/stock/price?symbol=VNM`
- **Method**: `GET`

#### Stock Overview
- **URL**: `/stock/overview?symbol=VNM`
- **Method**: `GET`

#### Stock Historical
- **URL**: `/stock/historical?symbol=VNM&start_date=2024-01-01`
- **Method**: `GET`

#### All-in-One Stock Info
- **URL**: `/stock/all?symbol=VNM`
- **Method**: `GET`

#### Stock News
- **URL**: `/stock/news?symbol=VNM`
- **Method**: `GET`

#### Stock Events
- **URL**: `/stock/events?symbol=VNM`
- **Method**: `GET`

### 3. Derivatives & Fixed Income

#### Futures Contracts
- **URL**: `/assets/futures`
- **Method**: `GET`

#### Covered Warrants
- **URL**: `/assets/warrants`
- **Method**: `GET`

#### Bonds
- **URL**: `/assets/bonds`
- **Method**: `GET`
- **Params**:
  - `corp` (optional): `true` (default) for Corporate, `false` for Government.

### 4. Funds

#### Fund Listing
- **URL**: `/funds/listing`
- **Method**: `GET`

#### Fund Details
- **URL**: `/funds/details/{symbol}`
- **Method**: `GET`

### 5. International Markets (MSN Source)

#### Forex History
- **URL**: `/forex/historical`
- **Method**: `GET`
- **Params**:
  - `symbol` (optional): e.g., `EURUSD`, `USDVND` (default: `EURUSD`).

#### Crypto History
- **URL**: `/crypto/historical`
- **Method**: `GET`
- **Params**:
  - `symbol` (optional): e.g., `BTC`, `ETH` (default: `BTC`).

---

## Error Handling
All endpoints return a 404 or 500 status code with a detail message if the data cannot be fetched.
Example: `{"detail": "Stock VNM not found"}`
