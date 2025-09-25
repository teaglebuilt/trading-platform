Role: Orchestration hub. Integrates with n8n (self-hosted) to manage workflows.

Responsibilities:

Receives webhooks from TradingView → sends to signal-adapter.

Orchestrates retries, branching logic, and simple transformations.

Delegates heavy compute to strategy/portfolio services.

Tech: n8n, REST/queue connectors.