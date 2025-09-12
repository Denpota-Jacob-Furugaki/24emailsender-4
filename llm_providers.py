"""
LLM Provider Interface - Free alternatives to OpenAI
Supports multiple free LLM providers with a unified interface
"""

import json
import os
import requests
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class LLMResponse:
    content: str
    model: str
    provider: str
    success: bool
    error: Optional[str] = None

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_completion(self, prompt: str, system_prompt: str = None, max_tokens: int = 2000) -> LLMResponse:
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        pass

class OllamaProvider(LLMProvider):
    """Ollama local LLM provider - completely free"""
    
    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.provider_name = "Ollama"
    
    def is_available(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(model["name"].startswith(self.model) for model in models)
            return False
        except:
            return False
    
    def generate_completion(self, prompt: str, system_prompt: str = None, max_tokens: int = 2000) -> LLMResponse:
        """Generate completion using Ollama"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.1
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("message", {}).get("content", "")
                return LLMResponse(
                    content=content,
                    model=self.model,
                    provider=self.provider_name,
                    success=True
                )
            else:
                return LLMResponse(
                    content="",
                    model=self.model,
                    provider=self.provider_name,
                    success=False,
                    error=f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            return LLMResponse(
                content="",
                model=self.model,
                provider=self.provider_name,
                success=False,
                error=str(e)
            )

class HuggingFaceProvider(LLMProvider):
    """Hugging Face Inference API provider - free tier available"""
    
    def __init__(self, model: str = "microsoft/DialoGPT-medium", api_key: str = None):
        self.model = model
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.provider_name = "Hugging Face"
        self.base_url = "https://api-inference.huggingface.co/models"
    
    def is_available(self) -> bool:
        """Check if Hugging Face API is available"""
        return bool(self.api_key)
    
    def generate_completion(self, prompt: str, system_prompt: str = None, max_tokens: int = 2000) -> LLMResponse:
        """Generate completion using Hugging Face"""
        try:
            if not self.api_key:
                return LLMResponse(
                    content="",
                    model=self.model,
                    provider=self.provider_name,
                    success=False,
                    error="Hugging Face API key not found"
                )
            
            # Combine system prompt and user prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": min(max_tokens, 500),  # HF has lower limits
                    "temperature": 0.1,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                f"{self.base_url}/{self.model}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    content = result[0].get("generated_text", "")
                else:
                    content = str(result)
                
                return LLMResponse(
                    content=content,
                    model=self.model,
                    provider=self.provider_name,
                    success=True
                )
            else:
                return LLMResponse(
                    content="",
                    model=self.model,
                    provider=self.provider_name,
                    success=False,
                    error=f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            return LLMResponse(
                content="",
                model=self.model,
                provider=self.provider_name,
                success=False,
                error=str(e)
            )

class GroqProvider(LLMProvider):
    """Groq provider - very fast inference with free tier"""
    
    def __init__(self, model: str = "llama-3.3-70b-versatile", api_key: str = None):
        self.model = model
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.provider_name = "Groq"
        self.base_url = "https://api.groq.com/openai/v1"
    
    def is_available(self) -> bool:
        """Check if Groq API is available"""
        return bool(self.api_key)
    
    def generate_completion(self, prompt: str, system_prompt: str = None, max_tokens: int = 2000) -> LLMResponse:
        """Generate completion using Groq"""
        try:
            if not self.api_key:
                return LLMResponse(
                    content="",
                    model=self.model,
                    provider=self.provider_name,
                    success=False,
                    error="Groq API key not found"
                )
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.1
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return LLMResponse(
                    content=content,
                    model=self.model,
                    provider=self.provider_name,
                    success=True
                )
            else:
                return LLMResponse(
                    content="",
                    model=self.model,
                    provider=self.provider_name,
                    success=False,
                    error=f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            return LLMResponse(
                content="",
                model=self.model,
                provider=self.provider_name,
                success=False,
                error=str(e)
            )

class TogetherAIProvider(LLMProvider):
    """Together AI provider - free tier available"""
    
    def __init__(self, model: str = "meta-llama/Llama-2-7b-chat-hf", api_key: str = None):
        self.model = model
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY")
        self.provider_name = "Together AI"
        self.base_url = "https://api.together.xyz/v1"
    
    def is_available(self) -> bool:
        """Check if Together AI API is available"""
        return bool(self.api_key)
    
    def generate_completion(self, prompt: str, system_prompt: str = None, max_tokens: int = 2000) -> LLMResponse:
        """Generate completion using Together AI"""
        try:
            if not self.api_key:
                return LLMResponse(
                    content="",
                    model=self.model,
                    provider=self.provider_name,
                    success=False,
                    error="Together AI API key not found"
                )
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.1
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return LLMResponse(
                    content=content,
                    model=self.model,
                    provider=self.provider_name,
                    success=True
                )
            else:
                return LLMResponse(
                    content="",
                    model=self.model,
                    provider=self.provider_name,
                    success=False,
                    error=f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            return LLMResponse(
                content="",
                model=self.model,
                provider=self.provider_name,
                success=False,
                error=str(e)
            )

class LLMManager:
    """Manager class to handle multiple LLM providers with fallback"""
    
    def __init__(self):
        self.providers = []
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available providers in order of preference"""
        # 1. Ollama (completely free, local)
        ollama = OllamaProvider()
        if ollama.is_available():
            self.providers.append(ollama)
            print("✅ Ollama provider available")
        
        # 2. Groq (very fast, free tier)
        groq = GroqProvider()
        if groq.is_available():
            self.providers.append(groq)
            print("✅ Groq provider available")
        
        # 3. Together AI (free tier)
        together = TogetherAIProvider()
        if together.is_available():
            self.providers.append(together)
            print("✅ Together AI provider available")
        
        # 4. Hugging Face (free tier)
        hf = HuggingFaceProvider()
        if hf.is_available():
            self.providers.append(hf)
            print("✅ Hugging Face provider available")
        
        if not self.providers:
            print("❌ No LLM providers available. Please set up at least one provider.")
    
    def generate_completion(self, prompt: str, system_prompt: str = None, max_tokens: int = 2000) -> LLMResponse:
        """Generate completion using the first available provider"""
        if not self.providers:
            return LLMResponse(
                content="",
                model="none",
                provider="none",
                success=False,
                error="No LLM providers available"
            )
        
        for provider in self.providers:
            print(f"🔄 Trying {provider.provider_name}...")
            response = provider.generate_completion(prompt, system_prompt, max_tokens)
            if response.success:
                print(f"✅ Success with {provider.provider_name}")
                return response
            else:
                print(f"❌ {provider.provider_name} failed: {response.error}")
        
        # If all providers failed
        return LLMResponse(
            content="",
            model="none",
            provider="none",
            success=False,
            error="All LLM providers failed"
        )
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        return [p.provider_name for p in self.providers]

# Global instance
llm_manager = LLMManager()
