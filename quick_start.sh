#!/bin/bash

# Python Code Editor - Quick Start Script
# This script helps you get started quickly

echo "🚀 Python Code Editor - Quick Start"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version is not compatible. Please install Python 3.8+ first."
    exit 1
fi

echo "✓ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp config.env.example .env
    echo "⚠️  Please edit .env file to configure Ollama API settings"
fi

# Create workspace directory if it doesn't exist
if [ ! -d "workspace" ]; then
    echo "📁 Creating workspace directory..."
    mkdir -p workspace
fi

# Run setup test
echo "🧪 Running setup tests..."
python3 test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Ensure Ollama is running: ollama serve"
    echo "2. Start the application: python3 app.py"
    echo "3. Open http://localhost:5002 in your browser"
    echo ""
    echo "To start the application now, run:"
    echo "  python3 app.py"
else
    echo ""
    echo "❌ Setup test failed. Please check the errors above."
    exit 1
fi
