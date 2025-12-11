#!/bin/bash
# Quick start script for FAA Dashboard

echo "=========================================="
echo "FAA Metrics Dashboard - Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Dependencies installed successfully!"
    echo ""
    echo "Running tests..."
    python3 test_dashboard.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "Starting FAA Dashboard..."
        echo "=========================================="
        echo ""
        echo "The dashboard will open in your browser at:"
        echo "http://localhost:8501"
        echo ""
        echo "Press Ctrl+C to stop the dashboard"
        echo ""
        streamlit run faa_dashboard.py
    else
        echo "❌ Tests failed. Please check the errors above."
        exit 1
    fi
else
    echo "❌ Failed to install dependencies. Please check the errors above."
    exit 1
fi
