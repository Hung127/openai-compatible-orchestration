from fastapi import Depends

from adapters.controllers.external_to_internal_openai import OpenAI2InternalInConverter
from adapters.controllers.interfaces.i_in_converter import IInConverter
from adapters.openai_schema import OpenAIRequest, OpenAIResponse
from adapters.presenters.interfaces.i_out_converter import IOutConverter
from adapters.presenters.internal_to_external_openai import Internal2OpenAIConverter
from infrastructure.interfaces.i_provider import IProvider
from infrastructure.providers.ollama import OllamaProvider
from use_cases.generate_text_completion import GenerateTextCompletionUseCase

openai_in_converter = OpenAI2InternalInConverter()
openai_out_converter = Internal2OpenAIConverter()


def get_openai_in_converter() -> IInConverter[OpenAIRequest]:
    return openai_in_converter


def get_openai_out_converter() -> IOutConverter[OpenAIResponse]:
    return openai_out_converter


def get_provider(
    in_converter: IInConverter[OpenAIRequest] = Depends(get_openai_in_converter),
    out_converter: IOutConverter[OpenAIResponse] = Depends(get_openai_out_converter),
) -> IProvider:
    return OllamaProvider(
        base_url="http://localhost:11434/v1",  # Ollama with openai-compatible api
        in_converter=in_converter,
        out_converter=out_converter,
    )


def get_completion_use_case(provider: IProvider = Depends(get_provider)):
    return GenerateTextCompletionUseCase(provider)
