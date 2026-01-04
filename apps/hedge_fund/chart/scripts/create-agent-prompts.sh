#!/bin/bash
set -e

echo "Creating/updating agent prompts ConfigMap..."

kubectl create configmap trading-agent-prompts \
  --namespace=ai \
  --from-file=market-analyst.md=.ai/agents/market-analyst.md \
  --from-file=strategy-agent.md=.ai/agents/strategy-agent.md \
  --from-file=position-sizer.md=.ai/agents/position-sizer.md \
  --from-file=timing-agent.md=.ai/agents/timing-agent.md \
  --from-file=governance-agent.md=.ai/agents/governance-agent.md \
  --dry-run=client -o yaml | kubectl apply -f -

echo "✓ ConfigMap 'trading-agent-prompts' created/updated in namespace 'ai'"

