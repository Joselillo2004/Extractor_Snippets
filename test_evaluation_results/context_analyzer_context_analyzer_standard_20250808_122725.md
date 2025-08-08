# Reporte de Evaluación de Efectividad
        
## Agente: context_analyzer
## Benchmark: context_analyzer_standard
## Fecha: 2025-08-08 12:27:25

### Resumen Ejecutivo

- **Tests ejecutados**: 6
- **Tests exitosos**: 6
- **Tests fallidos**: 0
- **Tasa de éxito**: 100.00%

### Métricas de Calidad

| Métrica | Valor |
|---------|--------|
| **Precisión** | 0.472 |
| **Recall** | 0.917 |
| **F1-Score** | 0.623 |
| **Accuracy** | 0.000 |

### Métricas de Performance

| Métrica | Valor |
|---------|--------|
| **Tiempo promedio** | 0.001s |
| **Tiempo máximo** | 0.002s |
| **Tiempo mínimo** | 0.001s |
| **Desviación estándar** | 0.001s |

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
- **Tiempo**: 0.002s
- **Precisión**: 0.5
- **Recall**: 1.0

#### Test Case 2: class_dependency

- **Status**: ✅ PASS
- **Tiempo**: 0.001s
- **Precisión**: 0.5
- **Recall**: 1.0

#### Test Case 3: import_dependency

- **Status**: ✅ PASS
- **Tiempo**: 0.001s
- **Precisión**: 0.5
- **Recall**: 1.0

#### Test Case 4: complex_multiple_dependencies

- **Status**: ✅ PASS
- **Tiempo**: 0.002s
- **Precisión**: 0.3333333333333333
- **Recall**: 0.5

#### Test Case 5: no_dependencies

- **Status**: ✅ PASS
- **Tiempo**: 0.001s
- **Precisión**: 0.0
- **Recall**: 1.0

#### Test Case 6: empty_snippet

- **Status**: ✅ PASS
- **Tiempo**: 0.001s
- **Precisión**: 1.0
- **Recall**: 1.0
