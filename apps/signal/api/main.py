from fastapi import FastAPI, HTTPException
from redis import Redis
from common.models import Signal
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = FastAPI(title="Signal Adapter", version="0.1.0")
redis = Redis.from_url(REDIS_URL, decode_responses=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/signals")
async def ingest_signal(sig: Signal):
    try:
        payload = sig.model_dump()
        # Store in Redis stream for downstream services
        redis.xadd("signals", payload)
        return {"status": "accepted", "signal": payload}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def cli():
    import uvicorn
    uvicorn.run("signal_adapter.main:app", host="0.0.0.0", port=8000, reload=True)
