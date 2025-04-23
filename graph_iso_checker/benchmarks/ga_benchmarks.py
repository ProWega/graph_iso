# graph_iso_checker/benchmarks/ga_benchmark.py
import os
import time
import random
from itertools import product
from tqdm import tqdm
from graph_iso_checker.graph import Graph, generate_random_graph
from graph_iso_checker.algorithms.genetic.builder import GeneticAlgorithmBuilder


def generate_test_graphs(sizes, p_list, num_per_config=3):
    pairs = []
    for n in sizes:
        # пустой
        g = Graph(n); g2, _ = g.random_permutation()
        pairs.append((g, g2, f"empty_n{n}"))
        # полный
        g = Graph(n)
        for u in range(n):
            for v in range(u+1,n):
                g.add_edge(u,v)
        g2, _ = g.random_permutation()
        pairs.append((g, g2, f"complete_n{n}"))
        # путь
        g = Graph(n)
        for u in range(n-1):
            g.add_edge(u,u+1)
        g2, _ = g.random_permutation()
        pairs.append((g, g2, f"path_n{n}"))
        # цикл
        g = Graph(n)
        for u in range(n-1):
            g.add_edge(u,u+1)
        if n>2: g.add_edge(n-1,0)
        g2, _ = g.random_permutation()
        pairs.append((g, g2, f"cycle_n{n}"))
        # случайные
        for p in p_list:
            for i in range(num_per_config):
                g = generate_random_graph(n, p)
                g2, _ = g.random_permutation()
                pairs.append((g, g2, f"rand_n{n}_p{p:.2f}_{i}"))
    return pairs


def benchmark_ga(graph_pairs, pop_size, gen_count, workers=None):
    stats = []
    builder = (GeneticAlgorithmBuilder()
               .with_population_size(pop_size)
               .with_generations(gen_count))
    if workers:
        builder = builder.with_workers(workers)
    ga = builder.build()


    print(f"\n→ pop={pop_size}, gens={gen_count}, workers={workers or os.cpu_count()}")
    for g1, g2, name in tqdm(graph_pairs, desc="Graphs", unit="g"):
        context = {}
        start = time.perf_counter()
        found, mapping = ga.run(g1, g2, context)
        elapsed = time.perf_counter() - start
        status = "OK" if found else "FAIL"
        # промежуточный вывод
        print(f"  {name:20s} : {status} in {elapsed:.2f}s")
        stats.append({
            "name":    name,
            "n":       g1.num_vertices,
            "pop":     pop_size,
            "gens":    gen_count,
            "workers": workers or os.cpu_count(),
            "success": found,
            "time_s":  elapsed
        })
    return stats


def run_benchmarks():
    sizes      = [10, 20]
    p_list     = [0.1, 0.5]
    num_per    = 2
    pop_sizes  = [10, 15]
    gen_counts = [3]
    workers    = None  # или 6


    graph_pairs = generate_test_graphs(sizes, p_list, num_per)


    all_stats = []
    for pop, gen in product(pop_sizes, gen_counts):
        stats = benchmark_ga(graph_pairs, pop, gen, workers)
        all_stats.extend(stats)


    # Сводный результат
    print("\n=== Summary ===")
    for rec in all_stats:
        print(rec)


if __name__ == "__main__":
    run_benchmarks()




