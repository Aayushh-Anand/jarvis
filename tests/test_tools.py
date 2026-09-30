from app.tools import (
    tool_registry,
    tool_executor
)


print("=" * 70)
print("J.A.R.V.I.S. TOOL ENGINE V1 TEST")
print("=" * 70)


# ============================================================
# AVAILABLE TOOLS
# ============================================================

print("\nAVAILABLE TOOLS:\n")

for tool in tool_registry.list_tools():

    print(f"✓ {tool.name}")
    print(f"  {tool.description}")
    print()


# ============================================================
# SYSTEM INFO
# ============================================================

print("=" * 70)
print("TEST 1 — SYSTEM INFORMATION")
print("=" * 70)

result = tool_executor.execute(
    tool_name="get_system_info",
    arguments={}
)

print(result)


# ============================================================
# TIME
# ============================================================

print("\n" + "=" * 70)
print("TEST 2 — CURRENT TIME")
print("=" * 70)

result = tool_executor.execute(
    tool_name="get_time",
    arguments={}
)

print(result)


# ============================================================
# LIST FOLDER
# ============================================================

print("\n" + "=" * 70)
print("TEST 3 — LIST JARVIS PROJECT")
print("=" * 70)

result = tool_executor.execute(
    tool_name="list_folder",
    arguments={
        "path": r"D:\Projects\jarvis"
    }
)

print(result)


# ============================================================
# SEARCH FILE
# ============================================================

print("\n" + "=" * 70)
print("TEST 4 — SEARCH BACKEND")
print("=" * 70)

result = tool_executor.execute(
    tool_name="search_file",
    arguments={
        "directory": r"D:\Projects\jarvis",
        "name": "backend"
    }
)

print(result)


# ============================================================
# OPEN APPLICATION
# ============================================================

print("\n" + "=" * 70)
print("TEST 5 — OPEN NOTEPAD")
print("=" * 70)

result = tool_executor.execute(
    tool_name="open_application",
    arguments={
        "application": "notepad"
    }
)

print(result)


# ============================================================
# CLOSE APPLICATION
# ============================================================

print("\n" + "=" * 70)
print("TEST 6 — CLOSE NOTEPAD WITHOUT CONFIRMATION")
print("=" * 70)

result = tool_executor.execute(
    tool_name="close_application",
    arguments={
        "application": "notepad"
    }
)

print(result)


# ============================================================
# CLOSE APPLICATION WITH CONFIRMATION
# ============================================================

print("\n" + "=" * 70)
print("TEST 7 — CLOSE NOTEPAD WITH CONFIRMATION")
print("=" * 70)

result = tool_executor.execute(
    tool_name="close_application",
    arguments={
        "application": "notepad"
    },
    confirmed=True
)

print(result)


# ============================================================
# CREATE FOLDER WITHOUT CONFIRMATION
# ============================================================

print("\n" + "=" * 70)
print("TEST 8 — CREATE FOLDER WITHOUT CONFIRMATION")
print("=" * 70)

result = tool_executor.execute(
    tool_name="create_folder",
    arguments={
        "path": r"D:\Projects\jarvis\test_safety_folder"
    }
)

print(result)


# ============================================================
# UNKNOWN TOOL
# ============================================================

print("\n" + "=" * 70)
print("TEST 9 — UNKNOWN TOOL")
print("=" * 70)

result = tool_executor.execute(
    tool_name="delete_everything",
    arguments={}
)

print(result)


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("J.A.R.V.I.S. TOOL ENGINE V1 TEST COMPLETE")
print("=" * 70)