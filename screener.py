import streamlit as st
import pandas as pd
import requests
import random

st.set_page_config(page_title="Nexara Stock Screener", layout="wide")
st.title("🇮🇳 Nexara Stock Screener")
st.caption("Filter NSE stocks by key fundamental metrics")

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
        change_pct = data.get("priceInfo", {}).get("pChange", None)
        week_high = data.get("priceInfo", {}).get("weekHighLow", {}).get("max", None)
        week_low = data.get("priceInfo", {}).get("weekHighLow", {}).get("min", None)
        return {
            "pe": float(pe) if pe else None,
            "price": float(price) if price else None,
            "change_pct": float(change_pct) if change_pct else None,
            "week_high": float(week_high) if week_high else None,
            "week_low": float(week_low) if week_low else None,
        }
    except:
        return None

symbols = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
    "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK",
    "ASIANPAINT", "MARUTI", "SUNPHARMA", "TITAN", "NESTLEIND",
    "WIPRO", "ULTRACEMCO", "BAJFINANCE", "PIDILITIND", "DABUR",
    "HCLTECH", "AXISBANK", "DRREDDY", "DIVISLAB", "CIPLA",
    "IRCTC", "ZYDUSLIFE", "LUPIN", "HAVELLS", "MARICO",
    "ADANIPORTS", "POWERGRID", "NTPC", "ONGC", "COALINDIA",
    "TATAMOTORS", "TATASTEEL", "JSWSTEEL", "HINDALCO", "VEDL",
    "BAJAJFINSV", "HDFCLIFE", "SBILIFE", "ICICIPRULI", "ICICIGI",
    "BRITANNIA", "COLPAL", "GODREJCP", "EMAMILTD", "VOLTAS",
    "BERGEPAINT", "MUTHOOTFIN", "CHOLAFIN", "MANAPPURAM", "PAGEIND",
    "RAYMOND", "ALKYLAMINE", "ATUL", "DEEPAKNI", "GALAXYSURF",
    "ABBOTINDIA", "PFIZER", "GLAXO", "ZOMATO", "DELHIVERY",
    "RAILVIKAS", "RVNL", "IRFC", "HUDCO", "TATAPOWER",
    "TORNTPOWER", "AUROPHARMA", "GLENMARK", "IPCALAB", "RADICO",
    "MCDOWELL-N", "UBL", "SCHAEFFLER", "CUMMINSIND", "THERMAX",
    "TIINDIA", "GRINDWELL", "ASTRAL", "SUPREMEIND", "POLYCAB",
    "DIXON", "AMBER", "WHIRLPOOL", "BLUESTARCO", "SYMPHONY",
    "KANSAINER", "AKZONOBEL", "RELAXO", "BATA", "VMART",
    "TRENT", "DMART", "NYKAA", "ZOMATO", "PAYTM",
    "PERSISTENT", "COFORGE", "LTIM", "MPHASIS", "HEXAWARE",
    "BANKBARODA", "PNB", "CANBK", "UNIONBANK", "IDFCFIRSTB",
    "FEDERALBNK", "BANDHANBNK", "RBLBANK", "INDUSINDBK", "AUBANK",
    "LICHSGFIN", "PNBHOUSING", "AAVAS", "HOMEFIRST", "APTUS",
    "SAIL", "NMDC", "MOIL", "NATIONALUM", "HINDCOPPER",
    "GRASIM", "SHREECEM", "JKCEMENT", "RAMCOCEM", "DALMIACIM",
    "SUNtv", "ZEEL", "PVRINOX", "INOXGREEN", "NAZARA",
    "APOLLOHOSP", "FORTIS", "MAXHEALTH", "METROPOLIS", "THYROCARE",
    "CONCOR", "BLUEDART", "MAHLOG", "GESHIP", "SCI"
]

scan_messages = [
    "🔍 Scanning market data...",
    "📊 Gathering financial metrics...",
    "⚖️ Matching values against filters...",
    "📈 Analysing stock performance...",
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
    "💡 IRCTC is one of the few listed government monopolies in India.",
    "💡 Revenue growth above 15% consistently is rare and valuable.",
    "💡 The Nifty 50 has delivered ~12% CAGR over the last 20 years.",
    "💡 Index funds beat 90% of actively managed funds over 10 years.",
    "💡 A company's 52-week high tells you a lot about market confidence.",
    "💡 Price alone means nothing — always compare to earnings.",
    "💡 Screener.in was built by one person and now has millions of users.",
]

st.markdown("### 🎛 Filters")

col1, col2 = st.columns(2)

with col1:
    pe_enabled = st.toggle("PE Ratio Filter", value=True)
    if pe_enabled:
        pe_min, pe_max = st.slider("PE Range", 0, 150, (0, 50))

with col2:
    price_enabled = st.toggle("Price Filter (₹)", value=False)
    if price_enabled:
        price_min, price_max = st.slider("Price Range (₹)", 0, 50000, (0, 5000))

col3, col4 = st.columns(2)

with col3:
    change_enabled = st.toggle("Day Change % Filter", value=False)
    if change_enabled:
        change_min, change_max = st.slider("Day Change %", -20, 20, (-5, 5))

with col4:
    week_range_enabled = st.toggle("Near 52-Week Low Filter", value=False)
    if week_range_enabled:
        st.caption("Shows stocks within 20% of their 52-week low")

st.markdown("---")

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

        if i % 50 == 0:
            fact_placeholder.caption(random.choice(fun_facts))

        progress_bar.progress(progress)

        data = get_nse_data(symbol)
        if not data:
            continue

        passed = True

        if pe_enabled:
            if data["pe"] is None or not (pe_min <= data["pe"] <= pe_max):
                passed = False

        if price_enabled:
            if data["price"] is None or not (price_min <= data["price"] <= price_max):
                passed = False

        if change_enabled:
            if data["change_pct"] is None or not (change_min <= data["change_pct"] <= change_max):
                passed = False

        if week_range_enabled:
            if data["week_low"] and data["price"]:
                if data["price"] > data["week_low"] * 1.20:
                    passed = False

        if passed:
            results.append({
                "Ticker": symbol,
                "PE": round(data["pe"], 1) if data["pe"] else "N/A",
                "Price (₹)": round(data["price"], 1) if data["price"] else "N/A",
                "Day Change %": round(data["change_pct"], 2) if data["change_pct"] else "N/A",
                "52W High": round(data["week_high"], 1) if data["week_high"] else "N/A",
                "52W Low": round(data["week_low"], 1) if data["week_low"] else "N/A",
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
