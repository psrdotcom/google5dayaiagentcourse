#!/bin/bash

# Agent Architectures Interactive Demo Launcher
# This script sets up and runs the interactive agent architectures demo

echo "🤖 Agent Architectures Interactive Demo"
echo "======================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "   Please install Python 3.7+ and try again."
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."

# Check if google-adk is installed
if ! python3 -c "import google.adk" &> /dev/null; then
    echo "📥 Installing required packages..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies."
        echo "   Please run: pip3 install -r requirements.txt"
        exit 1
    fi
fi

# Check if API key is set
if [ -z "$GOOGLE_API_KEY" ] && [ ! -f ".env" ]; then
    echo "🔑 GOOGLE_API_KEY not found!"
    echo ""
    echo "Please set up your Google API key:"
    echo "  1. Get an API key from: https://aistudio.google.com/app/apikey"
    echo "  2. Set it as an environment variable:"
    echo "     export GOOGLE_API_KEY='your_key_here'"
    echo "  3. Or create a .env file with:"
    echo "     GOOGLE_API_KEY=your_key_here"
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

echo "✅ Setup complete! Starting interactive demo..."
echo ""

# Run the interactive demo
python3 agent_architectures_interactive.py

echo ""
echo "👋 Thanks for trying the Agent Architectures Interactive Demo!"