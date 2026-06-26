from typing import Callable, Dict, Any

class Tool:
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func


TOOL_REGISTRY: Dict[str, Tool] = {}

def register_tool(tool: Tool):
    TOOL_REGISTRY[tool.name] = tool


def execute_tool(name: str, payload: Dict[str, Any]):
    if name not in TOOL_REGISTRY:
        raise Exception(f"Tool {name} not found")

    return TOOL_REGISTRY[name].func(payload)