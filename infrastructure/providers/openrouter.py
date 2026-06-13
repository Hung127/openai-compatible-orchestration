import os
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from adapters.controllers.interfaces.i_in_converter import IInConverter
from adapters.openai_schema import OpenAIRequest, OpenAIResponse
from adapters.presenters.interfaces.i_out_converter import IOutConverter
from domain.models import InternalRequest, InternalResponse
from infrastructure.interfaces.i_provider import IProvider


class OpenRouterProvider(IProvider):
    def __init__(
        self,
        in_converter: IInConverter[OpenAIRequest],
        out_converter: IOutConverter[OpenAIResponse],
        base_url: str = "https://openrouter.ai/api/v1",
    ):
        load_dotenv()
        self.client = OpenAI(
            base_url=base_url,
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
        self.in_converter = in_converter
        self.out_converter = out_converter

    def generate_completion(self, request: InternalRequest) -> InternalResponse:
        openai_request = self.in_converter.to_external_request(request)

        messages = cast(
            list[ChatCompletionMessageParam],
            [msg.model_dump() for msg in openai_request.messages],
        )

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=openai_request.model,
            top_p=openai_request.top_p,
            max_tokens=openai_request.max_tokens,
            temperature=openai_request.temperature,
        )

        openai_response = OpenAIResponse.model_validate(chat_completion.model_dump())

        return self.out_converter.to_internal_response(
            openai_response, provider="openrouter"
        )
