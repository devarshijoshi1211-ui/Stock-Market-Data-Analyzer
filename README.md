# Stock Market Data Analyzer

A Python-based stock market analysis application that retrieves historical stock data, cleans and analyzes financial datasets, calculates technical indicators, measures returns and volatility, and generates automated reports and visualizations.

## Project Overview

The Stock Market Data Analyzer is designed to demonstrate practical Python programming, data analysis, financial data processing, and visualization skills.

It uses Yahoo Finance data through `yfinance` and also supports loading historical stock data from CSV files.

## Features

- Historical stock data retrieval using Yahoo Finance
- CSV-based data loading and fallback
- Data cleaning and validation
- Exploratory data analysis
- 20-day and 50-day moving averages
- Daily percentage returns
- Cumulative return calculation
- Rolling 20-day volatility
- Annualized historical volatility
- Automated financial analysis reports
- Seven analytical visualizations, including a comprehensive dashboard
- Modular and reusable Python architecture

## Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- yfinance
- Google Colab

## Project Structure

```text
Stock-Market-Data-Analyzer/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py
│   ├── data_cleaner.py
│   ├── stock_analyzer.py
│   ├── visualization.py
│   └── report_generator.py
│
├── outputs/
│   ├── charts/
│   └── csv/
│
├── images/
├── reports/
├── docs/
│   └── architecture.md
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Stock-Market-Data-Analyzer.git
cd Stock-Market-Data-Analyzer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

Enter the requested information:

```text
Enter stock ticker (e.g. AAPL): AAPL
Enter start date (YYYY-MM-DD): 2025-01-01
Enter end date (YYYY-MM-DD): 2026-01-01
```

The application downloads historical data, processes it, calculates financial indicators, creates visualizations, and generates a text report.

### CSV Input

The application also supports CSV input through the `run_analysis()` function:

```python
from main import run_analysis

analysis_data, summary, output_paths = run_analysis(
    ticker="AAPL",
    start_date="2025-01-01",
    end_date="2026-01-01",
    csv_path="data/raw/AAPL_historical_data.csv"
)
```

## Sample Analysis

The initial demonstration analyzed Apple Inc. (`AAPL`) historical data for 2025.

| Metric | Demonstration Result |
|---|---:|
| Trading records | 250 |
| Latest closing price | $270.92 |
| Highest closing price | $285.20 |
| Lowest closing price | $171.24 |
| Average closing price | $230.98 |
| Average daily return | 0.0661% |
| Cumulative return | 11.99% |
| Annualized historical volatility | 32.46% |

These values are historical results from the demonstration dataset, not current market prices or forecasts.

## Generated Outputs

### Processed Data
- Cleaned historical stock data
- Moving-average and returns analysis data

### Visualizations
- Closing price chart
- Trading volume chart
- Moving averages chart
- Daily returns chart
- Return distribution chart
- Rolling volatility chart
- Complete analysis dashboard

### Reports
- Automated stock analysis report in TXT format

## Financial Disclaimer

This project is intended for educational and informational purposes only. It does not provide investment recommendations or financial advice.

Historical performance does not guarantee future results. Always conduct independent research before making financial decisions.

## Future Improvements

- Interactive Streamlit dashboard
- Multi-stock comparison
- Interactive Plotly charts
- Additional technical indicators
- Automated PDF reports
- Portfolio performance analysis

## Author

Developed as a Python and financial data analysis project.
