from infrastructure.interfaces.i_provider import IProvider
from use_cases.interfaces.i_generate_text_completion import (
    IGenerateTextCompletionUseCase, InternalRequest, InternalResponse)


class GenerateTextCompletionUseCase(IGenerateTextCompletionUseCase):
    def __init__(self, provider: IProvider):
        super().__init__()
        self.provider = provider

    def _expand_internal_request(self, raw_request: InternalRequest) -> InternalRequest:
        # adding more processes here, like adding memory or so
        return raw_request

    def execute(self, request: InternalRequest) -> InternalResponse:
        # TODO: modifying the request before sending it (like adding memory, prompt engineering in phase 2+)
        expanded_request = self._expand_internal_request(request)
        return self.provider.generate_completion(expanded_request)
