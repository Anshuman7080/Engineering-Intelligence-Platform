class LLMError(Exception):
    """Base exception for every LLM related error."""
    pass


class RateLimitError(LLMError):
    """Raised when provider quota is exceeded or too many requests are sent."""
    pass


class AuthenticationError(LLMError):
    """Raised when API key is invalid."""
    pass


class ProviderError(LLMError):
    """Raised for unexpected provider errors."""
    pass


class GenerationError(LLMError):
    """Raised when all configured providers fail to generate a response."""
    pass
