from app.database import engine, Base
from app.memory.models import (ConversationMessage, Conversation, ConversationSummary, UserMemory)


print("Creating database tables...")

Base.metadata.create_all(
    bind=engine
)

print("Database tables created successfully.")