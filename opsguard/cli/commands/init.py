from pathlib import Path
import json
import uuid

from git import Repo


def init_project():
    current_path = Path.cwd()

    try:
        repo = Repo(current_path)
    except Exception:
        print("Not inside a git repository.")
        return

    opsguard_dir = current_path / ".opsguard"

    opsguard_dir.mkdir(exist_ok=True)

    config_file = opsguard_dir / "config.json"

    remote_url = None

    if repo.remotes:
        remote_url = repo.remotes.origin.url

    config = {
        "project_id": str(uuid.uuid4()),
        "project_name": current_path.name,
        "project_path": str(current_path),
        "git_remote": remote_url,
        "containers": [],
        "settings": {
            "ai_provider": "ollama",
            "approval_required": True,
            "auto_execute": False
        }
    }

    with open(
        config_file,
        "w"
    ) as file:
        json.dump(
            config,
            file,
            indent=4
        )

    print("OpsGuard initialized successfully.")