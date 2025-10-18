trade:
	redis-cli XADD trades * trade_id t123 symbol AAPL side buy qty 10 fill_price 185.5 status filled ts 2025-09-25T14:10:11Z

run:
	uv run --package portfolio python -m portfolio.main

view:
	duckdb portfolio.db "SELECT * FROM trades;"
  duckdb portfolio.db "SELECT * FROM positions;"

pnl:
	@echo "total realized pnl: $(shell uv run --package portfolio portfolio-pnl)"
	@echo "unrealized pnl: $(shell uv run --package portfolio portfolio-pnl --price AAPL=190.0 BTCUSD=65000)"
