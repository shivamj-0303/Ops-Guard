import docker

client = docker.from_env()


def collect_docker_context(container_id):

    container = client.containers.get(container_id)

    return {

        "id": container.id,

        "name": container.name,

        "status": container.status,

        "image": container.image.tags,

        "attrs": container.attrs

    }