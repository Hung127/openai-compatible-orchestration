from use_cases.interfaces.context.i_context_step import IContextStep
from domain.models import InternalRequest, Message, Role

class InjectSystemPromptStep(IContextStep):
    def __init__(self, prompt: str):
        self.prompt = prompt

    def process(self, request: InternalRequest) -> InternalRequest:
        if not self.prompt:
            return request

        messages = [
            Message(role=Role.SYSTEM, content=self.prompt),
            *request.messages,
        ]

        return request.model_copy(update={"messages": messages})
