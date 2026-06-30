import json
from pathlib import Path
from opsguard.cli.utils.project import get_opsguard_dir


CONFIG_FILE = "config.json"


def _load_config():
    opsguard_dir = get_opsguard_dir()
    config_path = opsguard_dir / CONFIG_FILE

    if not config_path.exists():
        raise Exception("OpsGuard not initialized. Run: opsguard init")

    return config_path, json.loads(config_path.read_text())


def _save_config(config_path, config):
    config_path.write_text(json.dumps(config, indent=4))


# =========================
# ADD CONTAINER
# =========================

def add_container(name: str):
    config_path, config = _load_config()

    containers = config.get("containers", [])

    if any(c["container_name"] == name for c in containers):
        print(f"Container '{name}' already registered")
        return

    containers.append({
        "container_name": name,
        "runtime": "docker"
    })

    config["containers"] = containers
    _save_config(config_path, config)

    print(f"Added container: {name}")


# =========================
# REMOVE CONTAINER
# =========================

def remove_container(name: str):
    config_path, config = _load_config()

    containers = config.get("containers", [])

    new_containers = [
        c for c in containers
        if c["container_name"] != name
    ]

    config["containers"] = new_containers
    _save_config(config_path, config)

    print(f"Removed container: {name}")