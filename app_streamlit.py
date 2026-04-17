import streamlit as st, pandas as pd, matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from datetime import datetime

st.set_page_config(page_title="📈 Sales Forecast", page_icon="💼", layout="wide")
st.title("📈 Sales Forecast App")

if "page" not in st.session_state: st.session_state.page = "upload"
if "data" not in st.session_state: st.session_state.data = None

def load_data(): return st.session_state.data
def fit_arima(series, order): return ARIMA(series, order=order).fit()


if st.sidebar.button("📁 Upload Data"): st.session_state.page = "upload"
if st.sidebar.button("📊 Overview"): st.session_state.page = "overview"
if st.sidebar.button("🔬 Stationarity"): st.session_state.page = "stationarity"
if st.sidebar.button("🤖 ARIMA"): st.session_state.page = "ARIMA"
if st.sidebar.button("🔮 Forecast"): st.session_state.page = "forecast"

if st.session_state.page == "upload":
    st.header("📁 Upload Data")
    f = st.file_uploader("Choose CSV", type=['csv'])
    if f:
        df = pd.read_csv(f)
        st.success("✅ Uploaded")
        st.dataframe(df.head())
        date_col = st.selectbox("Date Column", df.columns.tolist())
        sales_col = st.selectbox("Sales Column", df.columns.tolist())
        if st.button("Process", type="primary"):
            try:
                df[date_col] = pd.to_datetime(df[date_col])
                df = df.sort_values(date_col)
                df.set_index(date_col, inplace=True)
                df = df[[sales_col]]
                df.columns = ['Amount']
                st.session_state.data = df
                st.success("✅ Processed")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    if st.button("Load Sample"):
        try:
            df = pd.read_csv("sales.csv")
            df["Date"] = pd.to_datetime(df["Date"])
            df.set_index("Date", inplace=True)
            df = df[['Amount']]
            st.session_state.data = df
            st.success("✅ Loaded")
        except: st.error("❌ Not found")

elif st.session_state.page == "overview":
    st.header("📊 Overview")
    d = load_data()
    if d is not None and not d.empty:
        c1,c2,c3,c4 = st.columns(4)
        with c1: st.metric("Records", len(d))
        with c2: st.metric("Avg", f"{d['Amount'].mean():.2f}")
        with c3: st.metric("Total", f"{d['Amount'].sum():.2f}")
        with c4: st.metric("Range", f"{d.index.min().date()}-{d.index.max().date()}")
        st.dataframe(d.head())
        st.line_chart(d["Amount"])
        st.write(d.describe())
    else: st.warning("⚠️ Upload data first")

elif st.session_state.page == "stationarity":
    st.header("🔬 Stationarity")
    d = load_data()
    if d is not None and not d.empty:
        col = st.selectbox("Column", d.columns.tolist())
        if st.button("Apply Diff"):
            d["1st_diff"] = d["Amount"].diff()
            d["2nd_diff"] = d["1st_diff"].diff()
            st.success("✅ Diff applied")
        if st.button("Run ADF", type="primary"):
            r = adfuller(d[col].dropna())
            c1,c2 = st.columns(2)
            with c1: st.metric("ADF Stat", f"{r[0]:.6f}")
            with c2: st.metric("p-value", f"{r[1]:.6f}")
            if r[1] <= 0.05: st.success("✅ Stationary")
            else: st.warning("⚠️ Non-stationary")
    else: st.warning("⚠️ Upload data first")

elif st.session_state.page == "ARIMA":
    st.header("🤖 ARIMA")
    d = load_data()
    if d is not None and not d.empty:
        c1,c2,c3 = st.columns(3)
        with c1: p = st.number_input("p", 0, 20, 1)
        with c2: n = st.number_input("d", 0, 10, 1)
        with c3: q = st.number_input("q", 0, 20, 1)
        if st.button("Fit", type="primary"):
            m = fit_arima(d["Amount"], (p,n,q))
            st.success("✅ Fitted")
            st.text(m.summary())
            f = m.forecast(30)
            c1,c2,c3,c4 = st.columns(4)
            with c1: st.metric("Min", f"{f.min():.2f}")
            with c2: st.metric("Max", f"{f.max():.2f}")
            with c3: st.metric("Mean", f"{f.mean():.2f}")
            with c4: st.metric("Growth", f"{((f.iloc[-1]/d['Amount'].iloc[-1])-1)*100:.1f}%")
            st.dataframe(f)
            st.line_chart(f)
    else: st.warning("⚠️ Upload data first")

elif st.session_state.page == "forecast":
    st.header("🔮 Forecast")
    d = load_data()
    if d is not None and not d.empty:
        m = fit_arima(d["Amount"], (17,2,3))
        c1,c2 = st.columns(2)
        with c1: s = st.date_input("Start", datetime(2009,1,1))
        with c2: e = st.date_input("End", datetime(2050,12,1))
        if st.button("Forecast", type="primary"):
            f = m.predict(start=pd.to_datetime(s), end=pd.to_datetime(e))
            c1,c2,c3,c4 = st.columns(4)
            with c1: st.metric("Min", f"{f.min():.2f}")
            with c2: st.metric("Max", f"{f.max():.2f}")
            with c3: st.metric("Avg", f"{f.mean():.2f}")
            with c4: st.metric("Growth", f"{((f.iloc[-1]/d['Amount'].iloc[-1])-1)*100:.1f}%")
            st.line_chart(f)
            st.dataframe(f)
            st.download_button("Download", f.to_csv(), "forecast.csv")
    else: st.warning("⚠️ Upload data first")
