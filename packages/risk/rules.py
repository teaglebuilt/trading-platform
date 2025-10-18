from __future__ import annotations
from pydantic import BaseModel
from typing import List, Tuple
from common.models import OrderIntent, Signal

class RiskConfig(BaseModel):
    max_position_value_usd: float = 2000.0        # per symbol
    max_daily_loss_usd: float = 500.0            # daily
    max_orders_per_minute: int = 6
    max_qty_per_order: float = 100.0
    kill_switch: bool = False

DEFAULT_RISK = RiskConfig()

# In real life, load these from Portfolio or a cache:
def get_account_snapshot() -> dict:
    # Replace with call to Portfolio API or broker; this is a stub.
    return {
        "equity_usd": 25000.0,
        "daily_realized_pnl": -120.0,
        "positions": {
            # symbol -> (qty, avg_price)
        }
    }

def est_order_value(intent: OrderIntent, last_price: float | None) -> float:
    p = intent.limit_price or last_price or 0.0
    return abs(p * float(intent.qty))

def apply_all_checks(sig: Signal, intents: List[OrderIntent], last_price: float | None = None,
                     cfg: RiskConfig = DEFAULT_RISK) -> Tuple[List[OrderIntent], list[str]]:
    warnings: list[str] = []
    if cfg.kill_switch:
        return [], ["kill_switch_enabled"]

    snapshot = get_account_snapshot()
    if snapshot["daily_realized_pnl"] <= -cfg.max_daily_loss_usd:
        return [], ["daily_loss_limit_reached"]

    safe: List[OrderIntent] = []
    for it in intents:
        # Cap qty per order
        if it.qty > cfg.max_qty_per_order:
            warnings.append(f"qty_capped:{it.symbol}:{it.qty}->{cfg.max_qty_per_order}")
            it = it.model_copy(update={"qty": cfg.max_qty_per_order})

        # Cap position value (very rough: per order check)
        value = est_order_value(it, last_price)
        if value > cfg.max_position_value_usd:
            # scale down qty to max value
            price = it.limit_price or last_price or 0.0
            new_qty = max(0.0, cfg.max_position_value_usd / price) if price > 0 else 0.0
            if new_qty <= 0.0:
                warnings.append(f"blocked:value_exceeds_cap:{it.symbol}")
                continue
            warnings.append(f"value_scaled:{it.symbol}:{it.qty}->{new_qty:.4f}")
            it = it.model_copy(update={"qty": round(new_qty, 4)})

        safe.append(it)
    return safe, warnings
