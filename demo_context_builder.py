#!/usr/bin/env python3
"""
Demostración del Context Builder Agent

Este script demuestra las capacidades del Context Builder
junto con el Enhanced Validator y Context Analyzer.
"""

import asyncio
from src.snippets.agents.base_agent import Snippet
from src.snippets.agents.context_analyzer import ContextAnalyzer
from src.snippets.agents.context_builder import ContextBuilder
from src.snippets.enhanced_validator import EnhancedValidator, create_enhanced_validator

# Ejemplos de snippets para la demostración
DEMO_SNIPPETS = [
    # Snippet 0: Definición de variables
    Snippet(content="name = 'Alice'\nage = 30\nactive = True", index=0),
    
    # Snippet 1: Definición de función
    Snippet(content="""
def calculate_discount(price, percentage):
    return price * (1 - percentage / 100)
""".strip(), index=1),
    
    # Snippet 2: Definición de clase
    Snippet(content="""
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hi, I'm {self.name}"
""".strip(), index=2),
    
    # Snippet 3: Uso de variables (necesita snippet 0)
    Snippet(content="greeting = f'Hello {name}, you are {age} years old'", index=3),
    
    # Snippet 4: Uso de función (necesita snippet 1)
    Snippet(content="discounted_price = calculate_discount(100, 10)", index=4),
    
    # Snippet 5: Uso de clase (necesita snippet 2)  
    Snippet(content="""
person = Person('Bob', 25)
message = person.greet()
""".strip(), index=5),
    
    # Snippet 6: Uso complejo (necesita múltiples dependencias)
    Snippet(content="""
if active and age > 18:
    discount = calculate_discount(100, 15)
    customer = Person(name, age)
    final_message = f"{customer.greet()}, your discount is ${discount:.2f}"
""".strip(), index=6),
]


async def demo_context_analysis():
    """Demuestra el análisis de contexto"""
    print("🔍 DEMOSTRACIÓN: Context Analysis")
    print("=" * 50)
    
    # Inicializar analyzer - usará fallback AST si no hay API key
    try:
        analyzer = ContextAnalyzer()
    except Exception as e:
        print(f"⚠️ LLM not available, will use AST fallback: {e}")
        analyzer = ContextAnalyzer()
    
    # Analizar snippet complejo (índice 6)
    target_snippet = DEMO_SNIPPETS[6]
    print(f"Target snippet: snippet_{target_snippet.index}")
    print(f"Content: {target_snippet.content}")
    print()
    
    result = await analyzer.analyze(target_snippet, DEMO_SNIPPETS, 6)
    
    if result.success:
        print("✅ Analysis successful!")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Processing time: {result.processing_time:.3f}s")
        print()
        
        dependencies = result.data
        print("📋 Dependencies found:")
        for dep_type, deps in dependencies.items():
            if deps:  # Solo mostrar si hay dependencias
                print(f"  {dep_type.capitalize()}:")
                for name, info in deps.items():
                    snippet_ref = info.get('defined_in_snippet', 'unknown')
                    print(f"    - {name} (from snippet {snippet_ref})")
        print()
        return dependencies
    else:
        print("❌ Analysis failed")
        return {}


async def demo_context_building(dependencies):
    """Demuestra la construcción de contexto"""
    print("🛠️  DEMOSTRACIÓN: Context Building")
    print("=" * 50)
    
    # Inicializar builder sin LLM para usar método heurístico
    try:
        builder = ContextBuilder(enable_llm=False)
    except Exception as e:
        print(f"⚠️ Builder fallback: {e}")
        builder = None
    
    # Construir contexto para snippet complejo
    target_snippet = DEMO_SNIPPETS[6]
    
    result = await builder.analyze(target_snippet, DEMO_SNIPPETS, 6, dependencies=dependencies)
    
    if result.success:
        built_context = result.data
        print("✅ Context built successfully!")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Processing time: {result.processing_time:.3f}s")
        print()
        
        context_code = built_context['context_code']
        print("📝 Generated context code:")
        print("-" * 30)
        print(context_code)
        print("-" * 30)
        print()
        
        print("📊 Context details:")
        print(f"  Lines of code: {built_context['lines_count']}")
        print(f"  Dependencies included: {len(built_context['dependencies_included'])}")
        print(f"  Optimization applied: {built_context['optimization_applied']}")
        print(f"  Safety validated: {built_context['safety_validated']}")
        print(f"  Syntax valid: {built_context['syntax_valid']}")
        print()
        
        return context_code + "\n\n" + target_snippet.content
        
    else:
        print("❌ Context building failed")
        return ""


async def demo_enhanced_validation(complete_code):
    """Demuestra la validación mejorada"""
    print("✅ DEMOSTRACIÓN: Enhanced Validation")
    print("=" * 50)
    
    # Crear validador mejorado sin agentes LLM para evitar errores
    validator = create_enhanced_validator(enable_llm_agents=False)
    
    # Crear snippet del código completo para validar
    test_snippet = Snippet(content=complete_code, index=999)
    
    result = await validator.validate_async(test_snippet)
    
    print("📈 Validation Results:")
    print(f"  Valid: {result.is_valid}")
    print(f"  Confidence: {result.confidence:.2f}")
    print(f"  Enhanced validation: {result.enhanced_validation}")
    print(f"  Processing time: {result.processing_time:.3f}s")
    print()
    
    if result.errors:
        print("❌ Errors found:")
        for error in result.errors[:3]:  # Mostrar solo los primeros 3
            print(f"  - {error}")
    else:
        print("✅ No errors detected")
    
    if result.warnings:
        print("⚠️  Warnings:")
        for warning in result.warnings[:3]:  # Mostrar solo las primeras 3  
            print(f"  - {warning}")
    
    print()
    return result


async def demo_execution_test(complete_code):
    """Prueba ejecutar el código generado"""
    print("🚀 DEMOSTRACIÓN: Code Execution Test")  
    print("=" * 50)
    
    try:
        # Ejecutar el código en un entorno controlado
        exec_globals = {}
        exec(complete_code, exec_globals)
        
        print("✅ Code executed successfully!")
        
        # Mostrar variables resultantes
        relevant_vars = {k: v for k, v in exec_globals.items() 
                        if not k.startswith('__') and not callable(v)}
        
        if relevant_vars:
            print("📋 Variables after execution:")
            for name, value in relevant_vars.items():
                print(f"  {name} = {repr(value)}")
        
        print()
        
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        print()


def demo_stats_and_summary():
    """Muestra estadísticas finales"""
    print("📊 DEMOSTRACIÓN: System Summary")
    print("=" * 50)
    
    print("🎯 Capabilities demonstrated:")
    print("  ✓ Context dependency analysis (AST-based)")
    print("  ✓ Minimal context construction")
    print("  ✓ Realistic value generation") 
    print("  ✓ Code safety validation")
    print("  ✓ Syntax correctness checking")
    print("  ✓ Enhanced snippet validation")
    print("  ✓ Fallback mechanisms (no LLM required)")
    print()
    
    print("🔧 Architecture highlights:")
    print("  • Modular agent design")
    print("  • LLM integration with fallbacks")
    print("  • Comprehensive error handling")
    print("  • Performance-optimized processing")
    print("  • Safety-first code generation")
    print()


async def main():
    """Función principal de la demostración"""
    print("🎉 CONTEXT BUILDER AGENT DEMONSTRATION")
    print("=" * 50)
    print()
    
    # 1. Análisis de dependencias
    dependencies = await demo_context_analysis()
    
    # 2. Construcción de contexto
    complete_code = await demo_context_building(dependencies)
    
    if complete_code:
        # 3. Validación mejorada
        validation_result = await demo_enhanced_validation(complete_code)
        
        # 4. Prueba de ejecución
        if validation_result.is_valid:
            await demo_execution_test(complete_code)
    
    # 5. Resumen final
    demo_stats_and_summary()
    
    print("Demo completed! 🎊")


if __name__ == "__main__":
    asyncio.run(main())
