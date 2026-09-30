class ToolSafety:

    # -----------------------------------------
    # Tools that can execute immediately
    # -----------------------------------------

    SAFE_TOOLS = {
        "get_system_info",
        "get_time",
        "list_folder",
        "search_file",
        "open_file",
        "open_folder",
        "open_application"
    }

    # -----------------------------------------
    # Tools requiring confirmation
    # -----------------------------------------

    CONFIRMATION_REQUIRED = {
        "close_application",
        "create_folder"
    }

    def requires_confirmation(
        self,
        tool_name: str
    ) -> bool:

        return (
            tool_name
            in self.CONFIRMATION_REQUIRED
        )

    def is_allowed(
        self,
        tool_name: str
    ) -> bool:

        return (
            tool_name in self.SAFE_TOOLS
            or
            tool_name in self.CONFIRMATION_REQUIRED
        )


tool_safety = ToolSafety()