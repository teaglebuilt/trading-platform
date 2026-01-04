from __future__ import annotations
from typing import List
from pydantic import BaseModel
import httpx
from strategy_engine.interfaces import EngineAdapter, Signal, OrderIntent, Venue
from strategy_engine.config import CONFIG


class FreqtradeAdapter(EngineAdapter):
    name = "freqtrade"

    async def evaluate(self, sig: Signal) -> List[OrderIntent]:
        """
        Example: call an internal Freqtrade sidecar that exposes a minimal endpoint
        which returns recommended orders for a signal + strategy.
        Replace with your real integration. If no endpoint configured, fall back.
        """
        if CONFIG.freqtrade_base_url:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(
                    f"{CONFIG.freqtrade_base_url}/evaluate",
                    json=sig.model_dump()
                )
                resp.raise_for_status()
                data = resp.json()
                return [OrderIntent(**x) for x in data.get("intents", [])]

        # Fallback demo: 1 market unit on crypto via Alpaca Crypto or CCXT
        venue = Venue.ALPACA_CRYPTO if hasattr(Venue, "ALPACA_CRYPTO") else "alpaca_crypto"
        return [OrderIntent(venue=venue, symbol=sig.symbol, side=sig.side, qty=1.0)]
