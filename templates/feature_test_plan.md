# Feature: <feature name>

## Metadata
- issue_number: `{issue_number}`
- adw_id: `{adw_id}`
- issue_json: `{issue_json}`
- build_plan_name: `{build_plan_name}`
- test_plan_name: `{test_plan_name}`
## Testing Environment
- Testing virtual environment should already exist.
- If not, run setup.md slash command to create virtual env for testing.
- 
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
<describe unit tests needed for the feature>

### Edge Cases
<list edge cases that need to be tested>

## Acceptance Criteria
<list specific, measurable criteria that must be met for the feature to be considered complete>

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

<Your last step should be running the `Validation Commands` to validate the feature works correctly with zero regressions.>
Execute every command to validate the feature works correctly with zero regressions.

<list commands you'll use to validate with 100% confidence the feature is implemented correctly with zero regressions. every command must execute without errors so be specific about what you want to run to validate the feature works as expected. Include commands to test the feature end-to-end.>


## Reference
- Read the build plan call <build_plan_name>

## Notes
<optionally list any additional notes, future considerations, or context that are relevant to the feature that will be helpful to the developer>
