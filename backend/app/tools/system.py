import platform
from datetime import datetime

from app.tools.base import BaseTool


class GetSystemInfoTool(BaseTool):

    name = "get_system_info"

    description = (
        "Get basic information about the user's computer "
        "including operating system, OS version, machine "
        "architecture and processor."
    )

    def execute(self, **kwargs):

        return {
            "success": True,
            "operating_system": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }


class GetTimeTool(BaseTool):

    name = "get_time"

    description = (
        "Get the current local date and time "
        "of the computer."
    )

    def execute(self, **kwargs):

        now = datetime.now()

        return {
            "success": True,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S")
        }