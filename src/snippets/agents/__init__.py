"""
Agents Module - Subagentes LLM para análisis contextual

Este módulo contiene los agentes especializados para Fase 3:
- Context Analyzer Agent: Análisis de dependencias contextual
- Validity Agent: Validación inteligente de necesidades (próximamente)
- Context Builder Agent: Construcción de contexto optimizado (próximamente)

Exports principales:
- ContextAnalyzer: Agent principal para análisis contextual
- BaseAgent: Clase base para todos los agentes
- Snippet: Estructura de datos para snippets
- AgentResult: Resultado estructurado de agentes
- DependencyMap: Mapa de dependencias
"""

from .base_agent import (
    BaseAgent,
    Snippet, 
    AgentResult,
    DependencyMap
)

from .context_analyzer import ContextAnalyzer

from .llm_client import (
    get_llm_client,
    GroqLLMClient,
    LLMConfig,
    LLMResponse,
    TokenUsage
)

__all__ = [
    # Base classes
    'BaseAgent',
    'Snippet',
    'AgentResult', 
    'DependencyMap',
    
    # Agents
    'ContextAnalyzer',
    
    # LLM Client
    'get_llm_client',
    'GroqLLMClient',
    'LLMConfig',
    'LLMResponse',
    'TokenUsage',
]

# Version info
__version__ = "0.1.0"
__author__ = "Asistente IA"
__description__ = "LLM-powered agents for Python code analysis"
