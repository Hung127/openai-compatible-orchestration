import pytest
from pydantic import ValidationError

from domain.models import InternalRequest, Message, Role


def test_InternalRequest_ValidRequiredFields_CreatesModelWithDefaults():
    # Arrange
    messages = [Message(role=Role.USER, content="Hello")]

    # Act
    request = InternalRequest(model="gemma3:270m", messages=messages, max_tokens=16)

    # Assert
    assert request.model == "gemma3:270m"
    assert request.messages == messages
    assert request.max_tokens == 16
    assert request.temperature == 0.7
    assert request.top_p == 1.0


def test_InternalRequest_TemperatureBelowMinimum_RaisesValidationError():
    # Arrange
    messages = [Message(role=Role.USER, content="Hello")]

    # Act / Assert
    with pytest.raises(ValidationError):
        InternalRequest(
            model="gemma3:270m",
            messages=messages,
            max_tokens=16,
            temperature=-0.01,
        )


def test_InternalRequest_TemperatureAboveMaximum_RaisesValidationError():
    # Arrange
    messages = [Message(role=Role.USER, content="Hello")]

    # Act / Assert
    with pytest.raises(ValidationError):
        InternalRequest(
            model="gemma3:270m",
            messages=messages,
            max_tokens=16,
            temperature=2.01,
        )


def test_InternalRequest_TopPBelowMinimum_RaisesValidationError():
    # Arrange
    messages = [Message(role=Role.USER, content="Hello")]

    # Act / Assert
    with pytest.raises(ValidationError):
        InternalRequest(
            model="gemma3:270m",
            messages=messages,
            max_tokens=16,
            top_p=-0.01,
        )


def test_InternalRequest_TopPAboveMaximum_RaisesValidationError():
    # Arrange
    messages = [Message(role=Role.USER, content="Hello")]

    # Act / Assert
    with pytest.raises(ValidationError):
        InternalRequest(
            model="gemma3:270m",
            messages=messages,
            max_tokens=16,
            top_p=1.01,
        )


def test_Message_InvalidRole_RaisesValidationError():
    # Arrange
    invalid_role = "developer"

    # Act / Assert
    with pytest.raises(ValidationError):
        Message(role=invalid_role, content="Hello")
