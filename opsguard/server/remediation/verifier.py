import docker

client = docker.from_env()

def verify_container(
    container_name
):
    container = (
        client.containers.get(
            container_name
        )
    )

    container.reload()

    return (
        container.status
        == "running"
    )