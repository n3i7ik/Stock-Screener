import streamlit as st
import yfinance as yf
import pandas as pd
import time
import random

st.set_page_config(page_title="Indian Stock Screener", layout="wide")
st.title("🇮🇳 Indian Stock Screener")
st.caption("Filter NSE stocks by key fundamental metrics")

col1, col2, col3 = st.columns(3)
with col1:
    pe_max = st.slider("Max PE Ratio", 10, 100, 30)
with col2:
    de_max = st.slider("Max Debt/Equity", 0, 100, 40)
with col3:
    growth_min = st.slider("Min Revenue Growth %", 0, 50, 10)

tickers = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
    "ASIANPAINT.NS", "MARUTI.NS", "SUNPHARMA.NS", "TITAN.NS", "NESTLEIND.NS",
    "WIPRO.NS", "ULTRACEMCO.NS", "BAJFINANCE.NS", "PIDILITIND.NS", "DABUR.NS",
    "HCLTECH.NS", "AXISBANK.NS", "DRREDDY.NS", "DIVISLAB.NS", "CIPLA.NS",
    "ADANIPORTS.NS", "POWERGRID.NS", "NTPC.NS", "ONGC.NS", "COALINDIA.NS",
    "TATAMOTORS.NS", "TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS",
    "BAJAJFINSV.NS", "HDFCLIFE.NS", "SBILIFE.NS", "ICICIPRULI.NS", "ICICIGI.NS",
    "BRITANNIA.NS", "MARICO.NS", "COLPAL.NS", "GODREJCP.NS", "EMAMILTD.NS",
    "HAVELLS.NS", "VOLTAS.NS", "WHIRLPOOL.NS", "BLUESTARCO.NS", "SYMPHONY.NS",
    "BERGEPAINT.NS", "KANSAINER.NS", "AKZONOBEL.NS", "SHEELA.NS", "RELAXO.NS",
    "PAGEIND.NS", "RAYMOND.NS", "MUTHOOTFIN.NS", "CHOLAFIN.NS", "MANAPPURAM.NS",
    "LICHSGFIN.NS", "PNBHOUSING.NS", "AAVAS.NS", "HOMEFIRST.NS", "APTUS.NS",
    "ALKYLAMINE.NS", "ATUL.NS", "DEEPAKNI.NS", "FINEORG.NS", "GALAXYSURF.NS",
    "ABBOTINDIA.NS", "ASTRAZEN.NS", "PFIZER.NS", "SANOFI.NS", "GLAXO.NS",
    "ZOMATO.NS", "NYKAA.NS", "POLICYBZR.NS", "PAYTM.NS", "DELHIVERY.NS",
    "IRCTC.NS", "RAILVIKAS.NS", "RVNL.NS", "IRFC.NS", "HUDCO.NS",
    "TATAPOWER.NS", "ADANIGREEN.NS", "ADANITRANS.NS", "TORNTPOWER.NS", "CESC.NS",
    "ZYDUSLIFE.NS", "LUPIN.NS", "AUROPHARMA.NS", "GLENMARK.NS", "IPCALAB.NS",
    "MCDOWELL-N.NS", "RADICO.NS", "UNITDSPR.NS", "UBL.NS", "GLOBUSSPR.NS"
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
    "💡 Promoter holding above 50% usually signals founder confidence.",
    "💡 Free Cash Flow is more reliable than reported profit.",
    "💡 The Nifty 50 has delivered ~12% CAGR over the last 20 years.",
    "💡 Benjamin Graham's book 'The Intelligent Investor' was published in 1949.",
    "💡 Index funds beat 90% of actively managed funds over 10 years.",
    "💡 A company with high margins and low debt is a rare combination.",
    "💡 Screener.in was built by one person and now has millions of users.",
]

if st.button("🔍 Run Screener"):
    total = len(tickers)
    results = []

    status_placeholder = st.empty()
    fact_placeholder = st.empty()
    progress_bar = st.progress(0)

    for i, t in enumerate(tickers):
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

        try:
            info = yf.Ticker(t).info
            pe = info.get('trailingPE', 999)
            de = info.get('debtToEquity', 999)
            growth = info.get('revenueGrowth', 0)
            volume = info.get('averageVolume', 0)
            margin = info.get('profitMargins', 0)

            if pe < pe_max and de < de_max and growth > growth_min / 100:
                results.append({
                    "Ticker": t.replace(".NS", ""),
                    "PE": round(pe, 1),
                    "D/E": round(de, 1),
                    "Revenue Growth %": round(growth * 100, 1),
                    "Profit Margin %": round(margin * 100, 1),
                    "Avg Volume (L)": round(volume / 100000, 1)
                })
        except:
            pass

    status_placeholder.empty()
    fact_placeholder.empty()
    progress_bar.empty()

    if results:
        df = pd.DataFrame(results).sort_values("Revenue Growth %", ascending=False)
        st.success(f"✅ {len(df)} stocks passed your filter")
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False)
        st.download_button("📥 Download Results as CSV", csv, "screener_results.csv")
    else:
        st.warning("No stocks passed. Try relaxing your filters.")