import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("figures", exist_ok=True)

def prepare_df(path, ticker):
    df = pd.read_csv(path)
    df = df.dropna(subset=["iv"])

    df["strike"] = df["strike"].astype(float)
    df["iv"] = df["iv"].astype(float)
    df["spot"] = df["spot"].astype(float)

    # Relax filters for single stocks
    iv_upper = 4.0 if ticker != "SPY" else 3.0
    df = df[(df["iv"] > 0.05) & (df["iv"] < iv_upper)]

    df["moneyness"] = df["strike"] / df["spot"]
    lower, upper = (0.7, 1.3) if ticker != "SPY" else (0.8, 1.2)
    df = df[(df["moneyness"] > lower) & (df["moneyness"] < upper)]

    print(f"{ticker} rows after filters:", len(df))
    return df


def plot_smiles(df, ticker):
    expiries = sorted(df["expiry"].unique())[:3]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for opt_type, ax in zip(["call", "put"], axes):
        plotted = False
        for exp in expiries:
            sub = df[(df["expiry"] == exp) & (df["type"] == opt_type)].sort_values("strike")
            if not sub.empty:
                plotted = True
                ax.plot(sub["strike"], sub["iv"], marker="o", label=exp)

        ax.set_title(f"{ticker} {opt_type.upper()} Smile")
        ax.set_xlabel("Strike")
        ax.set_ylabel("Implied Volatility")
        ax.grid(True)
        if plotted:
            ax.legend()

    plt.tight_layout()
    out_path = f"figures/{ticker.lower()}_smiles.png"
    plt.savefig(out_path, dpi=150)
    plt.show()

    print(f"Saved {out_path}")


if __name__ == "__main__":
    spy = prepare_df("outputs/SPY_options_snapshot.csv", "SPY")
    meta = prepare_df("outputs/META_options_snapshot.csv", "META")

    plot_smiles(spy, "SPY")
    plot_smiles(meta, "META")

