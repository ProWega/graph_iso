# graph_iso_checker/stages/genetic_stage.py
from ..stage import Stage, StageResult
from ..algorithms.genetic.builder import GeneticAlgorithmBuilder
from ..algorithms.genetic.strategies.termination import StagnationTermination


class GeneticStage(Stage):
    """
    Эвристический этап: GA с color‐refinement и остановкой по застою.
    """
    def __init__(self, population_size=50, generations=200, stall=20):
        self.population_size = population_size
        self.generations     = generations
        self.stall           = stall


    def run(self, g1, g2, context) -> StageResult:
        # пропускаем GA, если после refinement все вершины одной клетки
        cols = context.get('colors1')
        if cols is not None and len(set(cols)) <= 1:
            return StageResult.CONTINUE


        # настраиваем GA с остановкой по застою
        builder = (
            GeneticAlgorithmBuilder()
            .with_population_size(self.population_size)
            .with_generations(self.generations)
            .with_termination(StagnationTermination(self.stall))
        )
        ga = builder.build()


        # запускаем GA
        found, mapping = ga.run(g1, g2, context)
        if found:
            context['mapping'] = mapping
            context['result']  = True
            print(f"Генетический: {StageResult.ISO}")
            return StageResult.ISO

        print(f"Генетический: {StageResult.CONTINUE}")
        # если GA не нашёл — передаём дальше (CONTINUE)
        return StageResult.CONTINUE




