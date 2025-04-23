import os

import pytest
import random


from graph_iso_checker.graph import Graph
from graph_iso_checker.algorithms.genetic.generational import GeneticAlgorithm
from graph_iso_checker.algorithms.genetic.builder import GeneticAlgorithmBuilder


@pytest.fixture(autouse=True)
def seed_random():
    # фиксируем seed для воспроизводимости
    random.seed(0)
    yield


def test_complete_graph_iso():
    # полный граф на n вершинах всегда изоморфен сам себе под любой перестановкой
    n = 5
    g1 = Graph(n)
    for u in range(n):
        for v in range(u + 1, n):
            g1.add_edge(u, v)
    # создаём произвольную перестановку
    g2, perm = g1.random_permutation()


    # на небольшом количестве поколений и популяции GA должен найти решение сразу
    ga = (GeneticAlgorithmBuilder()
          .with_population_size(20)
          .with_generations(10)
          .with_workers(2)
          .build())


    found, mapping = ga.run(g1, g2, context={})
    assert found is True


    # mapping должен быть перестановкой числа вершин
    assert isinstance(mapping, list)
    assert sorted(mapping) == list(range(n))


    # проверяем корректность отображения
    for u in range(n):
        for v in g1.neighbors(u):
            if u < v:
                assert g2.has_edge(mapping[u], mapping[v])


def test_complete_graph_with_context_edge_count():
    # проверяем, что GA использует edge_count из контекста
    n = 6
    g1 = Graph(n)
    for u in range(n):
        for v in range(u + 1, n):
            g1.add_edge(u, v)
    g2, perm = g1.random_permutation()


    # заранее подсчитанное число рёбер
    m = sum(len(g1.neighbors(u)) for u in range(n)) // 2
    context = {'edge_count': m}


    ga = (GeneticAlgorithmBuilder()
          .with_population_size(10)
          .with_generations(5)
          .with_workers(1)
          .build())


    found, mapping = ga.run(g1, g2, context)
    assert found is True
    assert sorted(mapping) == list(range(n))


def test_non_iso_empty_vs_complete():
    # полный граф и пустой граф на тех же вершинах — GA не найдёт изоморфизма
    n = 4
    g1 = Graph(n)
    for u in range(n):
        for v in range(u + 1, n):
            g1.add_edge(u, v)
    g2 = Graph(n)  # без рёбер


    ga = (GeneticAlgorithmBuilder()
          .with_generations(5)
          .with_workers(1)
          .build())


    found, mapping = ga.run(g1, g2, context={})
    assert found is False
    assert mapping is None


def test_builder_default_and_workers():
    # проверяем настройки по умолчанию и метод with_workers
    builder = GeneticAlgorithmBuilder()
    ga_default = builder.build()
    assert ga_default.population_size == 50
    assert ga_default.max_gens == 200
    assert ga_default.num_workers == os.cpu_count()


    ga_custom = builder.with_workers(3).build()
    assert ga_custom.num_workers == 3


def test_termination_after_zero_generations():
    # проверяем, что при max_gens=0 GA сразу завершится без поиска
    n = 3
    g1 = Graph(n)
    g2 = Graph(n)
    # добавим одно ребро, чтобы target>0
    g1.add_edge(0,1)
    context = {}


    ga = (GeneticAlgorithmBuilder()
          .with_population_size(5)
          .with_generations(0)  # ноль поколений
          .with_workers(1)
          .build())


    found, mapping = ga.run(g1, g2, context)
    # не нашло (или могло, если случайно identity — но алгоритм должен остановиться сразу)
    assert found is False
    assert mapping is None




