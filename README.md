# Shaffer Capital Quant Strategy Automation

This repo automates a weekly long-only quantitative backtest using Google Colab, Financial Modeling Prep API, and Google Drive — with results delivered to Gmail and logged to Google Sheets.

## 🔧 Tech Stack
- Python (Google Colab)
- yFinance, pandas, matplotlib
- FinancialModelingPrep (FMP) API
- Google Apps Script (Gmail + Drive + Sheets)
- Google Drive for chart & data storage

## 📊 Strategy Overview
- Long entry model combining:
  - Momentum (6-month lookback)
  - Quality (ROIC, margins via FMP)
  - Moat (industry filters)
- Backtest includes:
  - Monthly rebalancing
  - Rolling drawdown check
  - SPY benchmark comparison

## 📁 Folder Structure
- 📂 `Shaffer Capital Quant` (Google Drive)
  - `latest_metrics.csv`
  - `top_50_contributors.csv`
  - `top_10_contributors.csv`
  - `performance_chart.png`

## 📝 Outputs
- 📧 Gmail weekly digest:
  - Metrics (CAGR, Volatility, Sharpe)
  - Top 10 contributors
  - Chart (PNG attachment)
- 📄 Google Sheet log:
  - Top 10 and Top 50 contributors with timestamps

## 🚀 Getting Started

### 1. Clone this Repo and Set Up Colab
- Open the [Google Colab notebook](https://colab.research.google.com/drive/1a41mjk-TBiYeQ32s5QKcd4zwqe8JLZcy)
- Run once to generate outputs in Drive folder

### 2. Create Google Drive Folder
- Name it `Shaffer Capital Quant`
- Share with your Gmail if using another account

### 3. Set Up Google Apps Script
- Open [Google Apps Script](https://script.google.com)
- Paste in the `runColabReminder` script
- Replace:
  - `driveFolderId` with your folder ID
  - `sheetId` with your Google Sheet ID

### 4. Authorize and Run
- Click ▶️ Run manually once
- Approve Drive and Gmail permissions
- Set up time-based trigger (weekly)

## 📆 Trigger Schedule
- Time-driven: Weekly (e.g., every Monday)
- Function: `runColabReminder`

## 📌 Notes
- Make sure `performance_chart.png` and CSVs are refreshed in Colab before trigger runs.
- Sheet will log top contributors on each run.
- Drive is used as both a data cache and report repository.

---

## 🤝 Contributing
Feel free to fork, extend, or plug in alternate data providers (e.g., Alpha Vantage, Tiingo).

## 🧠 Credits
Inspired by execution excellence principles (Freeman-Shor) and moat-based investing (TCI, Yacktman, Ensemble Capital).
