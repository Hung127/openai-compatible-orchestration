from abc import ABC, abstractmethod

from domain.models import InternalRequest, InternalResponse


class IProvider(ABC):
    @abstractmethod
    def send_completion_request(self, request: InternalRequest) -> InternalResponse:
        pass
