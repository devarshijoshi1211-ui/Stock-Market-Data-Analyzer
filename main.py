import os

from src.data_fetcher import (
    fetch_stock_data,
    load_stock_csv,
    save_raw_data
)
from src.data_cleaner import (
    clean_stock_data,
    save_cleaned_data
)
from src.stock_analyzer import (
    analyze_stock_data,
    save_analysis_data
)
from src.visualization import generate_stock_visualizations
from src.report_generator import generate_stock_report

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


def run_analysis(ticker, start_date, end_date, csv_path=None, project_path=None):
    """
    Run the complete stock market analysis workflow.
    Provide csv_path to use an existing CSV instead of downloading data from Yahoo Finance.
    """
    project_path = project_path or PROJECT_PATH
    ticker = ticker.strip().upper()

    if not ticker:
        raise ValueError("Please provide a valid stock ticker.")

    print("\n" + "=" * 60)
    print("       STOCK MARKET DATA ANALYZER")
    print("=" * 60)

    # STEP 1: Fetch or load data
    print("\n[1/6] Loading stock market data...")

    if csv_path:
        raw_data = load_stock_csv(csv_path)
        print("Data source: CSV file")
    else: 
        try:
            raw_data = fetch_stock_data(ticker, start_date, end_date)
            if raw_data is None or raw_data.empty:
                raise ValueError("No stock data was downloaded.")
            save_raw_data(raw_data, ticker, project_path)
            print("Data source: Yahoo Finance")
        except Exception as error:
            fallback_path = os.path.join(
                project_path, "data", "raw", f"{ticker}_historical_data.csv"
            )
            if not os.path.exists(fallback_path):
                raise RuntimeError(
                    f"Data download failed and no fallback CSV was found. Original error: {error}"
                ) from error
            print("Download failed. Using existing CSV.")
            print("Reason:", error)
            raw_data = load_stock_csv(fallback_path)

    print("Records loaded:", len(raw_data))

    # STEP 2: Clean data
    print("\n[2/6] Cleaning stock market data...")
    clean_data = clean_stock_data(raw_data)
    if clean_data.empty:
        raise ValueError("No valid records remain after cleaning.")
    save_cleaned_data(clean_data, ticker, project_path)
    print("Cleaned records:", len(clean_data))

    # STEP 3: Analyze data
    print("\n[3/6] Performing financial analysis...")
    analysis_data, summary = analyze_stock_data(clean_data)
    save_analysis_data(analysis_data, ticker, project_path)
    print("Financial indicators calculated successfully.")

    # STEP 4: Generate visualizations
    print("\n[4/6] Generating visualizations...")
    charts_path = generate_stock_visualizations(analysis_data, ticker, project_path)
    print("Charts saved:", charts_path)

    # STEP 5: Generate report
    print("\n[5/6] Generating analytical report...")
    report_path = generate_stock_report(analysis_data, summary, ticker, project_path)
    print("Report saved:", report_path)

    # STEP 6: Display summary
    print("\n[6/6] Analysis completed successfully!")
    print("\n" + "=" * 60)
    print("                 ANALYSIS SUMMARY")
    print("=" * 60)

    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title():35}: {value}")

    output_paths = {
        "cleaned_data": os.path.join(project_path, "data", "processed", f"{ticker}_cleaned_data.csv"),
        "analysis_data": os.path.join(project_path, "data", "processed", f"{ticker}_analysis_data.csv"),
        "charts_directory": charts_path,
        "report": report_path
    }

    print("\n" + "=" * 60)
    print("                 OUTPUT FILES")
    print("=" * 60)

    for name, path in output_paths.items():
        print(f"{name.replace('_', ' ').title():25}: {path}")

    print("\nDISCLAIMER: Educational analysis only. Not financial advice.")
    print("\n" + "=" * 60)
    print("          STOCK ANALYSIS FINISHED")
    print("=" * 60)

    return analysis_data, summary, output_paths


if __name__ == '__main__':
    ticker = input("Enter stock ticker (e.g. AAPL): ").strip()
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()
    run_analysis(ticker, start_date, end_date)
