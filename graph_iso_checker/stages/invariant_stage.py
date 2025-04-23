import numpy as np
from ..stage import Stage, StageResult
from abc import ABC, abstractmethod
from collections import deque


# Интерфейс инвариантов
class Invariant(ABC):
    @abstractmethod
    # Метод check должен вернуть StageResult.ISO, NON_ISO или CONTINUE
    def check(self, g1, g2, context) -> StageResult:
        pass


# Простые инварианты
class EdgeCountInvariant(Invariant):
    # Проверка равенства числа рёбер
    def check(self, g1, g2, context):
        m1 = sum(len(g1.neighbors(u)) for u in range(g1.num_vertices)) // 2
        m2 = sum(len(g2.neighbors(u)) for u in range(g2.num_vertices)) // 2
        if m1 != m2:
            return StageResult.NON_ISO
        context['edge_count'] = m1
        return StageResult.CONTINUE


class DegreeSequenceInvariant(Invariant):
    # Проверка равенства отсортированной последовательности степеней
    def check(self, g1, g2, context):
        seq1 = sorted(len(g1.neighbors(u)) for u in range(g1.num_vertices))
        seq2 = sorted(len(g2.neighbors(u)) for u in range(g2.num_vertices))
        if seq1 != seq2:
            return StageResult.NON_ISO
        context['degree_sequence'] = seq1
        return StageResult.CONTINUE


class UniqueDegreeInvariant(Invariant):
    # Если все степени уникальны — строим однозначное отображение по степени
    def check(self, g1, g2, context):
        deg1 = [len(g1.neighbors(u)) for u in range(g1.num_vertices)]
        deg2 = [len(g2.neighbors(u)) for u in range(g2.num_vertices)]
        if sorted(deg1) != sorted(deg2):
            return StageResult.CONTINUE
        if len(set(deg1)) != g1.num_vertices:
            return StageResult.CONTINUE
        map1 = {deg1[u]: u for u in range(g1.num_vertices)}
        map2 = {deg2[v]: v for v in range(g2.num_vertices)}
        mapping = {map1[d]: map2[d] for d in map1}
        context['mapping'] = mapping
        return StageResult.ISO


# Расширенные инварианты
class ConnectedComponentsInvariant(Invariant):
    # Проверка равенства числа и размеров связных компонент
    def _components(self, g):
        seen = [False] * g.num_vertices
        sizes = []
        for u in range(g.num_vertices):
            if not seen[u]:
                q = deque([u])
                seen[u] = True
                cnt = 0
                while q:
                    v = q.popleft()
                    cnt += 1
                    for w in g.neighbors(v):
                        if not seen[w]:
                            seen[w] = True
                            q.append(w)
                sizes.append(cnt)
        return sorted(sizes)


    def check(self, g1, g2, context):
        comp1 = self._components(g1)
        comp2 = self._components(g2)
        if comp1 != comp2:
            return StageResult.NON_ISO
        context['components'] = comp1
        return StageResult.CONTINUE


class GraphDiameterInvariant(Invariant):
    # Проверка равенства распределения всех пар расстояний
    def _all_pairs_distances(self, g):
        n = g.num_vertices
        dists = []
        for src in range(n):
            dist = [-1] * n
            dist[src] = 0
            q = deque([src])
            while q:
                v = q.popleft()
                for w in g.neighbors(v):
                    if dist[w] < 0:
                        dist[w] = dist[v] + 1
                        q.append(w)
            # собираем расстояния от src
            for d in dist:
                if d > 0:
                    dists.append(d)
        return sorted(dists)


    def check(self, g1, g2, context):
        d1 = self._all_pairs_distances(g1)
        d2 = self._all_pairs_distances(g2)
        if d1 != d2:
            return StageResult.NON_ISO
        context['distances'] = d1
        return StageResult.CONTINUE


class TriangleCountInvariant(Invariant):
    # Проверка равенства числа треугольников, инцидентных каждой вершине
    def check(self, g1, g2, context):
        def tri_counts(g):
            counts = []
            for v in range(g.num_vertices):
                nbrs = list(g.neighbors(v))
                cnt = 0
                L = len(nbrs)
                for i in range(L):
                    u = nbrs[i]
                    for j in range(i+1, L):
                        w = nbrs[j]
                        if w in g.neighbors(u):
                            cnt += 1
                counts.append(cnt)
            return sorted(counts)


        t1 = tri_counts(g1)
        t2 = tri_counts(g2)
        if t1 != t2:
            return StageResult.NON_ISO
        context['triangle_counts'] = t1
        return StageResult.CONTINUE


class ClusteringCoefficientInvariant(Invariant):
    # Проверка равенства коэффициентов кластеризации вершин
    def check(self, g1, g2, context):
        def clustering(g):
            coeffs = []
            for v in range(g.num_vertices):
                nbrs = list(g.neighbors(v))
                k = len(nbrs)
                if k < 2:
                    coeffs.append(0.0)
                    continue
                links = 0
                for i in range(k):
                    for j in range(i+1, k):
                        if nbrs[j] in g.neighbors(nbrs[i]):
                            links += 1
                coeffs.append(2*links/(k*(k-1)))
            return sorted(coeffs)


        c1 = clustering(g1)
        c2 = clustering(g2)
        if not np.allclose(c1, c2, atol=1e-6):
            return StageResult.NON_ISO
        context['clustering'] = c1
        return StageResult.CONTINUE


class LaplacianSpectrumInvariant(Invariant):
    # Проверка равенства спектров лапласианов графов
    def check(self, g1, g2, context):
        def laplacian_eigs(g):
            n = g.num_vertices
            A = np.zeros((n, n), dtype=float)
            for u in range(n):
                for v in g.neighbors(u):
                    A[u, v] = 1.0
            D = np.diag([len(g.neighbors(u)) for u in range(n)])
            L = D - A
            eigs = np.linalg.eigvalsh(L)
            return np.sort(eigs)


        e1 = laplacian_eigs(g1)
        e2 = laplacian_eigs(g2)
        if not np.allclose(e1, e2, atol=1e-6):
            return StageResult.NON_ISO
        context['spectrum'] = e1.tolist()
        return StageResult.CONTINUE


# Композит
class CompositeInvariant(Invariant):
    # Последовательно применяет все инварианты
    def __init__(self, invariants):
        self.invariants = invariants


    def check(self, g1, g2, context):
        for inv in self.invariants:
            res = inv.check(g1, g2, context)
            if res in (StageResult.NON_ISO, StageResult.ISO):
                return res
        return StageResult.CONTINUE


class InvariantStage(Stage):
    # Этап, применяющий CompositeInvariant
    def __init__(self, invariants=None):
        if invariants is None:
            invariants = [
                EdgeCountInvariant(),
                DegreeSequenceInvariant(),
                UniqueDegreeInvariant(),
                ConnectedComponentsInvariant(),
                GraphDiameterInvariant(),
                TriangleCountInvariant(),
                ClusteringCoefficientInvariant(),
                LaplacianSpectrumInvariant()
            ]
        self.composite = CompositeInvariant(invariants)


    def run(self, g1, g2, context) -> StageResult:
        res = self.composite.check(g1, g2, context)
        if res == StageResult.NON_ISO:
            context['result'] = False
        elif res == StageResult.ISO:
            context['result'] = True
        return res




