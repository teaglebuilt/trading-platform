from collections import defaultdict, deque
from strategy_engine.interfaces import Strategy, Signal, OrderIntent, classify_asset
from strategy_engine.position_sizer import size_to_value_usd


class MarkovChainStrategy(Strategy):
    """
    Simple 2-state Markov Chain strategy:
    - Builds transition probabilities of price direction (Up/Down)
    - Buys when P(U→U) > threshold (continuation up)
    - Sells when P(D→D) > threshold (continuation down)
    """
    name = "markov_chain"

    def __init__(self, window: int = 50, threshold: float = 0.6):
        self.window = window
        self.threshold = threshold
        self.history = deque(maxlen=window)
        self.transitions = defaultdict(lambda: {"U": 0, "D": 0})

    def _update_chain(self, new_state: str):
        if not self.history:
            self.history.append(new_state)
            return
        prev_state = self.history[-1]
        self.transitions[prev_state][new_state] += 1
        self.history.append(new_state)

    def _get_transition_prob(self):
        probs = {}
        for s, counts in self.transitions.items():
            total = counts["U"] + counts["D"]
            if total == 0:
                continue
            probs[s] = {k: v / total for k, v in counts.items()}
        return probs

    def evaluate(self, sig: Signal) -> list[OrderIntent]:
        price = sig.price
        meta = sig.meta or {}

        # Determine state based on last two closes
        prev_price = meta.get("prev_price")
        if not prev_price:
            return []

        new_state = "U" if price > prev_price else "D"
        self._update_chain(new_state)
        probs = self._get_transition_prob()

        last_state = self.history[-2] if len(self.history) > 1 else None
        if not last_state or last_state not in probs:
            return []

        next_prob = probs[last_state]
        asset_type = classify_asset(sig.symbol)
        venue = "alpaca_crypto" if asset_type == "crypto" else "alpaca_stocks"

        qty = (
            float(meta["qty"])
            if "qty" in meta
            else size_to_value_usd(float(meta.get("target_value_usd", 1000)), price)
        )

        intents = []
        # Uptrend continuation
        if new_state == "U" and next_prob["U"] > self.threshold:
            intents.append(OrderIntent(
                venue=venue, symbol=sig.symbol, side="buy", qty=qty,
                type="market", price=price, tag=self.name
            ))
        # Downtrend continuation
        elif new_state == "D" and next_prob["D"] > self.threshold:
            intents.append(OrderIntent(
                venue=venue, symbol=sig.symbol, side="sell", qty=qty,
                type="market", price=price, tag=self.name
            ))

        return intents
