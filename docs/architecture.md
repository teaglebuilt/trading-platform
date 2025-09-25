

### Apps
- **orchestrator/** → Workflow hub (n8n integration).
- **signal-adapter/** → Thin boundary for incoming signals (validate + persist).
- **strategy-engine/** → Wrapper around Freqtrade, Jesse, Backtrader (strategy runtime).
- **executor/** → Executes orders on brokers/exchanges via adapters.
- **portfolio/** → Central ledger for trades, positions, balances.
- **reporter/** → Reports, dashboards, alerts.
- **mcp-servers/**
  - **alpaca-mcp/** → AI-safe Alpaca adapter.
  - **research-mcp/** → AI research assistant (backtests, data analysis).

### Packages
- **common/** → Shared pydantic models (`Signal`, `OrderIntent`, `Trade`, etc.).
- **risk/** → Risk rules (exposure caps, daily loss limits).
- **storage/** → Persistence (SQLAlchemy, TimescaleDB, Redis).
- **analytics/** → Metrics and reporting (QuantStats, Pandas).
- **brokers/**
  - **alpaca-adapter/** → Wraps `alpaca-py`.
  - **etrade-adapter/** → Wraps E*TRADE API.
  - **ccxt-adapter/** → Wraps CCXT for crypto exchanges.

---

## 🔗 System Overview

```mermaid
flowchart LR
  TV[TradingView / Webhooks] --> N8N[n8n Orchestrator]
  N8N --> SA[Signal Adapter]
  SA --> SE[Strategy Engine]
  SE -->|OrderIntent| EX[Executor]
  EX -->|Trades| PF[Portfolio]
  PF --> RP[Reporter]

  SE -.->|Backtests| RE[Research MCP]
  PF -.-> RP
  RP --> Alerts[Slack/Email/Grafana]

  EX -->|Broker APIs| BA[Alpaca / E*TRADE / CCXT]

  subgraph MCP
    AM[Alpaca MCP]
    RE[Research MCP]
  end

  AM --> BA
  RE --> SE
  RE --> PF
```