from unittest.mock import Mock, patch

from use_cases.generate_text_completion import (
    GenerateTextCompletionUseCase,
    expand_internal_request,
)


def test_ExpandInternalRequest_AnyInternalRequest_ReturnsSameRequest(internal_request):
    # Arrange
    raw_request = internal_request

    # Act
    result = expand_internal_request(raw_request)

    # Assert
    assert result is raw_request


def test_Execute_ValidRequest_CallsProviderWithExpandedRequest(internal_request, internal_response):
    # Arrange
    provider = Mock()
    provider.generate_completion.return_value = internal_response
    use_case = GenerateTextCompletionUseCase(provider)

    # Act
    result = use_case.execute(internal_request)

    # Assert
    assert result == internal_response
    provider.generate_completion.assert_called_once_with(internal_request)


def test_Execute_ExpansionFunctionReturnsModifiedRequest_CallsProviderWithModifiedRequest(internal_request, internal_response):
    # Arrange
    expanded_request = internal_request.model_copy(update={"max_tokens": 128})
    provider = Mock()
    provider.generate_completion.return_value = internal_response
    use_case = GenerateTextCompletionUseCase(provider)

    # Act
    with patch("use_cases.generate_text_completion.expand_internal_request", return_value=expanded_request):
        result = use_case.execute(internal_request)

    # Assert
    assert result == internal_response
    provider.generate_completion.assert_called_once_with(expanded_request)
