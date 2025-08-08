"""
Sistema de Evaluación de Efectividad de Agentes
===============================================

Este módulo define un framework comprehensivo para medir la efectividad
de los agentes en tareas específicas usando métricas objetivas.

Métricas de efectividad:
- Precisión: ¿Qué tan correctos son los resultados?
- Recall: ¿Qué tan completos son los resultados?
- Tiempo de respuesta: ¿Qué tan rápido responde?
- Consistencia: ¿Responde igual ante inputs similares?
- Costo: ¿Cuánto cuesta usar el agente?
- Robustez: ¿Maneja bien casos edge y errores?

Autores: Proyecto Extractor Snippets
Fecha: 2025-01-08
"""

import os
import json
import time
import pytest
import asyncio
import statistics
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Union
from pathlib import Path

from src.snippets.agents import ContextAnalyzer, Snippet, get_llm_client, LLMConfig


@dataclass
class AgentMetrics:
    """Métricas de efectividad de un agente"""
    
    # Métricas de calidad
    precision: float = 0.0      # True Positives / (TP + FP)
    recall: float = 0.0         # True Positives / (TP + FN)
    f1_score: float = 0.0       # 2 * (precision * recall) / (precision + recall)
    accuracy: float = 0.0       # (TP + TN) / Total
    
    # Métricas de performance
    avg_response_time: float = 0.0
    max_response_time: float = 0.0
    min_response_time: float = 0.0
    response_time_std: float = 0.0
    
    # Métricas de costo
    total_tokens: int = 0
    total_cost: float = 0.0
    cost_per_request: float = 0.0
    
    # Métricas de confiabilidad
    success_rate: float = 0.0
    consistency_score: float = 0.0
    error_rate: float = 0.0
    
    # Metadatos
    total_tests: int = 0
    successful_tests: int = 0
    failed_tests: int = 0
    test_results: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TestCase:
    """Caso de prueba para evaluar un agente"""
    
    name: str
    description: str
    input_data: Dict[str, Any]
    expected_output: Dict[str, Any]
    complexity_level: str = "medium"  # low, medium, high, extreme
    timeout_seconds: float = 30.0
    tags: List[str] = field(default_factory=list)
    

@dataclass 
class BenchmarkSuite:
    """Suite de benchmarks para evaluar agentes"""
    
    name: str
    description: str
    test_cases: List[TestCase] = field(default_factory=list)
    baseline_metrics: Optional[AgentMetrics] = None


class AgentEffectivenessEvaluator:
    """
    Evaluador de efectividad de agentes con métricas objetivas
    """
    
    def __init__(self, output_dir: str = "evaluation_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    async def evaluate_context_analyzer(self, 
                                       analyzer: ContextAnalyzer, 
                                       benchmark: BenchmarkSuite) -> AgentMetrics:
        """
        Evalúa la efectividad del Context Analyzer
        
        Args:
            analyzer: Instancia del Context Analyzer
            benchmark: Suite de pruebas
            
        Returns:
            Métricas de efectividad
        """
        metrics = AgentMetrics()
        response_times = []
        all_results = []
        
        for test_case in benchmark.test_cases:
            start_time = time.time()
            
            try:
                # Ejecutar análisis
                result = await analyzer.analyze(
                    snippet=test_case.input_data['snippet'],
                    all_snippets=test_case.input_data['all_snippets'],
                    snippet_index=test_case.input_data['snippet_index']
                )
                
                response_time = time.time() - start_time
                response_times.append(response_time)
                
                # Evaluar resultado
                test_result = self._evaluate_context_analyzer_result(
                    result, test_case.expected_output, test_case
                )
                test_result['response_time'] = response_time
                test_result['test_case'] = test_case.name
                
                all_results.append(test_result)
                
                if test_result['success']:
                    metrics.successful_tests += 1
                else:
                    metrics.failed_tests += 1
                    
            except Exception as e:
                response_time = time.time() - start_time
                response_times.append(response_time)
                
                test_result = {
                    'success': False,
                    'error': str(e),
                    'precision': 0.0,
                    'recall': 0.0,
                    'test_case': test_case.name,
                    'response_time': response_time
                }
                all_results.append(test_result)
                metrics.failed_tests += 1
        
        # Calcular métricas agregadas
        metrics.total_tests = len(benchmark.test_cases)
        metrics.test_results = all_results
        
        # Métricas de performance
        if response_times:
            metrics.avg_response_time = statistics.mean(response_times)
            metrics.max_response_time = max(response_times)
            metrics.min_response_time = min(response_times)
            metrics.response_time_std = statistics.stdev(response_times) if len(response_times) > 1 else 0.0
        
        # Métricas de calidad
        successful_results = [r for r in all_results if r['success']]
        if successful_results:
            metrics.precision = statistics.mean([r['precision'] for r in successful_results])
            metrics.recall = statistics.mean([r['recall'] for r in successful_results])
            metrics.f1_score = (2 * metrics.precision * metrics.recall / 
                              (metrics.precision + metrics.recall)) if (metrics.precision + metrics.recall) > 0 else 0.0
        
        # Métricas de confiabilidad
        metrics.success_rate = metrics.successful_tests / metrics.total_tests
        metrics.error_rate = metrics.failed_tests / metrics.total_tests
        
        return metrics
    
    def _evaluate_context_analyzer_result(self, 
                                        actual_result: Any, 
                                        expected: Dict[str, Any],
                                        test_case: TestCase) -> Dict[str, Any]:
        """
        Evalúa el resultado de Context Analyzer contra lo esperado
        
        Args:
            actual_result: Resultado del análisis
            expected: Resultado esperado
            test_case: Caso de prueba
            
        Returns:
            Diccionario con métricas del resultado
        """
        if not actual_result.success:
            return {
                'success': False,
                'precision': 0.0,
                'recall': 0.0,
                'error': actual_result.error
            }
        
        actual_data = actual_result.data
        
        # Contar true positives, false positives, false negatives
        tp = fp = fn = 0
        
        # Evaluar variables
        expected_vars = set(expected.get('variables', {}).keys())
        actual_vars = set(actual_data.get('variables', {}).keys())
        
        tp += len(expected_vars.intersection(actual_vars))
        fp += len(actual_vars - expected_vars)
        fn += len(expected_vars - actual_vars)
        
        # Evaluar clases
        expected_classes = set(expected.get('classes', {}).keys())
        actual_classes = set(actual_data.get('classes', {}).keys())
        
        tp += len(expected_classes.intersection(actual_classes))
        fp += len(actual_classes - expected_classes)
        fn += len(expected_classes - actual_classes)
        
        # Evaluar imports
        expected_imports = set(expected.get('imports', {}).keys())
        actual_imports = set(actual_data.get('imports', {}).keys())
        
        tp += len(expected_imports.intersection(actual_imports))
        fp += len(actual_imports - expected_imports)
        fn += len(expected_imports - actual_imports)
        
        # Calcular métricas
        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        
        return {
            'success': True,
            'precision': precision,
            'recall': recall,
            'true_positives': tp,
            'false_positives': fp,
            'false_negatives': fn,
            'confidence': actual_result.confidence
        }
    
    async def evaluate_consistency(self, 
                                  analyzer: ContextAnalyzer, 
                                  test_case: TestCase, 
                                  num_runs: int = 5) -> float:
        """
        Evalúa la consistencia del agente ejecutando el mismo test múltiples veces
        
        Args:
            analyzer: Instancia del agente
            test_case: Caso de prueba
            num_runs: Número de ejecuciones
            
        Returns:
            Score de consistencia (0.0-1.0)
        """
        results = []
        
        for _ in range(num_runs):
            try:
                result = await analyzer.analyze(
                    snippet=test_case.input_data['snippet'],
                    all_snippets=test_case.input_data['all_snippets'],
                    snippet_index=test_case.input_data['snippet_index']
                )
                
                # Normalizar resultado para comparación
                normalized = self._normalize_result_for_comparison(result)
                results.append(normalized)
                
            except Exception as e:
                results.append({'error': str(e)})
        
        # Calcular similitud entre resultados
        similarity_scores = []
        for i in range(len(results)):
            for j in range(i + 1, len(results)):
                similarity = self._calculate_result_similarity(results[i], results[j])
                similarity_scores.append(similarity)
        
        return statistics.mean(similarity_scores) if similarity_scores else 0.0
    
    def _normalize_result_for_comparison(self, result: Any) -> Dict[str, Any]:
        """Normaliza resultado para comparación de consistencia"""
        if not result.success:
            return {'error': result.error}
        
        # Extraer elementos clave para comparación
        normalized = {
            'variables': sorted(result.data.get('variables', {}).keys()),
            'classes': sorted(result.data.get('classes', {}).keys()),
            'imports': sorted(result.data.get('imports', {}).keys()),
            'functions': sorted(result.data.get('functions', {}).keys()),
            'confidence_bucket': round(result.confidence, 1)  # Agrupar por décimas
        }
        
        return normalized
    
    def _calculate_result_similarity(self, result1: Dict[str, Any], result2: Dict[str, Any]) -> float:
        """Calcula similitud entre dos resultados normalizados"""
        if 'error' in result1 or 'error' in result2:
            return 1.0 if ('error' in result1 and 'error' in result2) else 0.0
        
        similarities = []
        
        for key in ['variables', 'classes', 'imports', 'functions']:
            set1 = set(result1.get(key, []))
            set2 = set(result2.get(key, []))
            
            if not set1 and not set2:
                similarities.append(1.0)
            elif not set1 or not set2:
                similarities.append(0.0)
            else:
                intersection = len(set1.intersection(set2))
                union = len(set1.union(set2))
                similarities.append(intersection / union)
        
        # Similitud de confianza
        conf_sim = 1.0 - abs(result1.get('confidence_bucket', 0) - result2.get('confidence_bucket', 0))
        similarities.append(conf_sim)
        
        return statistics.mean(similarities)
    
    def save_evaluation_report(self, 
                              metrics: AgentMetrics, 
                              benchmark_name: str,
                              agent_name: str) -> Path:
        """
        Guarda reporte de evaluación en formato JSON y Markdown
        
        Args:
            metrics: Métricas calculadas
            benchmark_name: Nombre del benchmark
            agent_name: Nombre del agente
            
        Returns:
            Path del archivo generado
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{agent_name}_{benchmark_name}_{timestamp}"
        
        # Guardar JSON
        json_file = self.output_dir / f"{filename}.json"
        with open(json_file, 'w') as f:
            json.dump(metrics.__dict__, f, indent=2, default=str)
        
        # Generar Markdown
        md_file = self.output_dir / f"{filename}.md"
        self._generate_markdown_report(metrics, benchmark_name, agent_name, md_file)
        
        return md_file
    
    def _generate_markdown_report(self, 
                                 metrics: AgentMetrics, 
                                 benchmark_name: str,
                                 agent_name: str, 
                                 output_file: Path):
        """Genera reporte en formato Markdown"""
        
        report = f"""# Reporte de Evaluación de Efectividad
        
## Agente: {agent_name}
## Benchmark: {benchmark_name}
## Fecha: {time.strftime("%Y-%m-%d %H:%M:%S")}

### Resumen Ejecutivo

- **Tests ejecutados**: {metrics.total_tests}
- **Tests exitosos**: {metrics.successful_tests}
- **Tests fallidos**: {metrics.failed_tests}
- **Tasa de éxito**: {metrics.success_rate:.2%}

### Métricas de Calidad

| Métrica | Valor |
|---------|--------|
| **Precisión** | {metrics.precision:.3f} |
| **Recall** | {metrics.recall:.3f} |
| **F1-Score** | {metrics.f1_score:.3f} |
| **Accuracy** | {metrics.accuracy:.3f} |

### Métricas de Performance

| Métrica | Valor |
|---------|--------|
| **Tiempo promedio** | {metrics.avg_response_time:.3f}s |
| **Tiempo máximo** | {metrics.max_response_time:.3f}s |
| **Tiempo mínimo** | {metrics.min_response_time:.3f}s |
| **Desviación estándar** | {metrics.response_time_std:.3f}s |

### Métricas de Costo

| Métrica | Valor |
|---------|--------|
| **Tokens totales** | {metrics.total_tokens:,} |
| **Costo total** | ${metrics.total_cost:.4f} |
| **Costo por request** | ${metrics.cost_per_request:.4f} |

### Métricas de Confiabilidad

| Métrica | Valor |
|---------|--------|
| **Tasa de éxito** | {metrics.success_rate:.2%} |
| **Score de consistencia** | {metrics.consistency_score:.3f} |
| **Tasa de error** | {metrics.error_rate:.2%} |

### Detalles por Test Case

"""
        
        for i, result in enumerate(metrics.test_results, 1):
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            report += f"""
#### Test Case {i}: {result['test_case']}

- **Status**: {status}
- **Tiempo**: {result['response_time']:.3f}s
- **Precisión**: {result.get('precision', 'N/A')}
- **Recall**: {result.get('recall', 'N/A')}
"""
            if not result['success']:
                report += f"- **Error**: {result.get('error', 'Unknown')}\n"
        
        with open(output_file, 'w') as f:
            f.write(report)


class StandardBenchmarks:
    """
    Benchmarks estándar para evaluar agentes
    """
    
    @staticmethod
    def create_context_analyzer_benchmark() -> BenchmarkSuite:
        """Crea benchmark estándar para Context Analyzer"""
        
        test_cases = [
            # Test básico de variables
            TestCase(
                name="basic_variable_dependency",
                description="Detectar variable definida en snippet anterior",
                complexity_level="low",
                input_data={
                    'snippet': Snippet("print(lista[0])", 2),
                    'all_snippets': [
                        Snippet("import os", 0),
                        Snippet("lista = [1, 2, 3, 4, 5]", 1),
                        Snippet("print(lista[0])", 2)
                    ],
                    'snippet_index': 2
                },
                expected_output={
                    'variables': {
                        'lista': {
                            'defined_in_snippet': 1,
                            'confidence': 0.9
                        }
                    }
                },
                tags=["variables", "basic"]
            ),
            
            # Test de clases
            TestCase(
                name="class_dependency",
                description="Detectar clase definida previamente",
                complexity_level="medium",
                input_data={
                    'snippet': Snippet("student = Student('Juan')", 2),
                    'all_snippets': [
                        Snippet("import sys", 0),
                        Snippet("class Student:\n    def __init__(self, name):\n        self.name = name", 1),
                        Snippet("student = Student('Juan')", 2)
                    ],
                    'snippet_index': 2
                },
                expected_output={
                    'classes': {
                        'Student': {
                            'defined_in_snippet': 1,
                            'confidence': 0.9
                        }
                    }
                },
                tags=["classes", "medium"]
            ),
            
            # Test de imports
            TestCase(
                name="import_dependency",
                description="Detectar import usado posteriormente",
                complexity_level="low",
                input_data={
                    'snippet': Snippet("now = datetime.now()", 2),
                    'all_snippets': [
                        Snippet("import os", 0),
                        Snippet("from datetime import datetime", 1),
                        Snippet("now = datetime.now()", 2)
                    ],
                    'snippet_index': 2
                },
                expected_output={
                    'imports': {
                        'datetime': {
                            'defined_in_snippet': 1,
                            'confidence': 0.9
                        }
                    }
                },
                tags=["imports", "basic"]
            ),
            
            # Test complejo con múltiples dependencias
            TestCase(
                name="complex_multiple_dependencies",
                description="Múltiples tipos de dependencias en un snippet",
                complexity_level="high",
                input_data={
                    'snippet': Snippet("result = helper_function(lista, Student('Ana'))", 4),
                    'all_snippets': [
                        Snippet("import random", 0),
                        Snippet("lista = [1, 2, 3, 4, 5]", 1),
                        Snippet("def helper_function(items, obj):\n    return len(items)", 2),
                        Snippet("class Student:\n    def __init__(self, name):\n        self.name = name", 3),
                        Snippet("result = helper_function(lista, Student('Ana'))", 4)
                    ],
                    'snippet_index': 4
                },
                expected_output={
                    'variables': {
                        'lista': {'defined_in_snippet': 1}
                    },
                    'functions': {
                        'helper_function': {'defined_in_snippet': 2}
                    },
                    'classes': {
                        'Student': {'defined_in_snippet': 3}
                    }
                },
                tags=["complex", "multiple", "high"]
            ),
            
            # Test sin dependencias
            TestCase(
                name="no_dependencies",
                description="Snippet sin dependencias externas",
                complexity_level="low",
                input_data={
                    'snippet': Snippet("x = 42\ny = x * 2", 1),
                    'all_snippets': [
                        Snippet("import os", 0),
                        Snippet("x = 42\ny = x * 2", 1)
                    ],
                    'snippet_index': 1
                },
                expected_output={
                    'variables': {},
                    'classes': {},
                    'imports': {},
                    'functions': {}
                },
                tags=["independent", "basic"]
            ),
            
            # Test de edge case - snippet vacío
            TestCase(
                name="empty_snippet",
                description="Snippet vacío o solo comentarios",
                complexity_level="low",
                input_data={
                    'snippet': Snippet("# Solo un comentario\npass", 1),
                    'all_snippets': [
                        Snippet("lista = [1, 2, 3]", 0),
                        Snippet("# Solo un comentario\npass", 1)
                    ],
                    'snippet_index': 1
                },
                expected_output={
                    'variables': {},
                    'classes': {},
                    'imports': {},
                    'functions': {}
                },
                tags=["edge_case", "empty"]
            )
        ]
        
        return BenchmarkSuite(
            name="context_analyzer_standard",
            description="Benchmark estándar para Context Analyzer",
            test_cases=test_cases
        )
    
    @staticmethod
    def create_stress_test_benchmark() -> BenchmarkSuite:
        """Benchmark de stress test para evaluar límites"""
        
        # Generar muchos snippets para test de performance
        many_snippets = [Snippet(f"var_{i} = {i}", i) for i in range(100)]
        target_snippet = Snippet("print(var_50)", 100)
        
        test_cases = [
            TestCase(
                name="large_codebase",
                description="Análisis en codebase grande (100+ snippets)",
                complexity_level="extreme", 
                timeout_seconds=60.0,
                input_data={
                    'snippet': target_snippet,
                    'all_snippets': many_snippets + [target_snippet],
                    'snippet_index': 100
                },
                expected_output={
                    'variables': {
                        'var_50': {'defined_in_snippet': 50}
                    }
                },
                tags=["stress", "performance", "large"]
            )
        ]
        
        return BenchmarkSuite(
            name="stress_test",
            description="Tests de stress y límites de performance",
            test_cases=test_cases
        )


# Tests del evaluador
class TestAgentEffectivenessEvaluator:
    """Tests para el sistema de evaluación"""
    
    @pytest.fixture
    def evaluator(self):
        return AgentEffectivenessEvaluator("test_evaluation_results")
    
    @pytest.fixture
    def sample_benchmark(self):
        return StandardBenchmarks.create_context_analyzer_benchmark()
    
    @pytest.mark.skipif(
        not os.getenv("GROQ_API_KEY"),
        reason="Requires GROQ_API_KEY environment variable"
    )
    @pytest.mark.asyncio 
    async def test_context_analyzer_evaluation(self, evaluator, sample_benchmark):
        """Test de evaluación completa del Context Analyzer"""
        
        # Configuración para testing
        config = LLMConfig(
            model="llama-3.1-8b-instant",
            max_tokens=300,
            max_cost_per_session=1.0,
            cache_enabled=True
        )
        
        llm_client = get_llm_client(config)
        analyzer = ContextAnalyzer(llm_client, window_size=5)
        
        # Ejecutar evaluación
        metrics = await evaluator.evaluate_context_analyzer(analyzer, sample_benchmark)
        
        # Validaciones básicas
        assert metrics.total_tests > 0
        assert metrics.total_tests == len(sample_benchmark.test_cases)
        assert metrics.successful_tests + metrics.failed_tests == metrics.total_tests
        
        # Métricas de calidad
        assert 0.0 <= metrics.precision <= 1.0
        assert 0.0 <= metrics.recall <= 1.0
        assert 0.0 <= metrics.f1_score <= 1.0
        
        # Performance
        assert metrics.avg_response_time > 0.0
        assert metrics.max_response_time >= metrics.avg_response_time
        assert metrics.min_response_time <= metrics.avg_response_time
        
        # Generar reporte
        report_path = evaluator.save_evaluation_report(
            metrics, 
            sample_benchmark.name, 
            "context_analyzer"
        )
        assert report_path.exists()
        
        print(f"\nEvaluation completed!")
        print(f"Success rate: {metrics.success_rate:.2%}")
        print(f"Precision: {metrics.precision:.3f}")
        print(f"Recall: {metrics.recall:.3f}")
        print(f"F1-Score: {metrics.f1_score:.3f}")
        print(f"Avg response time: {metrics.avg_response_time:.3f}s")
        print(f"Report saved to: {report_path}")
    
    @pytest.mark.asyncio
    async def test_consistency_evaluation(self, evaluator):
        """Test de evaluación de consistencia"""
        
        if not os.getenv("GROQ_API_KEY"):
            pytest.skip("Requires GROQ_API_KEY environment variable")
        
        config = LLMConfig(model="llama-3.1-8b-instant", cache_enabled=False)  # Sin cache para test de consistencia
        llm_client = get_llm_client(config)
        analyzer = ContextAnalyzer(llm_client)
        
        # Test case simple
        test_case = TestCase(
            name="consistency_test",
            description="Test de consistencia",
            input_data={
                'snippet': Snippet("print(lista)", 1),
                'all_snippets': [
                    Snippet("lista = [1, 2, 3]", 0),
                    Snippet("print(lista)", 1)
                ],
                'snippet_index': 1
            },
            expected_output={}
        )
        
        consistency_score = await evaluator.evaluate_consistency(analyzer, test_case, num_runs=3)
        
        assert 0.0 <= consistency_score <= 1.0
        print(f"\nConsistency score: {consistency_score:.3f}")


if __name__ == "__main__":
    # Ejecutar evaluación básica si se ejecuta directamente
    asyncio.run(pytest.main([__file__, "-v"]))
