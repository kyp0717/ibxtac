# Feature: Req Curr Time

## Metadata
issue_number: `01`
adw_id: `01`
issue_json: `{"title": "Req Curr Time", "body": "create a base app that request the current time from TWS with frontend shadcn button that make request"}`

## Feature Description
This feature implements a base application that connects to TWS (Interactive Brokers Trader Workstation) to request the current time. The application includes a three-layer architecture: TWS client for connection, FastAPI backend for middleware, and a React frontend with shadcn/ui components. The main functionality allows users to click a button in the frontend to request the current time from TWS through the backend API.

## User Story
As a user
I want to request the current time from TWS with a simple button click
So that I can verify TWS connectivity and access real-time information

## Problem Statement
There is currently no base application infrastructure to connect to TWS and provide a user-friendly interface. Users need a way to test TWS connectivity and access real-time data through a clean web interface. The application needs to demonstrate the foundational architecture that can be extended for more complex TWS operations.

## Solution Statement
Build a three-layer web application with TWS Python client integration, FastAPI backend middleware, and React frontend with shadcn/ui components. The solution provides a simple "Get Current Time" button that demonstrates end-to-end connectivity from frontend through backend to TWS, establishing the foundation for future TWS-based features.

## Relevant Files
Use these files to implement the feature:

### TWS Layer
- `app/tws/client.py` - TWS connection client using ibapi library
- `app/tws/models.py` - Data models for TWS responses
- `app/tws/__init__.py` - Package initialization

### Backend Layer
- `app/backend/main.py` - FastAPI application startup with integrated TWS client
- `app/backend/routers/tws.py` - TWS API endpoints
- `app/backend/models.py` - Pydantic models for API responses
- `app/backend/__init__.py` - Package initialization

### Frontend Layer
- `app/frontend/src/components/TimeRequest.tsx` - Main component with shadcn button
- `app/frontend/src/lib/api.ts` - API client for backend communication
- `app/frontend/src/App.tsx` - Updated to include TimeRequest component

### Configuration and Scripts
- `pyproject.toml` - Python project configuration (migrate from requirements.txt)
- `scripts/start_app.py` - Application startup script
- `scripts/start_backend.py` - Backend-only startup script

### Testing
- `app/backend/tests/test_tws.py` - Backend TWS endpoint tests
- `app/tws/tests/test_client.py` - TWS client integration tests

### New Files
- `.claude/commands/test/e2e/req_curr_time.md` - E2E test specification for the feature
- Read `.claude/commands/test/test_e2e.md` and `.claude/commands/test/e2e/test_basic_query.md` to understand how to create an E2E test file

## Implementation Plan
### Phase 1: Foundation
Set up Python project configuration, create directory structure, and establish TWS connection capability. Install required dependencies including ibapi, fastapi, and uvicorn. Migrate from requirements.txt to pyproject.toml for modern Python dependency management.

### Phase 2: Core Implementation
Implement TWS client layer with connection handling and current time request functionality. Build FastAPI backend with integrated TWS client and API endpoint. Create React frontend component using shadcn/ui button component for user interaction.

### Phase 3: Integration
Connect all layers through API calls, implement error handling and connection status management. Add startup scripts for application deployment and ensure proper integration between TWS client, backend, and frontend layers.

## Step by Step Tasks

### Task 1: Project Configuration Setup
- Create `pyproject.toml` with project metadata and dependencies
- Migrate dependencies from `requirements.txt` to pyproject.toml
- Add ibapi, fastapi, uvicorn, pytest, and python-multipart dependencies
- Remove old requirements.txt file
- Install dependencies using `uv sync`

### Task 2: TWS Client Layer Implementation
- Create `app/tws/__init__.py` package file
- Implement `app/tws/client.py` with TWS connection and current time request
- Create `app/tws/models.py` with data models for TWS responses
- Implement connection management and error handling
- Add logging for TWS operations

### Task 3: Backend API Layer Implementation
- Create `app/backend/__init__.py` package file
- Implement `app/backend/main.py` with FastAPI application and integrated TWS client
- Create `app/backend/routers/__init__.py` package file
- Implement `app/backend/routers/tws.py` with current time endpoint
- Create `app/backend/models.py` with Pydantic response models
- Add CORS configuration for frontend integration

### Task 4: Frontend Component Development
- Use shadcn-ui-developer subagent to implement shadcn/ui components
- Create `app/frontend/src/lib/api.ts` for backend API communication
- Implement `app/frontend/src/components/TimeRequest.tsx` with shadcn button component
- Update `app/frontend/src/App.tsx` to include TimeRequest component
- Style components using shadcn/ui design system

### Task 5: Application Scripts
- Create `scripts/start_app.py` for full application startup
- Create `scripts/start_backend.py` for backend-only startup
- Implement proper process management and error handling
- Add logging and status monitoring

### Task 6: Testing Infrastructure
- Create `app/backend/tests/__init__.py` package file
- Implement `app/backend/tests/test_tws.py` with API endpoint tests
- Create `app/tws/tests/__init__.py` package file (already exists)
- Implement `app/tws/tests/test_client.py` with TWS client tests
- Add integration tests for end-to-end functionality

### Task 7: E2E Test Specification
- Create `.claude/commands/test/e2e/req_curr_time.md` based on E2E test examples
- Include user story, test steps, and success criteria
- Define screenshot requirements and verification points
- Ensure test covers full user workflow from button click to time display

### Task 8: Integration and Validation
- Test TWS connection on port 7500
- Validate API endpoints functionality
- Test frontend-backend communication
- Verify error handling and edge cases
- Ensure proper startup and shutdown procedures

## Testing
- Testing can be found in a separate plan.

## Notes
- Ensure TWS application is running on port 7500 before testing
- The ibapi package requires special installation using `scripts/install_ibapi.sh`
- Use `uv add` for all dependency management instead of pip
- Follow shadcn/ui design patterns for consistent UI components
- Implement proper error handling for TWS connection failures
- Add logging throughout all layers for debugging and monitoring
- Consider implementing connection pooling for production use
- The application serves as foundation for future TWS integration features