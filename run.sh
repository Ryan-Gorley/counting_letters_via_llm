#!/bin/bash
# Activate the virtual environment and run the main Python module

VENV_DIR="$(dirname "$0")/.venv"
PYTHON="$VENV_DIR/bin/python"

if [ ! -x "$PYTHON" ]; then
    echo "Virtual environment not found or Python not executable at $PYTHON"
    echo "Please create the virtual environment first."
    echo "You may do so by running setup.sh"
    exit 1
fi

exec "$PYTHON" main.py "$@"
