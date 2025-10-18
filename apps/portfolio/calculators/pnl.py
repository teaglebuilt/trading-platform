import duckdb
from typing import Optional


class PnLCalculator:
    def __init__(self, db_file: str = "portfolio.db"):
        self.con = duckdb.connect(db_file)

    def realized_pnl(self, symbol: Optional[str] = None) -> float:
        sql = """
        SELECT
          SUM(CASE WHEN side='sell' THEN qty*fill_price ELSE 0 END) -
          SUM(CASE WHEN side='buy'  THEN qty*fill_price ELSE 0 END) AS pnl
        FROM trades
        """
        if symbol:
            sql += " WHERE symbol = ?"
            return self.con.execute(sql, [symbol]).fetchone()[0] or 0.0
        return self.con.execute(sql).fetchone()[0] or 0.0

    def unrealized_pnl(self, market_prices: dict[str, float]) -> dict[str, float]:
        """
        Calculate unrealized PnL based on current market prices.
        market_prices = {"AAPL": 190.0, "BTCUSD": 65000.0}
        """
        positions = self.con.execute("SELECT symbol, qty, avg_price FROM positions WHERE qty > 0").fetchall()
        results = {}
        for symbol, qty, avg_price in positions:
            if symbol in market_prices:
                market_price = market_prices[symbol]
                results[symbol] = (market_price - avg_price) * qty
        return results

    def all_pnl(self, market_prices: dict[str, float]) -> dict[str, float]:
        return {
            "realized": self.realized_pnl(),
            "unrealized": self.unrealized_pnl(market_prices)
        }
