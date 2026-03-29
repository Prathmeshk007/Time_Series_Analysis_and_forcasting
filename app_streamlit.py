import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from datetime import datetime

st.set_page_config(page_title="📈 Sales Forecast App", page_icon="💼", layout="wide")
st.title("📈 Sales Forecast and Analysis App 📈")
st.sidebar.title("Analysis and Prediction of Sales Data")

# --- Cached functions ---
@st.cache_data
def load_data():
    d = pd.read_csv("sales.csv")
    d["Date"] = pd.to_datetime(d["Date"])
    d.set_index("Date", inplace=True)
    return d

@st.cache_resource
def fit_arima(series, order):
    model = ARIMA(series, order=order)
    return model.fit()

# --- Session state for navigation ---
if "page" not in st.session_state:
    st.session_state.page = None

if st.sidebar.button("Overview of sales data"):
    st.session_state.page = "overview"
if st.sidebar.button("Stationarity Analysis"):
    st.session_state.page = "stationarity"
if st.sidebar.button("ARIMA MODEL"):
    st.session_state.page = "ARIMA"
if st.sidebar.button("Future Forecasting"):
    st.session_state.page = "Future Forecasting"

# --- Pages ---
if st.session_state.page == "overview":
    st.subheader("Sales Data")
    d = load_data()
    st.write(d.head(10))
    st.divider()
    st.subheader("Line Chart of Sales Data")
    st.line_chart(d["Amount"])
    st.divider()
    st.subheader("Summary of Sales")
    st.write(d.describe())

elif st.session_state.page == "stationarity":
    st.subheader("Stationarity Analysis")
    d = load_data()

    # Differencing
    d["1st_diff"] = d["Amount"].diff()
    d["2nd_diff"] = d["1st_diff"].diff()
    d["3rd_diff"] = d["2nd_diff"].diff()
    d["4th_diff"] = d["3rd_diff"].diff()
    d["5th_diff"] = d["4th_diff"].diff()

    column = st.selectbox("Select column for ADF test", d.columns)

    def adf_test(series, name="Series"):
        result = adfuller(series.dropna())
        st.write(f"ADF Statistic for {name}: {result[0]}")
        st.write(f"p-value: {result[1]}")
        if result[1] <= 0.05:
            st.success(f"{name} → Data is stationary")
        else:
            st.warning(f"{name} → Data is not stationary")

    if st.button("Run ADF Test"):
        adf_test(d[column], name=column)

elif st.session_state.page == "ARIMA":
    st.subheader("ARIMA Modeling")
    d = load_data()

    st.subheader("ACF Plots")
    if st.button("SHOW ACF"):
        fig1 = plt.figure(figsize=(6, 3))
        plot_acf(d["Amount"].diff().dropna(), ax=plt.gca())
        st.pyplot(fig1)

    st.subheader("PACF Plots")
    if st.button("Show PACF"):
        fig2 = plt.figure(figsize=(6, 3))
        plot_pacf(d["Amount"].diff().dropna(), ax=plt.gca())
        st.pyplot(fig2)

    # User inputs
    p = st.number_input("Enter the value of p", min_value=0, max_value=20)
    n = st.number_input("Enter the value of d", min_value=0, max_value=10)
    q = st.number_input("Enter the value of q", min_value=0, max_value=20)

    fitted_model = fit_arima(d["Amount"], (p, n, q))

    st.subheader("Summary")
    st.write(fitted_model.summary())
    st.divider()

    forecast = fitted_model.forecast(steps=30)
    st.write("Forecasted values:")
    st.write(forecast)
    st.line_chart(forecast)

elif st.session_state.page == "Future Forecasting":
    st.subheader("Future Forecasting")
    d = load_data()

    # Fit fixed ARIMA model
    model = fit_arima(d["Amount"], (17, 2, 3))

    st.subheader("Line Chart of Actual vs Predicted Values")
    st.write("The starting date for the prediction is 2003-01-01 and the ending date is 2008-12-01")
    pred = model.predict(start=pd.to_datetime("2003-01-01"), end=pd.to_datetime("2008-12-01"))
    d["predict"] = pred
    st.line_chart(d[["Amount", "predict"]])

    st.divider()
    st.subheader("Line Chart of Future Forecasting")
    sta = st.date_input("Select start date for future forecasting", value=datetime(2009, 1, 1))
    ed = st.date_input("Select end date for future forecasting", value=datetime(2050, 12, 1))
    pred1 = model.predict(start=pd.to_datetime(sta), end=pd.to_datetime(ed))
    d["future_pred"] = pred1
    st.line_chart(pred1)

    st.subheader("Future Forecasting Values")
    st.write(pred1)
