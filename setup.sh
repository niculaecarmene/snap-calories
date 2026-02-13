#!/bin/bash

# SnapCalories Setup Script
# This script sets up the development environment

set -e

echo "🍽️  Setting up SnapCalories..."
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "❌ Error: Python 3.11+ required (found $python_version)"
    exit 1
fi

echo "✅ Python $python_version found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"
echo ""

# Install dev dependencies
echo "Installing dev dependencies..."
pip install -r requirements-dev.txt --quiet
echo "✅ Dev dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please edit .env and add your API keys!"
else
    echo "ℹ️  .env file already exists"
fi
echo ""

# Create temp directories
echo "Creating temporary directories..."
mkdir -p temp_images
echo "✅ Directories created"
echo ""

# Run tests
echo "Running tests..."
pytest tests/ -v --tb=short || echo "⚠️  Some tests failed (expected if .env not configured)"
echo ""

echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API credentials"
echo "2. Run: source venv/bin/activate"
echo "3. Run: uvicorn app.main:app --reload"
echo "4. Visit: http://localhost:8000/docs"
echo ""
echo "📖 See README.md for detailed instructions"
