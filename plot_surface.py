import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import os

os.makedirs("figures", exist_ok=True)

def load_surface_data(path):
    df = pd.read_csv(path)
    df = df.dropna(subset=["iv"])

    df["strike"] = df["strike"].astype(float)
    df["iv"] = df["iv"].astype(float)
    df["spot"] = df["spot"].astype(float)
    df["T"] = df["T"].astype(float)

    df = df[(df["iv"] > 0.05) & (df["iv"] < 4.0)]
    df["moneyness"] = df["strike"] / df["spot"]
    df = df[(df["moneyness"] > 0.7) & (df["moneyness"] < 1.3)]

    return df


def plot_surface(df, ticker):
    strikes = df["strike"].values
    maturities = df["T"].values
    ivs = df["iv"].values

    strike_grid = np.linspace(strikes.min(), strikes.max(), 40)
    maturity_grid = np.linspace(maturities.min(), maturities.max(), 40)
    K, T = np.meshgrid(strike_grid, maturity_grid)

    IV = griddata((strikes, maturities), ivs, (K, T), method="linear")

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(K, T, IV, cmap="viridis", alpha=0.9)

    ax.set_title(f"{ticker} Implied Volatility Surface")
    ax.set_xlabel("Strike")
    ax.set_ylabel("Time to Maturity (Years)")
    ax.set_zlabel("Implied Volatility")

    fig.colorbar(surf, shrink=0.6, aspect=10)
    plt.tight_layout()

    plt.savefig(f"figures/{ticker.lower()}_vol_surface.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    plot_surface(load_surface_data("outputs/SPY_options_snapshot.csv"), "SPY")
    plot_surface(load_surface_data("outputs/META_options_snapshot.csv"), "META")

