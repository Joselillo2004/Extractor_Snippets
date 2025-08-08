# Reporte de Evaluación de Efectividad
        
## Agente: context_analyzer
## Benchmark: context_analyzer_standard
## Fecha: 2025-08-08 10:48:05

### Resumen Ejecutivo

- **Tests ejecutados**: 6
- **Tests exitosos**: 6
- **Tests fallidos**: 0
- **Tasa de éxito**: 100.00%

### Métricas de Calidad

| Métrica | Valor |
|---------|--------|
| **Precisión** | 0.464 |
| **Recall** | 1.000 |
| **F1-Score** | 0.634 |
| **Accuracy** | 0.000 |

### Métricas de Performance

| Métrica | Valor |
|---------|--------|
| **Tiempo promedio** | 0.933s |
| **Tiempo máximo** | 1.748s |
| **Tiempo mínimo** | 0.472s |
| **Desviación estándar** | 0.504s |

### Métricas de Costo

| Métrica | Valor |
|---------|--------|
| **Tokens totales** | 0 |
| **Costo total** | $0.0000 |
| **Costo por request** | $0.0000 |

### Métricas de Confiabilidad

| Métrica | Valor |
|---------|--------|
| **Tasa de éxito** | 100.00% |
| **Score de consistencia** | 0.000 |
| **Tasa de error** | 0.00% |

### Detalles por Test Case


#### Test Case 1: basic_variable_dependency

- **Status**: ✅ PASS
- **Tiempo**: 1.748s
- **Precisión**: 0.5
- **Recall**: 1.0

#### Test Case 2: class_dependency

- **Status**: ✅ PASS
- **Tiempo**: 0.472s
- **Precisión**: 0.5
- **Recall**: 1.0

#### Test Case 3: import_dependency

- **Status**: ✅ PASS
- **Tiempo**: 1.331s
- **Precisión**: 0.5
- **Recall**: 1.0

#### Test Case 4: complex_multiple_dependencies

- **Status**: ✅ PASS
- **Tiempo**: 0.718s
- **Precisión**: 0.2857142857142857
- **Recall**: 1.0

#### Test Case 5: no_dependencies

- **Status**: ✅ PASS
- **Tiempo**: 0.819s
- **Precisión**: 0.0
- **Recall**: 1.0

#### Test Case 6: empty_snippet

- **Status**: ✅ PASS
- **Tiempo**: 0.512s
- **Precisión**: 1.0
- **Recall**: 1.0
