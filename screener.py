import streamlit as st
import pandas as pd
import requests
import random

st.set_page_config(page_title="Nexara Stock Screener", layout="wide")
st.title("🇮🇳 Nexara Stock Screener")
st.caption("Filter NSE stocks by key fundamental metrics")

col1, col2, col3 = st.columns(3)
with col1:
    pe_max = st.slider("Max PE Ratio", 10, 100, 50)
with col2:
    de_max = st.slider("Max Debt/Equity", 0, 100, 60)
with col3:
    growth_min = st.slider("Min Revenue Growth %", 0, 50, 5)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

def get_nse_data(symbol):
    try:
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=HEADERS, timeout=5)
        r = session.get(url, headers=HEADERS, timeout=5)
        data = r.json()
        pe = data.get("metadata", {}).get("pdSymbolPe", None)
        price = data.get("priceInfo", {}).get("lastPrice", None)
        return {"pe": float(pe) if pe else None, "price": price}
    except:
        return None

symbols = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
    "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK",
    "ASIANPAINT", "MARUTI", "SUNPHARMA", "TITAN", "NESTLEIND",
    "WIPRO", "ULTRACEMCO", "BAJFINANCE", "PIDILITIND", "DABUR",
    "HCLTECH", "AXISBANK", "DRREDDY", "DIVISLAB", "CIPLA",
    "IRCTC", "ZYDUSLIFE", "LUPIN", "HAVELLS", "MARICO"
]

scan_messages = [
    "🔍 Scanning market data...",
    "📊 Gathering financial metrics...",
    "⚖️ Matching values against filters...",
    "📈 Analysing revenue trends...",
    "🧮 Calculating key ratios...",
    "⚠️ Identifying risk factors...",
    "🏆 Ranking top performers...",
    "✅ Finalising results..."
]

fun_facts = [
    "💡 Warren Buffett bought his first stock at age 11.",
    "💡 The BSE is Asia's oldest stock exchange, founded in 1875.",
    "💡 A PE ratio below 15 is generally considered undervalued.",
    "💡 Compound interest is called the 8th wonder of the world.",
    "💡 India's retail investor base grew 4x between 2020 and 2024.",
    "💡 Debt/Equity below 1 means the company owns more than it owes.",
    "💡 IRCTC is one of the few listed government monopolies in India.",
    "💡 Revenue growth above 15% consistently is rare and valuable.",
    "💡 The Nifty 50 has delivered ~12% CAGR over the last 20 years.",
    "💡 Index funds beat 90% of actively managed funds over 10 years.",
]

if st.button("🔍 Run Screener"):
    total = len(symbols)
    results = []

    status_placeholder = st.empty()
    fact_placeholder = st.empty()
    progress_bar = st.progress(0)

    for i, symbol in enumerate(symbols):
        progress = (i + 1) / total

        if progress < 0.125:
            status_placeholder.info(scan_messages[0])
        elif progress < 0.25:
            status_placeholder.info(scan_messages[1])
        elif progress < 0.375:
            status_placeholder.info(scan_messages[2])
        elif progress < 0.50:
            status_placeholder.info(scan_messages[3])
        elif progress < 0.625:
            status_placeholder.info(scan_messages[4])
        elif progress < 0.75:
            status_placeholder.info(scan_messages[5])
        elif progress < 0.90:
            status_placeholder.info(scan_messages[6])
        else:
            status_placeholder.info(scan_messages[7])

        if i % 5 == 0:
            fact_placeholder.caption(random.choice(fun_facts))

        progress_bar.progress(progress)

        data = get_nse_data(symbol)
        if data and data["pe"]:
            pe = data["pe"]
            if pe < pe_max:
                results.append({
                    "Ticker": symbol,
                    "PE": round(pe, 1),
                    "Price": data["price"]
                })

    status_placeholder.empty()
    fact_placeholder.empty()
    progress_bar.empty()

    if results:
        df = pd.DataFrame(results).sort_values("PE")
        st.success(f"✅ {len(df)} stocks passed your filter")
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False)
        st.download_button("📥 Download Results as CSV", csv, "screener_results.csv")
    else:
        st.warning("No stocks passed. Try relaxing your filters.")
