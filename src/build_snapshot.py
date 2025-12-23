print(">>> build_snapshot.py LOADED <<<")

import os
import pandas as pd

from .fetch import fetch_options
from .bs import bs_greeks

def mid_price(bid, ask, last):
    try:
        bid = float(bid)
        ask = float(ask)
        last = float(last)
    except Exception:
        return None

    if bid > 0 and ask > 0:
        return 0.5 * (bid + ask)
    if last > 0:
        return last
    return None

def build(ticker):
    df = fetch_options(ticker)

    df["mid"] = df.apply(
        lambda r: mid_price(r.bid, r.ask, r.lastPrice),
        axis=1
    )

    df = df.dropna(subset=["mid"])

    # ✅ USE YAHOO IMPLIED VOL (robust, realistic)
    df["iv"] = pd.to_numeric(df["impliedVolatility"], errors="coerce")

    df["delta"] = pd.NA
    df["gamma"] = pd.NA
    df["vega"] = pd.NA
    df["theta"] = pd.NA

    for idx, r in df.iterrows():
        try:
            d, g, v, th = bs_greeks(
                r.type,
                float(r.spot),
                float(r.strike),
                float(r.T),
                0.05,
                0.0,
                float(r.iv)
            )
        except Exception:
            continue

        df.at[idx, "delta"] = d
        df.at[idx, "gamma"] = g
        df.at[idx, "vega"] = v
        df.at[idx, "theta"] = th

    return df

if __name__ == "__main__":
    print(">>> MAIN BLOCK STARTED <<<")
    os.makedirs("outputs", exist_ok=True)

    for ticker in ["META", "SPY"]:
        out = build(ticker)
        out.to_csv(f"outputs/{ticker}_options_snapshot.csv", index=False)
        print(f"Wrote {ticker}")

