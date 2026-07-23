from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.session import SessionLocal
from app.repository.models import Repository
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

    def list_user_conversations(
        self,
        repository_id: str,
        user_id: str,
    ):

        with SessionLocal() as session:

            conversations = (
                session.execute(
                    select(Conversation)
                    .join(Repository)
                    .where(
                        Conversation.repository_id == repository_id,
                        Repository.user_id == user_id,
                    )
                    .order_by(
                        Conversation.updated_at.desc()
                    )
                )
                .scalars()
                .all()
            )

            return [
                {
                    "id": c.id,
                    "title": c.title,
                    "repository_id": c.repository_id,
                    "created_at": c.created_at,
                    "updated_at": c.updated_at,
                }
                for c in conversations
            ]
    
    def delete_user_conversation(
        self,
        conversation_id: str,
        user_id: str,
    ):

        with SessionLocal() as session:

            conversation = (
                session.execute(
                    select(Conversation)
                    .join(Repository)
                    .where(
                        Conversation.id == conversation_id,
                        Repository.user_id == user_id,
                    )
                )
                .scalars()
                .first()
            )

            if conversation is None:
                return False

            session.delete(conversation)
            session.commit()

            return True

    
     
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
        
    def get_user_conversation(
        self,
        conversation_id: str,
        user_id: str,
    ):

        with SessionLocal() as session:

            conversation = (
                session.execute(
                    select(Conversation)
                    .join(Repository)
                    .options(
                        selectinload(
                            Conversation.messages
                        )
                    )
                    .where(
                        Conversation.id == conversation_id,
                        Repository.user_id == user_id,
                    )
                )
                .scalars()
                .first()
            )

            if conversation is not None:

                session.refresh(conversation)
                session.expunge(conversation)

            return conversation