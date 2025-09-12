#!/bin/bash

echo "🚀 Setting up Ollama for Free LLM Usage"
echo "====================================="
echo

echo "📋 This script will help you set up Ollama (completely free LLM)"
echo

echo "1. Checking if Ollama is installed..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed"
    ollama --version
else
    echo "❌ Ollama not found"
    echo
    echo "📥 Please install Ollama first:"
    echo "   - macOS: brew install ollama"
    echo "   - Linux: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "   - Or download from: https://ollama.ai/"
    echo
    exit 1
fi

echo
echo "2. Starting Ollama service..."
ollama serve &
sleep 3

echo
echo "3. Pulling Llama 3.2 model (this may take a few minutes)..."
echo "   This is a one-time download. The model will be stored locally."
ollama pull llama3.2

echo
echo "4. Testing the setup..."
python3 test_free_llm.py

echo
echo "✅ Setup complete! Ollama is now ready to use."
echo
echo "🎯 You can now run your 24-hour mailer without any API costs!"
echo
