from unittest.mock import Mock

from fastapi.testclient import TestClient

from dependencies import (
    get_completion_use_case,
    get_openai_in_converter,
    get_openai_out_converter,
)
from main import app


def test_GetModels_NoState_ReturnsStaticModelList():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/v1/models")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "object": "list",
        "data": [
            {
                "id": "gemma3:270m",
                "object": "model",
                "created": 1770289171,
                "owned_by": "library",
            },
            {
                "id": "smallthinker:latest",
                "object": "model",
                "created": 1770095935,
                "owned_by": "library",
            },
        ],
    }


def test_Completions_ValidPayload_ReturnsConvertedOpenAIResponse(openai_request_payload, internal_request, internal_response, openai_response):
    # Arrange
    in_converter = Mock()
    use_case = Mock()
    out_converter = Mock()
    in_converter.to_internal_request.return_value = internal_request
    use_case.execute.return_value = internal_response
    out_converter.to_external_response.return_value = openai_response
    app.dependency_overrides[get_openai_in_converter] = lambda: in_converter
    app.dependency_overrides[get_completion_use_case] = lambda: use_case
    app.dependency_overrides[get_openai_out_converter] = lambda: out_converter
    client = TestClient(app)

    # Act
    response = client.post("/v1/chat/completions", json=openai_request_payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == "chatcmpl-test-123"
    assert response.json()["object"] == "chat.completion"
    assert response.json()["model"] == "gemma3:270m"
    assert response.json()["choices"][0]["message"] == {
        "role": "assistant",
        "content": "Hello back",
    }
    assert response.json()["usage"] == {
        "prompt_tokens": 3,
        "completion_tokens": 4,
        "total_tokens": 7,
    }
    in_converter.to_internal_request.assert_called_once()
    use_case.execute.assert_called_once_with(internal_request)
    out_converter.to_external_response.assert_called_once_with(internal_response)
    app.dependency_overrides.clear()


def test_Completions_MissingRequiredMaxTokens_ReturnsValidationError(openai_request_payload):
    # Arrange
    invalid_payload = dict(openai_request_payload)
    invalid_payload.pop("max_tokens")
    client = TestClient(app)

    # Act
    response = client.post("/v1/chat/completions", json=invalid_payload)

    # Assert
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "max_tokens"]


def test_Completions_InvalidMessageRole_ReturnsValidationError(openai_request_payload):
    # Arrange
    invalid_payload = dict(openai_request_payload)
    invalid_payload["messages"] = [{"role": "developer", "content": "Hello"}]
    client = TestClient(app)

    # Act
    response = client.post("/v1/chat/completions", json=invalid_payload)

    # Assert
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "messages", 0, "role"]


def test_Completions_UseCaseRaisesException_PropagatesServerException(openai_request_payload, internal_request):
    # Arrange
    in_converter = Mock()
    use_case = Mock()
    out_converter = Mock()
    in_converter.to_internal_request.return_value = internal_request
    use_case.execute.side_effect = RuntimeError("use case failed")
    app.dependency_overrides[get_openai_in_converter] = lambda: in_converter
    app.dependency_overrides[get_completion_use_case] = lambda: use_case
    app.dependency_overrides[get_openai_out_converter] = lambda: out_converter
    client = TestClient(app)

    # Act / Assert
    import pytest

    with pytest.raises(RuntimeError, match="use case failed"):
        client.post("/v1/chat/completions", json=openai_request_payload)

    app.dependency_overrides.clear()
