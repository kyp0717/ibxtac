# Feature: <feature name>

## Testing Strategy
### Unit Tests
<describe unit tests needed for the feature>

### Edge Cases
<list edge cases that need to be tested>

## Acceptance Criteria
<list specific, measurable criteria that must be met for the feature to be considered complete>

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

<list commands you'll use to validate with 100% confidence the feature is implemented correctly with zero regressions. every command must execute without errors so be specific about what you want to run to validate the feature works as expected. Include commands to test the feature end-to-end.>

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions


## Notes
<optionally list any additional notes, future considerations, or context that are relevant to the feature that will be helpful to the developer>
