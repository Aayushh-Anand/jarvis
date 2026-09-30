import json
import time

from google import genai
from google.genai import types

from app.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


MEMORY_EXTRACTION_PROMPT = """
You are the memory extraction system for J.A.R.V.I.S.

Your job is to determine whether the user's message contains
information that should be remembered for future conversations.

Only extract information that is:
- About the user
- Likely to remain useful in future conversations
- A preference, goal, skill, project, important fact, or ongoing activity

Do NOT save:
- Temporary questions
- General facts
- One-time requests
- Casual conversation
- Sensitive information unless explicitly requested to be remembered

Return a JSON object with this exact structure:

{
    "should_remember": true,
    "memory": "short factual statement",
    "category": "preference|goal|skill|project|learning|career|general",
    "importance": 1
}

Importance:
1-3 = low
4-6 = normal
7-8 = important
9-10 = very important

If nothing should be remembered, return:

{
    "should_remember": false,
    "memory": "",
    "category": "general",
    "importance": 1
}

Return ONLY valid JSON.
"""


def extract_memory(message: str):

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
                                text=message
                            )
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=MEMORY_EXTRACTION_PROMPT,
                    response_mime_type="application/json"
                )
            )

            try:
                return json.loads(response.text)

            except json.JSONDecodeError:

                return {
                    "should_remember": False,
                    "memory": "",
                    "category": "general",
                    "importance": 1
                }

        except Exception as e:

            error_message = str(e)

            print(
                f"MEMORY EXTRACTION ERROR "
                f"(attempt {attempt + 1}/{max_retries}): "
                f"{type(e).__name__}: {e}"
            )

            if "503" in error_message and attempt < max_retries - 1:

                wait_time = 2 ** attempt

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise