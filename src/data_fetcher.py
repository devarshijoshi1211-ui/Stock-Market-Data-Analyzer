import os
import pandas as pd
import yfinance as yf


def fetch_stock_data(ticker, start_date, end_date):
  """
  Download historical stock data from Yahoo Finance.

  Parameters:
    ticker (str): Stock ticker symbol.
    start_date (str): Starting date.
    end_date (str): Ending date (exclusive).

  Returns:
    pandas.DataFrame: Historical stock data.
  """

  try:
    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False
    )

    if data.empty:
      raise ValueError(
         f"No stock data found for {ticker}."
      )

    # Handle Yahoo Finance MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
      data.columns = data.columns.get_level_values(0)

    data.index.name = "Date"
    return data

  except Exception as error:
    raise RuntimeError(
      f"Failed to download data for {ticker}: {error}"
    ) from error

def load_stock_csv(file_path):
  """
  Load stock data from a local CSV file
  Supports standard CSV files and Yahoo Finance
  CSV files with two header rows.
  """

  if not os.path.exists(file_path):
    raise FileNotFoundError(
      f"CSV file not found: {file_path}"
    )

  # First attempt: standard CSV
  data = pd.read_csv(file_path)

  if "Date" not in data.columns:
    data = pd.read_csv(
      file_path,
      header=[0, 1],
      index_col=0
    )

    data = data[data.index != "Date"]
    data.columns = data.columns.get_level_values(0)
    data.index.name = "Date"
    data = data.reset_index()

  if "Date" not in data.columns:
    raise ValueError(
      "CSV must contain a Date column."
    )

  data["Date"] = pd.to_datetime(
      data["Date"],
      errors="coerce"
  )

  data = data.dropna(subset=["Date"])
  data = data.set_index("Date")
  data.index.name = "Date"

  return data


def save_raw_data(data, ticker, project_path):
  """
  Save downloaded data in the raw data directory.
  """
  raw_path = os.path.join(project_path, "data", "raw")
  os.makedirs(raw_path, exist_ok=True)

  file_path = os.path.join(
      raw_path,
      f"{ticker}_historical_data.csv"
  )

  data.to_csv(file_path)
  return file_path
