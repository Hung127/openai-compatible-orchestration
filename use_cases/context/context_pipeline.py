from use_cases.interfaces.context.i_context_pipeline import IContextPipeline
from use_cases.interfaces.context.i_context_step import IContextStep
from domain.models import InternalRequest

class ContextPipeline(IContextPipeline):
    def __init__(self, steps: list[IContextStep]):
        self.steps = steps

    def enrich(self, request: InternalRequest) -> InternalRequest:
        result = request.copy()
        for step in self.steps:
            result = step.process(result)
        return result
