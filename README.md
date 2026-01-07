## Volatility & Options Surface Builder

A Python-based project for constructing and visualizing implied volatility surfaces using live equity options data. The project replicates core analytical workflows used on derivatives desks and in quant-adjacent research roles to study volatility smile, skew, term structure, and earnings-driven risk premia.

The analysis compares an index ETF (SPY) with a single equity (META) to highlight structural differences between diversified market risk and idiosyncratic, event-driven volatility.

## Problem Context

Implied volatility contains forward-looking information about market expectations, risk asymmetry, and event uncertainty, but raw options data is noisy and difficult to interpret without proper structuring. This project was built to transform raw option chains into interpretable volatility smiles, term structures, and surfaces, allowing for systematic comparison across assets and maturities.

## Key Concepts Demonstrated

- Implied volatility smiles and skew  
- Call vs put asymmetry  
- At-the-money volatility term structure  
- Three-dimensional volatility surface construction  
- Live options data ingestion  
- Black–Scholes Greeks  

## Methodology Notes

- Option chains sourced from Yahoo Finance  
- Mid prices constructed using bid–ask midpoint (fallback to last price when necessary)  
- Implied volatility taken from exchange-provided IV for robustness  
- Black–Scholes Greeks computed analytically  
- Light filtering applied to remove illiquid and arbitrage-violating quotes  
- Volatility surfaces interpolated using linear grid interpolation  

## Key Takeaways

- Index volatility surfaces are smoother and primarily macro-driven  
- Single-stock options embed significant idiosyncratic and earnings-related risk  
- Volatility surfaces jointly capture smile, skew, and term structure effects  
- Careful filtering is required before raw option data can be used for surface construction  

## Possible Extensions

- Historical volatility surface evolution  
- Calendar and diagonal spread analysis  
- No-arbitrage smoothing constraints  
- Alternative volatility models (e.g., SABR, local volatility)  
- Explicit earnings event tagging  

## Visual Outputs

### Volatility Smiles (Calls vs Puts)

#### SPY
![SPY Smiles](figures/spy_smiles.png)

- Mild downside skew  
- Relatively flat smile  
- Reflects diversified index risk  

#### META
![META Smiles](figures/meta_smiles.png)

- Steeper downside skew  
- Higher front-end implied volatility  
- Reflects idiosyncratic and earnings-related risk  

### At-the-Money Implied Volatility Term Structure

![ATM Term Structure](figures/atm_term_structure.png)

- SPY exhibits a smooth, macro-driven term structure  
- META shows an elevated front-end volatility hump driven by earnings uncertainty  

### Three-Dimensional Implied Volatility Surfaces

#### SPY Surface
![SPY Surface](figures/spy_vol_surface.png)

- Smooth surface  
- Mild curvature across strikes and maturities  

#### META Surface
![META Surface](figures/meta_vol_surface.png)

- Strong downside skew  
- Elevated short-dated volatility  
- Clear earnings-driven structure  

## Scope Note

This project is intended for analytical demonstration and portfolio use and is not a live trading or investment system.
