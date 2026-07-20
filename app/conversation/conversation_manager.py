from app.conversation.repository import ConversationRepository


class ConversationManager:

    def __init__(self):

        self.repository = ConversationRepository()

    def create_conversation(
        self,
        repository_name: str,
        title: str,
    ) -> str:

        return self.repository.create_conversation(
            repository_name=repository_name,
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
        repository_name: str,
    ):

        return self.repository.list_conversations(
            repository_name
        )

    def delete_conversation(
        self,
        conversation_id: str,
    ):

        self.repository.delete_conversation(
            conversation_id
        )


    def get_conversation(
        self,
        conversation_id: str,
    ):
        return self.repository.get_conversation(
            conversation_id
        )    