#!/usr/bin/env python3
"""
Script de evaluación de agentes - Extractor Snippets
==================================================

Script ejecutable para evaluar la efectividad de los agentes
usando los benchmarks estándar.

Uso:
    python evaluate_agents.py --agent context_analyzer --benchmark standard
    python evaluate_agents.py --agent all --benchmark stress_test
    python evaluate_agents.py --consistency --runs 5

Autores: Proyecto Extractor Snippets
Fecha: 2025-01-08
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tests.agents.test_agent_effectiveness import (
    AgentEffectivenessEvaluator, 
    StandardBenchmarks,
    TestCase
)
from tests.agents.advanced_benchmarks import AdvancedBenchmarks
from src.snippets.agents import ContextAnalyzer, Snippet, get_llm_client, LLMConfig


class AgentEvaluationCLI:
    """CLI para evaluación de agentes"""
    
    def __init__(self):
        self.evaluator = AgentEffectivenessEvaluator("evaluation_results")
        self.results = []
    
    async def evaluate_context_analyzer(self, benchmark_name: str = "standard"):
        """Evalúa Context Analyzer"""
        print("🔍 Evaluando Context Analyzer...")
        
        # Crear benchmark
        if benchmark_name == "standard":
            benchmark = StandardBenchmarks.create_context_analyzer_benchmark()
        elif benchmark_name == "stress_test":
            benchmark = StandardBenchmarks.create_stress_test_benchmark()
        elif benchmark_name == "real_world":
            benchmark = AdvancedBenchmarks.create_real_world_benchmark()
        elif benchmark_name == "edge_cases":
            benchmark = AdvancedBenchmarks.create_edge_cases_benchmark()
        elif benchmark_name == "performance":
            benchmark = AdvancedBenchmarks.create_performance_benchmark()
        else:
            print(f"❌ Benchmark '{benchmark_name}' no encontrado")
            print("Benchmarks disponibles: standard, stress_test, real_world, edge_cases, performance")
            return None
        
        # Configurar cliente LLM
        config = LLMConfig(
            model="llama-3.1-8b-instant",
            max_tokens=500,
            max_cost_per_session=2.0,  # Límite de $2 para evaluaciones
            cache_enabled=True
        )
        
        llm_client = get_llm_client(config)
        analyzer = ContextAnalyzer(llm_client, window_size=10)
        
        # Evaluar
        try:
            metrics = await self.evaluator.evaluate_context_analyzer(analyzer, benchmark)
            
            # Guardar reporte
            report_path = self.evaluator.save_evaluation_report(
                metrics, benchmark.name, "context_analyzer"
            )
            
            self.results.append({
                'agent': 'context_analyzer',
                'benchmark': benchmark_name,
                'metrics': metrics,
                'report_path': report_path
            })
            
            print("✅ Context Analyzer evaluado exitosamente")
            self._print_summary(metrics, "Context Analyzer")
            print(f"📄 Reporte guardado en: {report_path}")
            
            return metrics
            
        except Exception as e:
            print(f"❌ Error evaluando Context Analyzer: {e}")
            return None
    
    async def evaluate_consistency(self, agent_name: str = "context_analyzer", runs: int = 5):
        """Evalúa consistencia de un agente"""
        print(f"🔄 Evaluando consistencia de {agent_name} ({runs} ejecuciones)...")
        
        # Test case simple para consistencia
        test_case = TestCase(
            name="consistency_test",
            description="Test de consistencia",
            input_data={
                'snippet': Snippet("print(lista)", 1),
                'all_snippets': [
                    Snippet("lista = [1, 2, 3]", 0),
                    Snippet("print(lista)", 1)
                ],
                'snippet_index': 1
            },
            expected_output={}
        )
        
        if agent_name == "context_analyzer":
            config = LLMConfig(
                model="llama-3.1-8b-instant", 
                cache_enabled=False  # Sin cache para test de consistencia
            )
            llm_client = get_llm_client(config)
            analyzer = ContextAnalyzer(llm_client)
            
            try:
                consistency_score = await self.evaluator.evaluate_consistency(
                    analyzer, test_case, num_runs=runs
                )
                
                print(f"✅ Consistencia evaluada: {consistency_score:.3f}")
                return consistency_score
                
            except Exception as e:
                print(f"❌ Error evaluando consistencia: {e}")
                return None
        
        else:
            print(f"❌ Agente '{agent_name}' no soportado para evaluación de consistencia")
            return None
    
    def _print_summary(self, metrics, agent_name: str):
        """Imprime resumen de métricas"""
        print(f"\n📊 Resumen de {agent_name}:")
        print(f"   Success Rate: {metrics.success_rate:.2%}")
        print(f"   Precision:    {metrics.precision:.3f}")
        print(f"   Recall:       {metrics.recall:.3f}")
        print(f"   F1-Score:     {metrics.f1_score:.3f}")
        print(f"   Avg Time:     {metrics.avg_response_time:.3f}s")
        print(f"   Tests:        {metrics.successful_tests}/{metrics.total_tests}")
    
    def print_final_summary(self):
        """Imprime resumen final de todas las evaluaciones"""
        if not self.results:
            print("⚠️  No se ejecutaron evaluaciones")
            return
        
        print(f"\n🎯 RESUMEN FINAL - {len(self.results)} evaluación(es) completada(s)")
        print("=" * 60)
        
        for result in self.results:
            metrics = result['metrics']
            print(f"\n{result['agent'].upper()} ({result['benchmark']}):")
            print(f"  ✅ Success Rate: {metrics.success_rate:.2%}")
            print(f"  🎯 Precision:    {metrics.precision:.3f}")
            print(f"  📈 Recall:       {metrics.recall:.3f}")
            print(f"  ⚡ F1-Score:     {metrics.f1_score:.3f}")
            print(f"  ⏱️  Avg Time:     {metrics.avg_response_time:.3f}s")
            print(f"  📄 Report:       {result['report_path']}")
        
        # Estadísticas agregadas
        avg_success_rate = sum(r['metrics'].success_rate for r in self.results) / len(self.results)
        avg_precision = sum(r['metrics'].precision for r in self.results) / len(self.results)
        avg_f1 = sum(r['metrics'].f1_score for r in self.results) / len(self.results)
        
        print(f"\n📈 ESTADÍSTICAS GLOBALES:")
        print(f"  Success Rate promedio: {avg_success_rate:.2%}")
        print(f"  Precisión promedio:    {avg_precision:.3f}")
        print(f"  F1-Score promedio:     {avg_f1:.3f}")


async def main():
    """Función principal del CLI"""
    parser = argparse.ArgumentParser(
        description="Evaluador de efectividad de agentes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python evaluate_agents.py --agent context_analyzer --benchmark standard
  python evaluate_agents.py --agent all --benchmark stress_test
  python evaluate_agents.py --consistency --runs 5
  python evaluate_agents.py --agent context_analyzer --consistency --runs 3
        """
    )
    
    parser.add_argument(
        "--agent", 
        choices=["context_analyzer", "context_builder", "all"],
        default="context_analyzer",
        help="Agente a evaluar (default: context_analyzer)"
    )
    
    parser.add_argument(
        "--benchmark",
        choices=["standard", "stress_test", "real_world", "edge_cases", "performance"],
        default="standard", 
        help="Benchmark a usar (default: standard)"
    )
    
    parser.add_argument(
        "--consistency",
        action="store_true",
        help="Ejecutar test de consistencia"
    )
    
    parser.add_argument(
        "--runs",
        type=int,
        default=5,
        help="Número de ejecuciones para test de consistencia (default: 5)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="evaluation_results",
        help="Directorio para guardar reportes (default: evaluation_results)"
    )
    
    args = parser.parse_args()
    
    # Verificar API key
    if not os.getenv("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY no encontrada en variables de entorno")
        print("   Configura tu API key: export GROQ_API_KEY='your-key-here'")
        sys.exit(1)
    
    print("🚀 Iniciando evaluación de agentes...")
    print(f"   Agente: {args.agent}")
    print(f"   Benchmark: {args.benchmark}")
    print(f"   Output: {args.output_dir}")
    
    cli = AgentEvaluationCLI()
    cli.evaluator = AgentEffectivenessEvaluator(args.output_dir)
    
    try:
        # Evaluación de efectividad
        if args.agent in ["context_analyzer", "all"]:
            await cli.evaluate_context_analyzer(args.benchmark)
        
        # TODO: Implementar context_builder cuando esté listo
        if args.agent == "context_builder":
            print("⚠️  Context Builder aún no implementado para evaluación")
        
        # Test de consistencia
        if args.consistency:
            await cli.evaluate_consistency(args.agent, args.runs)
        
        # Resumen final
        cli.print_final_summary()
        
    except KeyboardInterrupt:
        print("\n⚠️  Evaluación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error durante la evaluación: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
