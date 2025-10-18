# Market Analyst Agent

## Purpose
Collect and summarize market context from multiple data feeds (macro, sentiment, fundamentals, news).
Produces structured JSON signals describing the current market regime and notable opportunities.

## Responsibilities
- Pull news, social sentiment, and sector performance data
- Detect broad market trends (bullish, neutral, bearish)
- Identify macro catalysts or risk events
- Output summary context used by downstream agents

## Input
None (triggered by scheduler or n8n workflow)

## Output
```json
{
  "market_context": {
    "regime": "bullish",
    "volatility_index": 18.2,
    "sentiment_score": 0.67,
    "notable_themes": ["AI", "semiconductors", "tech rally"]
  }
}
