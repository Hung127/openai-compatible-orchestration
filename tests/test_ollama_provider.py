from unittest.mock import Mock, patch

from infrastructure.providers.ollama import OllamaProvider


def test_GenerateCompletion_ValidInternalRequest_SendsConvertedRequestToOpenAIClient(internal_request, openai_response, internal_response):
    # Arrange
    in_converter = Mock()
    out_converter = Mock()
    openai_request = in_converter.to_external_request.return_value
    openai_request.model = "gemma3:270m"
    openai_request.max_tokens = 64
    openai_request.temperature = 0.7
    openai_request.top_p = 0.9
    openai_request.messages = [Mock()]
    openai_request.messages[0].model_dump.return_value = {"role": "user", "content": "Hello"}
    out_converter.to_internal_response.return_value = internal_response
    chat_completion = Mock()
    chat_completion.model_dump.return_value = openai_response.model_dump()

    with patch("infrastructure.providers.ollama.OpenAI") as openai_class:
        openai_client = openai_class.return_value
        openai_client.chat.completions.create.return_value = chat_completion
        provider = OllamaProvider(
            base_url="http://localhost:11434/v1",
            in_converter=in_converter,
            out_converter=out_converter,
        )

        # Act
        result = provider.generate_completion(internal_request)

    # Assert
    openai_class.assert_called_once_with(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )
    in_converter.to_external_request.assert_called_once_with(internal_request)
    openai_client.chat.completions.create.assert_called_once_with(
        messages=[{"role": "user", "content": "Hello"}],
        model="gemma3:270m",
        top_p=0.9,
        max_tokens=64,
        temperature=0.7,
    )
    out_converter.to_internal_response.assert_called_once()
    assert out_converter.to_internal_response.call_args.kwargs == {"provider": "ollama"}
    assert result == internal_response


def test_GenerateCompletion_OpenAIClientRaisesException_PropagatesException(internal_request):
    # Arrange
    in_converter = Mock()
    out_converter = Mock()
    openai_request = in_converter.to_external_request.return_value
    openai_request.model = "gemma3:270m"
    openai_request.max_tokens = 64
    openai_request.temperature = 0.7
    openai_request.top_p = 0.9
    openai_request.messages = [Mock()]
    openai_request.messages[0].model_dump.return_value = {"role": "user", "content": "Hello"}

    with patch("infrastructure.providers.ollama.OpenAI") as openai_class:
        openai_client = openai_class.return_value
        openai_client.chat.completions.create.side_effect = RuntimeError("provider unavailable")
        provider = OllamaProvider(
            base_url="http://localhost:11434/v1",
            in_converter=in_converter,
            out_converter=out_converter,
        )

        # Act / Assert
        import pytest

        with pytest.raises(RuntimeError, match="provider unavailable"):
            provider.generate_completion(internal_request)
