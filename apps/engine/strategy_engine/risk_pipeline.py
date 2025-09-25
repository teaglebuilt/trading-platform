from __future__ import annotations
from typing import List, Tuple
from strategy_engine.interfaces import OrderIntent, Signal

# Try to import your real risk checks; fall back to simple checks
try:
    from risk.rules import apply_all_checks  # your package
except Exception:
    def apply_all_checks(account_state: dict, intents: List[OrderIntent]) -> Tuple[List[OrderIntent], list[str]]:
        # Minimal demo: cap qty to 5; block if more than 3 orders in batch
        warnings = []
        safe: List[OrderIntent] = []
        if len(intents) > 3:
            warnings.append("batch_size_exceeded")
            intents = intents[:3]
        for i in intents:
            if i.qty > 5:
                j = i.model_copy(update={"qty": 5})
                warnings.append(f"qty_capped:{i.symbol}")
                safe.append(j)
            else:
                safe.append(i)
        return safe, warnings

def run_risk(sig: Signal, intents: List[OrderIntent]) -> Tuple[List[OrderIntent], list[str]]:
    # TODO: fetch real account/position state from Portfolio
    dummy_state = {"daily_pnl": 0, "max_daily_loss": 1000}
    return apply_all_checks(dummy_state, intents)
