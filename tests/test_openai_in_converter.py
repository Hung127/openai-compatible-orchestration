from adapters.controllers.external_to_internal_openai import OpenAI2InternalInConverter
from adapters.openai_schema import OpenAIMessage, OpenAIRequest
from domain.models import InternalRequest, Message, Role


def test_ToInternalRequest_ValidOpenAIRequest_ReturnsEquivalentInternalRequest():
    # Arrange
    converter = OpenAI2InternalInConverter()
    openai_request = OpenAIRequest(
        model="gemma3:270m",
        messages=[OpenAIMessage(role="user", content="Hello")],
        max_tokens=64,
        temperature=0.6,
        top_p=0.8,
    )

    # Act
    result = converter.to_internal_request(openai_request)

    # Assert
    assert isinstance(result, InternalRequest)
    assert result.model == "gemma3:270m"
    assert result.messages == [Message(role=Role.USER, content="Hello")]
    assert result.max_tokens == 64
    assert result.temperature == 0.6
    assert result.top_p == 0.8


def test_ToExternalRequest_ValidInternalRequest_ReturnsEquivalentOpenAIRequest(internal_request):
    # Arrange
    converter = OpenAI2InternalInConverter()

    # Act
    result = converter.to_external_request(internal_request)

    # Assert
    assert isinstance(result, OpenAIRequest)
    assert result.model == internal_request.model
    assert result.messages[0].role == "user"
    assert result.messages[0].content == "Hello"
    assert result.max_tokens == internal_request.max_tokens
    assert result.temperature == internal_request.temperature
    assert result.top_p == internal_request.top_p


def test_ToInternalMessage_SystemRole_ReturnsInternalSystemMessage():
    # Arrange
    converter = OpenAI2InternalInConverter()
    message = OpenAIMessage(role="system", content="You are helpful")

    # Act
    result = converter._to_internal_message(message)

    # Assert
    assert result == Message(role=Role.SYSTEM, content="You are helpful")
