from opsguard.cli.utils.container_registry import (
    get_registered_containers
)


def list_containers():
    containers = (
        get_registered_containers()
    )

    print(
        "\nRegistered Containers\n"
    )

    if not containers:
        print("No containers registered")
        return

    for container in containers:
        print(
            f"- {container['container_name']}"
        )