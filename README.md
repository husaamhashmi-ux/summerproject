# Modular Algorithmic Backtesting & Optimization Engine

A production-grade quantitative research framework built on top of the Backtrader ecosystem. This engine enables the rapid prototyping, evaluation, and parallel parameter optimization of systematic trading strategies across multiple asset pipelines.

## Core Architecture Features
* Modular Multi-Strategy Layout: Complete separation of concerns. Trading logic, analytical ingestion, and parallel optimization exist in independent, decoupled modules.
* Dynamic Execution Pipelines: Features an automated string routing engine capable of handling single-asset pipelines (Trend Following / Volatility Breakouts) and dual-asset feeds simultaneously.
* Parallel Grid Optimization: Leverages multi-core processing to evaluate parameter matrices dynamically, tracking performance metrics via industrial-grade risk analyzers.

---

## Implemented Algorithmic Modules

### 1. Trend Following: Triple Moving Average (TMA)
* Logic: Employs structural macro alignment across Three Simple Moving Averages (Short, Medium, Long) to capture programmatic trend expansion.
* Risk Mitigation: Managed via automated trailing stop-losses (2.0%) to systematically preserve capital.

### 2. Volatility Mean Reversion: Bollinger Bands Breakout
* Logic: Exploits historical price distributions by tracking standard deviation volatility bands (+/- 3 standard deviations) around a lookback baseline. 
* Execution: Opens mean-reversion positions at statistical extremes (oversold/overbought) and liquidates positions once price returns to the moving average baseline.

### 3. Statistical Arbitrage: Cointegrated Pairs Trading
* Logic: A market-neutral strategy utilizing Ordinary Least Squares (OLS) regression to dynamically map the hedge ratio and intercept constant between two fundamentally cointegrated corporate assets (e.g., PEP vs. KO).
* Mathematical Framework: Computes a rolling Z-Score tracking spread deviations from historical equilibrium, opening paired long/short tracking legs when the absolute Z-Score is greater than 2.0.

---

## Installation & Getting Started

1. Clone the Repository:
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME

2. Install Dependencies:
   pip install -r requirements.txt

3. Run a Historical Backtest Simulation:
   Adjust your target ticker, timeframe, or algorithm choice directly within the USER CONTROL PANEL inside main.py and run:
   python main.py

4. Execute Parallel Parameter Optimization:
   python optimization.py

---

## Sample Execution Output
Below is an example log demonstrating the engine dynamically identifying spreads, managing trade execution states, and tracking realized net profits:

2023-10-14, BUY EXECUTED, Price: 158.20, Cost: 15820.00, Comm 15.82
2023-10-14, SELL EXECUTED, Price: 57.10, Cost: 5710.00, Comm 5.71
2023-11-02, OPERATION PROFIT, GROSS 412.50, NET 390.97
