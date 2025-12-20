from __future__ import annotations
from typing import Dict
from strategy_engine.interfaces import Strategy, EngineAdapter
from strategy_engine.strategies.ema_cross import EmaCross
from strategy_engine.strategies.markov_chain import MarkovChainStrategy
from strategy_engine.adapters.freqtrade_adapter import FreqtradeAdapter
from strategy_engine.adapters.jesse_adapter import JesseAdapter
from strategy_engine.adapters.backtrader_adapter import BacktraderAdapter


class _Registry:
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}
        self.adapters: Dict[str, EngineAdapter] = {}


registry = _Registry()

# Register local strategies
registry.strategies["ema_cross"] = EmaCross()
registry.strategies["markov_chain"] = MarkovChainStrategy()

# Register external adapters
registry.adapters["freqtrade"] = FreqtradeAdapter()
registry.adapters["jesse"] = JesseAdapter()
registry.adapters["backtrader"] = BacktraderAdapter()
