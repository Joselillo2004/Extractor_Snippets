#!/usr/bin/env python3
"""
Debug test para Context Analyzer
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from snippets.agents.context_analyzer import ContextAnalyzer
from snippets.agents.llm_client import get_llm_client, LLMConfig
from snippets.agents.base_agent import Snippet

async def debug_analyzer():
    """Debug del Context Analyzer paso a paso"""
    print("🔍 DEBUG: Context Analyzer")
    print("=" * 50)
    
    # Configuración mínima
    config = LLMConfig(
        model="llama-3.1-8b-instant",
        max_tokens=200,
        temperature=0.1
    )
    
    # Test simple con pocos snippets
    snippets = [
        Snippet(content='x = 5', index=0),
        Snippet(content='y = x + 10', index=1)
    ]
    
    target_snippet = snippets[1]  # y = x + 10
    
    print(f"Target: {target_snippet.content}")
    print(f"Context: {len(snippets)} snippets")
    print()
    
    # Crear analyzer
    analyzer = ContextAnalyzer()
    
    # Hacer request directo al LLM para ver la respuesta
    print("🧪 Testing direct LLM call...")
    
    # Preparar contexto manualmente
    context_formatted = """## Snippet 0 (-1)
```python
x = 5
```

## Snippet 1 >>> TARGET <<<
```python
y = x + 10
```"""
    
    # Usar template
    prompt = analyzer.prompt_template.format(
        target_snippet=target_snippet.content,
        context_snippets=context_formatted
    )
    
    print("📝 Prompt preview:")
    print("-" * 30)
    print(prompt[:400] + "..." if len(prompt) > 400 else prompt)
    print("-" * 30)
    
    try:
        # Hacer request directo
        llm_response = await analyzer.llm_client.generate(
            prompt=prompt,
            system_message="You are an expert Python code analyzer. Return valid JSON only."
        )
        
        print("\n📄 Raw LLM Response:")
        print("-" * 30)
        print(llm_response.content)
        print("-" * 30)
        
        # Intentar parsear
        dependency_map = analyzer._parse_llm_response(llm_response.content)
        
        print(f"\n📊 Parsed result:")
        print(f"  Confidence: {dependency_map.confidence}")
        print(f"  Error: {dependency_map.error}")
        print(f"  Variables: {dependency_map.variables}")
        
    except Exception as e:
        print(f"❌ LLM request failed: {e}")
        
        # Probar fallback
        print("\n🔄 Testing AST fallback...")
        try:
            fallback_result = analyzer._analyze_with_ast_fallback(target_snippet)
            print(f"  AST Variables: {fallback_result.variables}")
            print(f"  AST Confidence: {fallback_result.confidence}")
        except Exception as ast_e:
            print(f"❌ AST fallback also failed: {ast_e}")

if __name__ == "__main__":
    asyncio.run(debug_analyzer())
