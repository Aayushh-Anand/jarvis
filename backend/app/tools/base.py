from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):

    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """
        Execute the tool.

        Every JARVIS tool must implement this method.
        """
        pass