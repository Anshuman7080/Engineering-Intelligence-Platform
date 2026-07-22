from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.session import SessionLocal

from app.conversation.models import (
    Conversation,
    Message,
)


class ConversationRepository:

    def create_conversation(
        self,
        repository_id: str,
        title: str,
    ) -> str:

        with SessionLocal() as session:

            conversation = Conversation(
                repository_id=repository_id,
                title=title,
            )

            session.add(conversation)
            session.commit()
            session.refresh(conversation)

            return conversation.id

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ):

        with SessionLocal() as session:

            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
            )

            session.add(message)
            session.commit()

    def get_history(
        self,
        conversation_id: str,
    ) -> list[dict]:

        return self.get_conversation_messages(
            conversation_id
        )

    def list_conversations(
        self,
        repository_id: str,
    ) -> list[dict]:

        with SessionLocal() as session:

            conversations = session.execute(
                select(Conversation)
                .where(
                    Conversation.repository_id == repository_id
                )
                .order_by(
                    Conversation.updated_at.desc()
                )
            ).scalars().all()

            return [
                {
                    "id": conversation.id,
                    "title": conversation.title,
                    "repository_id": conversation.repository_id,
                    "created_at": conversation.created_at,
                    "updated_at": conversation.updated_at,
                }
                for conversation in conversations
            ]

    def delete_conversation(
        self,
        conversation_id: str,
    ):

        with SessionLocal() as session:

            conversation = session.get(
                Conversation,
                conversation_id,
            )

            if conversation:

                session.delete(conversation)
                session.commit()

    def get_conversation(
        self,
        conversation_id: str,
    ) -> dict | None:

        with SessionLocal() as session:

            conversation = session.get(
                Conversation,
                conversation_id,
            )

            if conversation is None:
                return None

            return {
                "id": conversation.id,
                "repository_id": conversation.repository_id,
                "title": conversation.title,
                "created_at": conversation.created_at,
                "updated_at": conversation.updated_at,
            }
     
    def delete_repository_conversations(
    self,
    repository_id: str,
    ):

        with SessionLocal() as session:

            conversations = session.execute(
                select(Conversation).where(
                    Conversation.repository_id == repository_id
                )
            ).scalars().all()

            for conversation in conversations:
                session.delete(conversation)

            session.commit() 


    def get_conversation_messages(
        self,
        conversation_id: str,
    ) -> list[dict]:

        with SessionLocal() as session:

            conversation = session.execute(
                select(Conversation)
                .options(
                    selectinload(
                        Conversation.messages
                    )
                )
                .where(
                    Conversation.id == conversation_id
                )
            ).scalar_one_or_none()

            if conversation is None:
                return []

            return [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in conversation.messages
            ]