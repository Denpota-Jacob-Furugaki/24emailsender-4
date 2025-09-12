# Free LLM Setup Guide

This guide will help you set up free alternatives to OpenAI for your 24-hour mailer project.

## 🎯 Why Use Free LLMs?

- **No API costs** - Completely free to use
- **No rate limits** - Use as much as you want
- **Privacy** - Your data stays local (with Ollama)
- **Reliability** - No dependency on external billing

## 🚀 Quick Start (Recommended: Ollama)

### Option 1: Ollama (Completely Free, Local)

**Best for**: Privacy, unlimited usage, no internet required

1. **Install Ollama**:
   - Windows: Download from https://ollama.ai/
   - Mac: `brew install ollama`
   - Linux: `curl -fsSL https://ollama.ai/install.sh | sh`

2. **Pull a model**:
   ```bash
   ollama pull llama3.2
   # or for a smaller model:
   ollama pull llama3.2:1b
   ```

3. **Start Ollama** (if not auto-started):
   ```bash
   ollama serve
   ```

4. **Test it**:
   ```bash
   py test_free_llm.py
   ```

**That's it!** No API keys needed. Ollama runs locally on your machine.

---

## 🌐 Cloud Options (Free Tiers)

### Option 2: Groq (Very Fast)

**Best for**: Speed, good free tier

1. **Sign up**: https://console.groq.com/
2. **Get API key**: Go to API Keys section
3. **Add to .env**:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Option 3: Together AI

**Best for**: Good models, generous free tier

1. **Sign up**: https://api.together.xyz/
2. **Get API key**: Go to API Keys section
3. **Add to .env**:
   ```
   TOGETHER_API_KEY=your_together_api_key_here
   ```

### Option 4: Hugging Face

**Best for**: Many model options

1. **Sign up**: https://huggingface.co/
2. **Get API token**: https://huggingface.co/settings/tokens
3. **Add to .env**:
   ```
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   ```

---

## 🧪 Testing Your Setup

Run the test script to verify everything works:

```bash
py test_free_llm.py
```

This will:
- Test each provider individually
- Test the LLM manager with fallback
- Test the real company generator
- Show you which providers are available

---

## 🔧 Configuration

### Environment Variables

Copy `env.example` to `.env` and configure:

```bash
# Choose one or more providers:

# Ollama (no API key needed)
# Just install Ollama and pull a model

# Groq
GROQ_API_KEY=your_groq_api_key_here

# Together AI
TOGETHER_API_KEY=your_together_api_key_here

# Hugging Face
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

### Provider Priority

The system tries providers in this order:
1. **Ollama** (local, fastest)
2. **Groq** (very fast cloud)
3. **Together AI** (good cloud option)
4. **Hugging Face** (fallback)

---

## 🎯 Usage Examples

### Generate Companies

```python
from real_companies import RealCompanyGenerator

generator = RealCompanyGenerator()
companies = generator.generate_real_companies(
    "gaming companies in Japan, esports, mobile games", 
    10
)
```

### Direct LLM Usage

```python
from llm_providers import llm_manager

response = llm_manager.generate_completion(
    "Find 5 tech companies in Japan",
    system_prompt="You are a business research assistant."
)

if response.success:
    print(f"Response from {response.provider}: {response.content}")
```

---

## 🚨 Troubleshooting

### Ollama Issues

**"Ollama not available"**:
- Make sure Ollama is installed: `ollama --version`
- Start Ollama: `ollama serve`
- Pull a model: `ollama pull llama3.2`

**"Model not found"**:
- List models: `ollama list`
- Pull the model: `ollama pull llama3.2`

### API Key Issues

**"API key not found"**:
- Check your `.env` file exists
- Verify the API key is correct
- Make sure there are no extra spaces

**"Rate limit exceeded"**:
- Wait a few minutes and try again
- Consider using Ollama for unlimited usage

### Performance Issues

**Slow responses**:
- Use Groq for fastest cloud responses
- Use Ollama for local, unlimited usage
- Reduce `max_tokens` parameter

---

## 💡 Tips

1. **Start with Ollama** - It's completely free and works offline
2. **Use multiple providers** - The system will fallback automatically
3. **Test first** - Run `py test_free_llm.py` before using in production
4. **Monitor usage** - Cloud providers have free tier limits

---

## 🔄 Migration from OpenAI

Your existing code will work without changes! The system automatically:

- Detects available providers
- Falls back to working providers
- Uses the same interface as before

Just remove your `OPENAI_API_KEY` from `.env` and set up one of the free providers above.

---

## 📞 Support

If you run into issues:

1. Run the test script: `py test_free_llm.py`
2. Check the error messages
3. Verify your setup using this guide
4. Try a different provider

The system is designed to be robust and will work with any available provider!
