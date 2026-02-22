import uuid
from enum import Enum
from time import time
from typing import List

from pydantic import BaseModel, Field


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    # TODO: add ID for memory later (Phase 2)
    role: Role
    content: str
    # TODO: add created time for memory later (Phase 2)
    # created: int = Field(default_factory=lambda: int(time()))


class ServiceInformation(BaseModel):
    provider: str  # "ollama"
    model: str  # gpt20b...


class UsageStats(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class InternalRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: int
    # TODO: move the default away from this layer (phase 2)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)  # Validated range
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)


class FinishReason(str, Enum):
    STOP = "stop"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"
    TOOL_CALLS = "tool_calls"


class InternalResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    service_info: ServiceInformation
    generated_message: Message  # TODO: research and check if we wanted to send system instructions (as system) and user prompt (as user), how many responses will be sent? -> use List or not
    created: int = Field(default_factory=lambda: int(time()))
    usage: UsageStats
    finish_reason: FinishReason = FinishReason.STOP


# the flow: ClientRequest -> Controller (at outer layer) convert that into InternalRequest (now we do something, like adding memory, some prompt engineering...) -> (Presenter) convert InternalRequest into ServiceRequest (like Ollama or so) -> send -> receive ServiceResponse -> convert to InternalResponse (Controller) -> now do some stuffs with the InternalResponse if we want to -> convert to OpenAIResponse or whatever client wants to (Presenter) -> send to client, I will need to do some dependency injection
