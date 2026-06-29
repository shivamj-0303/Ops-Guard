from pathlib import Path
import json

CONFIG_FILE = "config.json"


def get_opsguard_dir():
    current = Path.cwd()

    opsguard_dir = current / ".opsguard"

    if not opsguard_dir.exists():
        raise Exception(
            "OpsGuard not initialized. Run 'opsguard init'"
        )

    return opsguard_dir


def load_project_config():
    config_file = (
        get_opsguard_dir()
        / CONFIG_FILE
    )

    with open(config_file) as f:
        return json.load(f)


def get_project_path():
    config = load_project_config()

    return config["project_path"]