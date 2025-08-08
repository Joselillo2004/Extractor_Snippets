#!/usr/bin/env python3
"""
Test de conexión con Groq API
"""

import asyncio
import sys
from pathlib import Path
import pytest

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from snippets.agents.llm_client import get_llm_client, LLMConfig

@pytest.mark.asyncio
async def test_groq_api():
    """Test de conexión básico con Groq API"""
    print("🧪 Testing Groq API Connection...")
    
    try:
        # Configuración económica para test
        config = LLMConfig(
            model="llama-3.1-8b-instant",  # Modelo más económico
            max_tokens=50,
            max_cost_per_session=0.05,
            temperature=0.1
        )
        
        client = get_llm_client(config)
        print(f"✅ Client initialized with model: {config.model}")
        
        # Test simple
        response = await client.generate("Say hello in Python")
        
        print(f"✅ API Connection successful!")
        print(f"📊 Response details:")
        print(f"  Model: {response.model}")
        print(f"  Content: {response.content[:100]}...")
        print(f"  Tokens used: {response.usage.total_tokens}")
        print(f"  Estimated cost: ${response.usage.estimated_cost:.6f}")
        print(f"  Processing time: {response.processing_time:.3f}s")
        print(f"  Cached: {response.cached}")
        
        # Mostrar estadísticas de sesión
        stats = client.get_session_stats()
        print(f"\n📈 Session stats:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ API Test failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

@pytest.mark.asyncio
async def test_context_builder_with_api():
    """Test de Context Builder con API real"""
    print("\n🛠️ Testing Context Builder with real API...")
    
    try:
        from snippets.agents.context_builder import ContextBuilder
        from snippets.agents.base_agent import Snippet
        
        # Configuración para Context Builder
        config = LLMConfig(
            model="llama-3.1-8b-instant",
            max_tokens=200,
            max_cost_per_session=0.10
        )
        
        builder = ContextBuilder(
            llm_client=get_llm_client(config),
            enable_llm=True
        )
        
        # Snippet de prueba que necesita contexto
        target_snippet = Snippet(
            content="result = calculate_total(price, tax_rate)",
            index=0
        )
        
        # Dependencias simuladas
        dependencies = {
            "functions": {
                "calculate_total": {
                    "defined_in_snippet": None,
                    "parameters": ["price", "tax_rate"],
                    "return_type": "float"
                }
            },
            "variables": {
                "price": {"type": "float"},
                "tax_rate": {"type": "float"}
            }
        }
        
        result = await builder.analyze(
            target_snippet, [target_snippet], 0,
            dependencies=dependencies
        )
        
        if result.success:
            context = result.data
            print(f"✅ Context Builder with API successful!")
            print(f"📝 Generated context:")
            print(f"```python")
            print(context['context_code'])
            print(f"```")
            print(f"📊 Context stats:")
            print(f"  Lines: {context['lines_count']}")
            print(f"  Safe: {context['safety_validated']}")
            print(f"  Valid syntax: {context['syntax_valid']}")
            
            return True
        else:
            print(f"❌ Context Builder failed: {result.error}")
            return False
            
    except Exception as e:
        print(f"❌ Context Builder test failed: {e}")
        return False

async def main():
    """Función principal de tests"""
    print("🎉 GROQ API INTEGRATION TESTS")
    print("=" * 50)
    
    # Test 1: Conexión básica
    api_success = await test_groq_api()
    
    # Test 2: Context Builder con API (solo si el primer test funciona)
    if api_success:
        builder_success = await test_context_builder_with_api()
    else:
        builder_success = False
        print("\n⚠️ Skipping Context Builder test due to API connection issues")
    
    # Resumen
    print("\n🏆 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"✅ API Connection: {'PASS' if api_success else 'FAIL'}")
    print(f"🛠️ Context Builder with API: {'PASS' if builder_success else 'FAIL'}")
    
    if api_success and builder_success:
        print("\n🎊 All tests passed! API integration is working correctly.")
    elif api_success:
        print("\n⚠️ Basic API works, but Context Builder needs attention.")
    else:
        print("\n❌ API connection issues detected. Check API key and network.")

if __name__ == "__main__":
    asyncio.run(main())
