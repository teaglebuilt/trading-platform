import os
import asyncio
from datetime import datetime
import duckdb
import pandas as pd
import yfinance as yf
from common.models import Signal
from strategy_engine.strategies.ema_cross.strategy import EmaCross

RESULT_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULT_DIR, exist_ok=True)


async def run():
    strat = EmaCross()
    df = yf.download("GLD", start="2023-01-01", interval="1h")

    trades = []
    for ts, row in df.iterrows():
        short_ema = df["Close"].rolling(20).mean().loc[ts]
        long_ema = df["Close"].rolling(100).mean().loc[ts]
        if pd.isna(short_ema) or pd.isna(long_ema):
            continue

        side = "buy" if short_ema > long_ema else "sell"
        sig = Signal(
            symbol="GLD",
            side=side,
            price=float(row["Close"]),
            ts=str(ts),
            strategy="ema_cross",
            meta={"target_value_usd": 1000, "tp_pct": 0.02, "sl_pct": 0.01,
                  "short_ema": short_ema, "long_ema": long_ema}
        )
        intents = await strat.evaluate(sig)
        for i in intents:
            trades.append({
                "ts": ts, "symbol": i.symbol, "side": i.side,
                "qty": i.qty, "price": i.price, "tp_pct": i.tp_pct, "sl_pct": i.sl_pct
            })

    df_trades = pd.DataFrame(trades)
    filename = datetime.now().strftime("%Y-%m-%dT%H%M%S-glD-hourly.parquet")
    out_path = os.path.join(RESULT_DIR, filename)
    df_trades.to_parquet(out_path)
    print(f"✅ Backtest saved: {out_path}")

    con = duckdb.connect()
    con.execute("CREATE TABLE t AS SELECT * FROM df_trades")
    summary = con.execute("""
        SELECT side, COUNT(*) AS trades, AVG(price) AS avg_price FROM t GROUP BY side
    """).df()
    print(summary)

asyncio.run(run())
