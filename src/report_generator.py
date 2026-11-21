import os
from datetime import datetime


def generate_stock_report(data, summary, ticker, project_path):
    """
    Generate a text report containing stock price, moving-average,
    returns, and volatility analysis.
    """
    if data is None or data.empty:
        raise ValueError("No data available to generate the report.")

    reports_path = os.path.join(project_path, "reports")
    os.makedirs(reports_path, exist_ok=True)

    def get_value(key, default="N/A"):
        value = summary.get(key, default)
        if value is None:
            return default
        return value

    def format_number(key, decimals=2, suffix=""):
        value = get_value(key)
        try:
            return f"{float(value):,.{decimals}f}{suffix}"
        except (TypeError, ValueError):
            return str(value)

    report = f"""
============================================================
              STOCK MARKET DATA ANALYSIS REPORT
============================================================

Stock Ticker: {ticker}
Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

------------------------------------------------------------
1. DATASET OVERVIEW
------------------------------------------------------------

Total Records: {get_value("total_records")}
Start Date: {get_value("start_date")}
End Date: {get_value("end_date")}

------------------------------------------------------------
2. PRICE ANALYSIS
------------------------------------------------------------

Latest Closing Price: ${format_number("latest_close")}
Highest Closing Price: ${format_number("highest_close")}
Lowest Closing Price: ${format_number("lowest_close")}
Average Closing Price: ${format_number("average_close")}
Average Trading Volume: {format_number("average_volume", 0)}

------------------------------------------------------------
3. MOVING AVERAGE ANALYSIS
------------------------------------------------------------

Latest MA20: ${format_number("latest_ma20")}
Latest MA50: ${format_number("latest_ma50")}
Moving Average Relationship: {get_value("trend")}

------------------------------------------------------------
4. DAILY RETURNS ANALYSIS
------------------------------------------------------------

Average Daily Return: {format_number("average_daily_return", 4, "%")}
Best Trading Day: {get_value("best_day")}
Best Daily Return: {format_number("best_return", 4, "%")}
Worst Trading Day: {get_value("worst_day")}
Worst Daily Return: {format_number("worst_return", 4, "%")}
Cumulative Return: {format_number("cumulative_return", 2, "%")}

------------------------------------------------------------
5. VOLATILITY ANALYSIS
------------------------------------------------------------

Daily Volatility: {format_number("daily_volatility", 4, "%")}
Annualized Historical Volatility: {format_number("annualized_volatility", 2, "%")}

------------------------------------------------------------
6. ANALYTICAL SUMMARY
------------------------------------------------------------

The analysis covers {get_value("total_records")} trading records
for {ticker} between {get_value("start_date")} and
{get_value("end_date")}.

The moving-average relationship is:
{get_value("trend")}

The calculated cumulative return is
{format_number("cumulative_return", 2, "%")}.

Annualized historical volatility is
{format_number("annualized_volatility", 2, "%")}.

These measurements describe historical market behaviour.
They should not be treated as predictions of future performance.

------------------------------------------------------------
7. DISCLAIMER
------------------------------------------------------------

This report is for educational and informational purposes only.
It does not constitute investment, financial, or trading advice.

Historical performance does not guarantee future results.
Always conduct independent research before making financial
decisions.

============================================================
                            END OF REPORT
============================================================
"""

    report_file = os.path.join(
        reports_path,
        f"{ticker}_stock_analysis_report.txt"
    )

    with open(report_file, "w", encoding="utf-8") as file:
        file.write(report.strip() + "\n")

    return report_file
