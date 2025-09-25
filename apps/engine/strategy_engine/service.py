from __future__ import annotations
from typing import List
from typing_extensions import assert_never
from strategy_engine.interfaces import Signal, OrderIntent, is_crypto_symbol
from strategy_engine.registry import registry
from strategy_engine.config import CONFIG
from strategy_engine.risk_pipeline import run_risk

def select_backend(sig: Signal) -> str:
    # If a strategy name is provided and registered locally, prefer local
    if sig.strategy in registry.strategies:
        return "local"

    # Otherwise choose by asset class
    if is_crypto_symbol(sig.symbol):
        return CONFIG.default_crypto_backend
    return CONFIG.default_equity_backend

class StrategyEngineService:
    async def process_signal(self, sig: Signal) -> List[OrderIntent]:
        backend = select_backend(sig)

        if backend == "local":
            # Use registered local strategy if present; else fallback to a minimal intent
            strat = registry.strategies.get(sig.strategy)
            if strat:
                intents = strat.evaluate(sig)
            else:
                # minimal fallback
                venue = "alpaca_stocks" if not is_crypto_symbol(sig.symbol) else "alpaca_crypto"
                intents = [OrderIntent(venue=venue, symbol=sig.symbol, side=sig.side, qty=1.0)]
        elif backend == "freqtrade":
            intents = await registry.adapters["freqtrade"].evaluate(sig)
        elif backend == "jesse":
            intents = await registry.adapters["jesse"].evaluate(sig)
        elif backend == "backtrader":
            intents = await registry.adapters["backtrader"].evaluate(sig)
        else:
            assert_never(backend)  # type: ignore

        if CONFIG.enable_risk_pipeline:
            intents, warnings = run_risk(sig, intents)
            # You can log/emit warnings here

        return intents

def cli():
    import asyncio
    from pydantic import BaseModel
    class _Sig(Signal.__class__ if isinstance(Signal, type) else BaseModel):
        pass
    sig = Signal(symbol="AAPL", side="buy", strategy="ema_cross", meta={"qty": 2})
    intents = asyncio.run(StrategyEngineService().process_signal(sig))
    print("[CLI] intents:", [i.model_dump() for i in intents])
