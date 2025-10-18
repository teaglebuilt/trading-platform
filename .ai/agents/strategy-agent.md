# Strategy Agent

## Purpose

Selects or generates trading strategies based on market context and backtested performance.
Implements classic and AI-driven models (EMA Cross, Markov Chain, Reinforcement).

## Responsibilities

- Choose which strategy is active given market regime
- Generate directional trade signals (buy/sell/hold)
- Output structured Signal objects

## Input

```json
{"market_context": {"regime": "bullish"}}
```

## Output

```json
{
  "signals": [
    {"symbol": "AAPL", "side": "buy", "strategy": "ema_cross"},
    {"symbol": "NVDA", "side": "buy", "strategy": "markov_chain"}
  ]
}
```