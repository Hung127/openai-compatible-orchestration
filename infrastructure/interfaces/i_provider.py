from abc import ABC, abstractmethod

from domain.models import InternalRequest, InternalResponse


class IProvider(ABC):
    @abstractmethod
    def generate_completion(self, request: InternalRequest) -> InternalResponse:
        pass
