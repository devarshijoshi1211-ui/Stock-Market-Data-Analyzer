import os
import matplotlib.pyplot as plt
import seaborn as sns


def generate_stock_visualizations(data, ticker, project_path):
    """
    Generate stock market analysis charts and dashboard.
    """

    if data is None or data.empty:
        raise ValueError("No data available for visualization.")

    charts_path = os.path.join(
        project_path,
        "outputs",
        "charts"
    )

    os.makedirs(charts_path, exist_ok=True)

    # 1. Closing price
    plt.figure(figsize=(14, 6))
    plt.plot(data.index, data["Close"], linewidth=1.5)
    plt.title(f"{ticker} Historical Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(charts_path, f"{ticker}_closing_price.png"),
        dpi=300
    )
    plt.close()

    # 2. Trading volume
    plt.figure(figsize=(14, 6))
    plt.bar(data.index, data["Volume"], width=1)
    plt.title(f"{ticker} Daily Trading Volume")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(charts_path, f"{ticker}_trading_volume.png"),
        dpi=300
    )
    plt.close()

    # 3. Moving averages
    plt.figure(figsize=(14, 6))
    plt.plot(data.index, data["Close"], label="Close")
    plt.plot(data.index, data["MA20"], label="MA20")
    plt.plot(data.index, data["MA50"], label="MA50")
    plt.title(f"{ticker} Moving Average Analysis")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(charts_path, f"{ticker}_moving_averages.png"),
        dpi=300
    )
    plt.close()

    # 4. Daily returns
    plt.figure(figsize=(14, 6))
    plt.plot(
        data.index,
        data["Daily_Return"] * 100,
        linewidth=1
    )
    plt.axhline(y=0, linestyle="--")
    plt.title(f"{ticker} Daily Returns")
    plt.xlabel("Date")
    plt.ylabel("Return (%)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(charts_path, f"{ticker}_daily_returns.png"),
        dpi=300
    )
    plt.close()

    # 5. Return distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(
        data["Daily_Return"].dropna() * 100,
        bins=30,
        kde=True
    )
    plt.title(f"{ticker} Daily Return Distribution")
    plt.xlabel("Return (%)")
    plt.ylabel("Frequency")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(charts_path, f"{ticker}_return_distribution.png"),
        dpi=300
    )
    plt.close()

    # 6. Rolling volatility
    plt.figure(figsize=(14, 6))
    plt.plot(
        data.index,
        data["Rolling_20D_Volatility"] * 100
    )
    plt.title(f"{ticker} Rolling 20-Day Annualized Volatility")
    plt.xlabel("Date")
    plt.ylabel("Volatility (%)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(charts_path, f"{ticker}_rolling_volatility.png"),
        dpi=300
    )
    plt.close()

    # 7. Combined dashboard
    fig, axes = plt.subplots(3, 2, figsize=(18, 15))

    axes[0, 0].plot(data.index, data["Close"])
    axes[0, 0].set_title("Historical Closing Price")

    axes[0, 1].plot(data.index, data["Close"], label="Close")
    axes[0, 1].plot(data.index, data["MA20"], label="MA20")
    axes[0, 1].plot(data.index, data["MA50"], label="MA50")
    axes[0, 1].set_title("Moving Averages")
    axes[0, 1].legend()

    axes[1, 0].bar(data.index, data["Volume"], width=1)
    axes[1, 0].set_title("Trading Volume")

    axes[1, 1].plot(
        data.index,
        data["Daily_Return"] * 100
    )
    axes[1, 1].axhline(y=0, linestyle="--")
    axes[1, 1].set_title("Daily Returns (%)")

    sns.histplot(
        data["Daily_Return"].dropna() * 100,
        bins=30,
        kde=True,
        ax=axes[2, 0]
    )
    axes[2, 0].set_title("Return Distribution")

    axes[2, 1].plot(
        data.index,
        data["Rolling_20D_Volatility"] * 100
    )
    axes[2, 1].set_title("Rolling Volatility (%)")

    for ax in axes.flat:
        ax.grid(True, alpha=0.3)

    fig.suptitle(
        f"{ticker} Stock Analysis Dashboard",
        fontsize=18,
        fontweight="bold"
    )

    plt.tight_layout(rect=[0, 0, 1, 0.97])

    dashboard_path = os.path.join(
        charts_path,
        f"{ticker}_complete_analysis_dashboard.png"
    )

    plt.savefig(
        dashboard_path,
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    return charts_path
