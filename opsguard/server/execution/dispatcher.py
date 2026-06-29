from opsguard.server.tools.registry import execute_tool


def dispatch_action(action):
    tool = action["tool"]
    arguments = action.get("arguments", {})

    print(f"Executing tool: {tool}")
    print(f"Arguments: {arguments}")

    return execute_tool(
        tool,
        arguments
    )