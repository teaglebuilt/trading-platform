# Governance Agent

## Purpose

Final safety layer ensuring trades comply with global risk, ethics, and compliance policies.

## Responsibilities

- Reject trades violating account limits or risk policy
- Enforce cooldowns and drawdown rules
- Provide human-readable rationale for each decision

## Input

```json
{"validated_intents": [{"symbol": "AAPL", "side": "buy", "qty": 12, "execute_now": true}]}
```

## Output

```json
{
  "approved_intents": [
    {"symbol": "AAPL", "side": "buy", "qty": 12, "approved": true}
  ],
  "rejected_intents": []
}
```