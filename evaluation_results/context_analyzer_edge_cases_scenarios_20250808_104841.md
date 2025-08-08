# Reporte de Evaluación de Efectividad
        
## Agente: context_analyzer
## Benchmark: edge_cases_scenarios
## Fecha: 2025-08-08 10:48:41

### Resumen Ejecutivo

- **Tests ejecutados**: 6
- **Tests exitosos**: 6
- **Tests fallidos**: 0
- **Tasa de éxito**: 100.00%

### Métricas de Calidad

| Métrica | Valor |
|---------|--------|
| **Precisión** | 0.558 |
| **Recall** | 0.917 |
| **F1-Score** | 0.694 |
| **Accuracy** | 0.000 |

### Métricas de Performance

| Métrica | Valor |
|---------|--------|
| **Tiempo promedio** | 0.889s |
| **Tiempo máximo** | 1.636s |
| **Tiempo mínimo** | 0.596s |
| **Desviación estándar** | 0.382s |

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


#### Test Case 1: similar_variable_names

- **Status**: ✅ PASS
- **Tiempo**: 0.871s
- **Precisión**: 0.5
- **Recall**: 1.0

#### Test Case 2: variable_redefinition

- **Status**: ✅ PASS
- **Tiempo**: 0.776s
- **Precisión**: 1.0
- **Recall**: 1.0

#### Test Case 3: conflicting_import_aliases

- **Status**: ✅ PASS
- **Tiempo**: 0.830s
- **Precisión**: 0.25
- **Recall**: 0.5

#### Test Case 4: nested_functions_closures

- **Status**: ✅ PASS
- **Tiempo**: 1.636s
- **Precisión**: 0.4
- **Recall**: 1.0

#### Test Case 5: syntactic_errors

- **Status**: ✅ PASS
- **Tiempo**: 0.625s
- **Precisión**: 1.0
- **Recall**: 1.0

#### Test Case 6: complex_comprehensions

- **Status**: ✅ PASS
- **Tiempo**: 0.596s
- **Precisión**: 0.2
- **Recall**: 1.0
