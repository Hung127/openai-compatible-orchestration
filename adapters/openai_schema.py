from typing import List

from pydantic import BaseModel

from domain.models import Role


class OpenAIMessage(BaseModel):
    role: Role
    content: str


class OpenAIRequest(BaseModel):
    model: str = "mock-super-model"
    messages: List[OpenAIMessage]
    max_tokens: int = 512
    temperature: float = 0.1
    top_p: float = 0.5
