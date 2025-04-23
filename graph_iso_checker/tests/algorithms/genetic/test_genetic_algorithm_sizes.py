import pytest
import random


from graph_iso_checker.graph import Graph
from graph_iso_checker.algorithms.genetic.builder import GeneticAlgorithmBuilder


@pytest.fixture(autouse=True)
def seed_random():
    # фиксируем seed для воспроизводимости
    random.seed(42)
    yield


@pytest.mark.parametrize("n", [1, 2, 3, 5, 10])
def test_iso_random_graph(n):
    # для разных n генерируем случайный граф и его перестановку
    g1 = Graph(n)
    # случайное добавление ребер с вероятностью 0.3
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < 0.3:
                g1.add_edge(u, v)
    g2, _ = g1.random_permutation()


    ga = (GeneticAlgorithmBuilder()
          .with_population_size(20)
          .with_generations(100)
          .with_workers(1)
          .build())
    found, mapping = ga.run(g1, g2, context={})
    assert found is True
    assert isinstance(mapping, list)
    assert sorted(mapping) == list(range(n))
    # проверяем корректность отображения
    for u in range(n):
        for v in g1.neighbors(u):
            if u < v:
                assert g2.has_edge(mapping[u], mapping[v])


@pytest.mark.parametrize("n", [2, 3, 5, 10])
def test_non_iso_empty_vs_complete(n):
    # полный граф и пустой граф на n вершинах не изоморфны
    g1 = Graph(n)
    for u in range(n):
        for v in range(u + 1, n):
            g1.add_edge(u, v)
    g2 = Graph(n)


    ga = (GeneticAlgorithmBuilder()
          .with_population_size(20)
          .with_generations(50)
          .with_workers(1)
          .build())
    found, mapping = ga.run(g1, g2, context={})
    assert found is False
    assert mapping is None


@pytest.mark.parametrize("n", [4, 6, 8])
def test_non_iso_path_vs_cycle(n):
    # путь и цикл одинакового размера не изоморфны
    g_path = Graph(n)
    for u in range(n - 1):
        g_path.add_edge(u, u + 1)
    g_cycle = Graph(n)
    for u in range(n - 1):
        g_cycle.add_edge(u, u + 1)
    if n > 2:
        g_cycle.add_edge(n - 1, 0)


    ga = (GeneticAlgorithmBuilder()
          .with_population_size(20)
          .with_generations(50)
          .with_workers(1)
          .build())
    found, mapping = ga.run(g_path, g_cycle, context={})
    assert found is False
    assert mapping is None




