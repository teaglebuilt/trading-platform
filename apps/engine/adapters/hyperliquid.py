from strategy_engine.interfaces import EngineAdapter, Signal, OrderIntent, List


class HyperliquidAdapter(EngineAdapter):
    name = "hyperliquid"

    async def evaluate(self, sig: Signal) -> List[OrderIntent]:
        return []
