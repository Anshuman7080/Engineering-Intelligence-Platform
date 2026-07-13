from app.core.logger import logger
from app.core.settings import settings

from app.llm.provider_factory import ProviderFactory
from app.llm.exceptions import (
    GenerationError,
    RateLimitError,
    AuthenticationError,
    ProviderError,
)


class LLMService:

    def __init__(self):
        self.primary_provider = settings.LLM_PROVIDER.lower()

        self.providers = [self.primary_provider]

        if self.primary_provider == "gemini":
            self.providers.append("cohere")
        elif self.primary_provider == "cohere":
            self.providers.append("gemini")

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:

        last_exception = None

        for provider_name in self.providers:
            provider = ProviderFactory.get_provider(provider_name)

            try:
                logger.info(f"Trying LLM provider: {provider_name}")

                response = await provider.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=temperature,
                )

                logger.info(f"{provider_name} generated response successfully.")
                return response

            except RateLimitError as error:
                logger.warning(f"{provider_name} quota exceeded. Trying next provider.")
                last_exception = error

            except AuthenticationError as error:
                logger.error(f"{provider_name} authentication failed.")
                last_exception = error

            except ProviderError as error:
                logger.exception(f"{provider_name} provider error.")
                last_exception = error

            except Exception as error:
                logger.exception(f"{provider_name} failed with unexpected error.")
                last_exception = error

        raise GenerationError("All configured LLM providers failed.") from last_exception
