from pathlib import Path
import shutil

from opsguard.server.tools.registry import (
    Tool,
    register_tool
)


def read_file(payload):
    path = Path(payload["path"])

    if not path.exists():
        raise Exception(f"{path} not found")

    return {
        "path": str(path),
        "content": path.read_text()
    }


def file_exists(payload):
    path = Path(payload["path"])

    return {
        "path": str(path),
        "exists": path.exists()
    }


def find_file(payload):
    root = Path(payload["repo_path"])
    filename = payload["filename"]

    matches = []

    for file in root.rglob(filename):
        matches.append(str(file))

    return {
        "matches": matches
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
    path = Path(payload["path"])

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
    path = Path(payload["path"])

    if not path.exists():
        raise Exception(f"{path} not found")

    old = payload["old"]
    new = payload["new"]

    content = path.read_text()

    if old not in content:

        return {
            "status": "not_found",
            "path": str(path)
        }

    create_backup({
        "path": str(path)
    })

    updated = content.replace(
        old,
        new,
        1
    )

    path.write_text(updated)

    return {
        "status": "success",
        "path": str(path)
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