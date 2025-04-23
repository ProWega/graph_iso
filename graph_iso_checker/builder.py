from typing import List, Optional, Tuple
from .stage import Stage, StageResult
from .graph import Graph
from .stages.invariant_stage import InvariantStage
from .stages.refinement_stage import RefinementStage
from .stages.genetic_stage import GeneticStage
from .stages.exact_search_stage import ExactSearchStage


class GraphIsoChecker:
    """
    Выполняет последовательные этапы проверки изоморфизма.
    """
    def __init__(self, stages: List[Stage]):
        self.stages = stages


    def check_isomorphism(
        self, g1: Graph, g2: Graph
    ) -> Tuple[bool, Optional[dict]]:
        """
        Возвращает (is_iso, mapping).
        Если is_iso == True, mapping — отображение вершин g1→g2.
        Если is_iso == False, mapping == None.
        """
        context = {}
        for stage in self.stages:
            result = stage.run(g1, g2, context)
            if result == StageResult.ISO:
                return True, context.get("mapping")
            if result == StageResult.NON_ISO:
                return False, None
        # ни один этап не решил, подразумеваем NON-ISO
        return False, None


class GraphIsoCheckerBuilder:
    """
    Построитель конвейера этапов для GraphIsoChecker.
    """
    def __init__(self):
        self._stages: List[Stage] = []


    def add_invariant_stage(self) -> "GraphIsoCheckerBuilder":
        self._stages.append(InvariantStage())
        return self


    def add_refinement_stage(self) -> "GraphIsoCheckerBuilder":
        self._stages.append(RefinementStage())
        return self


    def add_genetic_stage(
        self, *, population_size: int = 50, generations: int = 200, stall: int = 20
    ) -> "GraphIsoCheckerBuilder":
        self._stages.append(
            GeneticStage(
                population_size=population_size,
                generations=generations,
                stall=stall
            )
        )
        return self


    def add_exact_search_stage(self) -> "GraphIsoCheckerBuilder":
        self._stages.append(ExactSearchStage())
        return self


    def add_stage(self, stage: Stage) -> "GraphIsoCheckerBuilder":
        self._stages.append(stage)
        return self


    def build(self) -> GraphIsoChecker:
        return GraphIsoChecker(self._stages)




