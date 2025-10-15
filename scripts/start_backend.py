#!/usr/bin/env python3
"""
Backend-only startup script.

This script starts only the FastAPI backend server for the IBxTAC application.
Useful for development or when running frontend separately.
"""

import os
import sys
import subprocess
import signal
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Find project root directory
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent

# Process tracking
backend_process = None


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Shutdown signal received. Stopping backend server...")

    global backend_process
    if backend_process and backend_process.poll() is None:
        logger.info(f"Terminating backend process {backend_process.pid}")
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            logger.warning(f"Force killing backend process {backend_process.pid}")
            backend_process.kill()
            backend_process.wait()

    logger.info("Backend server stopped. Exiting.")
    sys.exit(0)


def check_dependencies():
    """Check if required Python dependencies are available."""
    logger.info("Checking Python dependencies...")

    try:
        import fastapi
        import uvicorn
        import ibapi
        logger.info("All Python dependencies available")
        return True
    except ImportError as e:
        logger.error(f"Missing Python dependency: {e}")
        logger.info("Run 'uv sync' to install Python dependencies")
        return False


def start_backend():
    """Start the FastAPI backend server."""
    logger.info("Starting FastAPI backend server...")

    backend_cmd = [
        sys.executable, "-m", "uvicorn",
        "app.backend.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload",
        "--log-level", "info"
    ]

    try:
        process = subprocess.Popen(
            backend_cmd,
            cwd=PROJECT_ROOT
        )
        logger.info(f"Backend started with PID {process.pid}")
        logger.info("Backend API: http://localhost:8000")
        logger.info("API Documentation: http://localhost:8000/docs")
        logger.info("Health Check: http://localhost:8000/health")
        return process
    except Exception as e:
        logger.error(f"Failed to start backend: {e}")
        return None


def main():
    """Main backend startup function."""
    logger.info("Starting IBxTAC Backend Server...")
    logger.info(f"Project root: {PROJECT_ROOT}")

    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Check dependencies
    if not check_dependencies():
        logger.error("Dependency check failed. Exiting.")
        sys.exit(1)

    # Start backend
    global backend_process
    backend_process = start_backend()
    if not backend_process:
        logger.error("Failed to start backend. Exiting.")
        sys.exit(1)

    logger.info("Backend startup complete!")
    logger.info("Press Ctrl+C to stop the server.")

    # Wait for process to complete
    try:
        backend_process.wait()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)


if __name__ == "__main__":
    main()