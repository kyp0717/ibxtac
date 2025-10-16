# Check and Build Virtual Environment using UV
- Check for Python UV virtual environment.
- If there none, build one in the current directory or project.

## Check for uv virtual env and dependencies
```bash
# Check for .venv directory (default UV environment location)
if [ -d ".venv" ]; then
    echo "✅ UV environment found at .venv/"
    echo ""
    echo "Environment details:"
    ls -la .venv/ | head -5
    echo ""
    
    # Check Python version in the environment
    if [ -f ".venv/bin/python" ]; then
        echo "Python version:"
        .venv/bin/python --version
    elif [ -f ".venv/Scripts/python.exe" ]; then
        echo "Python version:"
        .venv/Scripts/python.exe --version
    fi
    
    # Check if environment is activated
    if [ "$VIRTUAL_ENV" = "$(pwd)/.venv" ]; then
        echo ""
        echo "📍 Environment is currently ACTIVATED"
    else
        echo ""
        echo "⚠️  Environment exists but is NOT activated"
        echo "To activate, run: source .venv/bin/activate"
    fi
else
    echo "❌ No UV environment found at .venv/"
    echo ""
    echo "To create one, run: uv venv"
fi

echo ""

# Check for pyproject.toml (UV project file)
if [ -f "pyproject.toml" ]; then
    echo "📦 Found pyproject.toml"
    echo "Dependencies defined:"
    grep -A 10 "^\[project\]" pyproject.toml 2>/dev/null || echo "No [project] section found"
else
    echo "📄 No pyproject.toml found"
fi

echo ""

## Check for uv.lock file
if [ -f "uv.lock" ]; then
    echo "🔒 Found uv.lock file"
    echo "Lock file size: $(ls -lh uv.lock | awk '{print $5}')"
else
    echo "🔓 No uv.lock file found"
fi

echo ""

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "✅ UV is installed"
    echo "UV version: $(uv --version)"
else
    echo "❌ UV is not installed"
    echo "To install: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

### Run ibapi package check
# Check for TWS IBAPI Python package
echo "Checking TWS IBAPI Python package..."
if python -c "import ibapi" 2>/dev/null; then
    echo "✅ IBAPI Python package is installed"
    python -c "import ibapi; import os; print(f'IBAPI location: {os.path.dirname(ibapi.__file__)}')"
else
    echo "❌ IBAPI Python package is not installed"
    echo ""
    
    # Check if install script exists and offer to run it
    if [ -f "scripts/install_ibapi.sh" ]; then
        echo "📦 Found install_ibapi.sh script"
        echo "Installing IBAPI..."
        echo ""
        
        # Run the installation script
        bash scripts/install_ibapi.sh
        
        # Check again after installation
        if python -c "import ibapi" 2>/dev/null; then
            echo ""
            echo "✅ IBAPI successfully installed!"
        else
            echo ""
            echo "⚠️  IBAPI installation may have failed. Please check the output above."
            echo "You can manually run: bash scripts/install_ibapi.sh"
        fi
    else
        echo "⚠️  Install script not found at scripts/install_ibapi.sh"
        echo "Please ensure you have the TWS API installed manually."
    fi
fi
```

## Report

Environment check complete. The script will show:
- Whether a .venv directory exists
- Python version in the environment
- Whether the environment is activated
- Presence of pyproject.toml and uv.lock files
- Whether UV itself is installed
- Whether TWS IBAPI Python package is installed (and auto-install if missing)