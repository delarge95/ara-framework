#!/bin/bash
# ARA Framework - Environment Setup Script
# This script sets up a clean Python virtual environment with all dependencies

set -e  # Exit on error

echo "🚀 ARA Framework - Environment Setup"
echo "===================================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
REQUIRED_VERSION="3.11"

echo "📌 Python version detected: $PYTHON_VERSION"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python $REQUIRED_VERSION or higher is required"
    echo "   Current version: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python version is compatible"
echo ""

# Check if virtual environment already exists
if [ -d ".venv" ]; then
    echo "⚠️  Virtual environment .venv already exists"
    read -p "Do you want to remove it and create a new one? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing old virtual environment..."
        rm -rf .venv
    else
        echo "ℹ️  Using existing virtual environment"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment found"
fi

echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

echo ""

# Install dependencies
echo "📚 Installing dependencies..."
echo "   This may take a few minutes..."
echo ""

if [ "$1" == "--dev" ]; then
    echo "🔧 Installing development dependencies..."
    pip install -r requirements-dev.txt
else
    echo "📦 Installing core dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Installation complete!"
echo ""

# Install Playwright browsers if needed
echo "🌐 Checking Playwright browsers..."
if command -v playwright &> /dev/null; then
    echo "   Installing Playwright Chromium browser..."
    playwright install chromium
    echo "✅ Playwright browsers installed"
else
    echo "⚠️  Playwright not found. Run 'playwright install chromium' manually after activation."
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Activate the environment: source .venv/bin/activate"
echo "   2. Copy .env.example to .env: cp .env.example .env"
echo "   3. Edit .env with your API keys"
echo "   4. Run tests: pytest tests/ -v"
echo "   5. Start using: ara run 'Your research topic'"
echo ""
echo "📚 Documentation: ../README.md"
echo "🐛 Issues: https://github.com/delarge95/ara-framework/issues"
echo ""
