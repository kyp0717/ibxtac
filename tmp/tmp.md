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

This ensures I'll always use the modern pyproject.toml standard instead of legacy requirements.txt files.