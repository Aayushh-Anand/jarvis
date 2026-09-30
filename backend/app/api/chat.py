from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ai.assistant import ask_jarvis
from app.memory import conversation_manager


router = APIRouter(
    prefix="/api",
    tags=["JARVIS"]
)


# =========================
# Chat
# =========================

class ChatRequest(BaseModel):
    conversation_id: str
    message: str


class ChatResponse(BaseModel):
    conversation_id: str
    response: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    response = ask_jarvis(
        request.conversation_id,
        request.message
    )

    return ChatResponse(
        conversation_id=request.conversation_id,
        response=response
    )


# =========================
# Conversations
# =========================

class CreateConversationRequest(BaseModel):
    conversation_id: str
    title: str = "New Conversation"


class RenameConversationRequest(BaseModel):
    title: str


class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str


@router.post(
    "/conversations",
    response_model=ConversationResponse
)
def create_conversation(
    request: CreateConversationRequest
):

    existing = conversation_manager.get_conversation(
        request.conversation_id
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Conversation already exists."
        )

    conversation_manager.create_conversation(
        request.conversation_id,
        request.title
    )

    conversation = conversation_manager.get_conversation(
        request.conversation_id
    )

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at.isoformat(),
        updated_at=conversation.updated_at.isoformat()
    )


@router.get(
    "/conversations",
    response_model=list[ConversationResponse]
)
def list_conversations():

    conversations = conversation_manager.list_conversations()

    return [
        ConversationResponse(
            id=conversation["id"],
            title=conversation["title"],
            created_at=conversation["created_at"].isoformat(),
            updated_at=conversation["updated_at"].isoformat()
        )
        for conversation in conversations
    ]


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationResponse
)
def get_conversation(
    conversation_id: str
):

    conversation = conversation_manager.get_conversation(
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at.isoformat(),
        updated_at=conversation.updated_at.isoformat()
    )


@router.patch(
    "/conversations/{conversation_id}",
    response_model=ConversationResponse
)
def rename_conversation(
    conversation_id: str,
    request: RenameConversationRequest
):

    success = conversation_manager.rename_conversation(
        conversation_id,
        request.title
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    conversation = conversation_manager.get_conversation(
        conversation_id
    )

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at.isoformat(),
        updated_at=conversation.updated_at.isoformat()
    )


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str
):

    success = conversation_manager.delete_conversation(
        conversation_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    return {
        "message": "Conversation deleted successfully.",
        "conversation_id": conversation_id
    }

# =========================
# Message History
# =========================

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: str


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse]
)
def get_messages(
    conversation_id: str
):

    conversation = conversation_manager.get_conversation(
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    messages = conversation_manager.get_messages(
        conversation_id
    )

    return [
        MessageResponse(
            id=message["id"],
            role=message["role"],
            content=message["content"],
            created_at=message["created_at"].isoformat()
        )
        for message in messages
    ]
# =========================
# Long-Term Memory
# =========================

class CreateMemoryRequest(BaseModel):
    memory: str
    category: str = "general"
    importance: int = 5


class MemoryResponse(BaseModel):
    id: int
    memory: str
    category: str
    importance: int
    created_at: str
    updated_at: str


@router.post(
    "/memories",
    response_model=MemoryResponse
)
def create_memory(
    request: CreateMemoryRequest
):

    if not 1 <= request.importance <= 10:
        raise HTTPException(
            status_code=400,
            detail="Importance must be between 1 and 10."
        )

    memory = conversation_manager.save_memory(
        memory=request.memory,
        category=request.category,
        importance=request.importance
    )

    return MemoryResponse(
        id=memory["id"],
        memory=memory["memory"],
        category=memory["category"],
        importance=memory["importance"],
        created_at=memory["created_at"].isoformat(),
        updated_at=memory["updated_at"].isoformat()
    )


@router.get(
    "/memories",
    response_model=list[MemoryResponse]
)
def get_memories(
    category: str | None = None
):

    memories = conversation_manager.get_memories(
        category=category
    )

    return [
        MemoryResponse(
            id=memory["id"],
            memory=memory["memory"],
            category=memory["category"],
            importance=memory["importance"],
            created_at=memory["created_at"].isoformat(),
            updated_at=memory["updated_at"].isoformat()
        )
        for memory in memories
    ]


@router.delete("/memories/{memory_id}")
def delete_memory(
    memory_id: int
):

    success = conversation_manager.delete_memory(
        memory_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Memory not found."
        )

    return {
        "message": "Memory deleted successfully.",
        "memory_id": memory_id
    }