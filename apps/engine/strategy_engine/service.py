from __future__ import annotations
from typing import List
from strategy_engine.registry import registry
from strategy_engine.risk_pipeline import run_risk
from strategy_engine.config import CONFIG
from strategy_engine.interfaces import Signal, OrderIntent, classify_asset
from typing_extensions import assert_never


def select_backend(sig: Signal) -> str:
    if sig.strategy in registry.strategies:
        return "local"
    asset = classify_asset(sig.symbol)
    if asset == "crypto":
        return CONFIG.default_crypto_backend
    return CONFIG.default_equity_backend


class StrategyEngineService:
    async def process_signal(self, sig: Signal) -> List[OrderIntent]:
        backend = select_backend(sig)

        if backend == "local":
            strat = registry.strategies.get(sig.strategy)
            intents = strat.evaluate(sig) if strat else []
        elif backend in registry.adapters:
            intents = await registry.adapters[backend].evaluate(sig)
        else:
            assert_never(backend)  # type: ignore

        if CONFIG.enable_risk_pipeline:
            intents, warnings = run_risk(sig, intents)
            if warnings:
                print(f"[risk] Warnings for {sig.symbol}: {warnings}")

        return intents


def cli():
    import asyncio
    from pydantic import BaseModel

    class _Sig(Signal.__class__ if isinstance(Signal, type) else BaseModel):
        pass

    sig = Signal(symbol="AAPL", side="buy", strategy="ema_cross", meta={"qty": 2})
    intents = asyncio.run(StrategyEngineService().process_signal(sig))
    print("[CLI] intents:", [i.model_dump() for i in intents])
