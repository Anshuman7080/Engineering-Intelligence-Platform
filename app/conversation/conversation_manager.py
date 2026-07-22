from app.conversation.repository import ConversationRepository


class ConversationManager:

    def __init__(self):

        self.repository = ConversationRepository()

    def create_conversation(
        self,
        repository_id: str,
        title: str,
    ) -> str:

        return self.repository.create_conversation(
            repository_id=repository_id,
            title=title,
        )

    def add_user_message(
        self,
        conversation_id: str,
        message: str,
    ):

        self.repository.add_message(
            conversation_id=conversation_id,
            role="user",
            content=message,
        )

    def add_assistant_message(
        self,
        conversation_id: str,
        message: str,
    ):

        self.repository.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=message,
        )

    def get_history(
        self,
        conversation_id: str,
    ):

        return self.repository.get_history(
            conversation_id
        )

    def list_conversations(
        self,
        repository_id: str,
        user_id,
    ):

        return self.repository.list_user_conversations(
            repository_id,
            user_id
        )

    def delete_conversation(
        self,
        conversation_id: str,
        user_id:str,
    ):

        self.repository.delete_user_conversation(
            conversation_id,
            user_id,
        )

    def get_conversation(
        self,
        conversation_id: str,
        user_id:str,
    ):

        return self.repository.get_user_conversation(
            conversation_id,
            user_id,
        )