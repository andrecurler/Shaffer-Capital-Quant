import yfinance as yf
import pandas as pd
import numpy as np

# Parameters
train_start, train_end = '2024-07-01', '2025-05-31'
test_start, test_end = '2025-06-01', '2025-07-29'
mom_pct = 0.2

# Utility: Download tickers/remove timeouts, plus FMP fundamentals (as before)
# ... reuse prior code to get `close_prices`, `momentum_tickers`, fetch FMP data, and filter final_longs

# Function to run a backtest on a given date range
def run_backtest(longs, start, end, benchmark_ticker='SPY'):
    prices = close_prices[longs].loc[start:end].dropna(how='any')
    bench = yf.download(benchmark_ticker, start=start, end=end, auto_adjust=True)['Close'].pct_change().loc[prices.index]
    daily_ret = prices.pct_change().dropna()
    vol21 = daily_ret.rolling(21).std()

    rebal = prices.resample('ME').first().index
    rebal = [d for d in rebal if d in prices.index]

    port_ret = pd.Series(index=daily_ret.index)
    for i in range(len(rebal)-1):
        s, e = rebal[i], rebal[i+1]
        w_window = daily_ret.loc[s:e]
        vs = vol21.loc[s].dropna()
        vs = vs[vs.index.isin(w_window.columns)]
        w = 1/vs; w /= w.sum()
        wpr = prices[w.index].loc[:s].ffill().rolling(30).max().iloc[-1]
        dd = prices.loc[s, w.index]/wpr - 1
        valid = dd[dd > -0.25].index
        w = w[w.index.isin(valid)]; w /= w.sum()
        if not w.empty:
            port_ret.loc[w_window.index] = (w_window[w.index] * w).sum(axis=1)

    port_ret = port_ret.dropna()
    cum = (1+port_ret).cumprod()
    
    metrics = {
        'CAGR': cum.iloc[-1]**(252/len(port_ret)) - 1,
        'Vol': port_ret.std()*np.sqrt(252),
        'Sharpe': (cum.iloc[-1]**(252/len(port_ret)) - 1) / (port_ret.std()*np.sqrt(252))
    }
    return cum, bench, metrics, port_ret, prices

# Train backtest
cum_train, bench_train, m_train, ret_train, _ = run_backtest(final_longs, train_start, train_end)
# Test backtest
cum_test, bench_test, m_test, ret_test, prices_test = run_backtest(final_longs, test_start, test_end)

# Attribution: contributions per ticker in test period
port_weights = ret_test.divide(ret_test, axis=0)
contr = port_weights.mul(prices_test.pct_change().loc[ret_test.index]).sum()
contr = contr.sort_values(ascending=False)

# GICS sector lookup
sectors = {sym: yf.Ticker(sym).info.get('sector', 'Unknown') for sym in final_longs}
sector_contr = contr.reset_index().rename(columns={'index':'symbol', 0:'contribution'})
sector_contr['sector'] = sector_contr['symbol'].map(sectors)
sector_summary = sector_contr.groupby('sector')['contribution'].sum().sort_values(ascending=False)

# Save results
pd.DataFrame.from_dict(m_train, orient='index', columns=['train']).to_csv('metrics_train.csv')
pd.DataFrame.from_dict(m_test, orient='index', columns=['test']).to_csv('metrics_test.csv')
sector_summary.to_csv('sector_contributions.csv')
contr.head(10).to_csv('top_contributors.csv')
