#!/bin/bash
# Create a Python virtual environment and install dependencies from requirements.txt

VENV_DIR="$(dirname "$0")/.venv"
PYTHON_BIN="python3"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    $PYTHON_BIN -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists at $VENV_DIR."
fi

# Upgrade pip
"$VENV_DIR/bin/pip" install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    "$VENV_DIR/bin/pip" install -r requirements.txt
else
    echo "requirements.txt not found. Skipping dependency installation."
fi
