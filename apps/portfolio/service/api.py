from fastapi import FastAPI, Query
from typing import Optional
from .pnl import PnLCalculator
import duckdb

app = FastAPI(title="Portfolio API", version="0.1.0")
DB_FILE = "portfolio.db"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/trades")
def list_trades(limit: int = Query(50, ge=1, le=500)):
    con = duckdb.connect(DB_FILE)
    rows = con.execute("SELECT * FROM trades ORDER BY ts DESC LIMIT ?", [limit]).fetchall()
    cols = [c[0] for c in con.description]
    return [dict(zip(cols, r)) for r in rows]


@app.get("/positions")
def list_positions():
    con = duckdb.connect(DB_FILE)
    rows = con.execute("SELECT * FROM positions ORDER BY symbol").fetchall()
    cols = [c[0] for c in con.description]
    return [dict(zip(cols, r)) for r in rows]


@app.get("/pnl/realized")
def realized(symbol: Optional[str] = None):
    calc = PnLCalculator(DB_FILE)
    return {"symbol": symbol, "realized_pnl": calc.realized_pnl(symbol)}


@app.post("/pnl/unrealized")
def unrealized(prices: dict[str, float]):
    calc = PnLCalculator(DB_FILE)
    return {"unrealized_pnl": calc.unrealized_pnl(prices)}


@app.post("/pnl/all")
def all_pnl(prices: dict[str, float]):
    calc = PnLCalculator(DB_FILE)
    return calc.all_pnl(prices)
