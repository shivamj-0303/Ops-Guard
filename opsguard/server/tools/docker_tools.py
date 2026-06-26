import docker
from opsguard.server.tools.registry import Tool, register_tool

client = docker.from_env()


def list_containers(payload):
    containers = client.containers.list(all=True)

    return [
        {
            "id": c.id[:12],
            "name": c.name,
            "status": c.status
        }
        for c in containers
    ]


def get_logs(payload):
    container_id = payload.get("container_id")

    if not container_id:
        raise Exception("container_id required")

    container = client.containers.get(container_id)
    logs = container.logs(tail=100).decode("utf-8")

    return {
        "container_id": container_id,
        "logs": logs
    }


def inspect_container(payload):
    container_id = payload.get("container_id")

    container = client.containers.get(container_id)

    return container.attrs


# REGISTER TOOLS
register_tool(Tool(
    name="list_containers",
    description="List all docker containers",
    func=list_containers
))

register_tool(Tool(
    name="get_logs",
    description="Fetch logs from a container",
    func=get_logs
))

register_tool(Tool(
    name="inspect_container",
    description="Inspect docker container metadata",
    func=inspect_container
))