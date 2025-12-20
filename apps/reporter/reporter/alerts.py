import httpx
from typing import Optional
from reporter.config import CONFIG


async def send_slack_alert(message: str, level: str = "warning"):
    """Send alert to Slack webhook if configured."""
    if not CONFIG.slack_webhook_url:
        print(f"[alert:{level}] {message}")
        return

    emoji = {
        "info": ":information_source:",
        "warning": ":warning:",
        "critical": ":rotating_light:",
    }.get(level, ":bell:")

    payload = {
        "text": f"{emoji} *Trading Alert*\n{message}",
        "username": "Trading Reporter",
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(CONFIG.slack_webhook_url, json=payload)
            resp.raise_for_status()
    except Exception as e:
        print(f"[alert] Failed to send Slack alert: {e}")


async def alert_daily_loss(loss_pct: float, limit_pct: float):
    """Alert when daily loss exceeds threshold."""
    await send_slack_alert(
        f"Daily loss of {loss_pct:.2%} exceeds limit of {limit_pct:.2%}",
        level="critical"
    )


async def alert_drawdown(drawdown_pct: float, limit_pct: float):
    """Alert when drawdown exceeds threshold."""
    await send_slack_alert(
        f"Portfolio drawdown of {drawdown_pct:.2%} exceeds threshold of {limit_pct:.2%}",
        level="warning"
    )


async def alert_position_concentration(symbol: str, concentration_pct: float, limit_pct: float):
    """Alert when position concentration is too high."""
    await send_slack_alert(
        f"Position in {symbol} at {concentration_pct:.2%} exceeds limit of {limit_pct:.2%}",
        level="warning"
    )


async def alert_trade_executed(symbol: str, side: str, qty: float, price: float):
    """Inform about executed trades."""
    await send_slack_alert(
        f"Trade executed: {side.upper()} {qty} {symbol} @ ${price:.2f}",
        level="info"
    )
