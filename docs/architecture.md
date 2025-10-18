## Architecture

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


### N8N Orchestration

```mermaid
flowchart TD
  %% External sources
  TV[TradingView Alerts] --> N8N[n8n Workflow]
  RSS[News / RSS / APIs] --> N8N
  Slack[Slack Commands] --> N8N
  Email[Email] --> N8N

  %% n8n responsibilities
  N8N -->|Validate + Transform JSON| SA[Signal Adapter]
  N8N -->|Enrich Signal| SA
  N8N -->|Retries if adapter is down| SA
  N8N -->|Error -> Notify| Ops[Slack/Email Alerts]

  %% Signal adapter (thin schema boundary)
  SA -->|Normalized Signal| SE[Strategy Engine]

  %% Strategy engine (pluggable backends)
  SE -->|Local/Freqtrade/Jesse/Backtrader| Intents[OrderIntents]
  Intents --> RP[Risk Pipeline]

  RP --> EX[Executor]

  %% Execution
  EX -->|Send Orders| Brokers[(Alpaca / E*TRADE / CCXT)]
  Brokers --> PF[Portfolio]

  %% Portfolio + Reporting
  PF --> RPT[Reporter]
  RPT --> Ops

  %% AI / MCP servers
  SE -.-> RE[Research MCP]
  PF -.-> RE
  EX -.-> AM[Alpaca MCP]
```