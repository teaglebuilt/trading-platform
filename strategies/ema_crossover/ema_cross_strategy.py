from strategy_engine.interfaces import Strategy, Signal, OrderIntent, classify_asset
from strategy_engine.position_sizer import size_to_value_usd


class EmaCross(Strategy):
    """
    EMA crossover strategy that supports:
    - Equities (e.g., AAPL, GLD, IAU) via Alpaca Stocks
    - Crypto (BTCUSD, ETHUSD) via Alpaca Crypto or CCXT
    - Optional TP/SL brackets
    - Risk-based sizing by target USD value
    """
    name = "ema_cross"

    def evaluate(self, sig: Signal) -> list[OrderIntent]:
        asset_type = classify_asset(sig.symbol)
        if asset_type == "crypto":
            venue = "alpaca_crypto"
        else:
            venue = "alpaca_stocks"

        if "qty" in sig.meta:
            qty = float(sig.meta["qty"])
        else:
            target = float(sig.meta.get("target_value_usd", 1000))
            last_price = sig.price or 0.0
            qty = size_to_value_usd(target, last_price) if last_price else 1.0

        tp_pct = float(sig.meta.get("tp_pct", 0))
        sl_pct = float(sig.meta.get("sl_pct", 0))

        short_ema = sig.meta.get("short_ema")
        long_ema = sig.meta.get("long_ema")
        # If both provided, only trade when crossover condition matches direction
        if short_ema and long_ema:
            if sig.side == "buy" and short_ema <= long_ema:
                return []
            if sig.side == "sell" and short_ema >= long_ema:
                return []

        intent = OrderIntent(
            venue=venue,
            symbol=sig.symbol,
            side=sig.side,
            qty=qty,
            type="market",
            price=sig.price,
            tp_pct=tp_pct or None,
            sl_pct=sl_pct or None,
            tag=self.name,
        )

        return [intent]
