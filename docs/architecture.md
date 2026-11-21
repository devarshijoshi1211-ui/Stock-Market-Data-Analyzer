# System Architecture

## 1. Overview

The Stock Market Data Analyzer is a modular Python application that retrieves historical stock market data, validates and cleans the dataset, performs financial analysis, generates visualizations, and produces automated reports.

## 2. Application Workflow

```text
User Input
    |
    v
    Data Fetcher
        |
        v
        Data Cleaner
            |
            v
            Stock Analyzer
                |
                +--------------------+
                |                    |
                v                    v
                Visualization       Report Generator
                    |                    |
                    v                    v
                    Chart Outputs       Text Report
                        |
                        v
                        Saved Project Outputs
```

## 3. Module Responsibilities

### data_fetcher.py
- Retrieves historical data through Yahoo Finance.
- Loads stock data from CSV files.
- Saves downloaded raw data.

### data_cleaner.py
- Standardizes column names.
- Converts dates and numerical values.
- Handles missing and invalid values.
- Removes duplicate records.
- Validates OHLC price relationships and trading volume.

### stock_analyzer.py
- Calculates 20-day moving averages.
- Calculates 50-day moving averages.
- Calculates daily returns.
- Calculates rolling 20-day volatility.
- Produces a financial summary.

### visualization.py
- Creates closing price charts.
- Creates trading volume charts.
- Visualizes moving averages.
- Visualizes daily returns and their distribution.
- Visualizes rolling volatility.
- Generates a combined analysis dashboard.

### report_generator.py
- Generates a structured text report.
- Includes dataset statistics, price analysis, returns, moving averages, and volatility.
- Adds an educational disclaimer.

### main.py
- Coordinates the complete application.
- Accepts user inputs.
- Connects the individual modules.
- Saves the final outputs.

## 4. Data Flow

1. The user supplies a ticker and date range.
2. Historical data is downloaded or loaded from CSV.
3. The cleaner validates and prepares the dataset.
4. The analyzer calculates financial indicators.
5. The visualization module generates charts.
6. The report generator creates a text report.
7. All outputs are saved in the project directories.

## 5. Technologies

- Python: application development
- Pandas: data manipulation
- NumPy: numerical calculations
- yfinance: historical stock data
- Matplotlib: chart generation
- Seaborn: statistical visualization

## 6. Error Handling and Data Validation

The application checks for empty datasets, validates required financial fields, removes invalid dates and duplicate records, and checks price and volume constraints.

If online retrieval fails, the application can use an existing ticker-specific CSV file when available.

## 7. Limitations

- Results depend on the availability and quality of historical market data.
- Historical indicators do not predict future market performance.
- The current version generates static visualizations and text reports.
- The application is an educational analysis tool, not an investment advisory system.
