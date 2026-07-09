from abc import ABC, abstractmethod
from domain.models import InternalRequest

class IContextPipeline(ABC):
    @abstractmethod
    def enrich(self, request: InternalRequest) -> InternalRequest:
        pass
