import duckdb
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel


class PortfolioMetrics(BaseModel):
    total_value: float = 0.0
    daily_pnl: float = 0.0
    daily_pnl_pct: float = 0.0
    total_pnl: float = 0.0
    total_pnl_pct: float = 0.0
    max_drawdown_pct: float = 0.0
    num_positions: int = 0
    largest_position_pct: float = 0.0
    largest_position_symbol: Optional[str] = None
    trades_today: int = 0
    win_rate: float = 0.0


def calculate_metrics(db_path: str) -> PortfolioMetrics:
    """Calculate portfolio metrics from DuckDB."""
    try:
        con = duckdb.connect(db_path, read_only=True)
    except Exception as e:
        print(f"[metrics] Cannot connect to DuckDB: {e}")
        return PortfolioMetrics()

    metrics = PortfolioMetrics()

    try:
        # Get current positions
        positions = con.execute("""
            SELECT symbol, qty, avg_price
            FROM positions
            WHERE qty > 0
        """).fetchall()

        metrics.num_positions = len(positions)

        if not positions:
            return metrics

        # Calculate total value (using avg_price as proxy for current price)
        total_value = sum(qty * avg_price for _, qty, avg_price in positions)
        metrics.total_value = total_value

        # Find largest position
        if positions:
            largest = max(positions, key=lambda p: p[1] * p[2])
            largest_value = largest[1] * largest[2]
            metrics.largest_position_symbol = largest[0]
            metrics.largest_position_pct = largest_value / total_value if total_value > 0 else 0

        # Get today's trades
        today = datetime.now().date()
        trades_today = con.execute("""
            SELECT COUNT(*) FROM trades
            WHERE DATE(ts) = ?
        """, [today]).fetchone()[0]
        metrics.trades_today = trades_today

        # Calculate daily P&L from today's trades
        daily_result = con.execute("""
            SELECT
                SUM(CASE WHEN side = 'sell' THEN qty * fill_price ELSE -qty * fill_price END)
            FROM trades
            WHERE DATE(ts) = ?
        """, [today]).fetchone()[0]

        if daily_result:
            metrics.daily_pnl = daily_result
            metrics.daily_pnl_pct = daily_result / total_value if total_value > 0 else 0

        # Calculate win rate from all trades
        win_count = con.execute("""
            WITH trade_pairs AS (
                SELECT
                    symbol,
                    side,
                    fill_price,
                    LAG(fill_price) OVER (PARTITION BY symbol ORDER BY ts) as prev_price
                FROM trades
            )
            SELECT COUNT(*) FROM trade_pairs
            WHERE side = 'sell' AND fill_price > prev_price
        """).fetchone()[0]

        total_sells = con.execute("""
            SELECT COUNT(*) FROM trades WHERE side = 'sell'
        """).fetchone()[0]

        metrics.win_rate = win_count / total_sells if total_sells > 0 else 0

    except Exception as e:
        print(f"[metrics] Error calculating metrics: {e}")
    finally:
        con.close()

    return metrics
