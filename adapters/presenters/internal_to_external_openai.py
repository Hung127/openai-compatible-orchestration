from adapters.openai_schema import (OpenAIChoice, OpenAIMessage,
                                    OpenAIResponse, OpenAIUsageStats)
from adapters.presenters.interfaces.i_out_converter import IOutConverter
from domain.models import (InternalResponse, Message, Role, ServiceInformation,
                           UsageStats)


class Internal2OpenAIConverter(IOutConverter[OpenAIResponse]):

    def _to_openai_usage_stats(
        self, internal_usage_stats: UsageStats
    ) -> OpenAIUsageStats:
        return OpenAIUsageStats(
            prompt_tokens=internal_usage_stats.prompt_tokens,
            completion_tokens=internal_usage_stats.completion_tokens,
            total_tokens=internal_usage_stats.total_tokens,
        )

    def _to_internal_usage_stats(
        self, openai_usage_stats: OpenAIUsageStats
    ) -> UsageStats:
        return UsageStats(
            prompt_tokens=openai_usage_stats.prompt_tokens,
            completion_tokens=openai_usage_stats.completion_tokens,
            total_tokens=openai_usage_stats.total_tokens,
        )

    def _to_openai_message(self, internal_message: Message) -> OpenAIMessage:
        return OpenAIMessage(
            role=internal_message.role.value,
            content=internal_message.content,
        )

    def _to_internal_message(self, openai_message: OpenAIMessage) -> Message:
        return Message(
            role=Role(openai_message.role),
            content=openai_message.content,
        )

    def to_external_response(self, response: InternalResponse) -> OpenAIResponse:
        response_id = response.id
        model = response.service_info.model
        created = response.created
        generated_message = self._to_openai_message(response.generated_message)
        choices = [
            OpenAIChoice(
                index=0,  # for now
                message=generated_message,
                finish_reason=response.finish_reason,
            )
        ]

        usage = self._to_openai_usage_stats(response.usage) if response.usage else None
        openai_response = OpenAIResponse(
            id=response_id, model=model, created=created, choices=choices, usage=usage
        )

        return openai_response

    def to_internal_response(
        self, response: OpenAIResponse, provider: str = "unknown"
    ) -> InternalResponse:
        if not response.choices:
            raise ValueError("OpenAI response must contain at least one choice")

        return InternalResponse(
            id=response.id,
            service_info=ServiceInformation(model=response.model, provider=provider),
            created=response.created,
            usage=(
                self._to_internal_usage_stats(response.usage)
                if response.usage
                else None
            ),
            finish_reason=(response.choices[0].finish_reason),
            generated_message=self._to_internal_message(response.choices[0].message),
        )
