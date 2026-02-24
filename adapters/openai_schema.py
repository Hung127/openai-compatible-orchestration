from typing import List, Literal

from pydantic import BaseModel

from domain.models import FinishReason

OpenAIRole = Literal["system", "user", "assistant"]


class OpenAIMessage(BaseModel):
    role: OpenAIRole
    content: str


class OpenAIRequest(BaseModel):
    model: str
    messages: List[OpenAIMessage]
    max_tokens: int
    temperature: float = 1.0
    top_p: float = 1.0


class OpenAIChoice(BaseModel):
    index: int
    message: OpenAIMessage
    finish_reason: FinishReason


class OpenAIUsageStats(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class OpenAIResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    model: str
    created: int
    choices: List[OpenAIChoice]
    usage: OpenAIUsageStats | None
