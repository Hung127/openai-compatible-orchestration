from use_cases.interfaces.i_generate_text_completion import (
    IGenerateTextCompletionUseCase,
    InternalRequest,
    InternalResponse,
)
from use_cases.interfaces.i_provider import IProvider


def expand_internal_request(raw_request: InternalRequest) -> InternalRequest:
    # adding more processes here, like adding memory or so
    return raw_request


class GenerateTextCompletionUseCase(IGenerateTextCompletionUseCase):
    def __init__(self, provider: IProvider):
        super().__init__()
        self.provider = provider

    def execute(self, request: InternalRequest) -> InternalResponse:
        # TODO: modifying the request before sending it (like adding memory, prompt engineering in phase 2+)
        expanded_request = expand_internal_request(request)
        return self.provider.send_completion_request(expanded_request)
