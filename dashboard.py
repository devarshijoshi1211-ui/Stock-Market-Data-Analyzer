import sys
from pathlib import Path
from datetime import date, timedelta

import streamlit as st
import pandas as pd
import numpy as np

PROJECT_PATH = Path(__file__).resolve().parent

if str(PROJECT_PATH) not in sys.path:
    sys.path.insert(0, str(PROJECT_PATH))

from main import run_analysis

st.set_page_config(
    page_title="Stock Market Data Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #17365d;
    }
    .subtitle {
        color: #64748b;
        font-size: 1rem;
    }
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.04);
    }
    .section-title {
        color: #17365d;
        font-weight: 700;
    }
    .disclaimer {
        background-color: #fff7ed;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
        color: #92400e;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">📈 Stock Market Data Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Interactive stock market analysis, financial trends, returns and volatility dashboard</div>',
    unsafe_allow_html=True
)

st.write("")

st.sidebar.title("⚙️ Analysis Settings")

ticker = st.sidebar.text_input(
    "Stock Ticker",
    value="AAPL",
    help="Examples: AAPL, MSFT, GOOGL, TSLA, RELIANCE.NS"
).strip().upper()

today = date.today()
default_start = today - timedelta(days=365)

start_date = st.sidebar.date_input(
    "Start Date",
    value=default_start,
    max_value=today
)

end_date = st.sidebar.date_input(
    "End Date",
    value=today,
    max_value=today
)

st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "Upload Stock CSV (Optional)",
    type=["csv"]
)

st.sidebar.caption(
    "Upload a historical stock CSV or use Yahoo Finance."
)

run_button = st.sidebar.button(
    "🚀 Run Stock Analysis",
    use_container_width=True,
    type="primary"
)

if run_button:
    if not ticker:
        st.sidebar.error("Please enter a stock ticker.")
    elif start_date >= end_date:
        st.sidebar.error("End date must be after start date.")
    else:
        with st.spinner("Analyzing stock market data..."):
            try:
                csv_path = None
                if uploaded_file is not None:
                    upload_dir = PROJECT_PATH / "data" / "uploads"
                    upload_dir.mkdir(parents=True, exist_ok=True)
                    csv_path = upload_dir / "uploaded_stock_data.csv"
                    csv_path.write_bytes(uploaded_file.getvalue())

                analysis_data, summary, output_paths = run_analysis(
                    ticker=ticker,
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                    csv_path=str(csv_path) if csv_path else None,
                    project_path=str(PROJECT_PATH)
                )

                st.session_state["analysis_data"] = analysis_data
                st.session_state["summary"] = summary
                st.session_state["output_paths"] = output_paths
                st.session_state["ticker"] = ticker
                st.success(f"Analysis for {ticker} completed successfully!")
            except Exception as error:
                st.error(f"Analysis failed: {error}")

if "analysis_data" in st.session_state:
    data = st.session_state["analysis_data"]
    summary = st.session_state["summary"]
    output_paths = st.session_state["output_paths"]
    active_ticker = st.session_state["ticker"]

    st.markdown("---")
    st.subheader(f"📊 {active_ticker} Financial Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest Closing Price", f"${summary['latest_close']:,.2f}")
    col2.metric("Cumulative Return", f"{summary['cumulative_return']:.2f}%")
    col3.metric("Highest Closing Price", f"${summary['highest_close']:,.2f}")
    col4.metric("Lowest Closing Price", f"${summary['lowest_close']:,.2f}")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Average Closing Price", f"${summary['average_close']:,.2f}")
    col6.metric("Average Daily Volume", f"{summary['average_volume']:,.0f}")
    col7.metric("Daily Volatility", f"{summary['daily_volatility']:.2f}%")
    col8.metric("Annualized Volatility", f"{summary['annualized_volatility']:.2f}%")

    st.markdown("---")
    st.subheader("📈 Price and Trend Analysis")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Closing Price",
        "Moving Averages",
        "Daily Returns",
        "Trading Volume"
    ])

    with tab1:
        st.markdown("#### Historical Closing Price")
        st.line_chart(data["Close"], use_container_width=True)

    with tab2:
        st.markdown("#### 20-Day and 50-Day Moving Averages")
        st.line_chart(data[["Close", "MA20", "MA50"]], use_container_width=True)

    with tab3:
        st.markdown("#### Daily Returns (%)")
        st.line_chart(data["Daily_Return"].dropna() * 100, use_container_width=True)

    with tab4:
        st.markdown("#### Daily Trading Volume")
        st.bar_chart(data["Volume"], use_container_width=True)

    st.markdown("---")
    st.subheader("📉 Risk and Return Analysis")

    risk_col1, risk_col2 = st.columns(2)
    with risk_col1:
        st.markdown("#### Rolling 20-Day Volatility")
        st.line_chart(data["Rolling_20D_Volatility"].dropna() * 100, use_container_width=True)

    with risk_col2:
        st.markdown("#### Daily Return Distribution")
        returns = data["Daily_Return"].dropna() * 100
        histogram = pd.DataFrame({"Daily Return (%)": returns})
        st.bar_chart(
            histogram["Daily Return (%)"].value_counts(bins=30).sort_index(),
            use_container_width=True
        )

    st.markdown("---")
    st.subheader("📋 Financial Analysis Summary")

    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        st.write("**Analysis Period**")
        st.write(f"{summary['start_date'].strftime('%Y-%m-%d')} to {summary['end_date'].strftime('%Y-%m-%d')}")
        st.write("**Total Trading Records**")
        st.write(f"{summary['total_records']:,}")
        st.write("**Latest 20-Day Moving Average**")
        st.write(f"${summary['latest_ma20']:,.2f}")
        st.write("**Latest 50-Day Moving Average**")
        st.write(f"${summary['latest_ma50']:,.2f}")
        st.write("**Trend**")
        st.write(summary["trend"])

    with summary_col2:
        st.write("**Best Trading Day**")
        st.write(str(summary["best_day"]))
        st.write("**Best Daily Return**")
        st.write(f"{summary['best_return']:.2f}%")
        st.write("**Worst Trading Day**")
        st.write(str(summary["worst_day"]))
        st.write("**Worst Daily Return**")
        st.write(f"{summary['worst_return']:.2f}%")
        st.write("**Average Daily Return**")
        st.write(f"{summary['average_daily_return']:.4f}%")

    st.markdown("---")
    st.subheader("🖼️ Original Financial Visualizations")

    charts_path = output_paths["charts_directory"]
    chart_files = [
        ("Closing Price", f"{active_ticker}_closing_price.png"),
        ("Trading Volume", f"{active_ticker}_trading_volume.png"),
        ("Moving Averages", f"{active_ticker}_moving_averages.png"),
        ("Daily Returns", f"{active_ticker}_daily_returns.png"),
        ("Return Distribution", f"{active_ticker}_return_distribution.png"),
        ("Rolling Volatility", f"{active_ticker}_rolling_volatility.png"),
        ("Complete Analysis Dashboard", f"{active_ticker}_complete_analysis_dashboard.png")
    ]

    for index in range(0, len(chart_files), 2):
        chart_col1, chart_col2 = st.columns(2)
        for column, chart_info in zip([chart_col1, chart_col2], chart_files[index:index + 2]):
            chart_name, filename = chart_info
            chart_path = Path(charts_path) / filename
            with column:
                if chart_path.exists():
                    st.markdown(f"**{chart_name}**")
                    st.image(str(chart_path), use_container_width=True)

    st.markdown("---")
    st.subheader("📥 Download Analysis Results")

    download_col1, download_col2, download_col3 = st.columns(3)
    with download_col1:
        st.download_button(
            "Download Analysis CSV",
            data=data.to_csv().encode("utf-8"),
            file_name=f"{active_ticker}_analysis_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    with download_col2:
        cleaned_path = output_paths["cleaned_data"]
        if Path(cleaned_path).exists():
            st.download_button(
                "Download Cleaned CSV",
                data=Path(cleaned_path).read_bytes(),
                file_name=f"{active_ticker}_cleaned_data.csv",
                mime="text/csv",
                use_container_width=True
            )

    with download_col3:
        report_path = Path(output_paths["report"])
        if report_path.exists():
            st.download_button(
                "Download Financial Report",
                data=report_path.read_bytes(),
                file_name=f"{active_ticker}_stock_analysis_report.txt",
                mime="text/plain",
                use_container_width=True
            )
else:
    st.info("👈 Enter a stock ticker, select your analysis dates, and click 'Run Stock Analysis' to begin.")

st.markdown("### ✨ Dashboard Features")
feature_col1, feature_col2, feature_col3 = st.columns(3)
feature_col1.markdown("**📊 Financial Analytics**\n\nStock prices, returns, moving averages and volatility.")
feature_col2.markdown("**📈 Interactive Charts**\n\nExplore financial trends with interactive visualizations.")
feature_col3.markdown("**📥 Export Reports**\n\nDownload analytical data and financial reports.")

st.markdown("---")
st.markdown(
    '<div class="disclaimer">⚠️ Educational analysis only. This application does not provide financial advice or investment recommendations.</div>',
    unsafe_allow_html=True
)

st.markdown(
    "<center>Built with Python, Pandas, NumPy, Yahoo Finance and Streamlit</center>",
    unsafe_allow_html=True
)
