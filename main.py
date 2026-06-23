import backtrader as bt
import yfinance as yf
import pandas as pd
from strategies.tma import TripleMovingAverageStrategy
from strategies.bollinger import BollingerBandsStrategy

def load_data(ticker_symbol, start_date, end_date):
    """Downloads trading data from yfinance and formats it for Backtrader."""
    print(f"Downloading historical data for {ticker_symbol}...")
    df = yf.download(
        ticker_symbol,
        start=start_date,
        end=end_date,
        auto_adjust=False
    )

    # Clean multi-index columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Fallback to standard Close if Adj Close is missing
    if 'Adj Close' in df.columns and not df['Adj Close'].isnull().all():
        df['Adj Close'] = df['Adj Close'].fillna(df['Close'])
        close_column = 'Adj Close'
    else:
        close_column = 'Close'

    # Reorder columns explicitly
    df = df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

    # Pass DataFrame directly into Backtrader PandasData feed
    data = bt.feeds.PandasData(
        dataname=df,
        datetime=None, 
        open='Open',
        high='High',
        low='Low',
        close=close_column,
        volume='Volume',
        openinterest=-1
    )
    return data

def run_backtest():
    # ==========================================
    # USER CONTROL PANEL (Change settings here!)
    # ==========================================
    STRATEGY_CHOICE     = "BOLLINGER"  # Options: "TMA" or "BOLLINGER"
    TICKER_SYMBOL       = "AAPL"       # Any Yahoo Finance ticker symbol (e.g., NVDA, TSLA, MSFT)
    START_DATE          = "2015-01-01" # Start of simulation time machine
    END_DATE            = "2024-01-01" # End of simulation time machine
    INITIAL_CASH        = 100000.0     # Virtual starting balance (£/$/€)
    COMMISSION_RATE     = 0.001        # 0.1% broker transaction fee per trade
    SLIPPAGE_PERCENT    = 0.0005       # 0.05% price execution slippage protection
    STAKE_SIZE          = 100          # Number of stock shares traded per signal
    # ==========================================

    # Initialize the core simulation engine
    cerebro = bt.Cerebro()

    # 1. Pull data and load it into the engine
    market_data = load_data(TICKER_SYMBOL, START_DATE, END_DATE)
    cerebro.adddata(market_data)

    # 2. Route the user's strategy choice dynamically
    if STRATEGY_CHOICE.upper() == "TMA":
        print("Initializing Strategy: Triple Moving Average...")
        cerebro.addstrategy(TripleMovingAverageStrategy)
    elif STRATEGY_CHOICE.upper() == "BOLLINGER":
        print("Initializing Strategy: Bollinger Bands Volatility Breakout...")
        cerebro.addstrategy(BollingerBandsStrategy)
    else:
        raise ValueError(f"Invalid strategy choice: '{STRATEGY_CHOICE}'. Please choose 'TMA' or 'BOLLINGER'.")

    # 3. Configure the Virtual Broker Settings
    cerebro.broker.setcash(INITIAL_CASH)
    cerebro.broker.setcommission(commission=COMMISSION_RATE)
    cerebro.broker.set_slippage_perc(SLIPPAGE_PERCENT)
    
    # Set execution asset size management
    cerebro.addsizer(bt.sizers.FixedSize, stake=STAKE_SIZE)

    # 4. Run the time-machine simulation
    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    cerebro.run()
    print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")

if __name__ == "__main__":
    run_backtest()
