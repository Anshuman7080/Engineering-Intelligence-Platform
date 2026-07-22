import shutil
from pathlib import Path

from app.core.logger import logger
from app.core.settings import settings

from app.graph.graph_service import GraphService
from app.repository.repository import RepositoryRepository
from app.conversation.repository import ConversationRepository
from app.services.pinecone_service import PineconeService


class RepositoryCleanupService:

    def __init__(self):

        self.repository_repository = RepositoryRepository()
        self.conversation_repository = ConversationRepository()
        self.graph_service = GraphService()
        self.vector_service = PineconeService()

    def delete_repository(
        self,
        repository_id: str,
    ):

        repository = self.repository_repository.get(
            repository_id
        )

        if repository is None:
            raise ValueError("Repository not found.")

        user_id = repository.user_id
        repository_name = repository.repository_name

        logger.info(
            f"Deleting repository '{repository_name}'"
        )

        try:

           
            logger.info("Deleting vectors...")

            self.vector_service.delete_repository_vectors(
                user_id=user_id,
                repository_name=repository_name,
            )

           
            logger.info("Deleting graph...")

            self.graph_service.delete_repository(
                user_id=user_id,
                repository_name=repository_name,
            )

           
            logger.info("Deleting conversations...")

            self.conversation_repository.delete_repository_conversations(
                repository_id
            )

            logger.info("Deleting repository folder...")

            self._delete_repository_folder(
                user_id,
                repository_name,
            )


            logger.info("Deleting repository row...")

            self.repository_repository.delete(
                repository_id
            )

            logger.info(
                "Repository deleted successfully."
            )

        except Exception as ex:

            logger.exception(ex)

            raise

    def _delete_repository_folder(
        self,
        user_id: str,
        repository_name: str,
    ):

        repository_path = (
            "data/repositories/"
            + repository_name.replace("/", "__")
        )

        if repository_path.exists():

            shutil.rmtree(repository_path)

            logger.info(
                f"Deleted folder: {repository_path}"
            )