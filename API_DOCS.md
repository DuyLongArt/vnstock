# Vnstock API Documentation

Welcome to the Vnstock API documentation. This service provides a high-performance wrapper for the `vnstock` library, optimized for mobile and web consumption.

## Base URL
`https://vnstock.finance.duylong.art`

## Authentication
Currently, the API is public and does not require authentication.

---

## Endpoints

### 1. Health Check
Verify if the service is running.

**URL**: `/health`  
**Method**: `GET`  
**Response**:
```json
{
  "status": "ok",
  "message": "Vnstock API is running"
}
```

### 2. Current Stock Price
Get real-time price, change statistics, and volume for a specific ticker.

**URL**: `/stock/price`  
**Method**: `GET`  
**Query Parameters**:
- `symbol` (Required): Stock ticker (e.g., `VNM`, `FPT`, `VIC`)

**Response**:
```json
{
  "data": {
    "symbol": "VNM",
    "price": 61400,
    "change": -600,
    "change_percent": -0.9677,
    "volume": 5855700,
    "high": 62100,
    "low": 60500,
    "time": 1777019549854
  }
}
```

### 3. Company Overview
Retrieve business model, history, and profile information for a company.

**URL**: `/stock/overview`  
**Method**: `GET`  
**Query Parameters**:
- `symbol` (Required): Stock ticker.

**Response**:
```json
{
  "symbol": "VNM",
  "overview": [
    {
      "business_model": "Chế biến, sản xuất kinh doanh sữa...",
      "ceo_name": "Ms. Mai Kiều Liên",
      "exchange": "HOSE",
      "website": "https://www.vinamilk.com.vn"
    }
  ]
}
```

### 4. Historical Data
Get daily OHLCV (Open, High, Low, Close, Volume) data.

**URL**: `/stock/historical`  
**Method**: `GET`  
**Query Parameters**:
- `symbol` (Required): Stock ticker.
- `start_date` (Optional): Start date in `YYYY-MM-DD` format (Default: `2024-01-01`).
- `end_date` (Optional): End date in `YYYY-MM-DD` format.
- `resolution` (Optional): Data resolution (Default: `1D`).

**Response**:
```json
{
  "symbol": "VNM",
  "source": "KBS",
  "data": [
    {
      "time": "2024-01-01",
      "open": 61000,
      "high": 62000,
      "low": 60500,
      "close": 61500,
      "volume": 1200000
    }
  ]
}
```

### 5. Unified Stock Data
Combines current price and company overview in a single call for dashboard efficiency.

**URL**: `/stock/all`  
**Method**: `GET`  
**Query Parameters**:
- `symbol` (Required): Stock ticker.

**Response**:
```json
{
  "price": { ... },
  "company": { ... }
}
```

---

## Flutter Integration Example

Using the `http` package in Flutter:

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class StockService {
  final String baseUrl = 'https://vnstock.finance.duylong.art';

  Future<Map<String, dynamic>> getStockInfo(String symbol) async {
    final response = await http.get(Uri.parse('$baseUrl/stock/all?symbol=$symbol'));
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load stock data');
    }
  }
}
```

---

## Errors
The API uses standard HTTP status codes:
- `200 OK`: Request succeeded.
- `400 Bad Request`: Invalid parameters.
- `404 Not Found`: Stock symbol not recognized.
- `500 Internal Server Error`: Server error or data source failure.
