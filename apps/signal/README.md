Role: Thin service, not a full router.

Responsibilities:

Validate incoming signals (pydantic Signal model from common).

Persist signals to storage (Redis/Postgres).

Publish clean events to strategy-engine.

Why: Keeps your system decoupled from n8n (no vendor lock-in, consistent schema