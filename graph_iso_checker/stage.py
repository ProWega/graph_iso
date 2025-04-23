from enum import Enum
from abc import ABC, abstractmethod


class StageResult(Enum):
    ISO      = 1
    NON_ISO  = 2
    CONTINUE = 3


class Stage(ABC):
    @abstractmethod
    def run(self, g1, g2, context) -> StageResult:
        # Возвращает один из StageResult.
        pass




