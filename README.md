# Sales Forecasting App

Streamlit app for sales forecasting with ARIMA models.

## Features

- Upload CSV data or use sample data
- View sales statistics and trends
- Stationarity analysis with ADF test
- ARIMA modeling with custom parameters
- Future forecasting with export option

## Requirements

Python 3.8+, Streamlit, pandas, matplotlib, statsmodels, numpy

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the app:
```bash
streamlit run app_streamlit.py
```

## CSV Format

| Date | Sales |
|------|-------|
| 2023-01-01 | 15000 |
| 2023-01-02 | 16500 |

## Navigation

- Upload Data: Load your CSV file
- Overview: View statistics and trends
- Stationarity: ADF test for stationarity
- ARIMA: Fit ARIMA models (p, d, q parameters)
- Forecast: Generate future predictions

## Files

- app_streamlit.py: Main app
- requirements.txt: Dependencies
- sales.csv: Sample data
