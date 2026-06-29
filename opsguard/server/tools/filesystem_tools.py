from pathlib import Path
import shutil

from opsguard.server.tools.registry import (
    Tool,
    register_tool
)


def read_file(payload):

    if "file_path" in payload:
        path = Path(payload["file_path"])

    else:
        root = Path(payload["repo_path"])
        filename = payload["filename"]

        matches = list(root.rglob(filename))

        if not matches:
            raise Exception(f"{filename} not found")

        path = matches[0]

    return {
        "file_path": str(path),
        "content": path.read_text()
    }

def file_exists(payload):
    path = Path(payload["repo_path"])

    return {
        "path": str(path),
        "exists": path.exists()
    }


def find_file(payload):
    root = Path(payload["repo_path"])
    filename = payload["filename"]

    matches = list(root.rglob(filename))

    if not matches:
        raise Exception(f"{filename} not found")

    return {
        "file_path": str(matches[0])
    }


def search_text(payload):
    root = Path(payload["repo_path"])
    text = payload["text"]

    matches = []

    for file in root.rglob("*"):

        if not file.is_file():
            continue

        try:
            content = file.read_text()

        except Exception:
            continue

        if text in content:

            matches.append({
                "path": str(file)
            })

    return {
        "matches": matches
    }


def create_backup(payload):
    path = Path(payload["repo_path"])

    if not path.exists():
        raise Exception(f"{path} not found")

    backup = path.with_suffix(
        path.suffix + ".bak"
    )

    shutil.copy2(
        path,
        backup
    )

    return {
        "original": str(path),
        "backup": str(backup)
    }


def replace_text(payload):

    if "file_path" in payload:
        path = Path(payload["file_path"])

    else:
        root = Path(payload["repo_path"])
        filename = payload["filename"]

        matches = list(root.rglob(filename))

        if not matches:
            raise Exception(f"{filename} not found")

        path = matches[0]

    content = path.read_text()

    content = content.replace(
        payload["old_text"],
        payload["new_text"]
    )

    path.write_text(content)

    return {
        "status": "success",
        "file_path": str(path)
    }

register_tool(
    Tool(
        name="filesystem.read_file",
        description="Read file contents",
        func=read_file
    )
)

register_tool(
    Tool(
        name="filesystem.file_exists",
        description="Check if file exists",
        func=file_exists
    )
)

register_tool(
    Tool(
        name="filesystem.find_file",
        description="Find file by name",
        func=find_file
    )
)

register_tool(
    Tool(
        name="filesystem.search_text",
        description="Search text inside repository",
        func=search_text
    )
)

register_tool(
    Tool(
        name="filesystem.create_backup",
        description="Create backup of file",
        func=create_backup
    )
)

register_tool(
    Tool(
        name="filesystem.replace_text",
        description="Replace text inside a file",
        func=replace_text
    )
)