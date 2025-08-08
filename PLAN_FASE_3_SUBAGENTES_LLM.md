# 🚀 PLAN FASE 3: SUBAGENTES LLM PARA ANÁLISIS CONTEXTUAL

## 📋 RESUMEN EJECUTIVO

**Proyecto**: Extractor de Snippets Python  
**Fase**: 3 - Enriquecimiento con Inteligencia Artificial  
**Objetivo**: Elevar success rate de 37.4% a 85%+ mediante subagentes LLM especializados  
**Estado Actual**: Fase 2 completada exitosamente  
**Target**: Resolver 113 runtime errors restantes mediante análisis contextual inteligente

---

## 🎯 SITUACIÓN ACTUAL (POST-FASE 2)

### ✅ **Logros Conseguidos**
- **185 snippets exitosos** de 495 total (37.4% success rate)
- **95% reducción** en errores sintácticos (257 → 13)
- **Sistema de normalización** robusto implementado
- **Pipeline estable** con parser + validador + sandbox

### 🎯 **Problemas Pendientes**
- **113 runtime errors** por contexto faltante
  - `NameError: name 'var1' is not defined`
  - `NameError: name 'Student' is not defined`  
  - `ModuleNotFoundError: No module named 'xyz'`
- **Dependencias complejas** entre snippets distantes
- **Contexto distribuido** a lo largo del archivo de referencia

---

## 🧠 CONCEPTO: SUBAGENTES LLM ESPECIALIZADOS

### **Problema Central**
Las heurísticas simples no pueden capturar dependencias semánticas complejas entre snippets que están separados por decenas o cientos de líneas en el archivo fuente.

### **Solución Propuesta**
Arquitectura de **subagentes LLM especializados** que trabajen en conjunto para:
1. **Analizar contexto** de snippets aledaños
2. **Validar coherencia** semántica  
3. **Construir contexto** específico y optimizado

---

## 🤖 ARQUITECTURA DE SUBAGENTES

### **1. Context Analyzer Agent**
```python
Responsabilidad: Análisis de contexto distributivo
Input: Snippet actual + ventana de snippets (±N posiciones)
Output: Mapa de dependencias (variables, clases, imports, funciones)

Casos de uso:
- Detectar variable 'lista' definida en snippet #45 para uso en #47
- Encontrar clase 'Student' definida en snippet #125 para #127
- Identificar imports establecidos en snippets anteriores
```

### **2. Validity Agent** 
```python
Responsabilidad: Diagnóstico de validez inteligente
Input: Snippet + análisis de contexto
Output: Diagnóstico detallado + confianza + recomendaciones

Capacidades:
- Determinar si snippet necesita contexto adicional
- Evaluar completitud de dependencias
- Clasificar tipos de problemas detectados
```

### **3. Context Builder Agent**
```python
Responsabilidad: Construcción de contexto optimizado
Input: Diagnóstico + contexto disponible
Output: Código de contexto mínimo y funcional

Optimizaciones:
- Contexto mínimo necesario (no redundante)
- Valores realistas para variables
- Imports solo cuando realmente se usan
```

---

## 💡 CASOS DE USO ESPECÍFICOS

### **Ejemplo 1: Variable Definida Anteriormente**
```python
# Snippet #45: lista = [1, 2, 3, 4, 5]
# ...intervalo de snippets...
# Snippet #47: print(lista[0])  # ← FALLA: NameError: 'lista' not defined

Context Analyzer → Escanea ±20 snippets, encuentra 'lista' en #45
Validity Agent → Confirma que necesita contexto de lista
Context Builder → Genera: lista = [1, 2, 3, 4, 5]
Resultado → Snippet ejecuta exitosamente
```

### **Ejemplo 2: Clase Definida Previamente**
```python
# Snippet #125: class Student:
#                   def __init__(self, name): self.name = name
# ...intervalo...  
# Snippet #127: student = Student("Juan")  # ← FALLA: NameError: 'Student'

Context Analyzer → Encuentra definición completa de Student en #125
Context Builder → Incluye clase completa con métodos
Resultado → Instanciación exitosa
```

### **Ejemplo 3: Cadena de Dependencias**
```python
# Snippet #200: import random
# Snippet #201: def roll_dice(): return random.randint(1,6)
# Snippet #203: result = roll_dice()  # ← FALLA: múltiples dependencias

Context Analyzer → Detecta cadena import → función → uso
Context Builder → Construye contexto completo con import + función
Resultado → Ejecución completa exitosa
```

---

## 🏗️ IMPLEMENTACIÓN TÉCNICA

### **Estructura de Módulos**
```
src/snippets/agents/
├── __init__.py
├── base_agent.py          # Clase base abstracta
├── context_analyzer.py    # Context Analyzer Agent
├── validity_agent.py      # Validity Agent  
├── context_builder.py     # Context Builder Agent
├── llm_client.py         # Cliente Groq configurado
└── prompt_templates/      # Templates de prompts
    ├── context_analysis.txt
    ├── validity_check.txt
    └── context_building.txt
```

### **Pipeline de Procesamiento**
```python
def enhanced_validate(snippet, all_snippets, snippet_index, use_agents=True):
    # Fase 1: Validación heurística (existente)
    basic_result = validate(snippet, normalize=True)
    
    if basic_result.status == 'ok' or not use_agents:
        return basic_result
    
    # Fase 2: Análisis LLM (solo si falla heurística)
    try:
        # Paso 1: Análisis contextual
        context_info = context_analyzer.analyze(
            snippet, all_snippets, snippet_index, window_size=20
        )
        
        # Paso 2: Validación inteligente
        validity_result = validity_agent.assess(snippet, context_info)
        
        # Paso 3: Construcción de contexto
        if validity_result.needs_context:
            enhanced_context = context_builder.build(snippet, context_info)
            enhanced_snippet = enhanced_context + "\n\n" + snippet
            
            # Paso 4: Validación final
            return validate(enhanced_snippet, normalize=True)
    
    except Exception as e:
        # Fallback graceful a resultado heurístico
        logging.warning(f"LLM agent failed: {e}")
        return basic_result
    
    return basic_result
```

---

## 📊 DEPENDENCIAS Y VALIDACIÓN

### **Dependencias Principales**
```python
# Validadas con brave_web_search
groq==0.4.1          # Cliente oficial Groq (VERIFICADO: seguro, no slopsquatting)
pydantic>=2.0.0      # Validación de esquemas de respuesta  
tenacity>=8.0.0      # Retry logic para API calls
```

### **Dependencias de Desarrollo**
```python
pytest-asyncio      # Tests async para agentes
pytest-mock         # Mocking de API calls
aioresponses        # Mock HTTP responses
```

---

## 🎛️ CONFIGURACIÓN Y CONTROL

### **Parámetros CLI Nuevos**
```bash
--use-agents          # Habilitar subagentes LLM (default: False)
--agent-model         # Modelo LLM (default: llama-3.1-70b-versatile)
--context-window      # Ventana de análisis (default: 20 snippets)
--agent-cache         # Cache de resultados LLM (default: True)
--max-agent-cost      # Límite de costo por ejecución (default: $5.00)
```

### **Variables de Entorno**
```bash
GROQ_API_KEY         # API key de Groq (requerida)
AGENT_LOG_LEVEL      # Nivel de logging (default: INFO)
AGENT_CACHE_DIR      # Directorio de cache (default: .agent_cache/)
```

---

## 💰 ANÁLISIS DE COSTOS Y PERFORMANCE

### **Estimación de Costos**
```python
Snippets objetivo: 113 (solo runtime errors)
Tokens promedio por snippet: ~500 tokens
Costo por 1K tokens (Groq): ~$0.0002
Costo estimado por ejecución completa: $2-5
Costo por snippet rescatado: ~$0.02-0.04
```

### **Optimizaciones de Costo**
- **Procesamiento selectivo**: Solo snippets fallidos
- **Cache inteligente**: Evitar re-análisis de contextos similares
- **Rate limiting**: Control de requests por minuto
- **Early termination**: Parar si confianza es baja

### **Métricas Target**
```python
Success Rate Actual: 37.4% (185/495)
Success Rate Target: 85%+ (420+/495)
Runtime Errors: 113 → ~20 esperado
Snippets rescatados esperados: ~235
Tiempo adicional por snippet: ~2-3 segundos
```

---

## 🧪 ESTRATEGIA DE TESTING (TDD)

### **Tests por Módulo**
```python
tests/agents/
├── test_base_agent.py           # Tests para clase base
├── test_context_analyzer.py     # Tests análisis contextual
├── test_validity_agent.py       # Tests validación inteligente  
├── test_context_builder.py      # Tests construcción contexto
├── test_llm_client.py          # Tests cliente Groq
└── test_integration.py         # Tests integración completa
```

### **Mocks y Fixtures**
```python
@pytest.fixture
def mock_groq_client():
    """Mock del cliente Groq para tests"""
    
@pytest.fixture  
def sample_snippets():
    """Conjunto de snippets de prueba con dependencias conocidas"""

@pytest.fixture
def expected_contexts():
    """Contextos esperados para validación"""
```

---

## 🔄 PLAN DE IMPLEMENTACIÓN

### **Fase 3.1: Preparación (TDD + Base)**
- [ ] Setup de entorno con dependencias validadas
- [ ] Implementación de `base_agent.py` con TDD
- [ ] Cliente LLM (`llm_client.py`) con manejo de errores robusto
- [ ] Tests de integración básica con Groq API

### **Fase 3.2: Context Analyzer Agent**
- [ ] Implementación TDD de análisis contextual
- [ ] Prompts optimizados para detección de dependencias
- [ ] Ventana dinámica de análisis
- [ ] Cache de análisis contextual

### **Fase 3.3: Validity + Context Builder Agents**
- [ ] Validity Agent con diagnóstico detallado
- [ ] Context Builder con generación optimizada
- [ ] Integración de los 3 agentes en pipeline
- [ ] Tests de casos complejos

### **Fase 3.4: Integración y Optimización**
- [ ] Integración con CLI existente
- [ ] Optimización de performance y costos
- [ ] Logging detallado y métricas
- [ ] Documentación completa

### **Fase 3.5: Validación Final**
- [ ] Ejecución completa sobre archivo de referencia
- [ ] Análisis de mejoras vs Fase 2
- [ ] Reporte final con métricas detalladas
- [ ] Actualización de documentación

---

## 🎯 CRITERIOS DE ÉXITO

### **Métricas Quantitativas**
- **Success Rate**: 37.4% → 85%+ 
- **Runtime Errors**: 113 → ≤20
- **Costo por snippet rescatado**: ≤$0.05
- **Tiempo adicional**: ≤5 segundos promedio por snippet

### **Métricas Cualitativas**
- **Robustez**: Sistema funciona sin agentes (fallback)
- **Usabilidad**: CLI intuitivo, configuración simple
- **Mantenibilidad**: Código TDD, logging completo
- **Escalabilidad**: Funciona con otros archivos de referencia

---

## 🚨 CONSIDERACIONES DE RIESGO

### **Riesgos Técnicos**
- **API Rate Limits**: Mitigado con rate limiting + cache
- **Costo excesivo**: Mitigado con límites configurables
- **Latencia alta**: Mitigado con procesamiento asíncrono
- **Calidad de respuestas LLM**: Mitigado con validación + fallback

### **Riesgos de Implementación**
- **Complejidad alta**: Mitigado con TDD riguroso
- **Debugging difícil**: Mitigado con logging detallado
- **Dependencia externa**: Mitigado con fallback a heurísticas

---

## 📈 ROADMAP POST-FASE 3

### **Extensiones Potenciales**
- **Multi-modelo**: Soporte para otros LLMs (OpenAI, Claude)
- **Especialización**: Agentes específicos por tipo de snippet
- **Aprendizaje**: Cache inteligente que mejora con uso
- **Exportadores**: Integración con IDE, notebooks, documentación

### **Escalabilidad**
- **Otros lenguajes**: Extensión a Java, C++, etc.
- **Otros formatos**: Libros técnicos, tutoriales, documentación
- **Colaborativo**: Sharing de contextos entre usuarios

---

## 🎯 CONCLUSIÓN

La **Fase 3 con Subagentes LLM** representa un salto cualitativo en el proyecto:

- **Inteligencia semántica** vs heurísticas simples
- **Escalabilidad natural** a otros tipos de archivos
- **ROI claro**: ~$2-5 de costo por ~235 snippets rescatados
- **Arquitectura robusta** con fallbacks y TDD completo

**El plan es técnicamente sólido, financieramente viable y estratégicamente coherente.**

---

*Documentado por: Asistente IA*  
*Fecha: 7 de Agosto, 2025*  
*Estado: Plan aprobado para implementación*
