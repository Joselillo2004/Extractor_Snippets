#!/usr/bin/env python3
"""
Demo script showing Context Analyzer improvements with robust JSON parser

This demonstrates the improvement in JSON parsing robustness before and after
the integration of the RobustJSONParser.
"""

import json
import asyncio
import pytest
from unittest.mock import MagicMock
from src.snippets.agents.context_analyzer import ContextAnalyzer
from src.snippets.agents.base_agent import Snippet
from core.robust_json_parser import RobustJSONParser

# Test cases with problematic JSON that commonly occurs from LLMs
PROBLEMATIC_JSON_SAMPLES = [
    {
        "name": "Trailing commas",
        "content": '''```json
{
    "variables": {"x": {"type": "int", "confidence": 0.9}, "y": {"type": "unknown", "confidence": 0.5},},
    "classes": {},
    "imports": {},
    "functions": {},
    "confidence": 0.8,
}
```'''
    },
    {
        "name": "Single quotes instead of double",
        "content": """```json
{
    'variables': {'data': {'type': 'unknown', 'confidence': 0.7}},
    'classes': {},
    'imports': {'pandas': {'confidence': 0.9}},
    'functions': {},
    'confidence': 0.75
}
```"""
    },
    {
        "name": "JSON with comments",
        "content": '''```json
{
    "variables": {"result": {"type": "int", "confidence": 0.8}}, // Found variables
    "classes": {}, /* No classes */
    "imports": {"numpy": {"confidence": 0.9}},
    "functions": {},
    "confidence": 0.85
}
```'''
    },
    {
        "name": "Very malformed - fallback parsing needed",
        "content": '''
Analysis complete. Found the following dependencies:

"variables": ["x", "y", "result"]
"classes": []
"imports": ["math", "numpy"]
"functions": ["calculate"]
"confidence": 0.78
        '''
    },
    {
        "name": "Unescaped characters and mixed format",
        "content": '''```
{
    "variables": {"file_path": {"type": "str", "confidence": 0.9}},
    classes: {},
    "imports": {"os": {"confidence": 1.0},},
    "functions": {},
    confidence: 0.82
}
```'''
    }
]

def simulate_original_json_parsing(content: str) -> dict:
    """Simulate how the original parser would handle these cases."""
    try:
        # Try to extract JSON using simple regex patterns (original approach)
        import re
        
        # Look for JSON block
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON directly
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1 and end > start:
                json_str = content[start:end+1]
            else:
                raise ValueError("No JSON found")
        
        # Standard JSON parsing (would fail on malformed JSON)
        return json.loads(json_str.strip())
        
    except Exception as e:
        raise ValueError(f"Original parsing failed: {e}")

def test_parsing_comparison():
    """Compare original vs robust parsing approaches."""
    
    print("🧪 JSON Parser Comparison Test")
    print("=" * 60)
    print("Testing how the Context Analyzer handles problematic JSON from LLMs")
    print()
    
    robust_parser = RobustJSONParser()
    success_counts = {"original": 0, "robust": 0}
    
    for i, test_case in enumerate(PROBLEMATIC_JSON_SAMPLES, 1):
        print(f"{i}. {test_case['name']}")
        print("-" * 40)
        
        # Test original approach
        try:
            original_result = simulate_original_json_parsing(test_case['content'])
            success_counts["original"] += 1
            print("✅ Original parser: SUCCESS")
        except Exception as e:
            print(f"❌ Original parser: FAILED - {str(e)[:80]}...")
        
        # Test robust approach
        try:
            robust_result = robust_parser.parse(test_case['content'])
            success_counts["robust"] += 1
            print("✅ Robust parser: SUCCESS")
            if 'variables' in robust_result:
                vars_found = list(robust_result['variables'].keys()) if isinstance(robust_result['variables'], dict) else robust_result['variables']
                print(f"   → Variables found: {vars_found}")
        except Exception as e:
            print(f"❌ Robust parser: FAILED - {str(e)[:80]}...")
        
        print()
    
    # Summary
    total_cases = len(PROBLEMATIC_JSON_SAMPLES)
    print("📊 RESULTS SUMMARY")
    print("=" * 40)
    print(f"Original parser success rate: {success_counts['original']}/{total_cases} ({success_counts['original']/total_cases*100:.1f}%)")
    print(f"Robust parser success rate:   {success_counts['robust']}/{total_cases} ({success_counts['robust']/total_cases*100:.1f}%)")
    
    improvement = success_counts['robust'] - success_counts['original']
    if improvement > 0:
        print(f"🚀 Improvement: +{improvement} cases ({improvement/total_cases*100:.1f}% better)")
    elif improvement == 0:
        print("📊 No improvement in success rate")
    else:
        print(f"📉 Regression: -{abs(improvement)} cases")
    
    # Show parser statistics
    print(f"\n📈 ROBUST PARSER STATISTICS")
    print("-" * 30)
    stats = robust_parser.get_stats()
    for strategy, count in stats.items():
        if count > 0:
            percentage = (count / sum(stats.values())) * 100
            print(f"   {strategy}: {count} ({percentage:.1f}%)")

@pytest.mark.asyncio
async def test_context_analyzer_integration():
    """Test the full Context Analyzer integration."""
    
    print("\n🔬 CONTEXT ANALYZER INTEGRATION TEST")
    print("=" * 50)
    
    # Create a mock LLM client that returns problematic JSON
    class MockLLMClient:
        def __init__(self, response):
            self.response = response
            
        async def generate(self, prompt, system_message=None):
            result = MagicMock()
            result.content = self.response
            result.processing_time = 0.1
            result.usage = MagicMock()
            result.usage.dict.return_value = {"tokens": 100}
            result.cached = False
            return result
    
    # Test snippet
    test_snippet = Snippet(
        content="result = process_data(df)",
        index=1,
        line_start=10,
        line_end=10
    )
    
    all_snippets = [
        Snippet(content="import pandas as pd", index=0, line_start=1, line_end=1),
        test_snippet,
        Snippet(content="df = pd.DataFrame(data)", index=2, line_start=5, line_end=5),
    ]
    
    # Test with a problematic JSON response
    problematic_response = '''```json
{
    "variables": {"df": {"type": "DataFrame", "confidence": 0.9}, "data": {"type": "unknown", "confidence": 0.6},},
    "classes": {},
    "imports": {"pandas": {"confidence": 0.95}},
    "functions": {"process_data": {"confidence": 0.8}},
    "confidence": 0.87,
}
```'''
    
    mock_client = MockLLMClient(problematic_response)
    analyzer = ContextAnalyzer(llm_client=mock_client)
    
    print("Testing Context Analyzer with problematic JSON response...")
    
    try:
        result = await analyzer.analyze(
            snippet=test_snippet,
            all_snippets=all_snippets,
            snippet_index=1
        )
        
        print(f"✅ Analysis completed successfully!")
        print(f"   Success: {result.success}")
        print(f"   Confidence: {result.confidence}")
        
        if result.data:
            variables = result.data.get('variables', {})
            functions = result.data.get('functions', {})
            imports = result.data.get('imports', {})
            
            if variables:
                print(f"   Variables: {list(variables.keys())}")
            if functions:
                print(f"   Functions: {list(functions.keys())}")
            if imports:
                print(f"   Imports: {list(imports.keys())}")
        
        # Show parser stats
        parser_stats = analyzer.json_parser.get_stats()
        successful_strategies = [k for k, v in parser_stats.items() if v > 0 and k != 'total_failures']
        if successful_strategies:
            print(f"   Parser strategy used: {successful_strategies[0]}")
            
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

if __name__ == "__main__":
    test_parsing_comparison()
    asyncio.run(test_context_analyzer_integration())
