from __future__ import annotations

from google import genai

from backend.assistant.models.ai_request import (
    AIRequest,
)
from backend.assistant.models.ai_response import (
    AIResponse,
)
from backend.assistant.models.usage import (
    Usage,
)
from backend.assistant.providers.base_provider import (
    LanguageModel,
)
from backend.shared.settings import settings


class GeminiProvider(LanguageModel):
    """
    Google Gemini language model provider.
    """

    def __init__(
        self,
    ) -> None:

        self._client = genai.Client(
            api_key=settings.assistant.api_key,
        )

    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:

        response = self._client.models.generate_content(
            model=settings.assistant.model,
            contents=[
                request.prompt.system,
                request.prompt.user,
            ],
        )

        usage = Usage()

        if response.usage_metadata:

            usage = Usage(
                input_tokens=(
                    response.usage_metadata.prompt_token_count
                ),
                output_tokens=(
                    response.usage_metadata.candidates_token_count
                ),
                total_tokens=(
                    response.usage_metadata.total_token_count
                ),
            )

        return AIResponse(
            content=response.text,
            model=settings.assistant.model,
            usage=usage,
        )