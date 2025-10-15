# Feature: <feature name>

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

- `cd app/backend && uv run pytest` - Run server tests to validate the feature works with zero regressions


## Reference
- Read the build plan call <build_plan_name>

## Notes
<optionally list any additional notes, future considerations, or context that are relevant to the feature that will be helpful to the developer>
