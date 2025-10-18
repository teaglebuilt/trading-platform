import os
import asyncio
from redis import Redis
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import (
    MarketOrderRequest,
    LimitOrderRequest,
    TakeProfitRequest,
    StopLossRequest,
)
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.common.exceptions import APIError
from common.models import OrderIntent, Trade

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET")
ALPACA_PAPER = os.getenv("ALPACA_PAPER", "true").lower() == "true"

redis = Redis.from_url(REDIS_URL, decode_responses=True)
client = TradingClient(ALPACA_API_KEY, ALPACA_API_SECRET, paper=ALPACA_PAPER)


def build_order(intent: OrderIntent, ref_price: float | None = None):
    side = OrderSide.BUY if intent.side == "buy" else OrderSide.SELL
    base_price = ref_price or intent.limit_price or intent.price

    tp_req = (
        TakeProfitRequest(limit_price=round(base_price * (1 + intent.tp_pct), 2))
        if intent.tp_pct and base_price
        else None
    )
    sl_req = (
        StopLossRequest(stop_price=round(base_price * (1 - intent.sl_pct), 2))
        if intent.sl_pct and base_price
        else None
    )

    if intent.type == "market":
        return MarketOrderRequest(
            symbol=intent.symbol,
            qty=intent.qty,
            side=side,
            time_in_force=TimeInForce.DAY,
            take_profit=tp_req,
            stop_loss=sl_req,
        )
    elif intent.type == "limit":
        return LimitOrderRequest(
            symbol=intent.symbol,
            qty=intent.qty,
            side=side,
            time_in_force=TimeInForce.DAY,
            limit_price=intent.limit_price,
            take_profit=tp_req,
            stop_loss=sl_req,
        )
    else:
        raise ValueError(f"Unsupported order type: {intent.type}")


async def consume_order_intents():
    last_id = "0-0"
    print("[executor] Listening for order_intents...")

    while True:
        msgs = redis.xread({"order_intents": last_id}, block=5000, count=1)
        if not msgs:
            continue
        stream, entries = msgs[0]
        for entry_id, payload in entries:
            last_id = entry_id
            try:
                intent = OrderIntent(**payload)
                print(f"[executor] Processing OrderIntent: {intent}")

                if redis.get("KILL_SWITCH") == "true":
                    print("[executor] Kill switch active, skipping order")
                    continue

                if intent.venue != "alpaca_stocks":
                    print(f"[executor] Skipping unsupported venue {intent.venue}")
                    continue

                order_req = build_order(intent, ref_price=intent.price)
                submitted = client.submit_order(order_req)

                trade = Trade(
                    trade_id=submitted.id,
                    symbol=submitted.symbol,
                    side=submitted.side.value,
                    qty=submitted.qty,
                    fill_price=float(submitted.filled_avg_price or 0),
                    status=submitted.status.value,
                    ts=str(submitted.submitted_at),
                )

                # Include reference back to original OrderIntent
                trade_payload = {**trade.model_dump(), "intent_id": entry_id}
                redis.xadd("trades", trade_payload)

                print(f"[executor] Executed trade → {trade_payload}")

            except APIError as e:
                err_msg = f"APIError: {e}"
                print(f"[executor] {err_msg}")
                redis.xadd("order_errors", {"intent_id": entry_id, "error": err_msg})
            except Exception as e:
                err_msg = f"Unexpected error: {e}"
                print(f"[executor] {err_msg}")
                redis.xadd("order_errors", {"intent_id": entry_id, "error": err_msg})


if __name__ == "__main__":
    asyncio.run(consume_order_intents())
