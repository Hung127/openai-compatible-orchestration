from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.models import InternalRequest, InternalResponse

TRequest = TypeVar("TRequest")


class IInConverter(ABC, Generic[TRequest]):
    """
    This is a 'in' converter (external -> internal) allows external request to be converted to internal request.
    We need this to make the external schema seperated to internal schema (follow the clean architecture)
    This approach allows us to have many converters for many providers
    """

    @abstractmethod
    def to_internal_request(self, request: TRequest) -> InternalRequest:
        pass
