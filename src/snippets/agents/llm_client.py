"""
LLM Client - Cliente configurado para Groq API con manejo robusto de errores

Features:
- Configuración automática de Groq
- Rate limiting inteligente  
- Cache de resultados
- Fallback graceful
- Logging detallado
- Cost tracking
"""

import os
import json
import time
import hashlib
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path

import groq
from tenacity import retry, stop_after_attempt, wait_exponential
from pydantic import BaseModel, Field

# Configurar logging
logger = logging.getLogger(__name__)


@dataclass
class LLMConfig:
    """Configuración del cliente LLM"""
    model: str = "llama-3.1-8b-instant"  # Modelo activo y rápido
    temperature: float = 0.1  # Baja temperatura para consistencia
    max_tokens: int = 1000
    timeout: float = 30.0
    max_retries: int = 3
    cache_enabled: bool = True
    cache_dir: str = ".agent_cache"
    max_cost_per_session: float = 5.00  # Límite de $5 por sesión


class TokenUsage(BaseModel):
    """Tracking de uso de tokens"""
    prompt_tokens: int = 0
    completion_tokens: int = 0  
    total_tokens: int = 0
    estimated_cost: float = 0.0


class LLMResponse(BaseModel):
    """Respuesta estructurada del LLM"""
    content: str
    usage: TokenUsage
    model: str
    cached: bool = False
    processing_time: float = 0.0
    
    class Config:
        validate_assignment = True


class GroqLLMClient:
    """
    Cliente LLM especializado para Groq con features robustos
    """
    
    # Precios aproximados por 1K tokens (pueden cambiar)
    PRICING = {
        "llama-3.1-70b-versatile": 0.0002,
        "llama-3.1-8b-instant": 0.0001,
    }
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """
        Inicializar cliente Groq
        
        Args:
            config: Configuración del cliente
        """
        self.config = config or LLMConfig()
        self.session_cost = 0.0
        self.session_requests = 0
        
        # Inicializar cliente Groq
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        self.client = groq.Groq(api_key=api_key)
        
        # Configurar cache
        if self.config.cache_enabled:
            self.cache_dir = Path(self.config.cache_dir)
            self.cache_dir.mkdir(exist_ok=True)
            logger.info(f"Cache enabled: {self.cache_dir}")
        
        logger.info(f"Groq client initialized with model: {self.config.model}")
    
    def _generate_cache_key(self, prompt: str, **kwargs) -> str:
        """
        Genera una clave de cache única para la request
        
        Args:
            prompt: Prompt del LLM
            **kwargs: Parámetros adicionales
            
        Returns:
            Hash único para la cache key
        """
        cache_data = {
            "prompt": prompt,
            "model": self.config.model,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **kwargs
        }
        
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _load_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Carga respuesta desde cache
        
        Args:
            cache_key: Clave de cache
            
        Returns:
            Datos cacheados o None
        """
        if not self.config.cache_enabled:
            return None
        
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.debug(f"Cache hit: {cache_key}")
                    return data
        except Exception as e:
            logger.warning(f"Cache read error: {e}")
        
        return None
    
    def _save_to_cache(self, cache_key: str, data: Dict[str, Any]) -> None:
        """
        Guarda respuesta en cache
        
        Args:
            cache_key: Clave de cache
            data: Datos a cachear
        """
        if not self.config.cache_enabled:
            return
        
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                logger.debug(f"Cached response: {cache_key}")
        except Exception as e:
            logger.warning(f"Cache write error: {e}")
    
    def _calculate_cost(self, usage: TokenUsage) -> float:
        """
        Calcula el costo estimado de la request
        
        Args:
            usage: Información de uso de tokens
            
        Returns:
            Costo estimado en USD
        """
        price_per_1k = self.PRICING.get(self.config.model, 0.0002)
        cost = (usage.total_tokens / 1000.0) * price_per_1k
        return round(cost, 6)
    
    def _check_cost_limit(self, estimated_cost: float) -> bool:
        """
        Verifica si la request excede el límite de costo
        
        Args:
            estimated_cost: Costo estimado de la request
            
        Returns:
            True si está dentro del límite
        """
        if self.session_cost + estimated_cost > self.config.max_cost_per_session:
            logger.error(f"Cost limit exceeded: ${self.session_cost + estimated_cost:.4f} > ${self.config.max_cost_per_session}")
            return False
        return True
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _make_groq_request(self, prompt: str, system_message: str = None) -> Dict[str, Any]:
        """
        Realiza request a Groq API con retry logic
        
        Args:
            prompt: Prompt del usuario
            system_message: Mensaje del sistema opcional
            
        Returns:
            Respuesta raw de Groq
        """
        messages = []
        
        if system_message:
            messages.append({
                "role": "system",
                "content": system_message
            })
        
        messages.append({
            "role": "user", 
            "content": prompt
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                stream=False
            )
            
            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "model": response.model
            }
            
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise
    
    async def generate(self, 
                      prompt: str,
                      system_message: str = None,
                      **kwargs) -> LLMResponse:
        """
        Genera respuesta usando Groq LLM
        
        Args:
            prompt: Prompt del usuario
            system_message: Mensaje del sistema opcional
            **kwargs: Parámetros adicionales
            
        Returns:
            LLMResponse estructurada
        """
        start_time = time.time()
        
        # Generar cache key
        cache_key = self._generate_cache_key(prompt, system=system_message, **kwargs)
        
        # Intentar cargar desde cache
        cached_data = self._load_from_cache(cache_key)
        if cached_data:
            return LLMResponse(
                content=cached_data["content"],
                usage=TokenUsage(**cached_data["usage"]),
                model=cached_data["model"],
                cached=True,
                processing_time=time.time() - start_time
            )
        
        # Estimación conservadora de tokens para verificar límite
        estimated_tokens = len(prompt.split()) * 1.5  # Aproximación
        estimated_cost = (estimated_tokens / 1000.0) * self.PRICING.get(self.config.model, 0.0002)
        
        if not self._check_cost_limit(estimated_cost):
            raise ValueError(f"Request would exceed cost limit of ${self.config.max_cost_per_session}")
        
        # Hacer request a Groq
        try:
            response_data = await self._make_groq_request(prompt, system_message)
            
            # Crear TokenUsage
            usage = TokenUsage(**response_data["usage"])
            usage.estimated_cost = self._calculate_cost(usage)
            
            # Actualizar contadores de sesión
            self.session_cost += usage.estimated_cost
            self.session_requests += 1
            
            # Crear respuesta
            llm_response = LLMResponse(
                content=response_data["content"],
                usage=usage,
                model=response_data["model"],
                cached=False,
                processing_time=time.time() - start_time
            )
            
            # Guardar en cache
            self._save_to_cache(cache_key, {
                "content": llm_response.content,
                "usage": usage.dict(),
                "model": llm_response.model
            })
            
            logger.info(f"LLM response generated: {usage.total_tokens} tokens, ${usage.estimated_cost:.4f}")
            
            return llm_response
            
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise
    
    def get_session_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la sesión actual
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            "requests_made": self.session_requests,
            "total_cost": self.session_cost,
            "cost_limit": self.config.max_cost_per_session,
            "cost_remaining": self.config.max_cost_per_session - self.session_cost,
            "model": self.config.model
        }
    
    def reset_session_stats(self) -> None:
        """Resetea las estadísticas de la sesión"""
        self.session_cost = 0.0
        self.session_requests = 0
        logger.info("Session stats reset")


# Singleton para uso global
_global_llm_client: Optional[GroqLLMClient] = None


def get_llm_client(config: Optional[LLMConfig] = None) -> GroqLLMClient:
    """
    Obtiene o crea el cliente LLM global
    
    Args:
        config: Configuración opcional
        
    Returns:
        Cliente LLM configurado
    """
    global _global_llm_client
    
    if _global_llm_client is None:
        _global_llm_client = GroqLLMClient(config)
    
    return _global_llm_client
