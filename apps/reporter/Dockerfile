FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy workspace files
COPY pyproject.toml ./
COPY packages ./packages
COPY apps/reporter ./apps/reporter

# Install dependencies
RUN uv pip install --system -e ./packages/domain -e ./apps/reporter

WORKDIR /app/apps/reporter

# Run reporter service
CMD ["python", "-m", "reporter.service"]
