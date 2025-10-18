import asyncio
import os
from strategy_engine.service import StrategyEngineService
from common.models import Signal
from redis import Redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
svc = StrategyEngineService()


async def consume_signals():
    redis = Redis.from_url(REDIS_URL, decode_responses=True)
    last_id = "0-0"
    print("[strategy-engine] Listening for signals...")

    while True:
        msgs = redis.xread({"signals": last_id}, block=5000, count=1)
        if not msgs:
            continue
        stream, entries = msgs[0]
        for entry_id, payload in entries:
            last_id = entry_id
            sig = Signal(**payload)
            intents = await svc.process_signal(sig)
            for i in intents:
                redis.xadd("order_intents", i.model_dump())
                print(f"[strategy-engine] OrderIntent → {i.model_dump()}")


if __name__ == "__main__":
    asyncio.run(consume_signals())
