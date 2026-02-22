from typing import List

from pydantic import BaseModel

from domain.models import FinishReason, Role


class OpenAIMessage(BaseModel):
    role: Role
    content: str


class OpenAIRequest(BaseModel):
    model: str
    messages: List[OpenAIMessage]
    max_tokens: int | None = None
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
