from __future__ import annotations
from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field


class Signal(BaseModel):
    """Normalized incoming trading signal."""
    symbol: str
    side: Literal["buy", "sell"]
    price: Optional[float] = None
    ts: Optional[str] = None
    strategy: str = "unknown"
    meta: Dict[str, Any] = Field(default_factory=dict)


class OrderIntent(BaseModel):
    venue: str = Field(..., description="Execution venue, e.g. 'alpaca_stocks'")
    symbol: str = Field(..., description="Ticker symbol, e.g. 'AAPL'")
    side: str = Field(..., description="'buy' or 'sell'")
    qty: float = Field(..., description="Quantity to trade")
    type: str = Field(..., description="'market' or 'limit'")
    limit_price: Optional[float] = Field(None, description="Limit price if type='limit'")
    tag: Optional[str] = Field(None, description="Strategy or risk tag")

    # 🆕 TP/SL fields
    tp_pct: Optional[float] = Field(
        None,
        description="Optional take-profit percentage (e.g. 0.02 = +2% from entry)",
        ge=0.0,
    )
    sl_pct: Optional[float] = Field(
        None,
        description="Optional stop-loss percentage (e.g. 0.01 = -1% from entry)",
        ge=0.0,
    )

    # Optional: you can also carry the last known signal price
    price: Optional[float] = Field(
        None,
        description="Last known market price at signal time, used for TP/SL calculation",
    )



class Trade(BaseModel):
    """Executed trade information."""
    trade_id: str
    symbol: str
    side: str  # buy or sell
    qty: float
    fill_price: float
    status: str  # new, pending_new, accepted, filled, partially_filled, canceled, etc.
    ts: str


class Position(BaseModel):
    """Open position in a portfolio."""
    symbol: str
    qty: float
    avg_price: float
    unrealized_pnl: Optional[float] = None
