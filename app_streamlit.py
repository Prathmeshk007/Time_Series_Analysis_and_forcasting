import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
st.set_page_config(page_title=" 📈 Sales Forecast App ",page_icon=" 💼 ",layout="wide")
st.title(" 📈 Sales Forecast add analysis App 📈 ")
st.sidebar.title("analysis and prediction of sales data")
# Use session state to track which page to show
if 'page' not in st.session_state:
    st.session_state.page = None

if st.sidebar.button("Overview of sales data"):
    st.session_state.page = "overview"

if st.sidebar.button("Stationarity Analysis"):
    st.session_state.page = "stationarity"

if st.sidebar.button("ARIMA MODEL"):
    st.session_state.page="ARIMA"

if st.sidebar.button("Future Forecasting"):
    st.session_state.page="Future Forecasting"


if st.session_state.page == "overview":
    st.subheader("sales data")
    d=pd.read_csv("sales.csv")
    st.write(d.head(10))
    st.divider()
    d["Date"]=pd.to_datetime(d["Date"])
    d.set_index("Date",inplace=True)
    st.subheader("Line chart of sales data")
    st.line_chart(d["Amount"])
    st.divider()
    st.subheader("Summary of sales")
    st.write(d.describe())
elif st.session_state.page == "stationarity":
    st.subheader("Stationary Analysis")

    d = pd.read_csv("sales.csv")
    d["Date"] = pd.to_datetime(d["Date"])
    d.set_index("Date", inplace=True)

    # Create differenced columns
    d["1st_diff"] = d["Amount"].diff()
    d["2nd_diff"] = d["1st_diff"].diff()
    d["3rd_diff"] = d["2nd_diff"].diff()
    d["4th_diff"] = d["3rd_diff"].diff()
    d["5th_diff"] = d["4th_diff"].diff()

    column = st.selectbox("Select column for ADF test", d.columns)
    from statsmodels.tsa.stattools import adfuller

    def adf_test(series, name="Series"):
        result = adfuller(series.dropna())
        st.write(f"ADF Statistic for {name}: {result[0]}")
        st.write(f"p-value: {result[1]}")
        if result[1] <= 0.05:
            st.success(f"{name} → Data is stationary")
        else:
            st.warning(f"{name} → Data is not stationary")

    # Run test only when button is clicked
    if st.button("Run ADF Test"):
        adf_test(d[column], name=column)

elif st.session_state.page == "ARIMA":
    st.subheader("ARIMA Modeling")
    import pandas as pd
    d=pd.read_csv("sales.csv")
    d["Date"]=pd.to_datetime(d["Date"])
    d.set_index("Date",inplace=True)
    from statsmodels.tsa.stattools import adfuller 
    def adf_test(data):
        res=adfuller(data)
        print("p_value :",res[1])
        if res[1]<=0.05:
            print("Reject hypothesis null, Data is stationary ")
        else:
            print("Accept hypothesis null, Data is not stationary ")
    adf_test(d["Amount"])
    d["1st_diff"]=d["Amount"]-d["Amount"].shift(1)

    adf_test(d["1st_diff"].dropna())
    d["2nd_diff"]=d["1st_diff"]-d["1st_diff"].shift(1)
    adf_test(d["2nd_diff"].dropna())


    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    from statsmodels.tsa.arima.model import ARIMA

    st.subheader("ACF Plots")
    if st.button("SHOW ACF"):
        fig1 = plt.figure(figsize=(6, 3))
        fig1 = plot_acf(d["2nd_diff"].dropna())
        st.pyplot(fig1)

    st.subheader("PACF plots")
    if st.button("Show PACF"):
        fig2=plt.figure(figsize=(6, 3))
        fig2 = plot_pacf(d["2nd_diff"].dropna())
        st.pyplot(fig2)

    # Fit ARIMA model
    train_data = d
    p=st.number_input("Enter the value of p",min_value=0,max_value=20)
    n=st.number_input("Enter the value of d",min_value=0,max_value=10)
    q=st.number_input("Enter the value of q",min_value=0,max_value=20)
    model = ARIMA(train_data["Amount"], order=(p, n,q))
    fitted_model = model.fit()

    st.subheader("Summary")
    st.write(fitted_model.summary())
    st.divider()
    forecast = fitted_model.forecast(steps=30)
    st.write("Forecasted values:")
    st.divider()
    st.write(forecast)
    st.divider()
    st.line_chart(forecast)
elif st.session_state.page == "Future Forecasting":
    st.subheader("Future Forecasting")
    import pandas as pd
    d=pd.read_csv("sales.csv")
    d["Date"]=pd.to_datetime(d["Date"])
    d.set_index("Date",inplace=True)
    from statsmodels.tsa.stattools import adfuller 
    def adf_test(data):
        res=adfuller(data)
        print("p_value :",res[1])
        if res[1]<=0.05:
            print("Reject hypothesis null, Data is stationary ")
        else:
            print("Accept hypothesis null, Data is not stationary ")
    adf_test(d["Amount"])
    d["1st_diff"]=d["Amount"]-d["Amount"].shift(1)

    adf_test(d["1st_diff"].dropna())
    d["2nd_diff"]=d["1st_diff"]-d["1st_diff"].shift(1)
    adf_test(d["2nd_diff"].dropna())


    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
    p1=plot_acf(d["2nd_diff"].dropna())
    p2=plot_pacf(d["2nd_diff"].dropna())
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.arima.model import ARIMA
    from datetime import datetime
    train_data=d
    m=ARIMA(train_data["Amount"],order=(17,2,3))
    model=m.fit()
    st.subheader("Line chart of actual vs Predicted values")
    s=st.date_input("Select start date",value=datetime(2003,1,1))
    e=st.date_input("Select end date",value=datetime(2008,12,1))
    pred=model.predict(start=pd.to_datetime(s),end=pd.to_datetime(e))
    train_data["predict"]=pred

    st.line_chart(train_data[["Amount","predict"]])
    st.divider()
    st.subheader("Line chart of future forecasting")
    sta=st.date_input("Select start date for future forecasting",value=datetime(2009,1,1))
    ed=st.date_input("Select end date for future forecasting",value=datetime(2050,12,1))
    pred1=model.predict(start=pd.to_datetime(sta),end=pd.to_datetime(ed))
    train_data["future_pred"]=pred1
    st.line_chart(pred1)
    st.divider()
    st.subheader("future forecasting values")
    st.write(pred1)
