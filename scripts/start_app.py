#!/usr/bin/env python3
"""
Full application startup script.

This script starts both the FastAPI backend and the React frontend
for the IBxTAC application.
"""

import os
import sys
import subprocess
import signal
import time
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
processes = []


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Shutdown signal received. Stopping all processes...")

    for process in processes:
        if process.poll() is None:  # Process is still running
            logger.info(f"Terminating process {process.pid}")
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning(f"Force killing process {process.pid}")
                process.kill()
                process.wait()

    logger.info("All processes stopped. Exiting.")
    sys.exit(0)


def check_dependencies():
    """Check if required dependencies are available."""
    logger.info("Checking dependencies...")

    # Check if Node.js is available
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"Node.js version: {result.stdout.strip()}")
        else:
            logger.error("Node.js not found")
            return False
    except FileNotFoundError:
        logger.error("Node.js not found")
        return False

    # Check if npm is available
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"npm version: {result.stdout.strip()}")
        else:
            logger.error("npm not found")
            return False
    except FileNotFoundError:
        logger.error("npm not found")
        return False

    # Check if Python venv exists or if packages are installed
    try:
        import fastapi
        import uvicorn
        import ibapi
        logger.info("Python dependencies available")
    except ImportError as e:
        logger.error(f"Missing Python dependency: {e}")
        logger.info("Run 'uv sync' to install Python dependencies")
        return False

    return True


def start_backend():
    """Start the FastAPI backend server."""
    logger.info("Starting FastAPI backend...")

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
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        processes.append(process)
        logger.info(f"Backend started with PID {process.pid}")
        return process
    except Exception as e:
        logger.error(f"Failed to start backend: {e}")
        return None


def start_frontend():
    """Start the React frontend development server."""
    logger.info("Starting React frontend...")

    frontend_dir = PROJECT_ROOT / "app" / "frontend"

    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        logger.info("Installing frontend dependencies...")
        install_process = subprocess.run(
            ["npm", "install"],
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )

        if install_process.returncode != 0:
            logger.error(f"Failed to install frontend dependencies: {install_process.stderr}")
            return None

    frontend_cmd = ["npm", "start"]

    try:
        process = subprocess.Popen(
            frontend_cmd,
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        processes.append(process)
        logger.info(f"Frontend started with PID {process.pid}")
        return process
    except Exception as e:
        logger.error(f"Failed to start frontend: {e}")
        return None


def monitor_processes():
    """Monitor running processes and log their output."""
    logger.info("Monitoring processes. Press Ctrl+C to stop all services.")

    try:
        while True:
            for i, process in enumerate(processes):
                if process.poll() is not None:
                    logger.error(f"Process {process.pid} has stopped unexpectedly")
                    return False

            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)


def main():
    """Main application startup function."""
    logger.info("Starting IBxTAC Application...")
    logger.info(f"Project root: {PROJECT_ROOT}")

    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Check dependencies
    if not check_dependencies():
        logger.error("Dependency check failed. Exiting.")
        sys.exit(1)

    # Start backend
    backend_process = start_backend()
    if not backend_process:
        logger.error("Failed to start backend. Exiting.")
        sys.exit(1)

    # Wait a moment for backend to start
    time.sleep(3)

    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        logger.error("Failed to start frontend. Stopping backend.")
        signal_handler(signal.SIGINT, None)
        sys.exit(1)

    # Wait a moment for frontend to start
    time.sleep(3)

    logger.info("Application startup complete!")
    logger.info("Backend API: http://localhost:8000")
    logger.info("Frontend UI: http://localhost:3000")
    logger.info("API Documentation: http://localhost:8000/docs")

    # Monitor processes
    monitor_processes()


if __name__ == "__main__":
    main()