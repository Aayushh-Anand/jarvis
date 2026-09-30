from datetime import datetime

from sqlalchemy import select, delete

from app.database import SessionLocal
from app.memory.models import (
    Conversation,
    ConversationMessage,
    ConversationSummary,
    UserMemory
)


class ConversationManager:

    # =========================
    # Conversations
    # =========================

    def create_conversation(
        self,
        conversation_id: str,
        title: str = "New Conversation"
    ):
        with SessionLocal() as db:

            conversation = Conversation(
                id=conversation_id,
                title=title
            )

            db.add(conversation)
            db.commit()

    def get_conversation(
        self,
        conversation_id: str
    ):
        with SessionLocal() as db:

            statement = (
                select(Conversation)
                .where(
                    Conversation.id == conversation_id
                )
            )

            return db.scalars(statement).first()

    def list_conversations(self):

        with SessionLocal() as db:

            statement = (
                select(Conversation)
                .order_by(
                    Conversation.updated_at.desc()
                )
            )

            conversations = db.scalars(statement).all()

            return [
                {
                    "id": conversation.id,
                    "title": conversation.title,
                    "created_at": conversation.created_at,
                    "updated_at": conversation.updated_at
                }
                for conversation in conversations
            ]

    def rename_conversation(
        self,
        conversation_id: str,
        title: str
    ):

        with SessionLocal() as db:

            statement = (
                select(Conversation)
                .where(
                    Conversation.id == conversation_id
                )
            )

            conversation = db.scalars(statement).first()

            if conversation is None:
                return False

            conversation.title = title
            conversation.updated_at = datetime.utcnow()

            db.commit()

            return True

    def delete_conversation(
        self,
        conversation_id: str
    ):

        with SessionLocal() as db:

            message_statement = delete(
                ConversationMessage
            ).where(
                ConversationMessage.conversation_id
                == conversation_id
            )

            db.execute(message_statement)

            conversation_statement = delete(
                Conversation
            ).where(
                Conversation.id == conversation_id
            )

            result = db.execute(
                conversation_statement
            )

            db.commit()

            return result.rowcount > 0

    # =========================
    # Conversation Messages
    # =========================

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str
    ):

        with SessionLocal() as db:

            conversation = db.get(
                Conversation,
                conversation_id
            )

            if conversation is None:

                conversation = Conversation(
                    id=conversation_id,
                    title="New Conversation"
                )

                db.add(conversation)

            message = ConversationMessage(
                conversation_id=conversation_id,
                role=role,
                content=content
            )

            conversation.updated_at = datetime.utcnow()

            db.add(message)
            db.commit()

    def get_history(
        self,
        conversation_id: str
    ):

        with SessionLocal() as db:

            statement = (
                select(ConversationMessage)
                .where(
                    ConversationMessage.conversation_id
                    == conversation_id
                )
                .order_by(
                    ConversationMessage.created_at
                )
            )

            messages = db.scalars(statement).all()

            return [
                {
                    "role": message.role,
                    "content": message.content
                }
                for message in messages
            ]

    def get_messages(
        self,
        conversation_id: str
    ):

        with SessionLocal() as db:

            statement = (
                select(ConversationMessage)
                .where(
                    ConversationMessage.conversation_id
                    == conversation_id
                )
                .order_by(
                    ConversationMessage.created_at
                )
            )

            messages = db.scalars(statement).all()

            return [
                {
                    "id": message.id,
                    "role": message.role,
                    "content": message.content,
                    "created_at": message.created_at
                }
                for message in messages
            ]

    def clear_conversation(
        self,
        conversation_id: str
    ):

        with SessionLocal() as db:

            statement = delete(
                ConversationMessage
            ).where(
                ConversationMessage.conversation_id
                == conversation_id
            )

            db.execute(statement)

            db.commit()

    # =========================
    # conversation summaries
    # =========================
    
    def get_summary(self, conversation_id: str):
        with SessionLocal() as db:

            statement = (
                select(ConversationSummary)
                .where(
                    ConversationSummary.conversation_id
                    == conversation_id
                )
            )

            summary = db.scalars(statement).first()

            if summary is None:
                return None

            return {
                "id": summary.id,
                "conversation_id": summary.conversation_id,
                "summary": summary.summary,
                "message_count": summary.message_count,
                "created_at": summary.created_at,
                "updated_at": summary.updated_at
            }

    def save_summary(
        self,
        conversation_id: str,
        summary_text: str,
        message_count: int
    ):
        with SessionLocal() as db:

            statement = (
                select(ConversationSummary)
                .where(
                    ConversationSummary.conversation_id
                    == conversation_id
                )
            )

            summary = db.scalars(statement).first()

            if summary is None:

                summary = ConversationSummary(
                    conversation_id=conversation_id,
                    summary=summary_text,
                    message_count=message_count
                )

                db.add(summary)

            else:

                summary.summary = summary_text
                summary.message_count = message_count
                summary.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(summary)

            return {
                "conversation_id": summary.conversation_id,
                "summary": summary.summary,
                "message_count": summary.message_count
            }

    # =========================
    # Long-Term Memory
    # =========================

    def save_memory(
        self,
        memory: str,
        category: str = "general",
        importance: int = 5
    ):

        with SessionLocal() as db:

            user_memory = UserMemory(
                memory=memory,
                category=category,
                importance=importance
            )

            db.add(user_memory)
            db.commit()
            db.refresh(user_memory)

            return {
                "id": user_memory.id,
                "memory": user_memory.memory,
                "category": user_memory.category,
                "importance": user_memory.importance,
                "created_at": user_memory.created_at,
                "updated_at": user_memory.updated_at
            }

    def get_memories(
        self,
        category: str | None = None
    ):

        with SessionLocal() as db:

            statement = select(UserMemory)

            if category:

                statement = statement.where(
                    UserMemory.category == category
                )

            statement = statement.order_by(
                UserMemory.importance.desc(),
                UserMemory.updated_at.desc()
            )

            memories = db.scalars(statement).all()

            return [
                {
                    "id": memory.id,
                    "memory": memory.memory,
                    "category": memory.category,
                    "importance": memory.importance,
                    "created_at": memory.created_at,
                    "updated_at": memory.updated_at
                }
                for memory in memories
            ]

    def delete_memory(
        self,
        memory_id: int
    ):

        with SessionLocal() as db:

            memory = db.get(
                UserMemory,
                memory_id
            )

            if memory is None:
                return False

            db.delete(memory)
            db.commit()

            return True
    def get_relevant_memories(
    self,
    query: str,
    limit: int = 5
    ):
        with SessionLocal() as db:

            statement = select(UserMemory)

        memories = db.scalars(statement).all()

        query_words = set(
            word.lower().strip(".,!?;:()[]{}")
            for word in query.split()
            if len(word) > 2
        )

        scored_memories = []

        for memory in memories:

            memory_words = set(
                word.lower().strip(".,!?;:()[]{}")
                for word in memory.memory.split()
                if len(word) > 2
            )

            overlap = query_words.intersection(memory_words)

            score = len(overlap)

            scored_memories.append(
                (score, memory.importance, memory)
            )

        scored_memories.sort(
            key=lambda item: (
                item[0],
                item[1]
            ),
            reverse=True
        )

        selected_memories = [
            item[2]
            for item in scored_memories
            if item[0] > 0
        ][:limit]

        return [
            {
                "id": memory.id,
                "memory": memory.memory,
                "category": memory.category,
                "importance": memory.importance
            }
            for memory in selected_memories
        ]
    def find_similar_memory(
    self,
    memory_text: str,
    category: str
    ):
        with SessionLocal() as db:

            statement = (
            select(UserMemory)
            .where(
                UserMemory.category == category
            )
        )

        memories = db.scalars(statement).all()

        new_words = set(
            memory_text.lower().split()
        )

        best_match = None
        best_score = 0

        for memory in memories:

            existing_words = set(
                memory.memory.lower().split()
            )

            if not new_words or not existing_words:
                continue

            intersection = (
                new_words & existing_words
            )

            score = (
                len(intersection)
                / len(new_words)
            )

            if score > best_score:

                best_score = score
                best_match = memory

        if best_score >= 0.5:
            return best_match

        return None
    def find_similar_memory(
    self,
    memory_text: str,
    category: str
    ):
        with SessionLocal() as db:

            statement = (
            select(UserMemory)
            .where(
                UserMemory.category == category
            )
        )

        memories = db.scalars(statement).all()

        new_words = set(
            memory_text.lower().split()
        )

        best_match = None
        best_score = 0

        for memory in memories:

            existing_words = set(
                memory.memory.lower().split()
            )

            if not new_words or not existing_words:
                continue

            intersection = (
                new_words & existing_words
            )

            score = (
                len(intersection)
                / len(new_words)
            )

            if score > best_score:

                best_score = score
                best_match = memory

        if best_score >= 0.5:
            return best_match

        return None