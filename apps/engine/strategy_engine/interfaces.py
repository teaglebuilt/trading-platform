from __future__ import annotations
from typing import Protocol, List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

# ---- Try to import workspace models; fall back to light stubs ----
try:
    from common.models import Signal, OrderIntent, Venue
except Exception:
    class Venue(str):
        ALPACA_STOCKS = "alpaca_stocks"
        ALPACA_CRYPTO = "alpaca_crypto"
        ETRADE = "etrade"
        CCXT = "ccxt"

    class Signal(BaseModel):
        symbol: str
        side: Literal["buy", "sell"]
        price: float | None = None
        ts: str | None = None
        strategy: str = "unknown"
        meta: Dict[str, Any] = Field(default_factory=dict)

    class OrderIntent(BaseModel):
        venue: str
        symbol: str
        side: Literal["buy", "sell"]
        qty: float
        type: Literal["market", "limit"] = "market"
        price: float | None = None
        limit_price: float | None = None
        time_in_force: str = "day"
        tp_pct: float | None = None
        sl_pct: float | None = None
        tag: str | None = None

# ---- Strategy / Adapter interfaces ----
class Strategy(Protocol):
    """Local strategy interface (pure-python strategy)."""
    name: str
    def evaluate(self, sig: Signal) -> List[OrderIntent]:
        ...

class EngineAdapter(Protocol):
    """External engine interface (Freqtrade/Jesse/Backtrader)."""
    name: str
    async def evaluate(self, sig: Signal) -> List[OrderIntent]:
        ...

def is_crypto_symbol(symbol: str) -> bool:
    # naive heuristic; adapt to your symbology
    return symbol.endswith("USD") or symbol.upper() in {"BTC", "ETH", "SOL"}


def classify_asset(symbol: str) -> Literal["crypto", "equity"]:
    if symbol.endswith("USD"):
        return "crypto"
    return "equity"
