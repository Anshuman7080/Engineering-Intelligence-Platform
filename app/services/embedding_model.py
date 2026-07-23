from sentence_transformers import SentenceTransformer

from app.core.settings import settings
from app.core.logger import logger

logger.info(
    f"Loading embedding model: {settings.EMBEDDING_MODEL}"
)

embedding_model = SentenceTransformer(
    settings.EMBEDDING_MODEL
)

logger.info(
    "Embedding model loaded successfully."
)