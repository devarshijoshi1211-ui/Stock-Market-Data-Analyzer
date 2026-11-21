import numpy as np
import pandas as pd


def clean_stock_data(data):
    """
    Clean and validate historical stock market data.

    Required columns:
        Open, High, Low, Close, Volume
    """

    if data is None or data.empty:
        raise ValueError("Input stock dataset is empty.")

    df = data.copy()

    # Standardize column names
    df.columns = [
        str(column).strip().title()
        for column in df.columns
    ]

    required_columns = [
        "Open", "High", "Low", "Close", "Volume"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Convert index to datetime
    df.index = pd.to_datetime(
        df.index,
        errors="coerce"
    )

    df.index.name = "Date"

    # Remove invalid dates and duplicate records
    df = df[df.index.notna()]
    df = df[~df.index.duplicated(keep="last")]
    df = df.sort_index()

    # Convert required fields to numeric
    for column in required_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove infinite values
    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    # Remove rows with missing required values
    df = df.dropna(subset=required_columns)

    # Validate prices
    if (df[["Open", "High", "Low", "Close"]] <= 0).any().any():
        raise ValueError("Stock prices must be positive.")

    if (df["Volume"] < 0).any():
        raise ValueError("Trading volume cannot be negative.")

    # Validate OHLC relationships
    invalid_rows = (
        (df["High"] < df["Low"]) |
        (df["High"] < df["Open"]) |
        (df["High"] < df["Close"]) |
        (df["Low"] > df["Open"]) |
        (df["Low"] > df["Close"])
    )

    if invalid_rows.any():
        raise ValueError(
            f"Found {invalid_rows.sum()} invalid OHLC records."
        )

    if df.empty:
        raise ValueError(
            "No valid records remain after cleaning."
        )

    return df


def save_cleaned_data(data, ticker, project_path):
    """
    Save cleaned stock data to processed directory.
    """
    import os

    processed_path = os.path.join(
        project_path,
        "data",
        "processed"
    )

    os.makedirs(processed_path, exist_ok=True)

    file_path = os.path.join(
        processed_path,
        f"{ticker}_cleaned_data.csv"
    )

    data.to_csv(file_path)

    return file_path
