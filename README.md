# 🎉 Context Builder Agent - Extractor de Snippets

Sistema avanzado de análisis y construcción de contexto para snippets de código Python usando IA y análisis estático.

## 🚀 Características Principales

- **🔍 Context Analyzer Agent**: Análisis inteligente de dependencias usando LLM y AST
- **🛠️ Context Builder Agent**: Construcción de contextos mínimos y ejecutables
- **✅ Enhanced Validator**: Validación mejorada con capacidades LLM
- **🔒 Safety First**: Validación de seguridad y detección de patrones peligrosos
- **⚡ Performance Optimized**: Fallbacks robustos y cache inteligente
- **🌐 API Integration**: Integración completa con Groq API

## 📁 Estructura del Proyecto

```
src/snippets/
├── agents/
│   ├── base_agent.py              # Clase base para agentes
│   ├── context_analyzer.py        # Análisis de dependencias
│   ├── context_builder.py         # Construcción de contexto
│   ├── llm_client.py              # Cliente LLM unificado
│   └── prompt_templates/
│       ├── context_analysis.txt   # Template para análisis
│       └── context_building.txt   # Template para construcción
├── enhanced_validator.py          # Validador mejorado
├── parser.py                      # Parser de snippets
├── validator.py                   # Validador base
├── normalizer.py                  # Normalizador de código
└── reporter.py                    # Generador de reportes

tests/
├── agents/                        # Tests de agentes
├── test_enhanced_validator.py     # Tests validador mejorado
└── ...                           # Tests adicionales

demos/
├── demo_simple.py                 # Demo básica ejecutando tests
├── demo_context_builder.py        # Demo completa con API
└── test_full_integration.py       # Test de integración completa
```

## 🔧 Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/Joselillo2004/Extractor_Snippets.git
   cd Extractor_Snippets
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Configurar API Key (opcional)**:
   ```bash
   export GROQ_API_KEY="your-api-key-here"
   ```

## 🎯 Uso Rápido

### Demo Básica (Sin API)
```bash
python demo_simple.py
```

### Demo Completa (Con API)
```bash
python demo_context_builder.py
```

### Test de Integración
```bash
python test_full_integration.py
```

### Ejecutar Tests
```bash
pytest tests/ -v
```

## 🏗️ Arquitectura

### Context Analyzer Agent
Analiza snippets para identificar dependencias:
- **Variables** no definidas que necesitan contexto
- **Funciones** llamadas que requieren definiciones
- **Clases** instanciadas que necesitan definiciones
- **Imports** requeridos para módulos externos

### Context Builder Agent
Construye contextos mínimos y ejecutables:
- **Construcción optimizada** con solo código necesario
- **Generación de valores** realistas para variables
- **Validación de seguridad** contra patrones peligrosos
- **Fallback heurístico** cuando LLM no disponible

### Enhanced Validator
Validación avanzada de snippets:
- **Integración con agentes** para análisis profundo
- **Construcción automática** de contexto para validación
- **Scoring de confianza** y métricas detalladas

## 📊 Ejemplo de Uso

```python
import asyncio
from src.snippets.agents.context_analyzer import ContextAnalyzer
from src.snippets.agents.context_builder import ContextBuilder
from src.snippets.agents.base_agent import Snippet

async def main():
    # Snippets de ejemplo
    snippets = [
        Snippet(content='name = "Alice"', index=0),
        Snippet(content='def greet(person): return f"Hello {person}!"', index=1),
        Snippet(content='message = greet(name)', index=2)  # Target
    ]
    
    # 1. Analizar dependencias
    analyzer = ContextAnalyzer()
    analysis_result = await analyzer.analyze(snippets[2], snippets, 2)
    
    # 2. Construir contexto
    builder = ContextBuilder()
    build_result = await builder.analyze(
        snippets[2], snippets, 2, 
        dependencies=analysis_result.data
    )
    
    # 3. Código ejecutable
    context_code = build_result.data['context_code']
    complete_code = context_code + "\n" + snippets[2].content
    
    # 4. Ejecutar
    exec(complete_code)  # ✅ Funciona!

asyncio.run(main())
```

## 🧪 Tests y Resultados

**✅ 38+ casos de prueba exitosos**:
- Context Builder Tests: 15 casos
- Context Analyzer Tests: 11 casos  
- Enhanced Validator Tests: 12 casos

**✅ Integración API completa**:
- Análisis LLM con confidence: 1.00
- Construcción de contexto funcional
- Ejecución exitosa de código generado

## 🎊 Capacidades Demostradas

- ✅ **Análisis contextual**: Identifica dependencias con AST y LLM
- ✅ **Construcción mínima**: Genera solo el código necesario
- ✅ **Optimización**: Deduplica imports y optimiza orden
- ✅ **Valores realistas**: Genera valores apropiados por tipo y contexto
- ✅ **Validación de seguridad**: Detecta patrones peligrosos
- ✅ **Sintaxis correcta**: Valida código generado con AST
- ✅ **Fallback mechanisms**: AST cuando LLM falla
- ✅ **Performance**: < 1s processing time, costos < $0.0001

## 🔧 Configuración Avanzada

### LLM Configuration
```python
from src.snippets.agents.llm_client import LLMConfig

config = LLMConfig(
    model="llama-3.1-8b-instant",
    max_tokens=1000,
    temperature=0.1,
    max_cost_per_session=5.00,
    cache_enabled=True
)
```

### Context Analysis Options
```python
analyzer = ContextAnalyzer(window_size=10)  # ±10 snippets context
```

### Context Building Options
```python
builder = ContextBuilder(enable_llm=True)   # Enable LLM enhancement
```

## 📈 Roadmap

- [ ] Soporte para más lenguajes (JavaScript, TypeScript)
- [ ] Integración con más proveedores LLM (OpenAI, Anthropic)
- [ ] Interface web para uso interactivo
- [ ] Métricas avanzadas y analytics
- [ ] Extensiones para IDEs

## 🤝 Contribuir

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [Groq](https://groq.com/) por la API de inferencia rápida
- [Pydantic](https://pydantic.dev/) por validación de datos
- [pytest](https://pytest.org/) por el framework de testing

---

**🎊 Proyecto completado exitosamente - Todos los objetivos alcanzados** 🚀
