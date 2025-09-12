@echo off
echo 🚀 Setting up Ollama for Free LLM Usage
echo =====================================
echo.

echo 📋 This script will help you set up Ollama (completely free LLM)
echo.

echo 1. Checking if Ollama is installed...
ollama --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama is already installed
    ollama --version
) else (
    echo ❌ Ollama not found
    echo.
    echo 📥 Please install Ollama first:
    echo    - Download from: https://ollama.ai/
    echo    - Or run: winget install Ollama.Ollama
    echo.
    pause
    exit /b 1
)

echo.
echo 2. Starting Ollama service...
ollama serve >nul 2>&1 &
timeout /t 3 /nobreak >nul

echo.
echo 3. Pulling Llama 3.2 model (this may take a few minutes)...
echo    This is a one-time download. The model will be stored locally.
ollama pull llama3.2

echo.
echo 4. Testing the setup...
py test_free_llm.py

echo.
echo ✅ Setup complete! Ollama is now ready to use.
echo.
echo 🎯 You can now run your 24-hour mailer without any API costs!
echo.
pause
