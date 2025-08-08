"""
Benchmarks Avanzados para Evaluación de Agentes
==============================================

Este módulo contiene benchmarks más desafiantes y realistas
para evaluar la efectividad de los agentes en escenarios
complejos del mundo real.

Incluye:
- Casos de código real de Python
- Dependencias complejas y anidadas
- Casos edge ambiguos
- Código con errores intencionales
- Patrones avanzados de programación

Autores: Proyecto Extractor Snippets
Fecha: 2025-01-08
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from tests.agents.test_agent_effectiveness import TestCase, BenchmarkSuite
from src.snippets.agents import Snippet


class AdvancedBenchmarks:
    """Benchmarks avanzados para evaluación exhaustiva"""
    
    @staticmethod
    def create_real_world_benchmark() -> BenchmarkSuite:
        """
        Benchmark con código real del mundo, extraído de proyectos reales
        """
        
        test_cases = [
            # Caso 1: Flask app con decorators y imports complejos
            TestCase(
                name="flask_app_complex",
                description="App Flask con múltiples decorators e imports",
                complexity_level="high",
                input_data={
                    'snippet': Snippet("@app.route('/users/<int:user_id>')\n@login_required\ndef get_user(user_id):\n    user = User.query.get_or_404(user_id)\n    return jsonify(user.to_dict())", 4),
                    'all_snippets': [
                        Snippet("from flask import Flask, jsonify, request", 0),
                        Snippet("from flask_login import login_required", 1), 
                        Snippet("from models import User", 2),
                        Snippet("app = Flask(__name__)", 3),
                        Snippet("@app.route('/users/<int:user_id>')\n@login_required\ndef get_user(user_id):\n    user = User.query.get_or_404(user_id)\n    return jsonify(user.to_dict())", 4)
                    ],
                    'snippet_index': 4
                },
                expected_output={
                    'imports': {
                        'jsonify': {'defined_in_snippet': 0},
                        'login_required': {'defined_in_snippet': 1}
                    },
                    'classes': {
                        'User': {'defined_in_snippet': 2}
                    },
                    'variables': {
                        'app': {'defined_in_snippet': 3}
                    }
                },
                tags=["flask", "decorators", "real_world"]
            ),
            
            # Caso 2: Data Science workflow con pandas/numpy
            TestCase(
                name="data_science_workflow",
                description="Workflow típico de data science",
                complexity_level="high",
                input_data={
                    'snippet': Snippet("correlation_matrix = cleaned_data.corr()\nsns.heatmap(correlation_matrix, annot=True)\nplt.title('Feature Correlations')\nplt.show()", 5),
                    'all_snippets': [
                        Snippet("import pandas as pd", 0),
                        Snippet("import numpy as np", 1),
                        Snippet("import matplotlib.pyplot as plt", 2),
                        Snippet("import seaborn as sns", 3),
                        Snippet("data = pd.read_csv('dataset.csv')", 4),
                        Snippet("cleaned_data = data.dropna().fillna(0)", 5),
                        Snippet("correlation_matrix = cleaned_data.corr()\nsns.heatmap(correlation_matrix, annot=True)\nplt.title('Feature Correlations')\nplt.show()", 6)
                    ],
                    'snippet_index': 6
                },
                expected_output={
                    'variables': {
                        'cleaned_data': {'defined_in_snippet': 5}
                    },
                    'imports': {
                        'sns': {'defined_in_snippet': 3},
                        'plt': {'defined_in_snippet': 2}
                    }
                },
                tags=["data_science", "pandas", "visualization"]
            ),
            
            # Caso 3: Manejo complejo de excepciones
            TestCase(
                name="complex_exception_handling",
                description="Manejo complejo de excepciones con logging",
                complexity_level="medium",
                input_data={
                    'snippet': Snippet("try:\n    result = api_client.fetch_data()\n    process_response(result)\nexcept APIError as e:\n    logger.error(f'API failed: {e}')\n    raise CustomAPIException(str(e))", 5),
                    'all_snippets': [
                        Snippet("import logging", 0),
                        Snippet("from api.client import APIClient", 1),
                        Snippet("from exceptions import APIError, CustomAPIException", 2),
                        Snippet("logger = logging.getLogger(__name__)", 3),
                        Snippet("api_client = APIClient()", 4),
                        Snippet("def process_response(response):\n    return response.json()", 5),
                        Snippet("try:\n    result = api_client.fetch_data()\n    process_response(result)\nexcept APIError as e:\n    logger.error(f'API failed: {e}')\n    raise CustomAPIException(str(e))", 6)
                    ],
                    'snippet_index': 6
                },
                expected_output={
                    'variables': {
                        'api_client': {'defined_in_snippet': 4},
                        'logger': {'defined_in_snippet': 3}
                    },
                    'functions': {
                        'process_response': {'defined_in_snippet': 5}
                    },
                    'imports': {
                        'APIError': {'defined_in_snippet': 2},
                        'CustomAPIException': {'defined_in_snippet': 2}
                    }
                },
                tags=["exceptions", "logging", "api"]
            ),
            
            # Caso 4: Clase con herencia múltiple
            TestCase(
                name="multiple_inheritance_complex",
                description="Clase con herencia múltiple y métodos complejos", 
                complexity_level="high",
                input_data={
                    'snippet': Snippet("class AdvancedProcessor(BaseProcessor, LoggingMixin):\n    def __init__(self, config):\n        super().__init__()\n        self.config = config\n        self.setup_logging()\n    \n    def process(self, data):\n        self.log_info('Processing started')\n        return self.transform_data(data)", 4),
                    'all_snippets': [
                        Snippet("from abc import ABC, abstractmethod", 0),
                        Snippet("class BaseProcessor(ABC):\n    @abstractmethod\n    def process(self, data):\n        pass", 1),
                        Snippet("class LoggingMixin:\n    def setup_logging(self):\n        pass\n    def log_info(self, msg):\n        print(msg)", 2),
                        Snippet("from utils import transform_data", 3),
                        Snippet("class AdvancedProcessor(BaseProcessor, LoggingMixin):\n    def __init__(self, config):\n        super().__init__()\n        self.config = config\n        self.setup_logging()\n    \n    def process(self, data):\n        self.log_info('Processing started')\n        return self.transform_data(data)", 4)
                    ],
                    'snippet_index': 4
                },
                expected_output={
                    'classes': {
                        'BaseProcessor': {'defined_in_snippet': 1},
                        'LoggingMixin': {'defined_in_snippet': 2}
                    },
                    'imports': {
                        'transform_data': {'defined_in_snippet': 3}
                    }
                },
                tags=["inheritance", "classes", "complex"]
            ),
            
            # Caso 5: Context managers y decorators personalizados
            TestCase(
                name="context_managers_decorators",
                description="Context managers y decorators personalizados",
                complexity_level="high",
                input_data={
                    'snippet': Snippet("@timing_decorator\n@cache_result\ndef expensive_calculation(n):\n    with database_transaction():\n        with file_lock('/tmp/calc.lock'):\n            return complex_math_operation(n)", 6),
                    'all_snippets': [
                        Snippet("import functools", 0),
                        Snippet("from contextlib import contextmanager", 1),
                        Snippet("def timing_decorator(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        # timing logic\n        return func(*args, **kwargs)\n    return wrapper", 2),
                        Snippet("def cache_result(func):\n    cache = {}\n    def wrapper(*args):\n        if args in cache:\n            return cache[args]\n        result = func(*args)\n        cache[args] = result\n        return result\n    return wrapper", 3),
                        Snippet("@contextmanager\ndef database_transaction():\n    # transaction logic\n    yield", 4),
                        Snippet("@contextmanager\ndef file_lock(path):\n    # file locking logic\n    yield", 5),
                        Snippet("def complex_math_operation(n):\n    return n ** 2", 6),
                        Snippet("@timing_decorator\n@cache_result\ndef expensive_calculation(n):\n    with database_transaction():\n        with file_lock('/tmp/calc.lock'):\n            return complex_math_operation(n)", 7)
                    ],
                    'snippet_index': 7
                },
                expected_output={
                    'functions': {
                        'timing_decorator': {'defined_in_snippet': 2},
                        'cache_result': {'defined_in_snippet': 3},
                        'database_transaction': {'defined_in_snippet': 4},
                        'file_lock': {'defined_in_snippet': 5},
                        'complex_math_operation': {'defined_in_snippet': 6}
                    }
                },
                tags=["decorators", "context_managers", "advanced"]
            )
        ]
        
        return BenchmarkSuite(
            name="real_world_scenarios",
            description="Escenarios reales de código Python complejo",
            test_cases=test_cases
        )
    
    @staticmethod
    def create_edge_cases_benchmark() -> BenchmarkSuite:
        """
        Benchmark con casos edge y situaciones ambiguas
        """
        
        test_cases = [
            # Caso 1: Variables con nombres similares
            TestCase(
                name="similar_variable_names",
                description="Variables con nombres muy similares",
                complexity_level="medium",
                input_data={
                    'snippet': Snippet("user_data = process_user_data(user_data_raw)", 3),
                    'all_snippets': [
                        Snippet("user_data = {'name': 'John'}", 0),
                        Snippet("user_data_raw = {'name': 'John', 'age': 30}", 1),
                        Snippet("def process_user_data(raw):\n    return {'processed': raw}", 2),
                        Snippet("user_data = process_user_data(user_data_raw)", 3)
                    ],
                    'snippet_index': 3
                },
                expected_output={
                    'variables': {
                        'user_data_raw': {'defined_in_snippet': 1}
                    },
                    'functions': {
                        'process_user_data': {'defined_in_snippet': 2}
                    }
                },
                tags=["edge_case", "ambiguous", "variables"]
            ),
            
            # Caso 2: Redefinición de variables
            TestCase(
                name="variable_redefinition",
                description="Variable redefinida múltiples veces", 
                complexity_level="medium",
                input_data={
                    'snippet': Snippet("print(f'Final value: {counter}')", 4),
                    'all_snippets': [
                        Snippet("counter = 0", 0),
                        Snippet("counter = counter + 1", 1), 
                        Snippet("counter = counter * 2", 2),
                        Snippet("counter = max(counter, 10)", 3),
                        Snippet("print(f'Final value: {counter}')", 4)
                    ],
                    'snippet_index': 4
                },
                expected_output={
                    'variables': {
                        'counter': {'defined_in_snippet': 3}  # La definición más reciente
                    }
                },
                tags=["edge_case", "redefinition", "variables"]
            ),
            
            # Caso 3: Imports con alias conflictivos
            TestCase(
                name="conflicting_import_aliases",
                description="Imports con alias que pueden generar confusión",
                complexity_level="medium",
                input_data={
                    'snippet': Snippet("result = pd.DataFrame(np.array([[1, 2], [3, 4]]))", 4),
                    'all_snippets': [
                        Snippet("import pandas as pd", 0),
                        Snippet("import numpy as np", 1),
                        Snippet("import pandas as dataframes  # alias diferente", 2),
                        Snippet("pd = 'not pandas'  # variable con mismo nombre", 3),
                        Snippet("result = pd.DataFrame(np.array([[1, 2], [3, 4]]))", 4)
                    ],
                    'snippet_index': 4
                },
                expected_output={
                    'imports': {
                        'np': {'defined_in_snippet': 1}
                    },
                    'variables': {
                        'pd': {'defined_in_snippet': 3}  # Variable más reciente, no el import
                    }
                },
                tags=["edge_case", "imports", "aliases", "ambiguous"]
            ),
            
            # Caso 4: Funciones anidadas y closures
            TestCase(
                name="nested_functions_closures",
                description="Funciones anidadas con closures complejos",
                complexity_level="high",
                input_data={
                    'snippet': Snippet("multiplier = create_multiplier(factor)\nresult = multiplier(base_value)", 4),
                    'all_snippets': [
                        Snippet("def create_multiplier(factor):\n    def multiply(x):\n        return x * factor\n    return multiply", 0),
                        Snippet("factor = 10", 1),
                        Snippet("base_value = 5", 2),
                        Snippet("another_factor = 20", 3),
                        Snippet("multiplier = create_multiplier(factor)\nresult = multiplier(base_value)", 4)
                    ],
                    'snippet_index': 4
                },
                expected_output={
                    'functions': {
                        'create_multiplier': {'defined_in_snippet': 0}
                    },
                    'variables': {
                        'factor': {'defined_in_snippet': 1},
                        'base_value': {'defined_in_snippet': 2}
                    }
                },
                tags=["edge_case", "closures", "nested_functions"]
            ),
            
            # Caso 5: Código con errores sintácticos intencionados
            TestCase(
                name="syntactic_errors",
                description="Snippet con errores sintácticos leves",
                complexity_level="high",
                input_data={
                    'snippet': Snippet("result = calculate_something(data,  # missing closing paren\nprint('Processing')", 2),
                    'all_snippets': [
                        Snippet("def calculate_something(data):\n    return len(data)", 0),
                        Snippet("data = [1, 2, 3, 4, 5]", 1),
                        Snippet("result = calculate_something(data,  # missing closing paren\nprint('Processing')", 2)
                    ],
                    'snippet_index': 2
                },
                expected_output={
                    'functions': {
                        'calculate_something': {'defined_in_snippet': 0}
                    },
                    'variables': {
                        'data': {'defined_in_snippet': 1}
                    }
                },
                tags=["edge_case", "syntax_errors", "robust_parsing"]
            ),
            
            # Caso 6: Comprehensions complejas
            TestCase(
                name="complex_comprehensions",
                description="List/dict comprehensions con múltiples dependencias",
                complexity_level="high",
                input_data={
                    'snippet': Snippet("processed = {key: transform_func(value) for key, value in raw_data.items() if filter_func(key)}", 4),
                    'all_snippets': [
                        Snippet("def transform_func(x):\n    return x * 2", 0),
                        Snippet("def filter_func(key):\n    return len(key) > 3", 1),
                        Snippet("raw_data = {'name': 'John', 'age': 30, 'email': 'john@example.com'}", 2),
                        Snippet("# Some other processing", 3),
                        Snippet("processed = {key: transform_func(value) for key, value in raw_data.items() if filter_func(key)}", 4)
                    ],
                    'snippet_index': 4
                },
                expected_output={
                    'functions': {
                        'transform_func': {'defined_in_snippet': 0},
                        'filter_func': {'defined_in_snippet': 1}
                    },
                    'variables': {
                        'raw_data': {'defined_in_snippet': 2}
                    }
                },
                tags=["edge_case", "comprehensions", "complex"]
            )
        ]
        
        return BenchmarkSuite(
            name="edge_cases_scenarios",
            description="Casos edge y situaciones ambiguas",
            test_cases=test_cases
        )
    
    @staticmethod  
    def create_performance_benchmark() -> BenchmarkSuite:
        """
        Benchmark enfocado en performance con diferentes tamaños
        """
        
        # Generar snippets de diferentes tamaños
        small_snippets = [Snippet(f"var_{i} = {i}", i) for i in range(10)]
        medium_snippets = [Snippet(f"var_{i} = {i}", i) for i in range(50)]  
        large_snippets = [Snippet(f"var_{i} = {i}", i) for i in range(200)]
        
        test_cases = [
            # Test con pocos snippets
            TestCase(
                name="small_codebase_performance",
                description="Performance en codebase pequeño (10 snippets)",
                complexity_level="low",
                timeout_seconds=5.0,
                input_data={
                    'snippet': Snippet("print(var_5)", 10),
                    'all_snippets': small_snippets + [Snippet("print(var_5)", 10)],
                    'snippet_index': 10
                },
                expected_output={
                    'variables': {
                        'var_5': {'defined_in_snippet': 5}
                    }
                },
                tags=["performance", "small"]
            ),
            
            # Test con codebase mediano
            TestCase(
                name="medium_codebase_performance", 
                description="Performance en codebase mediano (50 snippets)",
                complexity_level="medium",
                timeout_seconds=10.0,
                input_data={
                    'snippet': Snippet("print(var_25)", 50),
                    'all_snippets': medium_snippets + [Snippet("print(var_25)", 50)],
                    'snippet_index': 50
                },
                expected_output={
                    'variables': {
                        'var_25': {'defined_in_snippet': 25}
                    }
                },
                tags=["performance", "medium"]
            ),
            
            # Test con codebase grande
            TestCase(
                name="large_codebase_performance",
                description="Performance en codebase grande (200 snippets)", 
                complexity_level="extreme",
                timeout_seconds=30.0,
                input_data={
                    'snippet': Snippet("print(var_150)", 200),
                    'all_snippets': large_snippets + [Snippet("print(var_150)", 200)],
                    'snippet_index': 200
                },
                expected_output={
                    'variables': {
                        'var_150': {'defined_in_snippet': 150}
                    }
                },
                tags=["performance", "large", "stress"]
            ),
            
            # Test con snippet muy largo
            TestCase(
                name="long_snippet_performance",
                description="Performance con snippet individual muy largo",
                complexity_level="high",
                timeout_seconds=15.0,
                input_data={
                    'snippet': Snippet("result = very_long_function_name_that_processes_data_extensively(data_structure_with_complex_nested_information)", 2),
                    'all_snippets': [
                        Snippet("def very_long_function_name_that_processes_data_extensively(data):\n    # Very long function\n    " + "\n    ".join([f"step_{i} = process_step_{i}(data)" for i in range(20)]) + "\n    return final_result", 0),
                        Snippet("data_structure_with_complex_nested_information = {'level1': {'level2': {'level3': {'data': [1,2,3,4,5]}}}}", 1),
                        Snippet("result = very_long_function_name_that_processes_data_extensively(data_structure_with_complex_nested_information)", 2)
                    ],
                    'snippet_index': 2
                },
                expected_output={
                    'functions': {
                        'very_long_function_name_that_processes_data_extensively': {'defined_in_snippet': 0}
                    },
                    'variables': {
                        'data_structure_with_complex_nested_information': {'defined_in_snippet': 1}
                    }
                },
                tags=["performance", "long_names", "complex"]
            )
        ]
        
        return BenchmarkSuite(
            name="performance_scenarios",
            description="Tests de performance con diferentes escalas",
            test_cases=test_cases
        )
