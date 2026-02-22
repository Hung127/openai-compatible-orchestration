from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.models import InternalResponse

TResponse = TypeVar("TResponse")


class IOutConverter(ABC, Generic[TResponse]):
    """
    This is a 'out' converter (internal -> external) allows internal response to be converted to external response.
    We need this to make the external schema seperated to internal schema (follow the clean architecture)
    This approach allows us to have many converters for many providers
    """

    @abstractmethod
    def to_external_response(self, response: InternalResponse) -> TResponse:
        pass
