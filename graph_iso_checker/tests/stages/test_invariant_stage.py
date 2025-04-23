import pytest
from graph_iso_checker.stages.invariant_stage import InvariantStage
from graph_iso_checker.stage import StageResult
from graph_iso_checker.graph import Graph


@pytest.fixture
def stage():
    # создаем новый экземпляр InvariantStage перед каждым тестом
    return InvariantStage()


def test_non_iso_edge_count(stage):
    # g1 имеет 1 ребро, g2 — 0 ребер => NON_ISO на этапе EdgeCountInvariant
    g1 = Graph(3)
    g1.add_edge(0, 1)
    g2 = Graph(3)
    context = {}
    status = stage.run(g1, g2, context)
    assert status == StageResult.NON_ISO


def test_non_iso_degree_sequence(stage):
    # оба графа имеют по 2 ребра, но разные последовательности степеней => NON_ISO на DegreeSequenceInvariant
    g1 = Graph(4)
    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g2 = Graph(4)
    g2.add_edge(0, 1)
    g2.add_edge(2, 3)
    context = {}
    status = stage.run(g1, g2, context)
    assert status == StageResult.NON_ISO


def test_iso_unique_degree_trivial(stage):
    # граф из 1 вершины — степени уникальны => ISO, mapping == {0: 0}
    g1 = Graph(1)
    g2 = Graph(1)
    context = {}
    status = stage.run(g1, g2, context)
    assert status == StageResult.ISO
    assert context.get('mapping') == {0: 0}


def test_continue_for_isomorphic(stage):
    # простой путь P3 и его случайная перестановка => все инварианты совпадают, но mapping не построен => CONTINUE
    g1 = Graph(3)
    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g2, perm = g1.random_permutation()
    context = {}
    status = stage.run(g1, g2, context)
    assert status == StageResult.CONTINUE
    assert 'mapping' not in context




