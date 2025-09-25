from __future__ import annotations
from typing import List
from strategy_engine.interfaces import EngineAdapter, Signal, OrderIntent, Venue


class BacktraderAdapter(EngineAdapter):
    name = "backtrader"

    async def evaluate(self, sig: Signal) -> List[OrderIntent]:
        # Placeholder: in prod you would run a lightweight rule or call a local component
        # For demo, send 1 share via Alpaca stocks
        venue = getattr(Venue, "ALPACA_STOCKS", "alpaca_stocks")
        return [OrderIntent(venue=venue, symbol=sig.symbol, side=sig.side, qty=1.0)]
