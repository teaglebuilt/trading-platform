import os
from pydantic import BaseModel
from typing import Literal


class EngineConfig(BaseModel):
    # Choose default backend for symbols/classes
    default_crypto_backend: Literal["freqtrade", "jesse", "local"] = "freqtrade"
    default_equity_backend: Literal["backtrader", "local"] = "local"

    # External engine endpoints (sidecars / services)
    freqtrade_base_url: str | None = None   # e.g., http://freqtrade:8080
    jesse_base_url: str | None = None       # e.g., http://jesse:9000

    # Feature flags
    enable_risk_pipeline: bool = True


def load_config() -> EngineConfig:
    return EngineConfig(
        default_crypto_backend=os.getenv("DEFAULT_CRYPTO_BACKEND", "freqtrade"),
        default_equity_backend=os.getenv("DEFAULT_EQUITY_BACKEND", "local"),
        freqtrade_base_url=os.getenv("FREQTRADE_BASE_URL"),
        jesse_base_url=os.getenv("JESSE_BASE_URL"),
        enable_risk_pipeline=os.getenv("ENABLE_RISK_PIPELINE", "true").lower() == "true",
    )


CONFIG = load_config()
