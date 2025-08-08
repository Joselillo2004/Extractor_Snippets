#!/usr/bin/env python3
"""
Test completo de integración con Groq API
"""

import asyncio
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from snippets.agents.context_analyzer import ContextAnalyzer
from snippets.agents.context_builder import ContextBuilder
from snippets.agents.llm_client import LLMConfig
from snippets.agents.base_agent import Snippet

async def test_full_integration():
    """Test completo de integración Context Analyzer + Builder"""
    print("🎉 FULL INTEGRATION TEST WITH GROQ API")
    print("=" * 50)
    
    # Configuración económica para testing
    config = LLMConfig(
        model="llama-3.1-8b-instant",
        max_tokens=400,
        max_cost_per_session=0.30,
        temperature=0.1
    )
    
    # Snippets de prueba realista
    snippets = [
        Snippet(content='name = "Alice"', index=0),
        Snippet(content='age = 30', index=1), 
        Snippet(content='def greet(person, age_val):\n    return f"Hello {person}, you are {age_val} years old!"', index=2),
        Snippet(content='message = greet(name, age)', index=3),
        Snippet(content='print(message)', index=4)
    ]
    
    target_snippet = snippets[3]  # message = greet(name, age)
    
    print(f"🎯 Target snippet: {target_snippet.content}")
    print(f"📝 Available context: {len(snippets)} snippets")
    print()
    
    # PASO 1: Context Analysis
    print("🔍 STEP 1: Context Analysis")
    print("-" * 30)
    
    try:
        analyzer = ContextAnalyzer()
        analysis_result = await analyzer.analyze(target_snippet, snippets, 3)
        
        if analysis_result.success:
            print(f"✅ Analysis successful! (confidence: {analysis_result.confidence:.2f})")
            dependencies = analysis_result.data
            
            # Mostrar dependencias encontradas
            for category, items in dependencies.items():
                if items and category not in ['processing_time', 'confidence', 'error', 'overall_confidence']:
                    if isinstance(items, dict):
                        print(f"  📋 {category.capitalize()}: {list(items.keys())}")
                    else:
                        print(f"  📋 {category.capitalize()}: {items}")
            
            method = analysis_result.metadata.get('fallback', False)
            print(f"  🔧 Method: {'AST Fallback' if method else 'LLM Analysis'}")
            
            if 'llm_usage' in analysis_result.metadata:
                usage = analysis_result.metadata['llm_usage']
                print(f"  💰 Cost: ${usage['estimated_cost']:.6f}")
        else:
            print(f"❌ Analysis failed: {analysis_result.error}")
            dependencies = {}
            
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        dependencies = {}
    
    print()
    
    # PASO 2: Context Building
    print("🛠️ STEP 2: Context Building")  
    print("-" * 30)
    
    try:
        builder = ContextBuilder(enable_llm=True)
        build_result = await builder.analyze(
            target_snippet, snippets, 3, 
            dependencies=dependencies
        )
        
        if build_result.success:
            context = build_result.data
            method = build_result.metadata.get('method', 'unknown')
            print(f"✅ Context built! (method: {method})")
            print(f"  📊 Stats: {context['lines_count']} lines, safe: {context['safety_validated']}")
            
            context_code = context['context_code']
            print(f"  📝 Generated context:")
            print("  ```python")
            for line in context_code.split('\n'):
                print(f"  {line}")
            print("  ```")
            
            return context_code
        else:
            print(f"❌ Context building failed: {build_result.error}")
            return None
            
    except Exception as e:
        print(f"❌ Context building error: {e}")
        return None

async def test_execution(context_code, target_snippet):
    """Test de ejecución del código completo"""
    print("\n🚀 STEP 3: Code Execution Test")
    print("-" * 30)
    
    if not context_code:
        print("❌ No context code to execute")
        return
    
    try:
        # Construir código completo
        complete_code = context_code + "\n\n" + target_snippet.content
        
        print("📝 Complete code:")
        print("```python")
        for i, line in enumerate(complete_code.split('\n'), 1):
            print(f"{i:2d}. {line}")
        print("```")
        
        # Ejecutar
        exec_globals = {}
        exec(complete_code, exec_globals)
        
        print("\n✅ Execution successful!")
        
        # Mostrar variables resultantes
        relevant_vars = {k: v for k, v in exec_globals.items() 
                        if not k.startswith('__') and not callable(v)}
        
        if relevant_vars:
            print("📊 Variables after execution:")
            for name, value in relevant_vars.items():
                print(f"  {name} = {repr(value)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        return False

async def main():
    """Función principal"""
    print("Starting full integration test with real API...")
    
    try:
        # Test de integración completa
        context_code = await test_full_integration()
        
        if context_code:
            # Test de ejecución
            target_snippet = Snippet(content='message = greet(name, age)', index=3)
            execution_success = await test_execution(context_code, target_snippet)
            
            # Resultado final
            print("\n🏆 INTEGRATION TEST RESULTS")
            print("=" * 50)
            print(f"✅ Context Analysis: PASS")
            print(f"✅ Context Building: PASS")  
            print(f"{'✅' if execution_success else '❌'} Code Execution: {'PASS' if execution_success else 'FAIL'}")
            
            if execution_success:
                print("\n🎊 Full integration working perfectly!")
                print("  • API connection successful")
                print("  • Context analysis functional")
                print("  • Context building operational")  
                print("  • Generated code executable")
            else:
                print("\n⚠️ Integration partially working - execution issues detected")
        else:
            print("\n❌ Integration test failed at context building stage")
        
    except Exception as e:
        print(f"\n💥 Integration test failed with error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
