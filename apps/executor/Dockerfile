FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy workspace files
COPY pyproject.toml ./
COPY packages ./packages
COPY apps/executor ./apps/executor

# Install dependencies
RUN uv pip install --system -e ./packages/domain -e ./apps/executor

WORKDIR /app/apps/executor

# Run executor consumer
CMD ["python", "-m", "service.consumer"]
