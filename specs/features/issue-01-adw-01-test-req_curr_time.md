# Feature: Req Curr Time

## Testing Environment
- If .venv folder does not exist create one
- Check if python requirements packages are installed.  If not, installed all required python packages.
- **IMPORTANT** The ibapi python package is a special case.  This package must be installed using the file `scripts/install_ibapi.sh`.  If file does not exist, report back and stop implementation.

## Python Project Configuration

**Use pyproject.toml for all Python dependency management:**
- Never create or modify requirements.txt files
- Use `uv add <package>` to add dependencies
- Use `uv add <package> --dev` for development dependencies
- All project metadata, dependencies, and tool configurations should go in pyproject.toml
- If requirements.txt exists, migrate it to pyproject.toml and remove the old file

**Commands to use:**
```bash
# Add runtime dependency
uv add fastapi

# Add dev dependency
uv add pytest --dev

# Install all dependencies
uv sync

# Run commands
uv run python script.py
uv run pytest
```

## Testing Strategy
### Unit Tests
- **TWS Client Tests**: Test TWS connection, current time request, error handling, and connection management in isolation
- **Backend API Tests**: Test FastAPI endpoints, request/response handling, TWS client integration, and error responses
- **Frontend Component Tests**: Test TimeRequest component rendering, button interactions, API calls, and state management
- **Integration Tests**: Test end-to-end flow from frontend button click through backend to TWS and back

### Edge Cases
- TWS connection failure scenarios (TWS not running on port 7500)
- Network connectivity issues between layers
- Invalid or malformed responses from TWS
- Backend API timeout scenarios
- Frontend error state handling and user feedback
- Concurrent request handling
- TWS reconnection after disconnection
- API rate limiting and throttling

## Acceptance Criteria
- TWS client successfully connects to TWS application on port 7500
- Current time request returns valid timestamp from TWS
- FastAPI backend exposes functional `/tws/current-time` endpoint
- Frontend TimeRequest component renders with shadcn/ui button
- Button click triggers API request and displays time response
- Error states are properly handled and displayed to user
- All unit tests pass with 100% success rate
- Integration tests validate complete user workflow
- E2E test demonstrates full functionality from UI to TWS
- Application starts up properly using startup scripts
- Logging provides adequate debugging information
- CORS is properly configured for frontend-backend communication

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

Execute every command to validate the feature works correctly with zero regressions.

```bash
# Install and sync dependencies
cd /home/phage/work/ibxtac && uv sync

# Install ibapi package
cd /home/phage/work/ibxtac && ./scripts/install_ibapi.sh

# Run TWS client tests
cd /home/phage/work/ibxtac && uv run pytest app/tws/tests/ -v

# Run backend API tests
cd /home/phage/work/ibxtac && uv run pytest app/backend/tests/ -v

# Start TWS application (manual step - ensure TWS is running on port 7500)
# Note: This requires TWS to be installed and configured

# Test backend API endpoint directly
cd /home/phage/work/ibxtac && uv run python -c "
import requests
import time
time.sleep(2)  # Allow backend to start
try:
    response = requests.get('http://localhost:8000/tws/current-time')
    print(f'Status: {response.status_code}')
    print(f'Response: {response.json()}')
except Exception as e:
    print(f'Error: {e}')
"

# Start full application stack
cd /home/phage/work/ibxtac && uv run python scripts/start_app.py &

# Run E2E test to validate complete functionality
cd /home/phage/work/ibxtac && claude /claude/commands/test/test_e2e.md req_curr_time .claude/commands/test/e2e/req_curr_time.md http://localhost:5173

# Start frontend development server
cd /home/phage/work/ibxtac/app/frontend && npm run dev

# Verify frontend can communicate with backend
curl -X GET http://localhost:8000/tws/current-time

# Check application health endpoints
curl -X GET http://localhost:8000/health
curl -X GET http://localhost:5173/

# Run linting and type checking
cd /home/phage/work/ibxtac && uv run python -m black app/ --check
cd /home/phage/work/ibxtac && uv run python -m mypy app/ --ignore-missing-imports
cd /home/phage/work/ibxtac/app/frontend && npm run lint
cd /home/phage/work/ibxtac/app/frontend && npm run type-check
```

- `cd app/backend && uv run pytest` - Run server tests to validate the feature works with zero regressions

## Reference
- Read the build plan call issue-01-adw-01-build-req_curr_time.md

## Notes
- Ensure TWS application is running on port 7500 before running integration tests
- The ibapi package installation requires the special script due to licensing
- Frontend tests require the development server to be running
- Backend tests require TWS connection for integration scenarios
- E2E tests validate the complete user workflow and should capture screenshots
- Monitor logs during testing for debugging connection and API issues
- Test both success and failure scenarios to ensure robust error handling
- Validate CORS configuration allows frontend-backend communication
- Consider testing with different TWS configurations if available