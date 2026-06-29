import docker

client = docker.from_env()

def restart_container(
    container_name
):
    container = (
        client.containers.get(
            container_name
        )
    )

    container.restart()

    return {
        "success": True
    }