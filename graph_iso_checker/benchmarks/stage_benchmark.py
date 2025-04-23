# graph_iso_checker/benchmarks/stage_benchmark.py
import os
import time
import random
from itertools import product


from graph_iso_checker.graph import Graph, generate_random_graph
from graph_iso_checker.stages.invariant_stage import InvariantStage
from graph_iso_checker.stages.refinement_stage import RefinementStage
from graph_iso_checker.stages.genetic_stage import GeneticStage
from graph_iso_checker.stages.exact_search_stage import ExactSearchStage


def generate_test_graphs(sizes, p_list, num_random=2):
    """
    Генерирует список пар графов:
      - empty, complete, path, cycle
      - случайные G(n, p)
    """
    pairs = []
    for n in sizes:
        # empty
        g = Graph(n)
        g2, _ = g.random_permutation()
        pairs.append((g, g2, f"empty_n{n}"))
        # complete
        g = Graph(n)
        for u in range(n):
            for v in range(u+1, n):
                g.add_edge(u, v)
        g2, _ = g.random_permutation()
        pairs.append((g, g2, f"complete_n{n}"))
        # path
        g = Graph(n)
        for u in range(n-1):
            g.add_edge(u, u+1)
        g2, _ = g.random_permutation()
        pairs.append((g, g2, f"path_n{n}"))
        # cycle
        g = Graph(n)
        for u in range(n-1):
            g.add_edge(u, u+1)
        if n > 2:
            g.add_edge(n-1, 0)
        g2, _ = g.random_permutation()
        pairs.append((g, g2, f"cycle_n{n}"))
        # random
        for p in p_list:
            for i in range(num_random):
                g = generate_random_graph(n, p)
                g2, _ = g.random_permutation()
                pairs.append((g, g2, f"rand_n{n}_p{p:.2f}_{i}"))
    return pairs


def benchmark_stages(graph_pairs, stage_factories):
    """
    Запускает каждый этап для каждой пары графов,
    выводит промежуточные результаты и собирает статистику.
    """
    stats = []
    for stage_name, factory in stage_factories:
        print(f"\n*** Stage: {stage_name} ***")
        for g1, g2, gname in graph_pairs:
            stage = factory()
            context = {}
            start = time.perf_counter()
            result = stage.run(g1, g2, context)
            elapsed = time.perf_counter() - start
            # промежуточный вывод
            print(f"{stage_name:12s} on {gname:20s} n={g1.num_vertices:3d} -> "
                  f"{result.name:8s} in {elapsed:.4f}s")
            stats.append({
                "stage":  stage_name,
                "graph":  gname,
                "n":      g1.num_vertices,
                "result": result,
                "time_s": elapsed
            })
    return stats


def run_stage_benchmark():
    sizes = [20, 50, 100]
    p_list = [0.1, 0.5]
    num_random = 2


    graph_pairs = generate_test_graphs(sizes, p_list, num_random)


    stage_factories = [
        ("invariant",  lambda: InvariantStage()),
        ("refinement", lambda: RefinementStage()),
        ("genetic",    lambda: GeneticStage(population_size=50, generations=20)),
        ("exact",      lambda: ExactSearchStage())
    ]


    stats = benchmark_stages(graph_pairs, stage_factories)


    # итоговая сводка
    print("\n=== Summary ===")
    print(f"{'stage':12s} {'graph':20s} {'n':>3s} {'time_s':>8s} {'result':>8s}")
    print("-" * 54)
    for rec in stats:
        print(f"{rec['stage']:12s} {rec['graph']:20s} "
              f"{rec['n']:3d} {rec['time_s']:8.4f} {rec['result'].name:>8s}")


if __name__ == "__main__":
    run_stage_benchmark()




