

run:
	uv run --package executor python -m service.consumer

order:
	redis-cli XADD order_intents * venue alpaca_stocks symbol AAPL side buy qty 1 type market

check_stream:
	redis-cli XRANGE trades - +
