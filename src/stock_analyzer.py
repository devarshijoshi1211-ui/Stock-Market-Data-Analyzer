import numpy as np
import pandas as pd


def analyze_stock_data(data):
    """
    Calculate stock market indicators and statistics.

    Returns:
        analysis_data: DataFrame with calculated indicators.
        summary: Dictionary containing analysis results.
    """
    if data is None or data.empty:
        raise ValueError("Stock dataset is empty.")

    df = data.copy()
    required_columns = ["Close", "High", "Low", "Open", "Volume"]
    missing = [column for column in required_columns if column not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Moving averages
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()

    # Daily percentage returns
    df["Daily_Return"] = df["Close"].pct_change()

    # Rolling 20-day annualized volatility
    df["Rolling_20D_Volatility"] = (
        df["Daily_Return"].rolling(window=20).std() * np.sqrt(252)
    )

    returns = df["Daily_Return"].dropna()
    if returns.empty:
        raise ValueError("Insufficient data to calculate returns.")

    # Calculate summary statistics
    best_day = returns.idxmax()
    worst_day = returns.idxmin()
    cumulative_return = ((1 + returns).prod() - 1) * 100
    daily_volatility = returns.std()

    latest_ma20 = df["MA20"].iloc[-1]
    latest_ma50 = df["MA50"].iloc[-1]

    if pd.isna(latest_ma20) or pd.isna(latest_ma50):
        trend = "Insufficient data for moving-average comparison"
    elif latest_ma20 > latest_ma50:
        trend = "Positive moving-average relationship"
    elif latest_ma20 < latest_ma50:
        trend = "Negative moving-average relationship"
    else:
        trend = "Neutral moving-average relationship"

    summary = {
        "total_records": len(df),
        "start_date": df.index.min(),
        "end_date": df.index.max(),
        "latest_close": df["Close"].iloc[-1],
        "highest_close": df["Close"].max(),
        "lowest_close": df["Close"].min(),
        "average_close": df["Close"].mean(),
        "average_volume": df["Volume"].mean(),
        "latest_ma20": latest_ma20,
        "latest_ma50": latest_ma50,
        "trend": trend,
        "average_daily_return": returns.mean() * 100,
        "best_day": best_day,
        "best_return": returns.max() * 100,
        "worst_day": worst_day,
        "worst_return": returns.min() * 100,
        "cumulative_return": cumulative_return,
        "daily_volatility": daily_volatility * 100,
        "annualized_volatility": daily_volatility * np.sqrt(252) * 100,
    }

    return df, summary


def save_analysis_data(data, ticker, project_path):
    """
    Save the complete analytical dataset.
    """
    import os

    processed_path = os.path.join(project_path, "data", "processed")
    os.makedirs(processed_path, exist_ok=True)
    file_path = os.path.join(processed_path, f"{ticker}_analysis_data.csv")
    data.to_csv(file_path)
    return file_path
