"""
LLM Engine for Grant-Ready Business Plan Writer.
Supports multiple Llama providers:
 - Ollama (free, local)
 - Together AI (cloud)
 - Fireworks AI (cloud)
All providers use Meta's Llama models.
"""
import json
import requests
from app.config import config
class LLMEngine:
 """Unified interface for calling Llama across different providers."""
 def __init__(self):
 self.provider = config.LLM_PROVIDER
 self._validate_config()
 def _validate_config(self):
 """Ensure the selected provider has required credentials."""
 if self.provider == "together" and not config.TOGETHER_API_KEY:
 raise ValueError(
 "TOGETHER_API_KEY is required when LLM_PROVIDER=together. "
 "Get a key at https://together.ai"
 )
 if self.provider == "fireworks" and not config.FIREWORKS_API_KEY:
 raise ValueError(
 "FIREWORKS_API_KEY is required when LLM_PROVIDER=fireworks. "
 "Get a key at https://fireworks.ai"
 )
 def generate(self, system_prompt: str, messages: list[dict]) -> str:
 """
 Generate a response from Llama.
 Args:
 system_prompt: The system-level instructions.
 messages: List of {"role": "user"|"assistant", "content": "..."} dicts.
 Returns:
 The assistant's response text.
 """
 if self.provider == "ollama":
 return self._call_ollama(system_prompt, messages)
 elif self.provider == "together":
 return self._call_together(system_prompt, messages)
 elif self.provider == "fireworks":
 return self._call_fireworks(system_prompt, messages)
 else:
 raise ValueError(f"Unknown LLM provider: {self.provider}")
 # ------------------------------------------------------------------
 # OLLAMA (Local, Free)
 # ------------------------------------------------------------------
 def _call_ollama(self, system_prompt: str, messages: list[dict]) -> str:
 """Call Llama via local Ollama instance."""
 url = f"{config.OLLAMA_BASE_URL}/api/chat"
 ollama_messages = [{"role": "system", "content": system_prompt}]
 ollama_messages.extend(messages)
 payload = {
 "model": config.OLLAMA_MODEL,
 "messages": ollama_messages,
 "stream": False,
 "options": {
 "temperature": config.TEMPERATURE,
 "num_predict": config.MAX_TOKENS,
 },
 }
 try:
 response = requests.post(url, json=payload, timeout=120)
 response.raise_for_status()
 data = response.json()
 return data["message"]["content"]
 except requests.ConnectionError:
 return (
 " Could not connect to Ollama. Make sure it's running:\n\n"
 "```bash\nollama serve\nollama pull llama3.1:8b\n```"
 )
 except Exception as e:
 return f" Ollama error: {str(e)}"
 # ------------------------------------------------------------------
 # TOGETHER AI (Cloud)
 # ------------------------------------------------------------------
 def _call_together(self, system_prompt: str, messages: list[dict]) -> str:
 """Call Llama via Together AI API."""
 url = "https://api.together.xyz/v1/chat/completions"
 api_messages = [{"role": "system", "content": system_prompt}]
 api_messages.extend(messages)
 payload = {
 "model": config.TOGETHER_MODEL,
 "messages": api_messages,
 "max_tokens": config.MAX_TOKENS,
 "temperature": config.TEMPERATURE,
 }
 headers = {
 "Authorization": f"Bearer {config.TOGETHER_API_KEY}",
 "Content-Type": "application/json",
 }
 try:
 response = requests.post(url, json=payload, headers=headers, timeout=60)
 response.raise_for_status()
 data = response.json()
 return data["choices"][0]["message"]["content"]
 except Exception as e:
 return f" Together AI error: {str(e)}"
 # ------------------------------------------------------------------
 # FIREWORKS AI (Cloud)
 # ------------------------------------------------------------------
 def _call_fireworks(self, system_prompt: str, messages: list[dict]) -> str:
 """Call Llama via Fireworks AI API."""
 url = "https://api.fireworks.ai/inference/v1/chat/completions"
 api_messages = [{"role": "system", "content": system_prompt}]
 api_messages.extend(messages)
 payload = {
 "model": config.FIREWORKS_MODEL,
 "messages": api_messages,
 "max_tokens": config.MAX_TOKENS,
 "temperature": config.TEMPERATURE,
 }
 headers = {
 "Authorization": f"Bearer {config.FIREWORKS_API_KEY}",
 "Content-Type": "application/json",
 }
 try:
 response = requests.post(url, json=payload, headers=headers, timeout=60)
 response.raise_for_status()
 data = response.json()
 return data["choices"][0]["message"]["content"]
 except Exception as e:
 return f" Fireworks AI error: {str(e)}"
# Singleton instance
engine = LLMEngine()
