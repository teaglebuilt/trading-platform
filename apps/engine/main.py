from fastapi import FastAPI, HTTPException
from strategy_engine.service import StrategyEngineService
from strategy_engine.registry import registry
from strategy_engine.interfaces import Signal

app = FastAPI(title="Strategy Engine", version="0.1.0")
svc = StrategyEngineService()


@app.get("/health")
def health():
    return {"status": "ok", "strategies": list(registry.strategies.keys())}


@app.get("/strategies")
def list_strategies():
    return {"registered": list(registry.strategies.keys())}


@app.post("/process-signal")
async def process_signal(sig: Signal):
    try:
        intents = await svc.process_signal(sig)
        return {"count": len(intents), "intents": [i.model_dump() for i in intents]}
    except Exception as e:
        raise HTTPException(400, f"processing_error: {e}")