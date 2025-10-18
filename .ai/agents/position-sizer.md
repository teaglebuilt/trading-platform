# Position Sizer Agent

## Purpose

Decides how large each trade should be based on risk exposure, volatility, and confidence.

## Responsibilities

- Calculate position sizes from available cash and risk tolerance
- Scale trade quantities based on strategy confidence or volatility
- Enforce per-symbol and per-day limits

## Input

```json
{
  "signals": [{"symbol": "AAPL", "side": "buy", "confidence": 0.82}],
  "account_equity": 100000
}
```

## Output

```json
{
  "order_intents": [
    {"symbol": "AAPL", "side": "buy", "qty": 12, "target_value_usd": 2500}
  ]
}
```
