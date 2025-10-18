import argparse
from .pnl import PnLCalculator


def main():
    parser = argparse.ArgumentParser(description="Portfolio PnL CLI")
    parser.add_argument("--db", default="portfolio.db", help="Path to DuckDB file")
    parser.add_argument("--symbol", help="Symbol for realized PnL")
    parser.add_argument("--price", action="append", help="Market price in format SYMBOL=PRICE")
    args = parser.parse_args()

    calc = PnLCalculator(args.db)

    if args.symbol:
        print(f"Realized PnL for {args.symbol}: {calc.realized_pnl(args.symbol)}")
    else:
        print(f"Total realized PnL: {calc.realized_pnl()}")

    if args.price:
        market_prices = {s.split("=")[0]: float(s.split("=")[1]) for s in args.price}
        unreal = calc.unrealized_pnl(market_prices)
        print("Unrealized PnL:", unreal)


if __name__ == "__main__":
    main()
