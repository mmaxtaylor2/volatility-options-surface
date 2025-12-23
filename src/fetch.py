import yfinance as yf
import pandas as pd
import datetime as dt

def fetch_options(ticker, max_expiries=8):
    t = yf.Ticker(ticker)
    spot = t.history(period="1d")["Close"].iloc[-1]

    rows = []
    now = dt.datetime.now(dt.UTC)

    for exp in t.options[:max_expiries]:
        exp_dt = dt.datetime.strptime(exp, "%Y-%m-%d").replace(tzinfo=dt.UTC)
        T = (exp_dt - now).total_seconds() / (365 * 24 * 3600)
        if T <= 0:
            continue

        chain = t.option_chain(exp)

        for opt_type, df in [("call", chain.calls), ("put", chain.puts)]:
            df = df.copy()
            df["type"] = opt_type
            df["expiry"] = exp
            df["T"] = T
            df["spot"] = spot
            rows.append(df)

    return pd.concat(rows, ignore_index=True)

