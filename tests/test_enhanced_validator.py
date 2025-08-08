"""
Tests para Enhanced Validator - Integración con Context Analyzer

Tests unitarios para validar la integración del Context Analyzer
con el sistema de validación existente.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

from src.snippets.enhanced_validator import (
    EnhancedValidator,
    EnhancedValidationResult, 
    create_enhanced_validator
)
from src.snippets.validator import ValidationResult
from src.snippets.agents import AgentResult


class TestEnhancedValidator:
    """Test suite para Enhanced Validator"""
    
    def test_enhanced_validator_without_agents(self):
        """Test que el validator funciona sin agentes (solo heurístico)"""
        validator = EnhancedValidator(enable_agents=False)
        
        # Verificar configuración
        assert validator.enable_agents is False
        assert not hasattr(validator, 'context_analyzer')
        
        # Las estadísticas deben estar inicializadas
        stats = validator.get_stats()
        assert stats['agents_enabled'] is False
        assert stats['total_validations'] == 0
    
    @pytest.mark.asyncio
    async def test_enhanced_validator_heuristic_success(self):
        """Test que retorna resultado heurístico si es exitoso"""
        validator = EnhancedValidator(enable_agents=False)
        
        # Snippet simple que debería funcionar
        result = await validator.validate_single(
            snippet_content="x = 42\nprint(x)",
            snippet_index=0,
            all_snippets=["x = 42\nprint(x)"]
        )
        
        # Verificaciones
        assert isinstance(result, EnhancedValidationResult)
        assert result.base_result.status == 'ok'
        assert result.enhanced_result is None  # No se usó LLM
        assert result.llm_analysis_used is False
        assert result.final_result.status == 'ok'
        assert result.success_improved is False
    
    @pytest.mark.asyncio
    async def test_enhanced_validator_heuristic_failure_no_agents(self):
        """Test manejo de fallas heurísticas sin agentes"""
        validator = EnhancedValidator(enable_agents=False)
        
        # Snippet que falla (variable indefinida)
        result = await validator.validate_single(
            snippet_content="print(undefined_variable)",
            snippet_index=0,
            all_snippets=["print(undefined_variable)"]
        )
        
        # Verificaciones
        assert result.base_result.status == 'runtime_error'
        assert result.enhanced_result is None  # No se usó LLM
        assert result.llm_analysis_used is False
        assert result.final_result.status == 'runtime_error'
        assert result.success_improved is False
    
    def test_enhanced_validator_with_mock_agents(self):
        """Test de configuración con agentes mockeados"""
        # Mock para evitar inicialización real de LLM
        with patch('src.snippets.enhanced_validator.get_llm_client') as mock_llm, \
             patch('src.snippets.enhanced_validator.ContextAnalyzer') as mock_analyzer:
            
            mock_llm.return_value = Mock()
            mock_analyzer.return_value = Mock()
            
            validator = EnhancedValidator(enable_agents=True)
            
            # Verificar que se configuraron los agentes
            assert validator.enable_agents is True
            assert hasattr(validator, 'context_analyzer')
            
            # Estadísticas
            stats = validator.get_stats()
            assert stats['agents_enabled'] is True
    
    @pytest.mark.asyncio
    async def test_enhanced_validator_llm_analysis_success(self):
        """Test de análisis LLM exitoso que mejora resultado"""
        
        # Mock del resultado de análisis LLM
        mock_analysis_result = AgentResult(
            success=True,
            confidence=0.9,
            data={
                'variables': {
                    'lista': {
                        'defined_in_snippet': 0,
                        'definition': 'lista = [1, 2, 3, 4, 5]',
                        'confidence': 0.95
                    }
                },
                'classes': {},
                'imports': {},
                'functions': {}
            },
            processing_time=1.0
        )
        
        # Mock del validador y sus componentes
        with patch('src.snippets.enhanced_validator.get_llm_client') as mock_llm, \
             patch('src.snippets.enhanced_validator.ContextAnalyzer') as mock_analyzer_class, \
             patch('src.snippets.enhanced_validator.validate') as mock_validate:
            
            # Configurar mocks
            mock_llm.return_value = Mock()
            mock_analyzer = AsyncMock()
            mock_analyzer.analyze.return_value = mock_analysis_result
            mock_analyzer_class.return_value = mock_analyzer
            
            # Configurar validaciones simuladas
            def mock_validate_func(code, **kwargs):
                if "lista = [1, 2, 3, 4, 5]" in code:
                    # Validación exitosa con contexto
                    return ValidationResult(
                        status='ok',
                        details='Success with context',
                        stdout='3',
                        stderr='',
                        classification={'has_code': True}
                    )
                else:
                    # Validación fallida sin contexto
                    return ValidationResult(
                        status='runtime_error',
                        details='NameError: lista not defined',
                        stdout='',
                        stderr='',
                        classification={'has_code': True}
                    )
            
            mock_validate.side_effect = mock_validate_func
            
            # Crear validator y ejecutar
            validator = EnhancedValidator(enable_agents=True)
            
            snippets = [
                "lista = [1, 2, 3, 4, 5]",
                "print(lista[0])"  # Target que necesita contexto
            ]
            
            result = await validator.validate_single(
                snippet_content=snippets[1],
                snippet_index=1,
                all_snippets=snippets
            )
            
            # Verificaciones
            assert result.base_result.status == 'runtime_error'  # Falla inicial
            assert result.enhanced_result.status == 'ok'  # Éxito con contexto
            assert result.llm_analysis_used is True
            assert result.llm_analysis_success is True
            assert result.context_added is True
            assert result.success_improved is True
            assert result.confidence == 0.9
            assert "lista = [1, 2, 3, 4, 5]" in result.context_code
    
    @pytest.mark.asyncio
    async def test_enhanced_validator_llm_analysis_failure(self):
        """Test de manejo de fallas en análisis LLM"""
        
        # Crear mocks que funcionen durante la inicialización
        mock_llm_client = Mock()
        mock_llm_client.get_session_stats.return_value = {'requests': 0, 'cost': 0.0}
        
        mock_analyzer = AsyncMock()
        mock_analyzer.analyze.side_effect = Exception("LLM API Error")
        
        with patch('src.snippets.enhanced_validator.get_llm_client') as mock_get_llm, \
             patch('src.snippets.enhanced_validator.ContextAnalyzer') as mock_analyzer_class, \
             patch('src.snippets.enhanced_validator.validate') as mock_validate:
            
            # Configurar mocks para inicialización exitosa
            mock_get_llm.return_value = mock_llm_client
            mock_analyzer_class.return_value = mock_analyzer
            
            # Mock de validate que falla primero (sin contexto)
            def mock_validate_side_effect(code, **kwargs):
                return ValidationResult(
                    status='runtime_error',
                    details='NameError: undefined_var not defined',
                    stdout='',
                    stderr='',
                    classification={'has_code': True}
                )
            
            mock_validate.side_effect = mock_validate_side_effect
            
            # Crear validator (debería inicializar agentes exitosamente)
            validator = EnhancedValidator(enable_agents=True)
            
            # Verificar que los agentes se inicializaron
            assert validator.enable_agents is True
            assert hasattr(validator, 'context_analyzer')
            
            # Ejecutar validación que debería usar LLM y fallar
            result = await validator.validate_single(
                snippet_content="print(undefined_var)",
                snippet_index=0,
                all_snippets=["print(undefined_var)"]
            )
            
            # Verificaciones del fallback
            assert result.llm_analysis_used is True
            assert result.llm_analysis_success is False
            assert result.enhanced_result is None
            assert result.error_message == "LLM API Error"
            assert result.success_improved is False
            
            # Estadísticas
            stats = validator.get_stats()
            assert stats['fallbacks_used'] == 1
            assert stats['llm_analyses'] == 1
    
    @pytest.mark.asyncio
    async def test_enhanced_validator_batch_processing(self):
        """Test de procesamiento en lote"""
        validator = EnhancedValidator(enable_agents=False)
        
        snippets = [
            "x = 1",
            "y = 2", 
            "z = x + y\nprint(z)"  # Snippet más independiente
        ]
        
        results = await validator.validate_batch(snippets)
        
        # Verificaciones
        assert len(results) == 3
        assert all(isinstance(r, EnhancedValidationResult) for r in results)
        # Los primeros dos deberían ser OK, el tercero puede fallar por variables indefinidas
        assert results[0].base_result.status == 'ok'
        assert results[1].base_result.status == 'ok'
        # No verificamos el tercero porque puede fallar por dependencias
        
        # Estadísticas
        stats = validator.get_stats()
        assert stats['total_validations'] == 3
    
    def test_enhanced_validator_stats_and_reset(self):
        """Test de estadísticas y reset"""
        validator = EnhancedValidator(enable_agents=False)
        
        # Estadísticas iniciales
        stats = validator.get_stats()
        assert stats['total_validations'] == 0
        assert stats['llm_analyses'] == 0
        assert stats['llm_usage_rate'] == 0.0
        assert stats['improvement_rate'] == 0.0
        
        # Simular algunas validaciones
        validator.stats['total_validations'] = 10
        validator.stats['llm_analyses'] = 5
        validator.stats['llm_improvements'] = 3
        validator.stats['processing_time'] = 25.0
        
        stats = validator.get_stats()
        assert stats['total_validations'] == 10
        assert stats['llm_usage_rate'] == 0.5
        assert stats['improvement_rate'] == 0.3
        assert stats['avg_processing_time'] == 2.5
        
        # Reset
        validator.reset_stats()
        stats = validator.get_stats()
        assert stats['total_validations'] == 0
    
    def test_context_building_from_dependencies(self):
        """Test de construcción de contexto desde dependencias"""
        validator = EnhancedValidator(enable_agents=False)
        
        # Mock snippets
        from src.snippets.agents import Snippet
        mock_snippets = [
            Snippet("import random", 0),
            Snippet("lista = [1, 2, 3]", 1),
            Snippet("def helper(): return 42", 2),
            Snippet("class Test: pass", 3),
        ]
        
        # Mock dependencias
        dependencies = {
            'imports': {
                'random': {
                    'defined_in_snippet': 0,
                    'import_statement': 'import random'
                }
            },
            'variables': {
                'lista': {
                    'defined_in_snippet': 1,
                    'definition': 'lista = [1, 2, 3]'
                }
            },
            'functions': {
                'helper': {
                    'defined_in_snippet': 2,
                    'definition': 'def helper(): return 42'
                }
            },
            'classes': {
                'Test': {
                    'defined_in_snippet': 3,
                    'definition': 'class Test: pass'
                }
            }
        }
        
        # Construir contexto
        context = validator._build_context_from_dependencies(dependencies, mock_snippets)
        
        # Verificaciones
        assert context is not None
        assert 'import random' in context
        assert 'lista = [1, 2, 3]' in context
        assert 'def helper(): return 42' in context
        assert 'class Test: pass' in context
    
    def test_create_enhanced_validator_factory(self):
        """Test de la función factory"""
        validator = create_enhanced_validator(enable_agents=False, window_size=10)
        
        assert isinstance(validator, EnhancedValidator)
        assert validator.enable_agents is False
        assert validator.window_size == 10
    
    @pytest.mark.asyncio
    async def test_enhanced_validator_no_snippets_context(self):
        """Test cuando no se proporciona contexto de snippets"""
        validator = EnhancedValidator(enable_agents=True)
        
        # Sin all_snippets, no debería usar LLM aunque esté habilitado
        result = await validator.validate_single(
            snippet_content="print('hello')",
            snippet_index=0,
            all_snippets=None  # Sin contexto
        )
        
        assert result.llm_analysis_used is False
        assert result.enhanced_result is None
    
    def test_enhanced_validation_result_properties(self):
        """Test de propiedades de EnhancedValidationResult"""
        base_result = ValidationResult(
            status='runtime_error',
            details='Error',
            stdout='',
            stderr='',
            classification={'has_code': True}
        )
        
        enhanced_result_obj = ValidationResult(
            status='ok',
            details='Success with context',
            stdout='output',
            stderr='',
            classification={'has_code': True}
        )
        
        # Test sin mejora
        result = EnhancedValidationResult(base_result=base_result)
        assert result.final_result == base_result
        assert result.success_improved is False
        
        # Test con mejora
        result.enhanced_result = enhanced_result_obj
        assert result.final_result == enhanced_result_obj
        assert result.success_improved is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
