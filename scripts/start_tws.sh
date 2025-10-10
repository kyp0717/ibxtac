#!/bin/bash

###############################################################################
# TWS Application Startup Script
#
# This script starts the TWS (Trader Workstation) application that connects
# to Interactive Brokers TWS or IB Gateway and requests the current server time.
#
# Usage:
#   ./scripts/start_tws.sh [OPTIONS]
#
# Options:
#   --host HOST         TWS/Gateway host address (default: localhost)
#   --port PORT         TWS/Gateway port number (default: 7500)
#   --client-id ID      Client ID for connection (default: 1)
#   --help              Show help message
#
# Examples:
#   ./scripts/start_tws.sh
#   ./scripts/start_tws.sh --port 7497
#   ./scripts/start_tws.sh --host localhost --port 7500 --client-id 1
#
# Port Reference:
#   7496 - TWS live trading
#   7497 - TWS paper trading
#   7500 - Custom port (default)
#   4001 - IB Gateway live trading
#   4002 - IB Gateway paper trading
#
# Prerequisites:
#   - TWS or IB Gateway must be running
#   - API connections must be enabled in TWS settings
#   - Python virtual environment must be set up with uv
#   - ibapi package must be installed
#
###############################################################################

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to the app/server directory
cd "$PROJECT_ROOT/app/server"

# Check if .venv exists
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "Error: Virtual environment not found at $PROJECT_ROOT/.venv"
    echo "Please run 'uv venv' from the project root to create it."
    exit 1
fi

# Display startup banner
echo "=========================================="
echo "  TWS Application Startup"
echo "=========================================="
echo ""

# Run the TWS application with uv
# Pass all command-line arguments to the Python script
cd "$PROJECT_ROOT"
uv run python app/server/tws_app.py "$@"
