import pytest

from adapters.openai_schema import OpenAIResponse
from adapters.presenters.internal_to_external_openai import Internal2OpenAIConverter
from domain.models import InternalResponse, Message, Role, ServiceInformation


def test_ToExternalResponse_InternalResponseWithUsage_ReturnsOpenAIResponse(internal_response):
    # Arrange
    converter = Internal2OpenAIConverter()

    # Act
    result = converter.to_external_response(internal_response)

    # Assert
    assert isinstance(result, OpenAIResponse)
    assert result.id == "chatcmpl-test-123"
    assert result.object == "chat.completion"
    assert result.model == "gemma3:270m"
    assert result.created == 1770289171
    assert result.choices[0].index == 0
    assert result.choices[0].message.role == "assistant"
    assert result.choices[0].message.content == "Hello back"
    assert result.choices[0].finish_reason == internal_response.finish_reason
    assert result.usage.prompt_tokens == 3
    assert result.usage.completion_tokens == 4
    assert result.usage.total_tokens == 7


def test_ToExternalResponse_InternalResponseWithoutUsage_ReturnsOpenAIResponseWithNullUsage():
    # Arrange
    converter = Internal2OpenAIConverter()
    response = InternalResponse(
        id="chatcmpl-no-usage",
        service_info=ServiceInformation(provider="ollama", model="gemma3:270m"),
        generated_message=Message(role=Role.ASSISTANT, content="Done"),
        created=1770289171,
        usage=None,
    )

    # Act
    result = converter.to_external_response(response)

    # Assert
    assert result.id == "chatcmpl-no-usage"
    assert result.model == "gemma3:270m"
    assert result.usage is None
    assert result.choices[0].message.content == "Done"


def test_ToInternalResponse_OpenAIResponseWithChoice_ReturnsInternalResponse(openai_response):
    # Arrange
    converter = Internal2OpenAIConverter()

    # Act
    result = converter.to_internal_response(openai_response, provider="ollama")

    # Assert
    assert result.id == "chatcmpl-test-123"
    assert result.service_info.provider == "ollama"
    assert result.service_info.model == "gemma3:270m"
    assert result.created == 1770289171
    assert result.generated_message.role == Role.ASSISTANT
    assert result.generated_message.content == "Hello back"
    assert result.usage.prompt_tokens == 3
    assert result.usage.completion_tokens == 4
    assert result.usage.total_tokens == 7
    assert result.finish_reason == openai_response.choices[0].finish_reason


def test_ToInternalResponse_OpenAIResponseWithoutChoices_RaisesValueError(openai_response):
    # Arrange
    converter = Internal2OpenAIConverter()
    invalid_response = openai_response.model_copy(update={"choices": []})

    # Act / Assert
    with pytest.raises(ValueError, match="at least one choice"):
        converter.to_internal_response(invalid_response, provider="ollama")
