from adapters.openai_schema import (
    OpenAIChoice,
    OpenAIMessage,
    OpenAIResponse,
    OpenAIUsageStats,
)
from adapters.presenters.interfaces.i_out_converter import IOutConverter
from domain.models import InternalResponse, Message, UsageStats


class Internal2OpenAIConverter(IOutConverter[OpenAIResponse]):

    def to_openai_usage_stats(
        self, internal_usage_stats: UsageStats
    ) -> OpenAIUsageStats | None:
        return OpenAIUsageStats(
            prompt_tokens=internal_usage_stats.prompt_tokens,
            completion_tokens=internal_usage_stats.completion_tokens,
            total_tokens=internal_usage_stats.total_tokens,
        )

    def to_openai_message(self, internal_message: Message) -> OpenAIMessage:
        return OpenAIMessage(
            role=internal_message.role,
            content=internal_message.content,
        )

    def to_external_response(self, response: InternalResponse) -> OpenAIResponse:
        response_id = response.id
        model = response.service_info.model
        created = response.created
        generated_message = self.to_openai_message(response.generated_message)
        choices = [
            OpenAIChoice(
                index=0,
                message=generated_message,
                finish_reason=response.finish_reason,
            )
        ]

        usage = self.to_openai_usage_stats(response.usage)
        openai_response = OpenAIResponse(
            id=response_id, model=model, created=created, choices=choices, usage=usage
        )

        return openai_response
