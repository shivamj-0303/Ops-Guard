import json


def build_execution_context(
    investigation,
    container_name,
    repo_path
):
    context = {
        "repository_path": str(repo_path),
        "container_name": container_name,
        "investigation": investigation
    }

    return json.dumps(
        context,
        indent=2
    )