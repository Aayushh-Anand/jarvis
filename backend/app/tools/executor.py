from app.tools.registry import ToolRegistry
from app.tools.safety import ToolSafety


class ToolExecutor:

    def __init__(
        self,
        registry: ToolRegistry,
        safety: ToolSafety
    ):

        self.registry = registry
        self.safety = safety

    def execute(
        self,
        tool_name: str,
        arguments: dict,
        confirmed: bool = False
    ):

        # -----------------------------------------
        # Safety check
        # -----------------------------------------

        if not self.safety.is_allowed(
            tool_name
        ):

            return {
                "success": False,
                "tool": tool_name,
                "error": (
                    "This tool is not allowed "
                    "by JARVIS."
                )
            }

        # -----------------------------------------
        # Confirmation check
        # -----------------------------------------

        if (
            self.safety.requires_confirmation(
                tool_name
            )
            and not confirmed
        ):

            return {
                "success": False,
                "tool": tool_name,
                "requires_confirmation": True,
                "message": (
                    "User confirmation is required "
                    "before executing this action."
                )
            }

        # -----------------------------------------
        # Find tool
        # -----------------------------------------

        tool = self.registry.get(
            tool_name
        )

        if tool is None:

            return {
                "success": False,
                "tool": tool_name,
                "error": (
                    f"Tool '{tool_name}' not found."
                )
            }

        # -----------------------------------------
        # Execute
        # -----------------------------------------

        try:

            result = tool.execute(
                **arguments
            )

            return {
                "success": True,
                "tool": tool_name,
                "result": result
            }

        except TypeError as e:

            return {
                "success": False,
                "tool": tool_name,
                "error": (
                    f"Invalid tool arguments: {e}"
                )
            }

        except Exception as e:

            return {
                "success": False,
                "tool": tool_name,
                "error": str(e)
            }