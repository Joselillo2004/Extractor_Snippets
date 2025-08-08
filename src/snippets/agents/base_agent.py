"""
Base Agent Class - Clase abstracta para todos los agentes LLM

Esta clase define la interfaz común que deben implementar todos los subagentes:
- Context Analyzer Agent
- Validity Agent  
- Context Builder Agent
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
import logging
import asyncio
import time

# Configurar logging para agentes
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s'
)


@dataclass
class Snippet:
    """Estructura de datos para un snippet de código"""
    content: str
    index: int
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if not isinstance(self.content, str):
            raise ValueError("Snippet content must be string")
        if not isinstance(self.index, int) or self.index < 0:
            raise ValueError("Snippet index must be non-negative integer")


class DependencyMap(BaseModel):
    """Mapa estructurado de dependencias encontradas"""
    variables: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    classes: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    imports: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    functions: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    processing_time: float = Field(default=0.0, ge=0.0)
    error: Optional[str] = Field(default=None)
    
    class Config:
        """Configuración de Pydantic"""
        validate_assignment = True


class AgentResult(BaseModel):
    """Resultado base que retornan todos los agentes"""
    success: bool = Field(default=True)
    data: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    processing_time: float = Field(default=0.0, ge=0.0)
    error: Optional[str] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        """Configuración de Pydantic"""
        validate_assignment = True


class BaseAgent(ABC):
    """
    Clase base abstracta para todos los agentes LLM
    
    Proporciona funcionalidad común:
    - Logging estructurado
    - Manejo de errores
    - Medición de tiempo
    - Validación de entrada
    - Fallback graceful
    """
    
    def __init__(self, 
                 llm_client: Any,
                 agent_name: str,
                 max_retries: int = 3,
                 timeout_seconds: float = 30.0):
        """
        Initialize base agent
        
        Args:
            llm_client: Cliente LLM configurado (Groq, OpenAI, etc.)
            agent_name: Nombre del agente para logging
            max_retries: Número máximo de reintentos
            timeout_seconds: Timeout para operaciones
        """
        self.llm_client = llm_client
        self.agent_name = agent_name
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        
        # Configure logger específico para este agente
        self.logger = logging.getLogger(f"agents.{agent_name}")
        self.logger.info(f"Agent {agent_name} initialized")
    
    @abstractmethod
    async def analyze(self, 
                     snippet: Snippet,
                     all_snippets: List[Snippet],
                     snippet_index: int,
                     **kwargs) -> AgentResult:
        """
        Método abstracto que debe implementar cada agente
        
        Args:
            snippet: Snippet actual a analizar
            all_snippets: Lista completa de snippets
            snippet_index: Índice del snippet actual
            **kwargs: Argumentos adicionales específicos del agente
            
        Returns:
            AgentResult con los resultados del análisis
        """
        pass
    
    async def _measure_execution_time(self, coro) -> tuple[Any, float]:
        """
        Mide el tiempo de ejecución de una corrutina
        
        Args:
            coro: Corrutina a ejecutar
            
        Returns:
            Tupla (resultado, tiempo_en_segundos)
        """
        start_time = time.time()
        try:
            result = await coro
            end_time = time.time()
            return result, end_time - start_time
        except Exception as e:
            end_time = time.time()
            self.logger.error(f"Execution failed after {end_time - start_time:.2f}s: {e}")
            raise
    
    async def _with_timeout_and_retry(self, coro) -> Any:
        """
        Ejecuta una corrutina con timeout y retry logic
        
        Args:
            coro: Corrutina a ejecutar
            
        Returns:
            Resultado de la corrutina
            
        Raises:
            Exception: Si fallan todos los reintentos
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return await asyncio.wait_for(coro, timeout=self.timeout_seconds)
            except asyncio.TimeoutError:
                last_exception = f"Timeout after {self.timeout_seconds}s"
                self.logger.warning(f"Attempt {attempt + 1} timed out")
            except Exception as e:
                last_exception = str(e)
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
            
            if attempt < self.max_retries - 1:
                # Exponential backoff
                await asyncio.sleep(2 ** attempt)
        
        # Todos los reintentos fallaron
        raise Exception(f"All {self.max_retries} attempts failed. Last error: {last_exception}")
    
    def _validate_inputs(self, 
                        snippet: Snippet,
                        all_snippets: List[Snippet],
                        snippet_index: int) -> bool:
        """
        Valida las entradas comunes a todos los agentes
        
        Args:
            snippet: Snippet a validar
            all_snippets: Lista de snippets a validar
            snippet_index: Índice a validar
            
        Returns:
            bool: True si todas las validaciones pasan
            
        Raises:
            ValueError: Si alguna validación falla
        """
        if not isinstance(snippet, Snippet):
            raise ValueError("snippet must be Snippet instance")
        
        if not isinstance(all_snippets, list):
            raise ValueError("all_snippets must be list")
        
        if not all(isinstance(s, Snippet) for s in all_snippets):
            raise ValueError("All items in all_snippets must be Snippet instances")
        
        if not isinstance(snippet_index, int) or snippet_index < 0:
            raise ValueError("snippet_index must be non-negative integer")
        
        if snippet_index >= len(all_snippets):
            raise ValueError("snippet_index out of range")
        
        # Verificar que el snippet corresponde al índice
        if all_snippets[snippet_index].index != snippet.index:
            raise ValueError("Snippet index mismatch")
        
        return True
    
    def _create_fallback_result(self, error_msg: str) -> AgentResult:
        """
        Crea un resultado de fallback cuando el análisis falla
        
        Args:
            error_msg: Mensaje de error
            
        Returns:
            AgentResult con valores seguros de fallback
        """
        return AgentResult(
            success=False,
            data={},
            confidence=0.0,
            processing_time=0.0,
            error=error_msg,
            metadata={'fallback': True, 'agent': self.agent_name}
        )
    
    def _calculate_window_indices(self, 
                                 target_index: int,
                                 total_snippets: int,
                                 window_size: int) -> List[int]:
        """
        Calcula los índices de snippets dentro de la ventana de análisis
        
        Args:
            target_index: Índice del snippet objetivo
            total_snippets: Número total de snippets
            window_size: Tamaño de la ventana (±N snippets)
            
        Returns:
            Lista de índices a analizar
        """
        start_idx = max(0, target_index - window_size)
        end_idx = min(total_snippets, target_index + window_size + 1)
        
        indices = list(range(start_idx, end_idx))
        self.logger.debug(f"Window for index {target_index}: {indices}")
        
        return indices
    
    async def health_check(self) -> bool:
        """
        Verifica que el agente esté funcionando correctamente
        
        Returns:
            bool: True si el agente está healthy
        """
        try:
            # Test básico del cliente LLM
            if hasattr(self.llm_client, 'chat'):
                self.logger.info(f"Agent {self.agent_name} health check passed")
                return True
            else:
                self.logger.error(f"Agent {self.agent_name} missing LLM client")
                return False
        except Exception as e:
            self.logger.error(f"Agent {self.agent_name} health check failed: {e}")
            return False
