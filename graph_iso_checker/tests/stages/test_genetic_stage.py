# tests/stages/test_genetic_stage.py
import pytest
import random


from graph_iso_checker.graph import Graph
from graph_iso_checker.stages.genetic_stage import GeneticStage
from graph_iso_checker.stage import StageResult


@pytest.fixture(autouse=True)
def seed_random():
    # фиксируем seed для воспроизводимости
    random.seed(42)
    yield


def test_genetic_stage_iso_single_vertex():
    # граф из одной вершины — GA найдёт trivial mapping [0]
    g1 = Graph(1)
    g2, _ = g1.random_permutation()
    stage = GeneticStage(population_size=10, generations=10, stall=5)
    context = {}
    result = stage.run(g1, g2, context)
    assert result == StageResult.ISO
    mapping = context.get('mapping')
    assert isinstance(mapping, list)
    assert mapping == [0]


def test_genetic_stage_non_iso_empty_vs_complete():
    # пустой и полный граф на 2 вершинах — не изоморфны
    g1 = Graph(2)
    g2 = Graph(2)
    g2.add_edge(0, 1)
    stage = GeneticStage(population_size=10, generations=10, stall=5)
    context = {}
    result = stage.run(g1, g2, context)
    assert result == StageResult.CONTINUE
    assert 'mapping' not in context


def test_genetic_stage_skip_when_single_color():
    # пропуск GA, если после refinement все вершины одного цвета
    g = Graph(4)
    # полный граф: все вершины одной степени ⇒ один цвет
    for u in range(4):
        for v in range(u+1, 4):
            g.add_edge(u, v)
    context = {'colors1': [0]*4, 'colors2': [0]*4}
    stage = GeneticStage(population_size=10, generations=10, stall=5)
    result = stage.run(g, g, context)
    assert result == StageResult.CONTINUE


def test_genetic_stage_iso_path_graph():
    # путь из 5 вершин — GA должен найти изоморфизм
    g1 = Graph(5)
    for u in range(4):
        g1.add_edge(u, u+1)
    g2, _ = g1.random_permutation()
    stage = GeneticStage(population_size=30, generations=50, stall=10)
    context = {}
    result = stage.run(g1, g2, context)
    assert result == StageResult.ISO
    mapping = context.get('mapping')
    assert isinstance(mapping, list)
    assert sorted(mapping) == list(range(5))




