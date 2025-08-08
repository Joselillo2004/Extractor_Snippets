# Sistema de Evaluación de Efectividad de Agentes

Este documento describe el framework comprehensivo para medir la efectividad de los agentes en el proyecto Extractor Snippets.

## Índice

1. [Descripción General](#descripción-general)
2. [Métricas de Efectividad](#métricas-de-efectividad)
3. [Benchmarks Disponibles](#benchmarks-disponibles)
4. [Uso del Sistema](#uso-del-sistema)
5. [Interpretación de Resultados](#interpretación-de-resultados)
6. [Extensibilidad](#extensibilidad)

## Descripción General

El sistema de evaluación permite medir objetivamente la efectividad de los agentes LLM utilizando múltiples métricas y benchmarks especializados.

### Componentes Principales

- **`AgentEffectivenessEvaluator`**: Clase principal para ejecutar evaluaciones
- **`AgentMetrics`**: Estructura para almacenar métricas de efectividad
- **`TestCase`**: Caso de prueba individual con datos de entrada y salida esperada
- **`BenchmarkSuite`**: Conjunto de casos de prueba para evaluación
- **`StandardBenchmarks`**: Benchmarks estándar para casos comunes
- **`AdvancedBenchmarks`**: Benchmarks avanzados para casos complejos del mundo real

## Métricas de Efectividad

### Métricas de Calidad

- **Precisión**: `True Positives / (True Positives + False Positives)`
  - Mide qué tan correctos son los resultados positivos
  - Rango: 0.0 - 1.0 (mayor es mejor)

- **Recall**: `True Positives / (True Positives + False Negatives)`
  - Mide qué tan completos son los resultados
  - Rango: 0.0 - 1.0 (mayor es mejor)

- **F1-Score**: `2 × (Precisión × Recall) / (Precisión + Recall)`
  - Promedio armónico entre precisión y recall
  - Rango: 0.0 - 1.0 (mayor es mejor)

- **Accuracy**: `(TP + TN) / Total`
  - Porcentaje de predicciones correctas
  - Rango: 0.0 - 1.0 (mayor es mejor)

### Métricas de Performance

- **Tiempo Promedio de Respuesta**: Tiempo medio en completar un análisis
- **Tiempo Máximo/Mínimo**: Rangos de tiempo de respuesta
- **Desviación Estándar**: Variabilidad en tiempos de respuesta

### Métricas de Costo

- **Tokens Totales**: Número total de tokens consumidos
- **Costo Total**: Costo estimado en USD
- **Costo por Request**: Costo promedio por análisis

### Métricas de Confiabilidad

- **Tasa de Éxito**: Porcentaje de análisis completados exitosamente
- **Score de Consistencia**: Similitud entre múltiples ejecuciones del mismo test
- **Tasa de Error**: Porcentaje de fallos durante la evaluación

## Benchmarks Disponibles

### 1. Standard Benchmarks

**Benchmark: `standard`**
- Casos básicos de dependencias (variables, clases, imports)
- Tests de múltiples dependencias
- Casos sin dependencias
- Edge cases simples

**Benchmark: `stress_test`**
- Codebase grande (100+ snippets)
- Tests de límites de performance

### 2. Advanced Benchmarks

**Benchmark: `real_world`**
- Código de aplicaciones Flask con decorators
- Workflows de Data Science (pandas/numpy)
- Manejo complejo de excepciones
- Herencia múltiple
- Context managers y decorators personalizados

**Benchmark: `edge_cases`**
- Variables con nombres similares
- Redefinición de variables
- Imports con alias conflictivos
- Funciones anidadas y closures
- Código con errores sintácticos
- Comprehensions complejas

**Benchmark: `performance`**
- Tests con diferentes tamaños de codebase (10, 50, 200 snippets)
- Snippets individuales muy largos
- Nombres de variables/funciones extremadamente largos

## Uso del Sistema

### 1. Script de Línea de Comandos

```bash
# Evaluación estándar
python evaluate_agents.py --agent context_analyzer --benchmark standard

# Benchmark avanzado del mundo real
python evaluate_agents.py --agent context_analyzer --benchmark real_world

# Test de consistencia
python evaluate_agents.py --agent context_analyzer --consistency --runs 5

# Evaluación de performance
python evaluate_agents.py --agent context_analyzer --benchmark performance

# Casos edge complejos
python evaluate_agents.py --agent context_analyzer --benchmark edge_cases
```

### 2. Uso Programático

```python
from tests.agents.test_agent_effectiveness import (
    AgentEffectivenessEvaluator, 
    StandardBenchmarks
)
from src.snippets.agents import ContextAnalyzer, get_llm_client, LLMConfig

# Configurar evaluador
evaluator = AgentEffectivenessEvaluator("results")

# Crear benchmark
benchmark = StandardBenchmarks.create_context_analyzer_benchmark()

# Configurar agente
config = LLMConfig(model="llama-3.1-8b-instant")
llm_client = get_llm_client(config)
analyzer = ContextAnalyzer(llm_client)

# Ejecutar evaluación
metrics = await evaluator.evaluate_context_analyzer(analyzer, benchmark)

# Guardar reporte
report_path = evaluator.save_evaluation_report(
    metrics, benchmark.name, "context_analyzer"
)
```

### 3. Tests de Consistencia

```bash
# Test básico de consistencia (5 ejecuciones)
python evaluate_agents.py --consistency

# Test extenso de consistencia (10 ejecuciones)
python evaluate_agents.py --consistency --runs 10
```

## Interpretación de Resultados

### Scores de Calidad

| Métrica | Excelente | Bueno | Aceptable | Necesita Mejora |
|---------|----------|--------|-----------|----------------|
| Precisión | > 0.9 | 0.8-0.9 | 0.7-0.8 | < 0.7 |
| Recall | > 0.9 | 0.8-0.9 | 0.7-0.8 | < 0.7 |
| F1-Score | > 0.9 | 0.8-0.9 | 0.7-0.8 | < 0.7 |

### Performance

| Tiempo Promedio | Evaluación |
|----------------|------------|
| < 1 segundo | Excelente |
| 1-3 segundos | Bueno |
| 3-5 segundos | Aceptable |
| > 5 segundos | Lento |

### Consistencia

| Score | Interpretación |
|-------|----------------|
| > 0.95 | Muy consistente |
| 0.85-0.95 | Consistente |
| 0.70-0.85 | Moderadamente consistente |
| < 0.70 | Inconsistente |

## Reportes Generados

El sistema genera reportes en dos formatos:

### 1. JSON (datos estructurados)
```json
{
  "precision": 0.856,
  "recall": 0.923,
  "f1_score": 0.888,
  "success_rate": 0.833,
  "avg_response_time": 2.34,
  "total_tests": 6,
  "successful_tests": 5,
  ...
}
```

### 2. Markdown (reporte legible)
```markdown
# Reporte de Evaluación de Efectividad

## Agente: context_analyzer
## Benchmark: context_analyzer_standard
## Fecha: 2025-01-08 16:30:45

### Resumen Ejecutivo
- Tests ejecutados: 6
- Tests exitosos: 5
- Tests fallidos: 1
- Tasa de éxito: 83.33%

### Métricas de Calidad
| Métrica | Valor |
|---------|-------|
| Precisión | 0.856 |
| Recall | 0.923 |
| F1-Score | 0.888 |
...
```

## Extensibilidad

### Crear Nuevos Benchmarks

```python
from tests.agents.test_agent_effectiveness import TestCase, BenchmarkSuite
from src.snippets.agents import Snippet

def create_custom_benchmark() -> BenchmarkSuite:
    test_cases = [
        TestCase(
            name="my_custom_test",
            description="Descripción del test",
            complexity_level="medium",
            input_data={
                'snippet': Snippet("print(x)", 1),
                'all_snippets': [
                    Snippet("x = 42", 0),
                    Snippet("print(x)", 1)
                ],
                'snippet_index': 1
            },
            expected_output={
                'variables': {
                    'x': {'defined_in_snippet': 0}
                }
            },
            tags=["custom", "variables"]
        )
    ]
    
    return BenchmarkSuite(
        name="custom_benchmark",
        description="Mi benchmark personalizado",
        test_cases=test_cases
    )
```

### Agregar Nuevas Métricas

```python
@dataclass
class ExtendedAgentMetrics(AgentMetrics):
    custom_metric: float = 0.0
    another_metric: int = 0
```

### Evaluar Nuevos Agentes

```python
class CustomAgentEvaluator(AgentEffectivenessEvaluator):
    
    async def evaluate_my_agent(self, agent, benchmark):
        # Implementación de evaluación personalizada
        pass
```

## Mejores Prácticas

### 1. Configuración de LLM
- Usar límites de costo para evitar gastos excesivos
- Habilitar cache para tests repetitivos
- Configurar timeouts apropiados

### 2. Interpretación de Métricas
- Considerar el F1-Score como métrica principal de calidad
- Evaluar consistencia para asegurar confiabilidad
- Monitorear costos en evaluaciones extensas

### 3. Desarrollo de Benchmarks
- Incluir casos edge representativos
- Balancear complejidad (casos simples, medianos y complejos)
- Documentar expectativas claramente
- Etiquetar casos para análisis granular

### 4. Automatización
- Ejecutar evaluaciones periódicamente
- Comparar resultados entre versiones
- Establecer umbrales mínimos de calidad
- Integrar con CI/CD cuando sea posible

## Limitaciones y Consideraciones

### Limitaciones Actuales
- Evaluación limitada al Context Analyzer
- Métricas basadas en comparación exacta de claves
- No evalúa calidad semántica de dependencias detectadas
- Dependiente de la calidad de los casos de prueba definidos

### Consideraciones de Costo
- Cada evaluación consume tokens del LLM
- Benchmarks grandes pueden generar costos significativos
- Tests de consistencia requieren múltiples llamadas
- Usar limits de costo y cache para controlar gastos

### Consideraciones de Performance
- Evaluaciones grandes pueden tomar varios minutos
- El paralelismo está limitado por rate limits del LLM
- Cache mejora significativamente el rendimiento en tests repetitivos

## Futuras Mejoras

### Roadmap
1. **Métricas Semánticas**: Evaluar calidad semántica de las dependencias detectadas
2. **Evaluación de Context Builder**: Extender para evaluar el agente de construcción de contexto
3. **Benchmarks Automáticos**: Generar casos de prueba a partir de código real
4. **Análisis Comparativo**: Comparar diferentes modelos LLM
5. **Visualizaciones**: Dashboard web para visualizar resultados
6. **Integración CI/CD**: Ejecutión automática en pipeline de desarrollo
7. **Métricas de Negocio**: Correlacionar métricas técnicas con impacto en el usuario final

### Contribuciones
Para contribuir al sistema de evaluación:

1. Agregar nuevos benchmarks en `tests/agents/advanced_benchmarks.py`
2. Extender métricas en `tests/agents/test_agent_effectiveness.py`
3. Crear evaluadores especializados para nuevos agentes
4. Mejorar la documentación y ejemplos
5. Reportar bugs o limitaciones encontradas

---

*Documentación generada para el proyecto Extractor Snippets - Fecha: 2025-01-08*
