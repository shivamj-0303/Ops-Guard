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


def collect_logs(payload):
    container = None

    if "container_id" in payload:
        container = client.containers.get(payload["container_id"])

    elif "container_name" in payload:
        container = client.containers.get(payload["container_name"])

    else:
        raise Exception(
            "container_id or container_name required"
        )

    logs = container.logs(
        tail=100
    ).decode("utf-8")

    return {
        "container_id": container.id,
        "container_name": container.name,
        "logs": logs
    }


def inspect_container(payload):
    container_id = payload.get("container_id")

    container = client.containers.get(container_id)

    return container.attrs

def restart_container(payload):
    container = None

    if "container_id" in payload:
        container = client.containers.get(payload["container_id"])

    elif "container_name" in payload:
        container = client.containers.get(payload["container_name"])

    else:
        raise Exception(
            "container_id or container_name required"
        )

    container.restart()

    return {
        "status": "success",
        "container": container.name
    }

# REGISTER TOOLS
register_tool(Tool(
    name="docker.list_containers",
    description="List all docker containers",
    func=list_containers
))

register_tool(Tool(
    name="docker.collect_logs",
    description="Fetch logs from a container",
    func=collect_logs
))

register_tool(Tool(
    name="docker.inspect_container",
    description="Inspect docker container metadata",
    func=inspect_container
))

register_tool(
    Tool(
        name="docker.restart_container",
        description="Restart a Docker container",
        func=restart_container
    )
)