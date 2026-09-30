import re
from pathlib import Path


APPLICATIONS = {
    "chrome": "chrome",
    "google chrome": "chrome",
    "edge": "edge",
    "microsoft edge": "edge",
    "notepad": "notepad",
    "calculator": "calculator",
    "calc": "calculator",
    "file explorer": "explorer",
    "explorer": "explorer",
    "vs code": "vscode",
    "visual studio code": "vscode",
    "vscode": "vscode",
}


def _clean_text(text: str) -> str:
    return text.strip().lower()


def _extract_windows_path(message: str) -> str | None:
    match = re.search(
        r'([a-zA-Z]:\\[^<>:"|?*\r\n]+)',
        message
    )

    if match:
        return match.group(1).strip()

    return None


def _find_application(message: str) -> str | None:
    text = _clean_text(message)

    for name, application in APPLICATIONS.items():
        if name in text:
            return application

    return None


def _is_time_command(text: str) -> bool:
    patterns = [
        "what time is it",
        "what's the time",
        "whats the time",
        "tell me the time",
        "current time",
        "time right now",
        "time now",
    ]

    return any(pattern in text for pattern in patterns)


def _is_system_info_command(text: str) -> bool:
    patterns = [
        "system information",
        "system info",
        "computer information",
        "computer info",
        "pc information",
        "pc info",
        "show system",
        "show computer information",
    ]

    return any(pattern in text for pattern in patterns)


def _is_list_command(text: str) -> bool:
    patterns = [
        "list files",
        "list folder",
        "show files",
        "show folder",
        "show files in",
        "list files in",
    ]

    return any(pattern in text for pattern in patterns)


def _is_search_command(text: str) -> bool:
    patterns = [
        "search file",
        "find file",
        "find a file",
        "search for file",
    ]

    return any(pattern in text for pattern in patterns)


def _is_close_command(text: str) -> bool:
    patterns = [
        "close chrome",
        "close edge",
        "close notepad",
        "close calculator",
        "close vscode",
        "close vs code",
        "close file explorer",
        "close explorer",
    ]

    return any(pattern in text for pattern in patterns)


def _is_create_folder_command(text: str) -> bool:
    patterns = [
        "create folder",
        "make folder",
        "new folder",
    ]

    return any(pattern in text for pattern in patterns)


def _extract_search_query(text: str) -> str | None:
    patterns = [
        r"search file(?: named)?\s+(.+)",
        r"find file(?: named)?\s+(.+)",
        r"find a file(?: named)?\s+(.+)",
        r"search for file(?: named)?\s+(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return match.group(1).strip()

    return None


def _extract_application_for_close(text: str) -> str | None:
    for name, application in APPLICATIONS.items():
        if f"close {name}" in text:
            return application

    return None


def select_tool(message: str) -> dict:
    """
    Local deterministic tool router.

    IMPORTANT:
    This function does NOT call Gemini.
    It is designed for basic offline computer control.
    """

    text = _clean_text(message)

    # -------------------------
    # TIME
    # -------------------------

    if _is_time_command(text):
        return {
            "use_tool": True,
            "tool_name": "get_time",
            "arguments": {},
            "source": "local",
        }

    # -------------------------
    # SYSTEM INFORMATION
    # -------------------------

    if _is_system_info_command(text):
        return {
            "use_tool": True,
            "tool_name": "get_system_info",
            "arguments": {},
            "source": "local",
        }

    # -------------------------
    # CLOSE APPLICATION
    # -------------------------

    if _is_close_command(text):
        application = _extract_application_for_close(text)

        if application:
            return {
                "use_tool": True,
                "tool_name": "close_application",
                "arguments": {
                    "application": application
                },
                "source": "local",
            }

    # -------------------------
    # CREATE FOLDER
    # -------------------------

    if _is_create_folder_command(text):
        path = _extract_windows_path(message)

        if path:
            return {
                "use_tool": True,
                "tool_name": "create_folder",
                "arguments": {
                    "path": path
                },
                "source": "local",
            }

    # -------------------------
    # SEARCH FILE
    # -------------------------

    if _is_search_command(text):
        query = _extract_search_query(text)

        if query:
            return {
                "use_tool": True,
                "tool_name": "search_file",
                "arguments": {
                    "query": query
                },
                "source": "local",
            }

    # -------------------------
    # OPEN EXPLICIT PATH
    # -------------------------

    path = _extract_windows_path(message)

    if path:
        target = Path(path)

        if target.is_dir():
            return {
                "use_tool": True,
                "tool_name": "open_folder",
                "arguments": {
                    "path": path
                },
                "source": "local",
            }

        return {
            "use_tool": True,
            "tool_name": "open_file",
            "arguments": {
                "path": path
            },
            "source": "local",
        }

    # -------------------------
    # LIST FOLDER
    # -------------------------

    if _is_list_command(text):
        path = _extract_windows_path(message)

        if path:
            return {
                "use_tool": True,
                "tool_name": "list_folder",
                "arguments": {
                    "path": path
                },
                "source": "local",
            }

    # -------------------------
    # OPEN APPLICATION
    # -------------------------

    application = _find_application(text)

    if application and (
        "open" in text
        or "launch" in text
        or "start" in text
        or "run" in text
    ):
        return {
            "use_tool": True,
            "tool_name": "open_application",
            "arguments": {
                "application": application
            },
            "source": "local",
        }

    # -------------------------
    # NOT A LOCAL TOOL COMMAND
    # -------------------------

    return {
        "use_tool": False,
        "tool_name": None,
        "arguments": {},
        "source": "local",
    }