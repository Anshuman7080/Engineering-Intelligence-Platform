from app.database.base import Base
from app.database.session import engine

# Import every model
from app.conversation.models import Conversation, Message


def init_db():

    Base.metadata.create_all(bind=engine)