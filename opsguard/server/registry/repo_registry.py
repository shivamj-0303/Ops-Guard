import json
from pathlib import Path

REGISTRY_FILE = (
    Path(__file__).parent / "repos.json"
)


def load_registry():
    if not REGISTRY_FILE.exists():
        return {}

    with open(REGISTRY_FILE, "r") as file:
        return json.load(file)


def save_registry(data):
    with open(REGISTRY_FILE, "w") as file:
        json.dump(
            data,
            file,
            indent=4
        )


def register_repo(
    repo_id,
    repo_path
):
    data = load_registry()

    data[repo_id] = {
        "repo_path": repo_path
    }

    save_registry(data)


def get_repo(repo_id):
    data = load_registry()

    return data.get(repo_id)


def list_repos():
    return load_registry()


def remove_repo(repo_id):
    data = load_registry()

    if repo_id in data:
        del data[repo_id]

    save_registry(data)