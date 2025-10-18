# Timing Agent

## Purpose

Determine when to execute or delay trades based on technical indicators and intraday conditions.

## Responsibilities

- Confirm entries with short-term indicators (RSI, volume, momentum)
- Delay trades during high volatility or low liquidity
- Output executable or deferred intents

## Input

```json
{"order_intents": [{"symbol": "AAPL", "side": "buy", "qty": 12}]}
```

## Output

```json
{
  "validated_intents": [
    {"symbol": "AAPL", "side": "buy", "qty": 12, "execute_now": true}
  ]
}
```
