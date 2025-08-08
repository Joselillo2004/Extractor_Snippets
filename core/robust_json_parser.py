"""
Robust JSON Parser for LLM Responses

This module provides ultra-robust JSON parsing with multiple progressive strategies
to handle malformed JSON responses from LLMs, reducing parsing failures.
"""

import json
import re
import logging
from typing import Dict, Any, Optional, List, Union
from json import JSONDecodeError

logger = logging.getLogger(__name__)


class RobustJSONParser:
    """Ultra-robust JSON parser with multiple fallback strategies."""
    
    def __init__(self):
        self.parsing_stats = {
            'standard_json': 0,
            'json_block_extraction': 0,
            'error_correction': 0,
            'json5_parsing': 0,
            'minimal_fallback': 0,
            'total_failures': 0
        }
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse JSON from text using progressive strategies.
        
        Args:
            text: Text potentially containing JSON
            
        Returns:
            Parsed JSON dictionary
            
        Raises:
            ValueError: If all parsing strategies fail
        """
        if not text or not text.strip():
            raise ValueError("Empty or whitespace-only text provided")
        
        # Strategy 1: Standard JSON parsing
        result = self._try_standard_json(text.strip())
        if result is not None:
            self.parsing_stats['standard_json'] += 1
            return result
        
        # Strategy 2: Extract JSON blocks
        result = self._try_json_block_extraction(text)
        if result is not None:
            self.parsing_stats['json_block_extraction'] += 1
            return result
        
        # Strategy 3: Common error correction
        result = self._try_error_correction(text)
        if result is not None:
            self.parsing_stats['error_correction'] += 1
            return result
        
        # Strategy 4: JSON5-like parsing (more permissive)
        result = self._try_json5_parsing(text)
        if result is not None:
            self.parsing_stats['json5_parsing'] += 1
            return result
        
        # Strategy 5: Minimal fallback - extract basic structure
        result = self._try_minimal_fallback(text)
        if result is not None:
            self.parsing_stats['minimal_fallback'] += 1
            return result
        
        # All strategies failed
        self.parsing_stats['total_failures'] += 1
        logger.error(f"All JSON parsing strategies failed for text: {text[:200]}...")
        raise ValueError("Unable to parse JSON from response using any strategy")
    
    def _try_standard_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Try standard JSON parsing."""
        try:
            return json.loads(text)
        except JSONDecodeError:
            return None
    
    def _try_json_block_extraction(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON blocks from text (handles text with JSON embedded)."""
        # Look for JSON blocks between ```json and ``` or just { ... }
        patterns = [
            r'```json\s*(\{.*?\})\s*```',
            r'```\s*(\{.*?\})\s*```',
            r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})',  # Balanced braces
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                try:
                    return json.loads(match.strip())
                except JSONDecodeError:
                    continue
        
        return None
    
    def _try_error_correction(self, text: str) -> Optional[Dict[str, Any]]:
        """Try to correct common JSON errors."""
        corrections = [
            # Remove trailing commas
            (r',(\s*[}\]])', r'\1'),
            # Fix single quotes to double quotes (careful with apostrophes)
            (r"'([^']*)'(\s*:)", r'"\1"\2'),
            (r":(\s*)'([^']*)'", r':\1"\2"'),
            # Fix unescaped quotes
            (r'([^\\])"([^"]*)"([^:])', r'\1\"\2\"\3'),
            # Fix missing commas between objects
            (r'}(\s*)(["\'{])', r'},\1\2'),
            # Fix missing quotes on keys
            (r'(\w+)(\s*:)', r'"\1"\2'),
        ]
        
        corrected_text = text.strip()
        
        for pattern, replacement in corrections:
            corrected_text = re.sub(pattern, replacement, corrected_text)
        
        try:
            return json.loads(corrected_text)
        except JSONDecodeError:
            return None
    
    def _try_json5_parsing(self, text: str) -> Optional[Dict[str, Any]]:
        """JSON5-like parsing (more permissive)."""
        try:
            # Remove comments (// and /* */)
            text = re.sub(r'//.*?$', '', text, flags=re.MULTILINE)
            text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
            
            # Allow trailing commas
            text = re.sub(r',(\s*[}\]])', r'\1', text)
            
            # Convert single quotes to double quotes for simple cases
            text = re.sub(r"'([^'\\]*(?:\\.[^'\\]*)*)'", r'"\1"', text)
            
            return json.loads(text)
        except JSONDecodeError:
            return None
    
    def _try_minimal_fallback(self, text: str) -> Optional[Dict[str, Any]]:
        """Generate minimal JSON based on patterns found in text."""
        try:
            # Extract common patterns for dependencies and variables
            result = {}
            
            # Look for variables pattern
            variables_match = re.search(r'"variables"[^[]*\[(.*?)\]', text, re.DOTALL)
            if variables_match:
                variables_text = variables_match.group(1)
                variables = self._extract_list_items(variables_text)
                result['variables'] = variables
            
            # Look for dependencies pattern
            dependencies_match = re.search(r'"dependencies"[^[]*\[(.*?)\]', text, re.DOTALL)
            if dependencies_match:
                deps_text = dependencies_match.group(1)
                dependencies = self._extract_list_items(deps_text)
                result['dependencies'] = dependencies
            
            # Look for imports pattern
            imports_match = re.search(r'"imports"[^[]*\[(.*?)\]', text, re.DOTALL)
            if imports_match:
                imports_text = imports_match.group(1)
                imports = self._extract_list_items(imports_text)
                result['imports'] = imports
            
            # Look for functions pattern
            functions_match = re.search(r'"functions"[^[]*\[(.*?)\]', text, re.DOTALL)
            if functions_match:
                functions_text = functions_match.group(1)
                functions = self._extract_list_items(functions_text)
                result['functions'] = functions
            
            # Look for classes pattern
            classes_match = re.search(r'"classes"[^[]*\[(.*?)\]', text, re.DOTALL)
            if classes_match:
                classes_text = classes_match.group(1)
                classes = self._extract_list_items(classes_text)
                result['classes'] = classes
            
            # Look for confidence
            confidence_match = re.search(r'"confidence"[^0-9.]*([0-9.]+)', text)
            if confidence_match:
                try:
                    result['confidence'] = float(confidence_match.group(1))
                except ValueError:
                    result['confidence'] = 0.5
            
            # Return result if we found at least something
            if result:
                # Add default values for missing keys
                result.setdefault('variables', [])
                result.setdefault('dependencies', [])
                result.setdefault('imports', [])
                result.setdefault('functions', [])
                result.setdefault('classes', [])
                result.setdefault('confidence', 0.5)
                return result
            
        except Exception as e:
            logger.debug(f"Minimal fallback parsing failed: {e}")
        
        return None
    
    def _extract_list_items(self, text: str) -> List[str]:
        """Extract list items from text."""
        items = []
        
        # Try to find quoted strings
        quoted_items = re.findall(r'"([^"]*)"', text)
        if quoted_items:
            items.extend(quoted_items)
        else:
            # Try to find comma-separated items
            raw_items = [item.strip() for item in text.split(',')]
            items.extend([item for item in raw_items if item and not item.isspace()])
        
        return [item.strip() for item in items if item.strip()]
    
    def get_stats(self) -> Dict[str, int]:
        """Get parsing statistics."""
        return self.parsing_stats.copy()
    
    def reset_stats(self):
        """Reset parsing statistics."""
        self.parsing_stats = {key: 0 for key in self.parsing_stats}


# Convenience function for direct usage
def parse_json_robust(text: str) -> Dict[str, Any]:
    """
    Parse JSON from text using robust parsing strategies.
    
    Args:
        text: Text potentially containing JSON
        
    Returns:
        Parsed JSON dictionary
        
    Raises:
        ValueError: If all parsing strategies fail
    """
    parser = RobustJSONParser()
    return parser.parse(text)


if __name__ == "__main__":
    # Test the parser with various malformed JSON examples
    test_cases = [
        # Standard JSON
        '{"variables": ["x", "y"], "dependencies": ["math"]}',
        
        # JSON with trailing comma
        '{"variables": ["x", "y",], "dependencies": ["math",]}',
        
        # JSON with single quotes
        "{'variables': ['x', 'y'], 'dependencies': ['math']}",
        
        # JSON in code blocks
        '```json\n{"variables": ["x", "y"], "dependencies": ["math"]}\n```',
        
        # Malformed with comments
        '''
        {
            "variables": ["x", "y"], // Variables found
            "dependencies": ["math"] /* Math library */
        }
        ''',
        
        # Very malformed - should use fallback
        '''
        The analysis found:
        "variables": ["x", "y", "z"]
        "dependencies": ["numpy", "pandas"]
        "confidence": 0.8
        '''
    ]
    
    parser = RobustJSONParser()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Input: {test_case[:100]}...")
        try:
            result = parser.parse(test_case)
            print(f"Success: {result}")
        except ValueError as e:
            print(f"Failed: {e}")
    
    print(f"\nParsing Statistics:")
    for strategy, count in parser.get_stats().items():
        print(f"  {strategy}: {count}")
