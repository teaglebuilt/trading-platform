FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy workspace files
COPY pyproject.toml ./
COPY packages ./packages
COPY apps/engine ./apps/engine

# Install dependencies
RUN uv pip install --system -e ./packages/domain -e ./apps/engine

WORKDIR /app/apps/engine

# Run strategy engine CLI
CMD ["python", "-m", "strategy_engine.service"]
