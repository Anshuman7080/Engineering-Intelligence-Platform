from app.database.base import Base
from app.database.session import engine

# Import every model
from app.conversation.models import Conversation, Message
from app.auth.models import User
from app.repository.models import Repository

def init_db():

    Base.metadata.create_all(bind=engine)