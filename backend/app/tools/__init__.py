from app.tools.registry import ToolRegistry
from app.tools.executor import ToolExecutor
from app.tools.safety import ToolSafety

from app.tools.system import (
    GetSystemInfoTool,
    GetTimeTool
)

from app.tools.files import (
    OpenFileTool,
    OpenFolderTool,
    ListFolderTool,
    CreateFolderTool,
    SearchFileTool
)

from app.tools.applications import (
    OpenApplicationTool,
    CloseApplicationTool
)


# =========================================
# TOOL REGISTRY
# =========================================

tool_registry = ToolRegistry()


# =========================================
# SYSTEM TOOLS
# =========================================

tool_registry.register(
    GetSystemInfoTool()
)

tool_registry.register(
    GetTimeTool()
)


# =========================================
# FILE / FOLDER TOOLS
# =========================================

tool_registry.register(
    OpenFileTool()
)

tool_registry.register(
    OpenFolderTool()
)

tool_registry.register(
    ListFolderTool()
)

tool_registry.register(
    CreateFolderTool()
)

tool_registry.register(
    SearchFileTool()
)


# =========================================
# APPLICATION TOOLS
# =========================================

tool_registry.register(
    OpenApplicationTool()
)

tool_registry.register(
    CloseApplicationTool()
)


# =========================================
# SAFETY
# =========================================

tool_safety = ToolSafety()


# =========================================
# EXECUTOR
# =========================================

tool_executor = ToolExecutor(
    registry=tool_registry,
    safety=tool_safety
)