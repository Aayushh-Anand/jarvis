import os
import subprocess

from app.tools.base import BaseTool


class OpenFileTool(BaseTool):

    name = "open_file"

    description = (
        "Open a file on the user's Windows computer "
        "using its default application."
    )

    def execute(self, path: str):

        if not path:
            return {
                "success": False,
                "error": "File path is required."
            }

        if not os.path.isfile(path):
            return {
                "success": False,
                "error": "File does not exist."
            }

        try:

            os.startfile(path)

            return {
                "success": True,
                "message": f"Opened file: {path}"
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }


class OpenFolderTool(BaseTool):

    name = "open_folder"

    description = (
        "Open a folder on the user's Windows computer "
        "using File Explorer."
    )

    def execute(self, path: str):

        if not path:
            return {
                "success": False,
                "error": "Folder path is required."
            }

        if not os.path.isdir(path):
            return {
                "success": False,
                "error": "Folder does not exist."
            }

        try:

            subprocess.Popen(
                ["explorer", path]
            )

            return {
                "success": True,
                "message": f"Opened folder: {path}"
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }


class ListFolderTool(BaseTool):

    name = "list_folder"

    description = (
        "List files and folders inside a directory."
    )

    def execute(self, path: str):

        if not path:
            return {
                "success": False,
                "error": "Folder path is required."
            }

        if not os.path.isdir(path):
            return {
                "success": False,
                "error": "Folder does not exist."
            }

        try:

            items = []

            for item in os.listdir(path):

                full_path = os.path.join(
                    path,
                    item
                )

                items.append({
                    "name": item,
                    "type": (
                        "folder"
                        if os.path.isdir(full_path)
                        else "file"
                    )
                })

            return {
                "success": True,
                "path": path,
                "items": items
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }


class CreateFolderTool(BaseTool):

    name = "create_folder"

    description = (
        "Create a new folder on the user's computer."
    )

    def execute(self, path: str):

        if not path:
            return {
                "success": False,
                "error": "Folder path is required."
            }

        if os.path.exists(path):
            return {
                "success": False,
                "error": "A file or folder already exists at this path."
            }

        try:

            os.makedirs(path)

            return {
                "success": True,
                "message": f"Folder created: {path}"
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }


class SearchFileTool(BaseTool):

    name = "search_file"

    description = (
        "Search for files or folders by name "
        "inside a specified directory."
    )

    def execute(
        self,
        directory: str,
        name: str
    ):

        if not directory:
            return {
                "success": False,
                "error": "Search directory is required."
            }

        if not name:
            return {
                "success": False,
                "error": "File or folder name is required."
            }

        if not os.path.isdir(directory):
            return {
                "success": False,
                "error": "Search directory does not exist."
            }

        results = []

        try:

            for root, dirs, files in os.walk(directory):

                for item in dirs + files:

                    if name.lower() in item.lower():

                        results.append(
                            os.path.join(
                                root,
                                item
                            )
                        )

            return {
                "success": True,
                "directory": directory,
                "query": name,
                "results": results
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }