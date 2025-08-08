"""
Test script to verify robust JSON parser integration with Context Analyzer

This script tests the Context Analyzer with various malformed JSON responses
to demonstrate the improved parsing capability.
"""

import asyncio
import logging
import pytest
from unittest.mock import AsyncMock, MagicMock

from src.snippets.agents.context_analyzer import ContextAnalyzer
from src.snippets.agents.base_agent import Snippet

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockLLMClient:
    """Mock LLM client to simulate different JSON response formats."""
    
    def __init__(self, response_content: str):
        self.response_content = response_content
    
    async def generate(self, prompt: str, system_message: str = None):
        """Mock generate method that returns predefined content."""
        mock_result = MagicMock()
        mock_result.content = self.response_content
        mock_result.processing_time = 0.5
        mock_result.usage = MagicMock()
        mock_result.usage.dict.return_value = {
            'prompt_tokens': 100,
            'completion_tokens': 50,
            'total_tokens': 150
        }
        mock_result.cached = False
        return mock_result

@pytest.mark.asyncio
async def test_robust_parser_integration():
    """Test the Context Analyzer with various JSON response formats."""
    
    # Create test snippet
    test_snippet = Snippet(
        content="result = x + y\nprint(data)",
        index=2,
        line_start=10,
        line_end=11
    )
    
    # Create additional context snippets
    all_snippets = [
        Snippet(content="import numpy as np", index=0, line_start=1, line_end=1),
        Snippet(content="x = 10", index=1, line_start=5, line_end=5),
        test_snippet,
        Snippet(content="y = 20", index=3, line_start=15, line_end=15),
    ]
    
    test_cases = [
        {
            "name": "Standard JSON",
            "response": '''```json
{
    "variables": {"x": {"type": "int", "confidence": 0.9}, "y": {"type": "int", "confidence": 0.9}, "data": {"type": "unknown", "confidence": 0.5}},
    "classes": {},
    "imports": {},
    "functions": {},
    "confidence": 0.8
}
```'''
        },
        {
            "name": "JSON with trailing commas",
            "response": '''```json
{
    "variables": {"x": {"type": "int", "confidence": 0.9}, "data": {"type": "unknown", "confidence": 0.5},},
    "classes": {},
    "imports": {},
    "functions": {},
    "confidence": 0.7,
}
```'''
        },
        {
            "name": "JSON with single quotes",
            "response": """```json
{
    'variables': {'x': {'type': 'int', 'confidence': 0.9}, 'data': {'type': 'unknown', 'confidence': 0.5}},
    'classes': {},
    'imports': {},
    'functions': {},
    'confidence': 0.7
}
```"""
        },
        {
            "name": "JSON with comments",
            "response": '''```json
{
    "variables": {"x": {"type": "int", "confidence": 0.9}, "data": {"type": "unknown", "confidence": 0.5}}, // Found variables
    "classes": {}, /* No classes found */
    "imports": {},
    "functions": {},
    "confidence": 0.6
}
```'''
        },
        {
            "name": "Malformed JSON - fallback parsing",
            "response": '''
The analysis found the following dependencies:
"variables": ["x", "y", "data"]
"classes": []
"imports": ["numpy"]
"functions": []
"confidence": 0.65
'''
        },
        {
            "name": "JSON with alternative key names",
            "response": '''```json
{
    "variable_dependencies": ["x", "y", "data"],
    "class_dependencies": [],
    "import_dependencies": ["numpy"],
    "function_dependencies": [],
    "overall_confidence": 0.75
}
```'''
        }
    ]
    
    print("Testing Robust JSON Parser Integration with Context Analyzer")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 40)
        
        # Create mock LLM client with test response
        mock_llm_client = MockLLMClient(test_case['response'])
        
        # Create Context Analyzer with mock client
        analyzer = ContextAnalyzer(llm_client=mock_llm_client)
        
        try:
            # Run analysis
            result = await analyzer.analyze(
                snippet=test_snippet,
                all_snippets=all_snippets,
                snippet_index=2
            )
            
            print(f"✅ Success: {result.success}")
            print(f"   Confidence: {result.confidence}")
            
            if result.data:
                variables = result.data.get('variables', {})
                print(f"   Variables found: {list(variables.keys()) if isinstance(variables, dict) else variables}")
                
            if result.error:
                print(f"   Error: {result.error}")
                
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    # Test JSON parser statistics
    print(f"\nJSON Parser Statistics:")
    print("-" * 25)
    stats = analyzer.json_parser.get_stats()
    for strategy, count in stats.items():
        if count > 0:
            print(f"   {strategy}: {count}")

@pytest.mark.asyncio
async def test_original_vs_robust_parsing():
    """Compare original parsing vs robust parsing on malformed JSON."""
    
    malformed_json_examples = [
        # Trailing comma
        '{"variables": ["x", "y",], "confidence": 0.8,}',
        
        # Single quotes
        "{'variables': ['x', 'y'], 'confidence': 0.8}",
        
        # Missing quotes on keys
        '{variables: ["x", "y"], confidence: 0.8}',
        
        # JSON with comments
        '''
        {
            "variables": ["x", "y"], // Variables found
            "confidence": 0.8 /* High confidence */
        }
        ''',
        
        # Very malformed - should use fallback
        '''
        Analysis results:
        "variables": ["x", "y", "z"]
        "confidence": 0.7
        '''
    ]
    
    print(f"\nComparing Parsing Approaches:")
    print("=" * 40)
    
    # Test with Context Analyzer's robust parser
    analyzer = ContextAnalyzer()
    
    for i, malformed_json in enumerate(malformed_json_examples, 1):
        print(f"\n{i}. Testing malformed JSON:")
        print(f"   Input: {malformed_json[:50].replace(chr(10), ' ')}...")
        
        try:
            # Test robust parser
            result = analyzer.json_parser.parse(malformed_json)
            print(f"   ✅ Robust parser: Success - {result}")
            
        except Exception as e:
            print(f"   ❌ Robust parser: Failed - {e}")
    
    print(f"\nFinal Parser Statistics:")
    stats = analyzer.json_parser.get_stats()
    total_attempts = sum(stats.values())
    print(f"   Total parsing attempts: {total_attempts}")
    for strategy, count in stats.items():
        if total_attempts > 0:
            percentage = (count / total_attempts) * 100
            print(f"   {strategy}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    asyncio.run(test_robust_parser_integration())
    asyncio.run(test_original_vs_robust_parsing())
