from __future__ import annotations

def size_to_value_usd(target_value: float, last_price: float) -> float:
    if last_price <= 0:
        return 0.0
    return round(target_value / last_price, 4)
