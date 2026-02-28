from controllers.interfaces.i_in_converter import IInConverter

from adapters.openai_schema import OpenAIMessage, OpenAIRequest
from domain.models import InternalRequest, Message, Role


class OpenAI2InternalInConverter(IInConverter[OpenAIRequest]):
    """
    This is a converter allows external request to be converted to internal request.
    We need this to make the external schema seperated to internal schema (follow the clean architecture)
    This approach allows us to have many converters for many providers
    """

    def _to_internal_message(self, message: OpenAIMessage):
        internal_message = Message(role=Role(message.role), content=message.content)
        return internal_message

    def to_internal_request(self, request) -> InternalRequest:

        internal_request = InternalRequest.model_validate(request.model_dump())

        return internal_request

    def to_external_request(self, request: InternalRequest) -> OpenAIRequest:
        openai_request = OpenAIRequest.model_validate(request.model_dump())
        return openai_request
