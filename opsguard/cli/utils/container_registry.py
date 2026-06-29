import json

from opsguard.cli.utils.project import get_opsguard_dir


CONFIG_FILE = "config.json"


def get_registered_containers():
    opsguard_dir = get_opsguard_dir()

    config_file = (
        opsguard_dir / CONFIG_FILE
    )

    if not config_file.exists():
        return []

    with open(config_file) as file:
        config = json.load(file)

    return config.get("containers", [])


def register_container(container_name):
    opsguard_dir = get_opsguard_dir()

    config_file = (
        opsguard_dir / CONFIG_FILE
    )

    if not config_file.exists():
        raise Exception(
            "OpsGuard project is not initialized."
        )

    with open(config_file) as file:
        config = json.load(file)

    containers = config.get(
        "containers",
        []
    )

    already_registered = any(
        container["container_name"] == container_name
        for container in containers
    )

    if already_registered:
        return False

    containers.append({
        "container_name": container_name,
        "runtime": "docker"
    })

    config["containers"] = containers

    with open(
        config_file,
        "w"
    ) as file:
        json.dump(
            config,
            file,
            indent=4
        )

    return True


def is_registered_container(container_name):
    containers = (
        get_registered_containers()
    )

    return any(
        container["container_name"] == container_name
        for container in containers
    )