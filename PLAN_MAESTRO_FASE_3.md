# 🚀 PLAN MAESTRO FASE 3: IMPLEMENTACIÓN SUBAGENTES LLM

## 📋 ESTADO ACTUAL Y OBJETIVO

**Proyecto**: Extractor de Snippets Python  
**Fase Actual**: Transición de Fase 2 a Fase 3  
**Success Rate Actual**: 37.4% (185/495 snippets)  
**Success Rate Objetivo**: 85%+ (420+/495 snippets)  
**Problema Principal**: 113 runtime errors por contexto faltante

---

## 🛠️ PROTOCOLO OBLIGATORIO

1. ✅ **`sequentialthinking`** para planificación estratégica
2. 🐍 **Activar entorno virtual** existente (protocolo venv)
3. 🔍 **Validar dependencias** con `brave_web_search` (anti-slopsquatting)
4. 🧪 **TDD con pytest** (tests primero, implementación después)
5. 🧠 **Actualizar memoria** tras cada hito importante
6. 📋 **Generar reporte markdown** final con métricas
7. 📢 **Comunicación clara** durante todo el proceso

---

## 📊 PLAN DETALLADO (12 PASOS CRÍTICOS)

### 🔍 FASE A: DIAGNÓSTICO Y PREPARACIÓN (Pasos 1-3)

#### Paso 1: Validación Entorno Virtual
- [ ] ✅ Detectar proyecto Python por `requirements.txt` o `*.py`
- [ ] 🔍 Verificar existencia de `venv/` en raíz del proyecto
- [ ] ⚡ Validar integridad del entorno (python.exe, pip, estructura completa)
- [ ] 🐛 Si corrupto: AVISAR problema y CONFIRMAR eliminación antes de recrear
- [ ] 🎯 Activación con validación doble: `$VIRTUAL_ENV` Y prompt `(venv)`
- [ ] 📝 **Criterio éxito**: Entorno activo y funcional al 100%

#### Paso 2: Revisión Documentación Técnica
- [ ] 📚 Revisar `PLAN_FASE_3_SUBAGENTES_LLM.md` completo
- [ ] 🎯 Validar que arquitectura de 3 subagentes está clara
- [ ] 📊 Confirmar métricas objetivo: 37.4% → 85% success rate
- [ ] 💰 Revisar límites de costo: $2-5 por ejecución completa
- [ ] 📝 **Criterio éxito**: Plan técnico 100% comprendido

#### Paso 3: Validación Dependencias Anti-Slopsquatting
- [ ] 🔍 Ejecutar `brave_web_search` para validar `groq==0.4.1`
- [ ] 🛡️ Verificar que es paquete oficial (no slopsquatting)
- [ ] 📦 Validar dependencias secundarias: `pydantic>=2.0.0`, `tenacity>=8.0.0`
- [ ] 🧪 Instalar dependencias de desarrollo: `pytest-asyncio`, `pytest-mock`
- [ ] 📝 **Criterio éxito**: Todas las dependencias validadas como seguras

### 🚀 FASE B: IMPLEMENTACIÓN GRADUAL TDD (Pasos 4-9)

#### Paso 4: Context Analyzer - Tests + Implementación
- [ ] 🧪 **TDD**: Crear `tests/agents/test_context_analyzer.py` PRIMERO
- [ ] 📋 Tests casos específicos:
  - Detección variable definida ±N snippets
  - Detección clase definida previamente
  - Identificación cadena de imports
  - Manejo ventana dinámica (±20 snippets)
- [ ] 🔨 **Implementación**: `src/snippets/agents/context_analyzer.py`
- [ ] ⚡ Integración con cliente LLM (`llm_client.py`)
- [ ] 📊 Tests de performance: tiempo < 3 segundos por análisis
- [ ] 📝 **Criterio éxito**: 100% tests passing + análisis contextual funcional

#### Paso 5: Context Analyzer - Integración
- [ ] 🔄 Integrar con pipeline actual de validación
- [ ] 🎛️ Feature flag: `enable_context_analyzer=True/False`
- [ ] 📊 Tests de integración con dataset pequeño (10 snippets)
- [ ] 🐛 Debugging y logs detallados
- [ ] 📝 **Criterio éxito**: Context Analyzer integrado sin regresiones

#### Paso 6: Context Builder - Tests + Implementación
- [ ] 🧪 **TDD**: Crear `tests/agents/test_context_builder.py` PRIMERO
- [ ] 📋 Tests casos específicos:
  - Construcción contexto mínimo para variables
  - Construcción contexto completo para clases
  - Optimización: evitar código redundante
  - Generación valores realistas
- [ ] 🔨 **Implementación**: `src/snippets/agents/context_builder.py`
- [ ] 🎯 Integración con resultados de Context Analyzer
- [ ] 📝 **Criterio éxito**: 100% tests passing + construcción contextual funcional

#### Paso 7: Context Builder - Integración
- [ ] 🔄 Integrar Context Analyzer → Context Builder pipeline
- [ ] 📊 Tests de casos complejos: cadenas de dependencias
- [ ] 💰 Monitoreo de costos: tracking tokens por snippet
- [ ] 📝 **Criterio éxito**: Pipeline A→B funcional con métricas claras

#### Paso 8: Validity Agent - Tests + Implementación
- [ ] 🧪 **TDD**: Crear `tests/agents/test_validity_agent.py` PRIMERO
- [ ] 📋 Tests casos específicos:
  - Diagnóstico necesidad de contexto
  - Evaluación completitud dependencias
  - Clasificación tipos de problemas
  - Scoring de confianza
- [ ] 🔨 **Implementación**: `src/snippets/agents/validity_agent.py`
- [ ] 🎯 Validación final del contexto construido
- [ ] 📝 **Criterio éxito**: 100% tests passing + validación inteligente funcional

#### Paso 9: Validity Agent - Integración Completa
- [ ] 🔄 Integrar pipeline completo: Context Analyzer → Context Builder → Validity Agent
- [ ] 🎛️ Feature flag maestro: `enable_llm_subagents=True/False`
- [ ] 🛡️ Fallback automático a Fase 2 si algún agente falla
- [ ] 📝 **Criterio éxito**: Los 3 subagentes funcionando en armonía

### ✅ FASE C: INTEGRACIÓN Y VALIDACIÓN (Pasos 10-12)

#### Paso 10: Tests de Integración Completos
- [ ] 🧪 Tests de integración con casos reales del dataset
- [ ] 🎯 Validación de los 113 runtime errors objetivo
- [ ] 🛡️ Tests de fallback cuando LLM falla
- [ ] 📊 Tests de performance: tiempo total < +50% vs Fase 2
- [ ] 💰 Tests de costo: mantenerse dentro de $2-5
- [ ] 📝 **Criterio éxito**: Sistema robusto bajo todas las condiciones

#### Paso 11: Ejecución Dataset Completo con Métricas
- [ ] 🎯 Ejecutar sobre los 495 snippets completos
- [ ] 📊 Métricas críticas:
  - Success rate actual vs 85% objetivo
  - Runtime errors: 113 → ≤20 esperado
  - Tiempo procesamiento total
  - Costo real vs estimado
  - Snippets rescatados por cada agente
- [ ] 📋 Comparativa detallada vs Fase 2 (37.4% baseline)
- [ ] 📝 **Criterio éxito**: Objetivos cumplidos o plan de ajuste definido

#### Paso 12: Reporte Final y Actualización Memoria
- [ ] 📋 Generar reporte markdown con:
  - Métricas antes/después detalladas
  - Análisis de costos reales
  - Casos edge detectados
  - Recomendaciones optimización
  - Lecciones aprendidas
- [ ] 🧠 Actualizar memoria con resultados específicos
- [ ] 📚 Actualizar documentación técnica
- [ ] 🎉 Plan maestro completado exitosamente
- [ ] 📝 **Criterio éxito**: Documentación completa y memoria actualizada

---

## 🎯 MÉTRICAS DE ÉXITO POR FASE

### Fase A (Preparación):
- ✅ Entorno virtual 100% funcional
- ✅ Dependencias 100% validadas como seguras
- ✅ Plan técnico 100% comprendido

### Fase B (Implementación):
- ✅ 100% tests coverage en nuevos componentes
- ✅ Context Analyzer: detección dependencias >90%
- ✅ Context Builder: construcción contexto optimizado
- ✅ Validity Agent: diagnóstico inteligente funcional
- ✅ Pipeline integrado sin regresiones

### Fase C (Validación):
- 🎯 **Success rate: 37.4% → 85%**
- 🎯 **Runtime errors: 113 → ≤20**
- 🎯 **Tiempo: +50% máximo vs Fase 2**
- 🎯 **Costo: $2-5 por dataset completo**
- 🎯 **Robustez: 100% snippets procesables (con/sin LLM)**

---

## 🛡️ ESTRATEGIA DE ROLLBACK Y MITIGACIÓN

- **Feature flags** granulares por cada subagente
- **Fallback automático** a Fase 2 (37.4% garantizado)
- **Tests de regresión** continuos
- **Logging diferenciado** para debugging rápido
- **Cache de resultados** para minimizar re-procesamiento
- **Rate limiting** para evitar límites de API
- **Timeouts configurables** para evitar bloqueos

---

## 📊 DIAGRAMA DE FLUJO DEL PROCESO

```
INPUT: snippet → [normalizer.py] → [validador.py]
  |
  ├── SUCCESS (37.4%) → ✅ Resultado ok (mantener)
  |
  └── ERROR (62.6%) → [FASE 3: LLM Subagentes]
      |
      ├── 1. Context Analyzer: Analiza dependencias
      |     |
      ├── 2. Validity Agent: Evalúa necesidad contexto
      |     |
      ├── 3. Context Builder: Construye contexto mínimo
      |     |
      └── OUTPUT: snippet mejorado → [validador.py]
          |
          ├── SUCCESS → ✅ Resultado ok (+47.6% esperado)
          |
          └── ERROR → ❌ Fallo (≤15% esperado)
```

---

## 🚨 LOGGING PARA DEBUGGING

### Niveles de Logging Implementados
- **DEBUG**: Detalles internos de procesamiento (prompts, responses)
- **INFO**: Flujo normal, decisiones, métricas
- **WARNING**: Problemas no críticos, fallbacks
- **ERROR**: Fallos recuperables, retries
- **CRITICAL**: Fallos irrecuperables

### Formato y Rotación
- **Formato**: `[TIMESTAMP] [LEVEL] [AGENT] [SNIPPET_ID] - Message`
- **Rotación**: Logs diarios con compresión
- **Ubicación**: `/logs/agents/YYYY-MM-DD.log`

---

*Documentado por: Asistente IA*  
*Fecha: 8 de Agosto, 2025*  
*Versión: 1.0*
