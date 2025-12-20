import os
from pydantic import BaseModel


class ReporterConfig(BaseModel):
    redis_url: str = "redis://localhost:6379/0"
    duckdb_file: str = "portfolio.db"
    slack_webhook_url: str | None = None

    # Alert thresholds
    daily_loss_limit_pct: float = 0.02  # 2% daily loss triggers alert
    position_size_limit_pct: float = 0.10  # 10% of portfolio in single position
    drawdown_alert_pct: float = 0.05  # 5% drawdown triggers alert

    # Reporting schedule
    report_interval_seconds: int = 300  # 5 minutes


def load_config() -> ReporterConfig:
    return ReporterConfig(
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        duckdb_file=os.getenv("DUCKDB_FILE", "portfolio.db"),
        slack_webhook_url=os.getenv("SLACK_WEBHOOK_URL"),
        daily_loss_limit_pct=float(os.getenv("DAILY_LOSS_LIMIT_PCT", "0.02")),
        position_size_limit_pct=float(os.getenv("POSITION_SIZE_LIMIT_PCT", "0.10")),
        drawdown_alert_pct=float(os.getenv("DRAWDOWN_ALERT_PCT", "0.05")),
        report_interval_seconds=int(os.getenv("REPORT_INTERVAL_SECONDS", "300")),
    )


CONFIG = load_config()
