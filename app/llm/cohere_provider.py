import cohere

from app.core.settings import settings
from app.llm.base import BaseLLMProvider
from app.core.logger import logger

from app.llm.exceptions import (
      AuthenticationError,
    ProviderError,
    RateLimitError,
)

from fastapi.concurrency import run_in_threadpool



class CohereProvider(BaseLLMProvider):

    def __init__(self):
        self.client = cohere.ClientV2(
            api_key=settings.COHERE_API_KEY
        )

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:

        logger.info("Sending request to Cohere.")

        try:

            response = await run_in_threadpool(
                self.client.chat,
                model=settings.COHERE_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
            )     
            # response = self.client.chat(
            #     model=settings.COHERE_MODEL,
            #     messages=[
            #         {"role": "system", "content": system_prompt},
            #         {"role": "user", "content": user_prompt},
            #     ],
            #     temperature=temperature,
            # )

            print("response of cohere",response)
            if not response.message or not response.message.content:
                raise ProviderError("Cohere returned an empty response.")

            # text = response.message.content[0].text.strip()

            text = None

            for item in response.message.content:
                if getattr(item, "type", None) == "text":
                    text = item.text.strip()
                    break

            if text is None:
                raise ProviderError("No text returned by Cohere.")

            logger.info("Cohere response generated successfully.")
            return text

        except Exception as e:
            message = str(e).lower()
            logger.exception("Cohere request failed.")

            
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
