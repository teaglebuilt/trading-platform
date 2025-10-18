import asyncio
import uvicorn
import os
from .api import app
from .consumer import consume_trades


async def main():
    # Run trade consumer in background
    asyncio.create_task(consume_trades())
    # Run FastAPI server
    port = int(os.getenv("PORT", 8100))
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
