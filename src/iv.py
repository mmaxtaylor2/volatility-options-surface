import math
from .bs import bs_price

def implied_vol(option_type, price, S, K, T, r, q):
    if price <= 0 or T <= 0:
        return float("nan")

    low, high = 1e-6, 5.0

    for _ in range(100):
        mid = 0.5 * (low + high)
        val = bs_price(option_type, S, K, T, r, q, mid)

        if not math.isfinite(val):
            return float("nan")

        if abs(val - price) < 1e-6:
            return mid

        if val > price:
            high = mid
        else:
            low = mid

    return mid

