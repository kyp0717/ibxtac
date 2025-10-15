# Feature Planning

- Create a new plan to implement the `Feature` using the exact specified markdown `feature_build_plan.md`. 
- Create another new plan to test the `Feature` using the exact specified markdown `feature_test_plan.md`. 
- Follow the `Instructions` to create the plan use the `Relevant Files` to focus on the right files.

## Variables
- issue_number: $1
- adw_id: $2
- issue_json: $3
- build_plan_name: Create the build plan in the `specs/features` directory with filename: `issue-{issue_number}-adw-{adw_id}-build-{descriptive_name}.md`
  - Replace `{descriptive_name}` with the `title` from the issue_json.
  - Descriptive name based on the feature title (e.g., "add_auth_system", "implement_search", "create_dashboard")
- test_plan_name: Create the test plan in the `specs/features` directory with filename: `issue-{issue_number}-adw-{adw_id}-test-{descriptive_name}.md`
  - Replace `{descriptive_name}` with the `title` from the issue_json.
  - Descriptive name based on the feature title (e.g., "add_auth_system", "implement_search", "create_dashboard")

## Instructions
- IMPORTANT: You're writing a plan to implement a net new feature based on the `Feature` in python code and only python code.
- IMPORTANT: You're writing a plan to implement a net new feature based on the `Feature` that will add value to the application.
- IMPORTANT: The `Feature` describes the feature that will be implemented but remember we're not implementing a new feature, we're creating the plan that will be used to implement the feature based on the build plan specify in the `Plan Format` below.
- Research the codebase to understand existing patterns, architecture, and conventions before planning the feature.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value. Add as much detail as needed to implement the feature successfully.
- IMPORTANT: Once you have completed the build plan, create the test plan base on the test plan format 
- Use your reasoning model: THINK HARD about the feature requirements, design, and implementation approach.
- Follow existing patterns and conventions in the codebase. Don't reinvent the wheel.
- Design for extensibility and maintainability.
- If you need a new library, use `uv add` and be sure to report it in the `Notes` section of the `Plan Format`.
- Don't use decorators. Keep it simple.
- Don't create any shell scripts.
- Respect requested files in the `Relevant Files` section.
- Start your research by reading the `README.md` file.
- IMPORTANT: When build python test code, do not use mock testing strategy.  
  - Tests should be conducted when TWS app is running on a port.
- IMPORTANT: In the feature includes UI components or user interactions:
  - Add a task in the `Step by Step Tasks` section to create a separate E2E test file in `.claude/commands/test/e2e/<descriptive_name>.md` based on examples in that directory
  - Add E2E test validation to your Validation Commands section
  - IMPORTANT: When you fill out the `Plan Format: Relevant Files` section, add an instruction to read `.claude/commands/test/test_e2e.md`, and `.claude/commands/test/e2e/test_basic_query.md` to understand how to create an E2E test file. List your new E2E test file to the `Plan Format: New Files` section.
  - To be clear, we're not creating a new E2E test file, we're creating a task to create a new E2E test file in the `Plan Format` below
- IMPORTANT: When implementing frontend, follow shadcn ui design and employed the shadcn-ui-developer subagent to support the build

## Architecture
- Build the web app with three layers:
  - TWS Client:
    - Python client that will connect to TWS on port 7500
  - Backend:
    - Python fastapi layer that will server as middleware between TWS layer and frontend
    - **IMPORTANT** the main.py file in should start up the backend and the tws client. Python client should be integrated into the backend layer.
  - Frontend layer is typescript react that will interact with backenn layer.

## Relevant Files

Focus on the following files:
- `README.md` - Contains the project overview and instructions.
- `app/tws/**` - Contains the python codebase for TWS client.
- `app/backend/**` - Contains the python codebase for http server.
- `app/frontend/**` - Contains the typescript codebase for http client.
- `scripts/**` - Contains the scripts to start and stop the server + client.
- `adws/**` - Contains the AI Developer Workflow (ADW) scripts.
Ignore all other files in the codebase.

## Plan Format
- `.claude/plan_format/feature_build_plan.md
- `.claude/plan_format/feature_test_plan.md

## Feature
Extract the feature details from the `issue_json` variable (parse the JSON and use the title and body fields).

## Report

- IMPORTANT: Return exclusively the path to the plan file created and nothing else.