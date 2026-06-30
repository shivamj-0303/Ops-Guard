from pathlib import Path
import json


def get_project_root():
    current = Path.cwd()

    opsguard_dir = current / ".opsguard"

    if not opsguard_dir.exists():
        raise Exception("OpsGuard not initialized")

    return current


def get_project_config():
    root = get_project_root()
    config_path = root / ".opsguard" / "config.json"

    return json.loads(config_path.read_text())