from abc import ABC, abstractmethod

from domain.models import InternalRequest, InternalResponse


class IGenerateTextCompletionUseCase(ABC):
    @abstractmethod
    def execute(self, request: InternalRequest) -> InternalResponse:
        pass
