Link=https://prathmeshk007-time-series-analysis-and-for-app-streamlit-x1o0aa.streamlit.app/#line-chart-of-future-forecasting
# 📈 Time Series Analysis & Forecasting Dashboard

A comprehensive Streamlit application for time series analysis, stationarity testing, ARIMA modeling, and forecasting built with Python.

## 🚀 Features

### 📊 Data Overview
- View sales data with interactive tables
- Time series visualization with line charts
- Statistical summary of the dataset
- Data preprocessing with date formatting

### 🔬 Stationarity Analysis
- **ADF Test Implementation**: Augmented Dickey-Fuller test for stationarity
- **Multiple Differencing Levels**: Automatic creation of 1st to 5th order differences
- **Interactive Column Selection**: Test any column from your dataset
- **Real-time Results**: Instant ADF statistics and p-value interpretation

### 🤖 ARIMA Modeling
- **Parameter Configuration**: Interactive input for ARIMA (p,d,q) parameters
- **ACF/PACF Visualization**: Autocorrelation and Partial Autocorrelation plots
- **Model Training**: Fit ARIMA models with custom parameters
- **Model Summary**: Detailed statistical results and diagnostics
- **Short-term Forecasting**: 30-step ahead predictions

### 🔮 Future Forecasting
- **Custom Date Ranges**: Select any forecast period
- **Historical vs Predicted**: Compare actual values with model predictions
- **Long-term Forecasts**: Generate predictions up to year 2050
- **Interactive Visualizations**: Dynamic charts for forecast results

## 📋 Requirements

### Python Packages
```bash
pip install streamlit pandas numpy matplotlib statsmodels
```

### Data File
- `sales.csv` - Must contain `Date` and `Amount` columns
- Place in the same directory as the application

## 🛠️ Installation & Setup

1. **Clone/Download** the application files
2. **Install dependencies**:
   ```bash
   pip install streamlit pandas numpy matplotlib statsmodels
   ```
3. **Prepare data**: Ensure `sales.csv` is in the correct directory
4. **Run the application**:
   ```bash
   streamlit run app_streamlit.py
   ```

## 📖 Usage Guide

### 1. Data Overview
- Click "Overview of sales data" in the sidebar
- View the first 10 rows of your dataset
- Explore the time series plot and statistical summary

### 2. Stationarity Analysis
- Click "Stationarity Analysis" in the sidebar
- Select a column from the dropdown (e.g., "Amount", "1st_diff", "2nd_diff", etc.)
- Click "Run ADF Test" to perform stationarity testing
- Interpret results:
  - ✅ **Stationary**: p-value ≤ 0.05
  - ❌ **Non-stationary**: p-value > 0.05

### 3. ARIMA Modeling
- Click "ARIMA MODEL" in the sidebar
- The app automatically performs stationarity analysis and differencing
- Click "SHOW ACF" to view Autocorrelation Function plot
- Click "Show PACF" to view Partial Autocorrelation Function plot
- Enter ARIMA parameters:
  - **p**: AR order (0-20)
  - **d**: Differencing order (0-10)  
  - **q**: MA order (0-20)
- View model summary and 30-step forecast

### 4. Future Forecasting
- Click "Future Forecasting" in the sidebar
- Uses pre-configured ARIMA(17,2,3) model
- Select date ranges for:
  - Historical predictions: Compare actual vs predicted (2003-2008)
  - Future forecasts: Generate predictions (2009-2050)
- View interactive charts and forecast values

## 📊 Understanding the Results

### ADF Test Results
- **ADF Statistic**: More negative values indicate stronger evidence against non-stationarity
- **p-value**: Probability of observing the test statistic under null hypothesis
- **Interpretation**:
  - p ≤ 0.05: Reject null hypothesis → Data is stationary
  - p > 0.05: Accept null hypothesis → Data is non-stationary

### ARIMA Parameters
- **p (AR)**: Number of lag observations included in the model
- **d (I)**: Number of times the raw observations are differenced
- **q (MA)**: Size of the moving average window

### Based on Your Data Analysis
- Original data is non-stationary (p ≈ 0.56)
- First difference is still non-stationary (p ≈ 0.07)
- Second difference becomes stationary (p ≈ 3.49e-15)
- Recommended ARIMA parameters: (17, 2, 3)

## 🎯 Best Practices

### Data Preparation
- Ensure your CSV file has consistent date formatting
- Handle missing values before analysis
- Check for outliers that might affect results

### Model Selection
- Use ACF/PACF plots to guide parameter selection
- Start with simpler models before trying complex parameters
- Validate model performance on holdout data

### Interpretation
- Always consider the business context of your forecasts
- Monitor model performance over time
- Update models regularly with new data

## 🐛 Troubleshooting

### Common Issues
1. **"sales.csv not found"**: Ensure the data file is in the correct directory
2. **Button not working**: Check if session state is properly implemented
3. **Model convergence warnings**: Try different parameter combinations
4. **Memory issues**: Reduce forecast horizon for large datasets

### Performance Tips
- Use data caching for large datasets
- Limit forecast steps to reasonable ranges
- Clear session state if needed

## 🔧 Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Backend**: Python data processing pipeline
- **Libraries**: pandas, statsmodels, matplotlib, numpy

### Key Functions
- `adf_test()`: Augmented Dickey-Fuller stationarity testing
- `plot_acf()`/`plot_pacf()`: Correlation analysis
- `ARIMA()`: Time series modeling
- `model.predict()`: Forecasting

### Session Management
- Uses `st.session_state` for page navigation
- Maintains state across button interactions
- Preserves user selections and results

## 📈 Example Workflow

1. **Load Data**: Start with Data Overview to understand your dataset
2. **Test Stationarity**: Use Stationarity Analysis to determine differencing needs
3. **Model Building**: Move to ARIMA Modeling for parameter selection and training
4. **Generate Forecasts**: Use Future Forecasting for predictions
5. **Iterate**: Refine parameters based on results

## 🤝 Contributing

Feel free to enhance the application with:
- Additional time series models (SARIMA, Prophet, etc.)
- Model performance metrics
- Data preprocessing tools
- Export functionality for results

## 📄 License

This project is open source and available under the MIT License.

---

**🚀 Ready to start forecasting? Run `streamlit run app_streamlit.py` and begin your time series analysis journey!**
