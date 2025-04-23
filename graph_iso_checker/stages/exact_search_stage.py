from ..stage import Stage, StageResult


class ExactSearchStage(Stage):
    # Этап точного поиска изоморфизма (упрощённый VF2 / backtracking)
    def run(self, g1, g2, context) -> StageResult:
        # 1) проверка числа вершин
        if g1.num_vertices != g2.num_vertices:
            return StageResult.NON_ISO
        n = g1.num_vertices


        # 2) предварительная проверка последовательности степеней
        deg1 = [len(g1.neighbors(u)) for u in range(n)]
        deg2 = [len(g2.neighbors(v)) for v in range(n)]
        if sorted(deg1) != sorted(deg2):
            return StageResult.NON_ISO


        # 3) выбираем порядок вершин (по убыванию степени) для ускорения поиска
        order = sorted(range(n), key=lambda u: -len(g1.neighbors(u)))


        mapping = {}
        used = set()


        # рекурсивный бэктрекинг
        def backtrack(idx):
            if idx == n:
                return True
            u = order[idx]
            for v in range(n):
                if v in used:
                    continue
                # проверка соответствия степени
                if len(g2.neighbors(v)) != len(g1.neighbors(u)):
                    continue
                # проверка согласованности с уже отображёнными соседями
                ok = True
                for u2 in g1.neighbors(u):
                    if u2 in mapping and not g2.has_edge(v, mapping[u2]):
                        ok = False
                        break
                if not ok:
                    continue
                # пробуем сопоставить u -> v
                mapping[u] = v
                used.add(v)
                if backtrack(idx + 1):
                    return True
                # откат
                used.remove(v)
                del mapping[u]
            return False


        # запуск поиска
        if backtrack(0):
            context['mapping'] = mapping
            context['result'] = True
            return StageResult.ISO
        else:
            return StageResult.NON_ISO




