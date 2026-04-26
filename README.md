# Vnstock API Service

A FastAPI wrapper for the [vnstock](https://github.com/thinh-vu/vnstock) library, optimized for Flutter applications.

## Live API
The service is hosted at: **[vnstock.finance.duylong.art](https://vnstock.finance.duylong.art)**

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
