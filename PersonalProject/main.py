import streamlit as st
import requests
import pandas as pd
import sqlite3


st.set_page_config(page_title="Crypto Arbitrage Finder", layout="wide")
st.title("🚀 Crypto Arbitrage Monitor")


st.sidebar.header("Settings")
coin = st.sidebar.selectbox("Select Coin", ["BTC", "ETH", "SOL", "BNB"])
alert_val = st.sidebar.slider("Alert Threshold (%)", 0.0, 5.0, 0.5)


if st.button("Check for Gaps 🔍"):
    with st.spinner("Fetching data from API and Scraper..."):
        try:

            response = requests.get(f"http://127.0.0.1:8000/api/v1/compare/{coin}?threshold={alert_val}")
            data = response.json()


            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Official API Price", f"${data['api_price']:,}")

            with col2:
                st.metric("Scraped Price", f"${data['scraped_price']:,}")

            with col3:

                diff = data['spread_percentage']
                color = "normal" if not data['is_profitable'] else "inverse"
                st.metric("Current Spread", f"{diff}%", delta=f"{diff}%", delta_color=color)


            if data['is_profitable']:
                st.success(f"🔥 PROFIT OPPORTUNITY FOUND! Spread is above {alert_val}%")
                st.balloons()
            else:
                st.info("No major arbitrage detected at this time.")

        except Exception as e:
            st.error(f"Could not connect to Backend. Is Uvicorn running? Error: {e}")


st.divider()
st.subheader("📜 Search History")
search_term = st.text_input("Filter history by coin (e.g. BTC)")


try:
    conn = sqlite3.connect("crypto.db")
    query = "SELECT symbol, api_price, scraped_price, spread, timestamp FROM history ORDER BY timestamp DESC"
    df = pd.read_sql_query(query, conn)

    if search_term:
        df = df[df['symbol'].str.contains(search_term.upper())]

    st.dataframe(df, use_container_width=True)
    conn.close()
except Exception:
    st.write("No history found yet. Try checking a price first!")
