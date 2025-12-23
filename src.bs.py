import math

SQRT_2PI = math.sqrt(2.0 * math.pi)

def norm_pdf(x):
    return math.exp(-0.5 * x * x) / SQRT_2PI

def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def d1_d2(S, K, T, r, q, sigma):
    if T <= 0 or sigma <= 0:
        return None, None
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return d1, d2

def bs_price(option_type, S, K, T, r, q, sigma):
    d1, d2 = d1_d2(S, K, T, r, q, sigma)
    if d1 is None:
        return float("nan")

    if option_type == "call":
        return math.exp(-q*T)*S*norm_cdf(d1) - math.exp(-r*T)*K*norm_cdf(d2)
    else:
        return math.exp(-r*T)*K*norm_cdf(-d2) - math.exp(-q*T)*S*norm_cdf(-d1)

def bs_greeks(option_type, S, K, T, r, q, sigma):
    d1, d2 = d1_d2(S, K, T, r, q, sigma)
    if d1 is None:
        return (None, None, None, None)

    pdf = norm_pdf(d1)

    if option_type == "call":
        delta = math.exp(-q*T) * norm_cdf(d1)
    else:
        delta = math.exp(-q*T) * (norm_cdf(d1) - 1)

    gamma = math.exp(-q*T) * pdf / (S * sigma * math.sqrt(T))
    vega = S * math.exp(-q*T) * pdf * math.sqrt(T)

    theta = -S * pdf * sigma * math.exp(-q*T) / (2 * math.sqrt(T))

    return delta, gamma, vega, theta

