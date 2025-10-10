# Feature: Basic TWS App

## Metadata
issue_number: `01`
adw_id: `adw-01`
issue_json: `{'title': 'basic tws app', 'body': 'create tws app in the app/server folder to req current current time from TWS app on port 7500'}`

## Feature Description
Create a Python-based TWS (Trader Workstation) application in the app/server folder that connects to Interactive Brokers TWS application on port 7500 and requests the current server time. This serves as a foundational integration with the Interactive Brokers API using the ibapi library that is already installed in the virtual environment.

## User Story
As a trader/developer
I want to connect to Interactive Brokers TWS and retrieve the current time
So that I can verify the connection is working and establish a foundation for future trading operations

## Problem Statement
There is currently no TWS integration in the app/server directory. We need to establish a basic connection to Interactive Brokers TWS application to verify connectivity and demonstrate the ability to communicate with the IB API. This is essential for building any trading functionality on top of the IB platform.

## Solution Statement
Create a Python application using the ibapi library (already installed) that:
1. Establishes a connection to TWS running on localhost:7500
2. Requests the current server time from TWS
3. Displays the response to demonstrate successful communication
4. Provides a clean, extensible foundation for future TWS operations

## Relevant Files
Use these files to implement the feature:

- **ibapi library** (already installed in venv at version 10.30.1) - Provides the EClient and EWrapper classes needed to communicate with TWS
- **app/server/** - Currently empty directory where the TWS application will be created
- **scripts/** - Currently empty, may need start/stop scripts for the TWS application
- **.env.sample** and **app/server/.env.sample** - Will need to check if these exist and add TWS connection configuration if needed

### New Files
- **app/server/tws_app.py** - Main TWS application with EClient/EWrapper implementation
- **app/server/tws_client.py** - TWS client wrapper class that extends EClient and EWrapper
- **app/server/__init__.py** - Package initialization file
- **app/server/requirements.txt** or **pyproject.toml** - Python dependencies (if not using root uv environment)
- **app/server/tests/test_tws_client.py** - Unit tests for the TWS client
- **scripts/start_tws.sh** - Script to start the TWS application
- **.claude/commands/e2e/test_tws_connection.md** - E2E test to validate TWS connection and time retrieval

## Implementation Plan

### Phase 1: Foundation
- Set up the basic project structure in app/server/
- Create the TWS client wrapper class extending EClient and EWrapper
- Implement connection handling and the reqCurrentTime functionality
- Add basic error handling and logging

### Phase 2: Core Implementation
- Implement the main application entry point that uses the TWS client
- Add connection status tracking and reconnection logic
- Implement proper disconnection and cleanup
- Add command-line interface for running the application

### Phase 3: Integration
- Create start/stop scripts for the TWS application
- Add unit tests for the TWS client functionality
- Create E2E test documentation for validating the connection
- Document the setup and usage in comments and README updates

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Task 1: Create TWS Client Wrapper Class
- Create `app/server/__init__.py` as an empty file to make it a Python package
- Create `app/server/tws_client.py` with a `TWSClient` class that:
  - Extends both `EClient` and `EWrapper` from ibapi
  - Implements `__init__` method to initialize the connection
  - Implements `nextValidId` callback (required by IB API)
  - Implements `currentTime` callback to receive the time from TWS
  - Implements `error` callback for error handling
  - Adds a `connect_and_run` method to establish connection and start the message loop
  - Adds proper logging throughout

### Task 2: Implement Main Application Entry Point
- Create `app/server/tws_app.py` that:
  - Imports the TWSClient class
  - Sets up argument parsing for host and port (default: localhost:7500)
  - Creates an instance of TWSClient
  - Connects to TWS using the specified host and port
  - Requests current time using `reqCurrentTime()`
  - Handles the response and displays it
  - Implements graceful shutdown on Ctrl+C

### Task 3: Add Unit Tests
- Create `app/server/tests/__init__.py` as an empty file
- Create `app/server/tests/test_tws_client.py` with tests for:
  - TWSClient initialization
  - Connection method exists and is callable
  - Error callback handling
  - Mock tests for the callbacks (nextValidId, currentTime, error)

### Task 4: Create Start Script
- Create `scripts/start_tws.sh` that:
  - Activates the virtual environment
  - Runs the TWS application with default or provided arguments
  - Includes helpful usage documentation in comments

### Task 5: Create E2E Test Documentation
- Read `.claude/commands/e2e/test_basic_query.md` to understand the E2E test format
- Create `.claude/commands/e2e/test_tws_connection.md` that documents:
  - Prerequisites (TWS must be running on port 7500)
  - Step-by-step test procedure
  - Expected outputs
  - Success criteria
  - Screenshot requirements

### Task 6: Add Configuration and Documentation
- Check if `.env.sample` exists, if not create it with TWS configuration variables:
  - TWS_HOST (default: localhost)
  - TWS_PORT (default: 7500)
  - TWS_CLIENT_ID (default: 1)
- Add inline documentation and docstrings to all Python files
- Add type hints where appropriate

### Task 7: Run Validation Commands
- Execute all commands in the Validation Commands section below
- Ensure zero errors and all tests pass
- Verify the E2E test can be executed successfully

## Testing Strategy

### Unit Tests
- **Test TWSClient initialization**: Verify the client initializes with correct default values
- **Test callback registration**: Ensure all required callbacks are properly implemented
- **Test error handling**: Mock error scenarios and verify proper error callback execution
- **Test connection parameters**: Verify host, port, and client_id are correctly set
- **Test mock time response**: Mock the currentTime callback and verify it processes the response correctly

### Edge Cases
- **TWS not running**: Application should handle connection failure gracefully with clear error message
- **Invalid port**: Should fail with appropriate error message
- **Connection timeout**: Should timeout gracefully after reasonable wait period
- **Unexpected disconnection**: Should handle mid-operation disconnections
- **Multiple connection attempts**: Should prevent multiple simultaneous connections
- **Invalid host**: Should handle DNS/network errors appropriately

## Acceptance Criteria
- [ ] TWS client class successfully extends EClient and EWrapper
- [ ] Application connects to TWS on localhost:7500
- [ ] Current time is successfully retrieved from TWS server
- [ ] Current time is displayed in human-readable format with timestamp
- [ ] Connection errors are handled gracefully with informative messages
- [ ] Application can be started using the provided script
- [ ] Unit tests exist and pass with 100% success rate
- [ ] E2E test documentation is created and can be executed
- [ ] Code includes proper logging for debugging
- [ ] Application disconnects cleanly on exit
- [ ] All validation commands execute without errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run python -m pytest tests/ -v` - Run server unit tests to validate the TWS client implementation
- `cd app/server && uv run python tws_app.py --help` - Verify the application CLI is working
- `cd app/server && uv run python -m py_compile tws_app.py tws_client.py` - Verify Python syntax is correct
- `bash scripts/start_tws.sh --help` - Verify the start script exists and shows usage
- Read `.claude/commands/test/test_e2e.md` if it exists, then read and follow `.claude/commands/e2e/test_tws_connection.md` to validate TWS connection functionality (requires TWS running on port 7500)

Note: Full E2E test requires TWS application to be running. For CI/CD, consider mocking the TWS connection or using IB Gateway in paper trading mode.

## Notes
- **ibapi Library**: Already installed at version 10.30.1 in the virtual environment
- **TWS Connection**: Requires Interactive Brokers TWS or IB Gateway to be running on port 7500. For development, use paper trading mode.
- **Client ID**: Each connection needs a unique client ID. Default is 1, but can be configured for multiple connections.
- **Port Options**:
  - 7496: TWS live trading
  - 7497: TWS paper trading
  - 7500: Custom port (as specified in requirements)
  - 4001: IB Gateway live trading
  - 4002: IB Gateway paper trading
- **Message Loop**: The IB API uses a message loop that must run in a thread or the main thread. The implementation should use `client.run()` which blocks until disconnection.
- **Threading**: For a production application, consider running the EClient message loop in a separate thread to allow for non-blocking operations.
- **Future Enhancements**: This foundation enables future features like:
  - Real-time market data subscriptions
  - Order placement and management
  - Account information retrieval
  - Historical data requests
  - Contract details lookup
- **Dependencies**: Using uv for dependency management. The ibapi package is already installed globally in the venv.
