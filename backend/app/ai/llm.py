import time

from google import genai
from google.genai import types

from app.config import settings
from app.ai.prompts import JARVIS_SYSTEM_PROMPT


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def generate_response(
    message: str,
    history: list[dict],
    memories: list[dict] | None = None,
    conversation_summary: str | None = None,
    tool_result: dict | None = None
) -> str:

    contents = []

    for item in history:

        contents.append(
            types.Content(
                role=item["role"],
                parts=[
                    types.Part.from_text(
                        text=item["content"]
                    )
                ]
            )
        )

    summary_context = ""

    if conversation_summary:

        summary_context = (
            "\n\nCONVERSATION SUMMARY:\n"
            + conversation_summary
            + "\n\n"
        )

    memory_context = ""

    if memories:

        memory_lines = []

        for memory in memories:

            memory_lines.append(
                f"- {memory['memory']}"
            )

        memory_context = (
            "\n\nIMPORTANT USER MEMORY:\n"
            + "\n".join(memory_lines)
            + "\n\n"
        )

    tool_context = ""

    if tool_result:

        tool_context = (
            "\n\nTOOL EXECUTION RESULT:\n"
            + str(tool_result)
            + "\n\n"
        )

    current_message = (
        summary_context
        + memory_context
        + tool_context
        + "CURRENT USER MESSAGE:\n"
        + message
    )

    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=current_message
                )
            ]
        )
    )

    # Only retry temporary server overload.
    # Do NOT repeatedly retry quota errors.

    for attempt in range(2):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        JARVIS_SYSTEM_PROMPT
                        + """
When a tool execution result is provided:
- Treat it as the result of an action that has already been executed.
- Do not claim an action succeeded if the tool result says it failed.
- Respond naturally and concisely.
- Do not expose internal tool names, JSON, or implementation details unless the user asks.
"""
                    )
                )
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response.text

        except Exception as e:

            error_message = str(e)

            print(
                "JARVIS AI ERROR "
                f"(attempt {attempt + 1}/2): "
                f"{type(e).__name__}: {e}"
            )

            # Quota errors should immediately
            # fall back to offline mode.

            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED"
                in error_message
            ):
                raise

            # Temporary server issue.

            if (
                "503" in error_message
                and attempt == 0
            ):

                time.sleep(2)

                continue

            raise