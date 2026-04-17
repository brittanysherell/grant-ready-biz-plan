"""
Configuration management for Grant-Ready Business Plan Writer.
Loads settings from environment variables or .env file.
"""
import os
from dotenv import load_dotenv
load_dotenv()
class Config:
 """Application configuration loaded from environment."""
 # LLM Provider
 LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")
 # Ollama settings
 OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
 OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
 # Together AI settings
 TOGETHER_API_KEY: str = os.getenv("TOGETHER_API_KEY", "")
 TOGETHER_MODEL: str = os.getenv(
 "TOGETHER_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
 )
 # Fireworks AI settings
 FIREWORKS_API_KEY: str = os.getenv("FIREWORKS_API_KEY", "")
 FIREWORKS_MODEL: str = os.getenv(
 "FIREWORKS_MODEL", "accounts/fireworks/models/llama-v3p1-8b-instruct"
 )
 # App settings
 APP_TITLE: str = os.getenv("APP_TITLE", "Grant-Ready Business Plan Writer")
 APP_SUBTITLE: str = os.getenv(
 "APP_SUBTITLE", "Your AI-powered guide to a professional business plan"
 )
 DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
 # Generation parameters
 MAX_TOKENS: int = 2048
 TEMPERATURE: float = 0.7
config = Config()
