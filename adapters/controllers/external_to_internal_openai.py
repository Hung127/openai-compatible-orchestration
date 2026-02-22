from controllers.interfaces.i_in_converter import IInConverter

from adapters.openai_schema import OpenAIMessage, OpenAIRequest
from domain.models import InternalRequest, Message


class OpenAI2InternalInConverter(IInConverter[OpenAIRequest]):
    """
    This is a converter allows external request to be converted to internal request.
    We need this to make the external schema seperated to internal schema (follow the clean architecture)
    This approach allows us to have many converters for many providers
    """

    def to_internal_message(self, message: OpenAIMessage):
        internal_message = Message(role=message.role, content=message.content)
        return internal_message

    def to_internal_request(self, request) -> InternalRequest:
        model = request.model
        external_messages = request.messages
        max_tokens = request.max_tokens
        temperature = request.temperature
        top_p = request.top_p
        internal_messages = list()

        for msg in external_messages:
            internal_messages.append(self.to_internal_message(msg))

        internal_request = InternalRequest(
            messages=internal_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            model=model,
        )

        return internal_request
