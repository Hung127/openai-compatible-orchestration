import pytest

from adapters.openai_schema import OpenAIChoice, OpenAIMessage, OpenAIResponse, OpenAIUsageStats
from domain.models import (
    FinishReason,
    InternalRequest,
    InternalResponse,
    Message,
    Role,
    ServiceInformation,
    UsageStats,
)


@pytest.fixture
def internal_request():
    return InternalRequest(
        model="gemma3:270m",
        messages=[Message(role=Role.USER, content="Hello")],
        max_tokens=64,
        temperature=0.7,
        top_p=0.9,
    )


@pytest.fixture
def internal_response():
    return InternalResponse(
        id="chatcmpl-test-123",
        service_info=ServiceInformation(provider="ollama", model="gemma3:270m"),
        generated_message=Message(role=Role.ASSISTANT, content="Hello back"),
        created=1770289171,
        usage=UsageStats(prompt_tokens=3, completion_tokens=4, total_tokens=7),
        finish_reason=FinishReason.STOP,
    )


@pytest.fixture
def openai_request_payload():
    return {
        "model": "gemma3:270m",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 64,
        "temperature": 0.7,
        "top_p": 0.9,
    }


@pytest.fixture
def openai_response():
    return OpenAIResponse(
        id="chatcmpl-test-123",
        model="gemma3:270m",
        created=1770289171,
        choices=[
            OpenAIChoice(
                index=0,
                message=OpenAIMessage(role="assistant", content="Hello back"),
                finish_reason=FinishReason.STOP,
            )
        ],
        usage=OpenAIUsageStats(prompt_tokens=3, completion_tokens=4, total_tokens=7),
    )
