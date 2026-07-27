# from sentence_transformers import SentenceTransformer

# from app.core.settings import settings
# from app.core.logger import logger

# logger.info(
#     f"Loading embedding model: {settings.EMBEDDING_MODEL}"
# )

# embedding_model = SentenceTransformer(
#     settings.EMBEDDING_MODEL
# )

# logger.info(
#     "Embedding model loaded successfully."
# )


from langchain_cohere import CohereEmbeddings

from app.core.settings import settings
from app.core.logger import logger


logger.info(
    f"Loading Cohere embedding model: {settings.COHERE_EMBEDDING_MODEL}"
)


embedding_model = CohereEmbeddings(
    model=settings.COHERE_EMBEDDING_MODEL,
    cohere_api_key=settings.COHERE_API_KEY
)


logger.info(
    "Cohere embedding model loaded successfully."
)