import os
import asyncio
import duckdb
from redis import Redis
from datetime import datetime
from common.models import Trade

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DB_FILE = os.getenv("DUCKDB_FILE", "portfolio.db")

# Connect DuckDB
con = duckdb.connect(DB_FILE)
con.execute("""
CREATE TABLE IF NOT EXISTS trades (
    trade_id TEXT PRIMARY KEY,
    symbol TEXT,
    side TEXT,
    qty DOUBLE,
    fill_price DOUBLE,
    status TEXT,
    ts TIMESTAMP
)
""")
con.execute("""
CREATE TABLE IF NOT EXISTS positions (
    symbol TEXT PRIMARY KEY,
    qty DOUBLE,
    avg_price DOUBLE
)
""")

redis = Redis.from_url(REDIS_URL, decode_responses=True)

async def consume_trades():
    last_id = "0-0"
    print("[portfolio] Listening for trades...")

    while True:
        msgs = redis.xread({"trades": last_id}, block=5000, count=1)
        if not msgs:
            continue
        stream, entries = msgs[0]
        for entry_id, payload in entries:
            last_id = entry_id
            try:
                trade = Trade(**payload)
                print(f"[portfolio] Recording trade: {trade}")

                # Insert trade
                con.execute(
                    "INSERT OR REPLACE INTO trades VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [
                        trade.trade_id,
                        trade.symbol,
                        trade.side,
                        trade.qty,
                        trade.fill_price,
                        trade.status,
                        datetime.fromisoformat(trade.ts),
                    ],
                )

                # Update position
                pos = con.execute("SELECT qty, avg_price FROM positions WHERE symbol = ?", [trade.symbol]).fetchone()
                if not pos:
                    if trade.side == "buy":
                        con.execute(
                            "INSERT INTO positions VALUES (?, ?, ?)",
                            [trade.symbol, trade.qty, trade.fill_price],
                        )
                else:
                    qty, avg_price = pos
                    if trade.side == "buy":
                        total_cost = avg_price * qty + trade.fill_price * trade.qty
                        qty += trade.qty
                        avg_price = total_cost / qty
                        con.execute(
                            "UPDATE positions SET qty=?, avg_price=? WHERE symbol=?",
                            [qty, avg_price, trade.symbol],
                        )
                    elif trade.side == "sell":
                        qty -= trade.qty
                        if qty < 0:
                            qty = 0
                        con.execute(
                            "UPDATE positions SET qty=? WHERE symbol=?",
                            [qty, trade.symbol],
                        )

                print(f"[portfolio] Updated position: {trade.symbol}")
            except Exception as e:
                print(f"[portfolio] Error: {e}")


if __name__ == "__main__":
    asyncio.run(consume_trades())
