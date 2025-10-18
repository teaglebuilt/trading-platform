# Trading Platform Automation

## Overview

...

### Quant Hedge Fund Team

AI Agent prompts are stored in `.ai/agents/*.md` files at the repository root.
These prompts are loaded into a Kubernetes ConfigMap that KAgent resources reference.

- `market-analyst.md` → Market context and sentiment analysis
- `stock-market-expert.md` → Comprehensive market knowledge
- `strategy-agent.md` → Strategy selection and signal generation  
- `position-sizer.md` → Position sizing and risk allocation
- `timing-agent.md` → Entry/exit timing validation
- `governance-agent.md` → Risk and compliance enforcement

### Deployment

These agents can run on kubernetes

```bash
helm upgrade --install trading-agents ./chart \
  --namespace ai \
  --create-namespace
```
