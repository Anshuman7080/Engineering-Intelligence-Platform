import uuid

from app.conversation.memory import ConverstaionMemory


class ConversationManager:

    def __init__(self):

        self.memory = ConverstaionMemory()

    def create_conversation(self):

        conversation_id = str(uuid.uuid4())

        return conversation_id

    def add_user_message(
        self,
        conversation_id: str,
        message: str,
    ):

        self.memory.add_message(
            conversation_id=conversation_id,
            role="user",
            content=message,
        )

    def add_assistant_message(
        self,
        conversation_id: str,
        message: str,
    ):

        self.memory.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=message,
        )

    def get_history(
        self,
        conversation_id: str,
    ):

        return self.memory.get_history(conversation_id)

    def clear(
        self,
        conversation_id: str,
    ):

        self.memory.clear(conversation_id)