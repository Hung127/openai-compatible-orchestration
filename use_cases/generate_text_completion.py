from infrastructure.interfaces.i_provider import IProvider
from use_cases.interfaces.i_generate_text_completion import (
    IGenerateTextCompletionUseCase, InternalRequest, InternalResponse)
from use_cases.interfaces.context.i_context_pipeline import IContextPipeline


class GenerateTextCompletionUseCase(IGenerateTextCompletionUseCase):
    def __init__(self, provider: IProvider, context_pipeline: IContextPipeline):
        super().__init__()
        self.provider = provider
        self.context_pipeline = context_pipeline

    def execute(self, request: InternalRequest) -> InternalResponse:
        expanded_request = self.context_pipeline.enrich(request=request)
        return self.provider.generate_completion(expanded_request)
