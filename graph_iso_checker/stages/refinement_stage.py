from ..stage import Stage, StageResult
from collections import Counter


class RefinementStage(Stage):
    # Этап цветового уточнения (Color Refinement / 1-WL)
    def run(self, g1, g2, context) -> StageResult:
        # смотрели на проверке инвариантов
        n = g1.num_vertices


        # начальная раскраска по степеням
        degs1 = [len(g1.neighbors(u)) for u in range(n)]
        degs2 = [len(g2.neighbors(u)) for u in range(n)]


        # компрессия степеней в начальные цвета
        unique_degs = sorted(set(degs1 + degs2))
        deg_to_color = {d: i for i, d in enumerate(unique_degs)}
        colors1 = [deg_to_color[d] for d in degs1]
        colors2 = [deg_to_color[d] for d in degs2]


        # итерации
        while True:
            # собираем сигнатуры (старый цвет, отсортированный список соседних цветов)
            sigs1 = [(colors1[u], tuple(sorted(colors1[v] for v in g1.neighbors(u)))) for u in range(n)]
            sigs2 = [(colors2[u], tuple(sorted(colors2[v] for v in g2.neighbors(u)))) for u in range(n)]


            # создаём новую цветовую карту по уникальным сигнатурам
            all_sigs = sorted(set(sigs1 + sigs2))
            sig_to_color = {sig: i for i, sig in enumerate(all_sigs)}
            new_colors1 = [sig_to_color[s] for s in sigs1]
            new_colors2 = [sig_to_color[s] for s in sigs2]


            # если раскраска не изменилась — выходим
            if new_colors1 == colors1 and new_colors2 == colors2:
                break
            colors1, colors2 = new_colors1, new_colors2


        context['colors1'] = colors1
        context['colors2'] = colors2


        # проверяем совпадение распределения цветов
        if Counter(colors1) != Counter(colors2):
            print(f"Окраска: {StageResult.NON_ISO}")
            return StageResult.NON_ISO


        # если все вершины получили уникальные цвета — строим отображение
        if len(set(colors1)) == n:
            mapping = {u: colors2.index(colors1[u]) for u in range(n)}
            context['mapping'] = mapping
            print(f"Окраска: {StageResult.ISO}")
            return StageResult.ISO


        # иначе продолжаем
        print(f"Окраска: {StageResult.CONTINUE}")
        return StageResult.CONTINUE