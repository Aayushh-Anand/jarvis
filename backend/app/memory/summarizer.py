import json
import time

from google import genai
from google.genai import types

from app.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


SUMMARY_PROMPT = """
You are the conversation summarization system for J.A.R.V.I.S.

Your job is to summarize the conversation so that J.A.R.V.I.S.
can continue the conversation later without needing the full
old conversation.

Keep only useful information such as:

- What the user is trying to accomplish
- Important decisions
- Important technical details
- Problems and errors
- Solutions already tried
- Important preferences mentioned in this conversation
- Current progress
- Unfinished tasks

Do NOT include:

- Repetitive greetings
- Small talk
- Unimportant details
- Information unrelated to the conversation

Write a concise factual summary.

Return ONLY valid JSON:

{
    "summary": "conversation summary"
}
"""


def summarize_conversation(
    messages: list[dict]
) -> str:

    conversation_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in messages
    )

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",

                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(
                                text=conversation_text
                            )
                        ]
                    )
                ],

                config=types.GenerateContentConfig(
                    system_instruction=SUMMARY_PROMPT,
                    response_mime_type="application/json"
                )
            )

            result = json.loads(response.text)

            return result.get(
                "summary",
                ""
            )

        except Exception as e:

            error_message = str(e)

            print(
                f"SUMMARY ERROR "
                f"(attempt {attempt + 1}/{max_retries}): "
                f"{type(e).__name__}: {e}"
            )

            if (
                "503" in error_message
                and attempt < max_retries - 1
            ):

                wait_time = 2 ** attempt

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                raise