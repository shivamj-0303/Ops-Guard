from pathlib import Path
import json


def get_opsguard_dir():
    current = Path.cwd()

    opsguard_dir = current / ".opsguard"

    if opsguard_dir.exists():
        return opsguard_dir

    raise Exception(
        "OpsGuard not initialized. Run 'opsguard init'"
    )


def get_project_config():
    opsguard_dir = get_opsguard_dir()

    config_file = opsguard_dir / "config.json"

    if not config_file.exists():
        raise Exception(
            "config.json not found."
        )

    with open(config_file) as file:
        return json.load(file)


def get_project_path():
    config = get_project_config()

    return config["project_path"]