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

CONFIG = EngineConfig()
