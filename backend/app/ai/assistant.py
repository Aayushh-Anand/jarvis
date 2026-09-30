from app.ai.llm import generate_response
from app.memory import conversation_manager
from app.memory.extractor import extract_memory
from app.memory.summarizer import summarize_conversation
from app.tools import tool_executor
from app.tools.router import select_tool


MAX_RECENT_MESSAGES = 20
SUMMARY_TRIGGER_MESSAGES = 20
SUMMARY_INTERVAL = 10


def _save_messages(
    conversation_id: str,
    user_message: str,
    response: str
):
    conversation_manager.add_message(
        conversation_id,
        "user",
        user_message
    )

    conversation_manager.add_message(
        conversation_id,
        "model",
        response
    )


def _format_tool_response(
    tool_name: str,
    tool_result: dict
) -> str:

    if not tool_result.get("success"):
        error = tool_result.get(
            "error",
            "The action could not be completed."
        )

        return f"I couldn't complete that action. {error}"

    result = tool_result.get("result")

    if result:
        return str(result)

    messages = {
        "get_time": "The current time has been retrieved.",
        "get_system_info": "System information has been retrieved.",
        "open_application": "The application has been opened.",
        "open_folder": "The folder has been opened.",
        "open_file": "The file has been opened.",
        "list_folder": "The folder contents have been retrieved.",
        "search_file": "The file search has been completed.",
        "close_application": "The application has been closed.",
        "create_folder": "The folder has been created.",
    }

    return messages.get(
        tool_name,
        "The requested action was completed."
    )


def _update_summary_if_needed(
    conversation_id: str
):
    updated_history = conversation_manager.get_history(
        conversation_id
    )

    existing_summary = conversation_manager.get_summary(
        conversation_id
    )

    should_summarize = False

    if len(updated_history) >= SUMMARY_TRIGGER_MESSAGES:

        if existing_summary is None:
            should_summarize = True

        elif (
            len(updated_history)
            >= existing_summary["message_count"]
            + SUMMARY_INTERVAL
        ):
            should_summarize = True

    if should_summarize:

        try:

            new_summary = summarize_conversation(
                updated_history
            )

            if new_summary:

                conversation_manager.save_summary(
                    conversation_id=conversation_id,
                    summary_text=new_summary,
                    message_count=len(updated_history)
                )

                print(
                    "JARVIS CONVERSATION SUMMARY UPDATED"
                )

        except Exception as e:

            print(
                "Conversation summary skipped:",
                f"{type(e).__name__}: {e}"
            )


def _try_local_memory(message: str):
    """
    Lightweight local memory handling.

    This avoids Gemini for explicit memory commands.
    """

    text = message.strip()

    lower = text.lower()

    memory_prefixes = [
        "remember that ",
        "remember ",
        "please remember that ",
        "please remember ",
    ]

    memory_text = None

    for prefix in memory_prefixes:

        if lower.startswith(prefix):

            memory_text = text[len(prefix):].strip()
            break

    if not memory_text:
        return None

    if not memory_text:
        return None

    try:

        result = conversation_manager.save_or_update_memory(
            memory=memory_text,
            category="general",
            importance=5
        )

        print(
            "JARVIS LOCAL MEMORY:",
            result.get("action"),
            result.get("memory")
        )

        return (
            "Got it. I'll remember that."
        )

    except Exception as e:

        print(
            "Local memory save failed:",
            f"{type(e).__name__}: {e}"
        )

        return (
            "I couldn't save that memory locally."
        )


def _offline_response(message: str) -> str:

    text = message.strip().lower()

    if text in {
        "hi",
        "hello",
        "hey",
        "hi jarvis",
        "hello jarvis",
        "hey jarvis",
    }:
        return (
            "Hello. JARVIS is running in offline mode. "
            "Your local computer controls are available."
        )

    if text in {
        "who are you",
        "what are you",
        "what is jarvis",
    }:
        return (
            "I am J.A.R.V.I.S., your local computer assistant. "
            "I can control supported laptop functions offline."
        )

    if "help" in text:
        return (
            "Offline commands include opening applications, "
            "opening files and folders, searching files, "
            "checking system information, and getting the time."
        )

    return (
        "I'm currently offline, so I can't use Gemini for "
        "general AI questions. Your local computer commands "
        "are still available."
    )


def ask_jarvis(
    conversation_id: str,
    message: str
) -> str:

    # ==================================================
    # 1. LOCAL MEMORY COMMAND
    # ==================================================

    local_memory_response = _try_local_memory(
        message
    )

    if local_memory_response:

        _save_messages(
            conversation_id,
            message,
            local_memory_response
        )

        return local_memory_response

    # ==================================================
    # 2. LOCAL TOOL ROUTER
    # ==================================================

    tool_request = select_tool(message)

    if tool_request.get("use_tool"):

        tool_name = tool_request["tool_name"]
        arguments = tool_request["arguments"]

        print(
            f"JARVIS LOCAL TOOL: {tool_name}"
        )

        print(
            f"JARVIS LOCAL ARGUMENTS: {arguments}"
        )

        try:

            tool_result = tool_executor.execute(
                tool_name=tool_name,
                arguments=arguments
            )

            print(
                "JARVIS LOCAL TOOL RESULT:",
                tool_result
            )

            response = _format_tool_response(
                tool_name,
                tool_result
            )

        except Exception as e:

            print(
                "Local tool execution failed:",
                f"{type(e).__name__}: {e}"
            )

            response = (
                "I couldn't complete that local action."
            )

        _save_messages(
            conversation_id,
            message,
            response
        )

        return response

    # ==================================================
    # 3. NORMAL AI REQUEST
    # ==================================================

    full_history = conversation_manager.get_history(
        conversation_id
    )

    conversation_summary = conversation_manager.get_summary(
        conversation_id
    )

    summary_text = ""

    if conversation_summary:
        summary_text = conversation_summary["summary"]

    history = full_history[-MAX_RECENT_MESSAGES:]

    memories = conversation_manager.get_relevant_memories(
        query=message,
        limit=5
    )

    # ==================================================
    # 4. GEMINI / OFFLINE FALLBACK
    # ==================================================

    try:

        response = generate_response(
            message=message,
            history=history,
            memories=memories,
            conversation_summary=summary_text,
            tool_result=None
        )

    except Exception as e:

        print(
            "Online AI unavailable:",
            f"{type(e).__name__}: {e}"
        )

        response = _offline_response(
            message
        )

    # ==================================================
    # 5. SAVE CONVERSATION
    # ==================================================

    _save_messages(
        conversation_id,
        message,
        response
    )

    # ==================================================
    # 6. AUTOMATIC MEMORY
    # ==================================================

    try:

        memory_result = extract_memory(
            message
        )

        if memory_result.get(
            "should_remember"
        ):

            conversation_manager.save_or_update_memory(
                memory=memory_result["memory"],
                category=memory_result["category"],
                importance=memory_result["importance"]
            )

    except Exception as e:

        print(
            "Automatic memory extraction skipped:",
            f"{type(e).__name__}: {e}"
        )

    # ==================================================
    # 7. SUMMARY
    # ==================================================

    _update_summary_if_needed(
        conversation_id
    )

    return response