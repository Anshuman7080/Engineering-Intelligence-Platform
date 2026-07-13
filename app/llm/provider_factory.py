from app.llm.gemini_provider import GeminiProvider
from app.llm.cohere_provider import CohereProvider


class ProviderFactory:

    @staticmethod
    def get_provider(provider_name: str):

        provider_name = provider_name.lower()

        if provider_name == "gemini":
            return GeminiProvider()

        if provider_name == "cohere":
            return CohereProvider()

        raise ValueError(
            f"Unsupported provider: {provider_name}"
        )