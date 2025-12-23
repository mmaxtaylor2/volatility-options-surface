import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("figures", exist_ok=True)

def load_and_prepare(path):
    df = pd.read_csv(path)
    df = df.dropna(subset=["iv"])

    df["strike"] = df["strike"].astype(float)
    df["iv"] = df["iv"].astype(float)
    df["spot"] = df["spot"].astype(float)
    df["T"] = df["T"].astype(float)

    df = df[(df["iv"] > 0.05) & (df["iv"] < 4.0)]
    df["moneyness"] = df["strike"] / df["spot"]

    return df


def atm_term_structure(df):
    rows = []

    for exp in sorted(df["expiry"].unique()):
        sub = df[df["expiry"] == exp].copy()
        sub["atm_dist"] = (sub["moneyness"] - 1.0).abs()

        atm = sub.nsmallest(4, "atm_dist")
        if atm.empty:
            continue

        rows.append({
            "T": atm["T"].mean(),
            "iv": atm["iv"].mean()
        })

    return pd.DataFrame(rows).sort_values("T")


if __name__ == "__main__":
    spy = load_and_prepare("outputs/SPY_options_snapshot.csv")
    meta = load_and_prepare("outputs/META_options_snapshot.csv")

    spy_ts = atm_term_structure(spy)
    meta_ts = atm_term_structure(meta)

    plt.figure(figsize=(10, 6))
    plt.plot(spy_ts["T"], spy_ts["iv"], marker="o", label="SPY ATM IV")
    plt.plot(meta_ts["T"], meta_ts["iv"], marker="o", label="META ATM IV")

    plt.title("ATM Implied Volatility Term Structure")
    plt.xlabel("Time to Maturity (Years)")
    plt.ylabel("Implied Volatility")
    plt.legend()
    plt.grid(True)

    plt.savefig("figures/atm_term_structure.png", dpi=150)
    plt.show()

