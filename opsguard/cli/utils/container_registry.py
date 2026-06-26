import json

from opsguard.cli.utils.project import get_opsguard_dir


CONTAINERS_FILE = "containers.json"


def get_registered_containers():
    opsguard_dir = get_opsguard_dir()

    container_file = (
        opsguard_dir / CONTAINERS_FILE
    )

    if not container_file.exists():
        return []

    with open(container_file) as file:
        return json.load(file)


def register_container(container_name):
    containers = get_registered_containers()

    already_registered = any(
        container["container_name"] == container_name
        for container in containers
    )

    if already_registered:
        return False

    containers.append({
        "container_name": container_name
    })

    opsguard_dir = get_opsguard_dir()

    with open(
        opsguard_dir / CONTAINERS_FILE,
        "w"
    ) as file:
        json.dump(
            containers,
            file,
            indent=4
        )

    return True

def is_registered_container(
    container_name
):
    containers = (
        get_registered_containers()
    )

    return any(
        container["container_name"]
        == container_name
        for container in containers
    )