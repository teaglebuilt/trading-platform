from __future__ import annotations
from typing import List
import httpx
from strategy_engine.interfaces import EngineAdapter, Signal, OrderIntent, Venue
from strategy_engine.config import CONFIG


class JesseAdapter(EngineAdapter):
    name = "jesse"

    async def evaluate(self, sig: Signal) -> List[OrderIntent]:
        if CONFIG.jesse_base_url:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(
                    f"{CONFIG.jesse_base_url}/evaluate",
                    json=sig.model_dump()
                )
                resp.raise_for_status()
                data = resp.json()
                return [OrderIntent(**x) for x in data.get("intents", [])]

        venue = getattr(Venue, "ALPACA_CRYPTO", "alpaca_crypto")
        return [OrderIntent(venue=venue, symbol=sig.symbol, side=sig.side, qty=1.0)]
