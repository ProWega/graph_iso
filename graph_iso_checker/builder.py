from .stage import StageResult
from .stage import Stage
from .graph import Graph
from .stages.invariant_stage import InvariantStage
from .stages.refinement_stage import RefinementStage
from .stages.genetic_stage import GeneticStage
from .stages.exact_search_stage import ExactSearchStage


class GraphIsoChecker:
    def __init__(self, stages: list[Stage]):
        self.stages = stages


    def check_isomorphism(self, g1: Graph, g2: Graph):
        context = {}
        for st in self.stages:
            res = st.run(g1, g2, context)
            if res == StageResult.ISO:
                return True, context.get('mapping')
            if res == StageResult.NON_ISO:
                return False, None
        return False, None


class GraphIsoCheckerBuilder:
    def __init__(self):
        self._stages = []


    def add_invariant_stage(self):
        self._stages.append(InvariantStage())
        return self


    def add_refinement_stage(self):
        self._stages.append(RefinementStage())
        return self


    def add_genetic_stage(self, **kwargs):
        self._stages.append(GeneticStage(**kwargs))
        return self


    def add_exact_search_stage(self):
        self._stages.append(ExactSearchStage())
        return self


    def add_stage(self, stage: Stage):
        self._stages.append(stage)
        return self


    def build(self):
        return GraphIsoChecker(self._stages)




