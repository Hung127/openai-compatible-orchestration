from abc import ABC, abstractmethod
from domain.models import InternalRequest

class IContextStep(ABC):
    @abstractmethod
    def process(self, request: InternalRequest) -> InternalRequest:
        pass
