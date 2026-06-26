from opsguard.cli.utils.container_registry import (
    register_container
)


def register_container_command(
    container_name
):
    success = register_container(
        container_name
    )

    if success:
        print(
            f"Container registered: {container_name}"
        )
    else:
        print(
            f"Container already registered: {container_name}"
        )