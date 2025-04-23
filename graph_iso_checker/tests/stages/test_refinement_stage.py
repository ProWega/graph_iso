import pytest
from collections import Counter
from graph_iso_checker.stages.refinement_stage import RefinementStage
from graph_iso_checker.stage import StageResult
from graph_iso_checker.graph import Graph


@pytest.fixture
def stage():
    # создаём новый экземпляр RefinementStage для каждого теста
    return RefinementStage()


def test_iso_single_vertex(stage):
    # для 1 вершины раскраска уникальна сразу, должно вернуть ISO и mapping {0: 0}
    g1 = Graph(1)
    g2 = Graph(1)
    context = {}
    status = stage.run(g1, g2, context)
    assert status == StageResult.ISO
    assert context.get('mapping') == {0: 0}
    # проверяем, что цвета записаны
    assert 'colors1' in context and 'colors2' in context
    assert context['colors1'] == [0]
    assert context['colors2'] == [0]


def test_continue_two_vertices_edge(stage):
    # граф из 2 вершин с ребром не дает уникальные цвета: status CONTINUE
    g1 = Graph(2)
    g1.add_edge(0, 1)
    g2, perm = g1.random_permutation()
    context = {}
    status = stage.run(g1, g2, context)
    assert status == StageResult.CONTINUE
    # цвета обеих графов имеют одинаковое распределение
    assert Counter(context['colors1']) == Counter(context['colors2'])
    # mapping не должен быть построен
    assert 'mapping' not in context


def test_continue_path_of_length_2(stage):
    # путь из 3 вершин: две концовые одного цвета, центральная другого
    g1 = Graph(3)
    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g2, perm = g1.random_permutation()
    context = {}
    status = stage.run(g1, g2, context)
    assert status == StageResult.CONTINUE
    # должно получиться ровно 2 класса цветов
    assert len(set(context['colors1'])) == 2
    assert Counter(context['colors1']) == Counter(context['colors2'])


def test_continue_cycle_of_4(stage):
    # цикл из 4 вершин не разделяется алгоритмом - особенность
    g1 = Graph(4)
    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g1.add_edge(2, 3)
    g1.add_edge(3, 0)
    g2, perm = g1.random_permutation()
    context = {}
    status = stage.run(g1, g2, context)
    assert status == StageResult.CONTINUE
    # все вершины одного цвета
    assert set(context['colors1']) == {0}
    assert context['colors1'] == context['colors2']


def test_non_iso_degree_distribution(stage):
    # разные распределения степеней приводят к NON_ISO
    g1 = Graph(3)
    g1.add_edge(0, 1)  # degs: [1,1,0]
    g2 = Graph(3)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)  # degs: [1,2,1]
    context = {}
    status = stage.run(g1, g2, context)
    assert status == StageResult.NON_ISO




