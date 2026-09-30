from app.tools.router import select_tool


tests = [

    "What is Python?",

    "What time is it?",

    r"Open the folder D:\Projects\jarvis\backend",

    r"List the files in D:\Projects\jarvis",

    r"Open the file D:\Projects\jarvis\README.md"
]


for message in tests:

    print("\n" + "=" * 60)

    print("USER:")
    print(message)

    print("\nJARVIS TOOL ROUTER:")

    result = select_tool(message)

    print(result)