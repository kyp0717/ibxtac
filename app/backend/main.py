"""
FastAPI main application with integrated TWS client.
"""

import logging
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .models import HealthResponse
from .routers import tws
from ..tws.client import TWSClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting IBxTAC application...")

    # Startup
    try:
        # Initialize TWS client
        tws_client = TWSClient(host="127.0.0.1", port=7500, client_id=1)
        app.state.tws_client = tws_client
        logger.info("TWS client initialized")

        # Optionally try to connect at startup
        # if tws_client.connect():
        #     logger.info("Connected to TWS at startup")
        # else:
        #     logger.warning("Could not connect to TWS at startup")

    except Exception as e:
        logger.error(f"Error during startup: {e}")

    yield

    # Shutdown
    try:
        if hasattr(app.state, 'tws_client'):
            app.state.tws_client.disconnect()
            logger.info("Disconnected from TWS")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

    logger.info("IBxTAC application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="IBxTAC API",
    description="Interactive Brokers TWS Trading Application Client API",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tws.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "IBxTAC API is running", "version": "0.1.0"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    tws_connected = False

    try:
        if hasattr(app.state, 'tws_client'):
            tws_connected = app.state.tws_client.is_connected()
    except Exception as e:
        logger.error(f"Error checking TWS connection: {e}")

    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.now(),
        tws_connected=tws_connected
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )