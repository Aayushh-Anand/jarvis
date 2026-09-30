import os
import subprocess

from app.tools.base import BaseTool


# -------------------------------------------------
# Allowed applications
# -------------------------------------------------

ALLOWED_APPLICATIONS = {
    "chrome": {
        "display_name": "Google Chrome",
        "command": "chrome"
    },

    "edge": {
        "display_name": "Microsoft Edge",
        "command": "msedge"
    },

    "notepad": {
        "display_name": "Notepad",
        "command": "notepad"
    },

    "calculator": {
        "display_name": "Calculator",
        "command": "calc"
    },

    "explorer": {
        "display_name": "File Explorer",
        "command": "explorer"
    }
}


class OpenApplicationTool(BaseTool):

    name = "open_application"

    description = (
        "Open an allowed desktop application on the "
        "user's Windows computer."
    )

    def execute(self, application: str):

        if not application:
            return {
                "success": False,
                "error": "Application name is required."
            }

        application_key = (
            application.strip().lower()
        )

        app = ALLOWED_APPLICATIONS.get(
            application_key
        )

        if app is None:
            return {
                "success": False,
                "error": (
                    f"Application '{application}' "
                    "is not allowed."
                )
            }

        try:

            subprocess.Popen(
                app["command"],
                shell=True
            )

            return {
                "success": True,
                "message": (
                    f"Opened {app['display_name']}."
                )
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }


class CloseApplicationTool(BaseTool):

    name = "close_application"

    description = (
        "Close an allowed desktop application "
        "on the user's Windows computer."
    )

    def execute(self, application: str):

        if not application:
            return {
                "success": False,
                "error": "Application name is required."
            }

        application_key = (
            application.strip().lower()
        )

        process_map = {
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "notepad": "notepad.exe",
            "calculator": "CalculatorApp.exe"
        }

        process_name = process_map.get(
            application_key
        )

        if process_name is None:
            return {
                "success": False,
                "error": (
                    f"Application '{application}' "
                    "cannot be closed by JARVIS."
                )
            }

        try:

            result = subprocess.run(
                [
                    "taskkill",
                    "/IM",
                    process_name,
                    "/F"
                ],
                capture_output=True,
                text=True,
                shell=False
            )

            if result.returncode != 0:

                return {
                    "success": False,
                    "error": (
                        f"{application} is not "
                        "currently running."
                    )
                }

            return {
                "success": True,
                "message": (
                    f"Closed {application}."
                )
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }