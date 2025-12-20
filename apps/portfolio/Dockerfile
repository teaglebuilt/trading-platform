FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy workspace files
COPY pyproject.toml ./
COPY packages ./packages
COPY apps/portfolio ./apps/portfolio

# Install dependencies
RUN uv pip install --system -e ./packages/domain -e ./apps/portfolio

WORKDIR /app/apps/portfolio

# Create data directory for DuckDB
RUN mkdir -p /data

ENV DUCKDB_FILE=/data/portfolio.db

# Run portfolio consumer
CMD ["python", "-m", "service.consumer"]
