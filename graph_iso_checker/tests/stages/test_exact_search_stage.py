# tests/stages/test_exact_search_stage.py
import pytest
import random


from graph_iso_checker.graph import Graph
from graph_iso_checker.stages.exact_search_stage import ExactSearchStage
from graph_iso_checker.stage import StageResult


@pytest.fixture(autouse=True)
def seed_random():
    # Фиксируем seed для воспроизводимости
    random.seed(0)
    yield


def test_exact_single_vertex():
    # Граф из одной вершины
    g1 = Graph(1)
    g2, perm = g1.random_permutation()
    stage = ExactSearchStage()
    context = {}
    result = stage.run(g1, g2, context)
    assert result == StageResult.ISO
    mapping = context.get('mapping')
    assert isinstance(mapping, dict)
    assert mapping.keys() == {0}
    assert mapping[0] == perm[0]


@pytest.mark.parametrize("n", [2, 3, 5])
def test_exact_iso_random_permutation(n):
    # Случайный граф и его перестановка
    g1 = Graph(n)
    for u in range(n):
        for v in range(u+1, n):
            if random.random() < 0.5:
                g1.add_edge(u, v)
    g2, _ = g1.random_permutation()
    stage = ExactSearchStage()
    context = {}
    result = stage.run(g1, g2, context)
    assert result == StageResult.ISO
    mapping = context.get('mapping')
    # mapping должен быть отображением всех вершин
    assert set(mapping.keys()) == set(range(n))
    assert set(mapping.values()) == set(range(n))
    # Проверяем корректность отображения рёбер
    for u in range(n):
        for v in g1.neighbors(u):
            if u < v:
                assert g2.has_edge(mapping[u], mapping[v])


def test_non_iso_vertex_count():
    # Разное число вершин
    g1 = Graph(3)
    g2 = Graph(4)
    stage = ExactSearchStage()
    context = {}
    result = stage.run(g1, g2, context)
    assert result == StageResult.NON_ISO


def test_non_iso_degree_sequence():
    # Разные последовательности степеней
    g1 = Graph(3)
    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g2 = Graph(3)
    g2.add_edge(0, 1)
    stage = ExactSearchStage()
    context = {}
    result = stage.run(g1, g2, context)
    assert result == StageResult.NON_ISO


def test_non_iso_path_vs_cycle():
    # Путь vs цикл одного размера
    g_path = Graph(4)
    for u in range(3):
        g_path.add_edge(u, u+1)
    g_cycle = Graph(4)
    for u in range(3):
        g_cycle.add_edge(u, u+1)
    g_cycle.add_edge(3, 0)
    stage = ExactSearchStage()
    context = {}
    result = stage.run(g_path, g_cycle, context)
    assert result == StageResult.NON_ISO


def test_exact_iso_complete_graph_100():
    # Полный граф на 100 вершинах и его перестановка
    n = 100
    g1 = Graph(n)
    for u in range(n):
        for v in range(u+1, n):
            g1.add_edge(u, v)
    g2, perm = g1.random_permutation()
    stage = ExactSearchStage()
    context = {}
    result = stage.run(g1, g2, context)
    assert result == StageResult.ISO
    mapping = context.get('mapping')
    # mapping должен корректно отображать все вершины
    assert set(mapping.keys()) == set(range(n))
    assert set(mapping.values()) == set(range(n))
    # проверяем сохранение edge correspondence
    for u in range(n):
        for v in g1.neighbors(u):
            if u < v:
                assert g2.has_edge(mapping[u], mapping[v])




