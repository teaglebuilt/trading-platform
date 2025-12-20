import asyncio
from redis import Redis
from reporter.config import CONFIG
from reporter.metrics import calculate_metrics
from reporter.alerts import (
    alert_daily_loss,
    alert_drawdown,
    alert_position_concentration,
    alert_trade_executed,
)
from common.models import Trade


async def monitor_trades():
    """Monitor trade stream and send alerts."""
    redis = Redis.from_url(CONFIG.redis_url, decode_responses=True)
    last_id = "0-0"

    print("[reporter] Monitoring trades stream...")

    while True:
        try:
            msgs = redis.xread({"trades": last_id}, block=5000, count=10)
            if not msgs:
                continue

            stream, entries = msgs[0]
            for entry_id, payload in entries:
                last_id = entry_id
                try:
                    trade = Trade(**payload)
                    await alert_trade_executed(
                        trade.symbol,
                        trade.side,
                        trade.qty,
                        trade.fill_price
                    )
                except Exception as e:
                    print(f"[reporter] Error processing trade: {e}")
        except Exception as e:
            print(f"[reporter] Error reading trades: {e}")
            await asyncio.sleep(5)


async def monitor_metrics():
    """Periodically check portfolio metrics and alert on thresholds."""
    print(f"[reporter] Monitoring metrics every {CONFIG.report_interval_seconds}s...")

    while True:
        try:
            metrics = calculate_metrics(CONFIG.duckdb_file)

            # Check daily loss limit
            if metrics.daily_pnl_pct < -CONFIG.daily_loss_limit_pct:
                await alert_daily_loss(
                    abs(metrics.daily_pnl_pct),
                    CONFIG.daily_loss_limit_pct
                )

            # Check drawdown
            if metrics.max_drawdown_pct > CONFIG.drawdown_alert_pct:
                await alert_drawdown(
                    metrics.max_drawdown_pct,
                    CONFIG.drawdown_alert_pct
                )

            # Check position concentration
            if metrics.largest_position_pct > CONFIG.position_size_limit_pct:
                await alert_position_concentration(
                    metrics.largest_position_symbol,
                    metrics.largest_position_pct,
                    CONFIG.position_size_limit_pct
                )

            # Log current status
            print(f"[reporter] Portfolio: ${metrics.total_value:.2f} | "
                  f"Daily P&L: {metrics.daily_pnl_pct:.2%} | "
                  f"Positions: {metrics.num_positions} | "
                  f"Win Rate: {metrics.win_rate:.1%}")

        except Exception as e:
            print(f"[reporter] Error calculating metrics: {e}")

        await asyncio.sleep(CONFIG.report_interval_seconds)


async def run():
    """Run reporter service."""
    print("[reporter] Starting reporter service...")
    await asyncio.gather(
        monitor_trades(),
        monitor_metrics(),
    )


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
