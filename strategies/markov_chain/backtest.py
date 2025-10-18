from strategy_engine.strategies.markov_chain.strategy import MarkovChainStrategy
from common.models import Signal
import asyncio
import pandas as pd
import yfinance as yf


async def run():
    strat = MarkovChainStrategy(window=100, threshold=0.6)
    df = yf.download("GLD", start="2023-01-01", interval="1h")

    prev_price = None
    for ts, row in df.iterrows():
        if prev_price is None:
            prev_price = row["Close"]
            continue
        sig = Signal(
            symbol="GLD",
            side="buy",  # dummy (strategy decides)
            price=float(row["Close"]),
            ts=str(ts),
            strategy="markov_chain",
            meta={"prev_price": float(prev_price)}
        )
        intents = await strat.evaluate(sig)
        for i in intents:
            print(f"{ts}: {i.side} {i.symbol} @ {i.price}")
        prev_price = row["Close"]


asyncio.run(run())
