from __future__ import annotations
from typing import List, Tuple
from strategy_engine.interfaces import OrderIntent, Signal
from risk.rules import apply_all_checks


def run_risk(sig: Signal, intents: List[OrderIntent], last_price: float | None = None) -> Tuple[List[OrderIntent], list[str]]:
    return apply_all_checks(sig, intents, last_price=last_price)
