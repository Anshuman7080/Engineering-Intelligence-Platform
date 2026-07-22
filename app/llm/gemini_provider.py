from google import genai

from app.core.logger import logger
from app.core.settings import settings

from app.llm.base import BaseLLMProvider
from app.llm.exceptions import (
    AuthenticationError,
    ProviderError,
    RateLimitError,
)
from fastapi.concurrency import run_in_threadpool

class GeminiProvider(BaseLLMProvider):

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        logger.info(
            "Gemini provider initialized."
        )

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:

        logger.info(
            "Sending request to Gemini."
        )

        try:


            response = await run_in_threadpool(
                self.client.models.generate_content,
                model=settings.GEMINI_MODEL,
                contents=user_prompt,
                config={
                    "system_instruction": system_prompt,
                    "temperature": temperature,
                },
            )

            # response = self.client.models.generate_content(
            #     model=settings.GEMINI_MODEL,
            #     contents=user_prompt,
            #     config={
            #         "system_instruction": system_prompt,
            #         "temperature": temperature,
            #     },
            # )
            
            print("response of gemini",response)

            if not response.text:
                raise ProviderError(
                    "Gemini returned an empty response."
                )

            logger.info(
                "Gemini response generated successfully."
            )

            return response.text.strip()

        except Exception as e:

            message = str(e).lower()

            logger.exception(
                "Gemini request failed."
            )

            if (
                "429" in message
                or "quota" in message
                or "rate limit" in message
                or "resource_exhausted" in message
            ):
                raise RateLimitError(message)

            if (
                "401" in message
                or "403" in message
                or "api key" in message
                or "permission" in message
            ):
                raise AuthenticationError(message)

            raise ProviderError(message)