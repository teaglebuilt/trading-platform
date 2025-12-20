FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy workspace files
COPY pyproject.toml ./
COPY packages ./packages
COPY apps/signal ./apps/signal

# Install dependencies
RUN uv pip install --system -e ./packages/domain -e ./apps/signal

WORKDIR /app/apps/signal

EXPOSE 8000

# Run signal API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
