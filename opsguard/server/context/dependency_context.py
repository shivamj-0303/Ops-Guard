from pathlib import Path


FILES = [
    "requirements.txt",
    "pyproject.toml",
    "Pipfile"
]


def collect_dependencies(repo_path):

    result = {}

    for filename in FILES:

        file = Path(repo_path) / filename

        if file.exists():
            result[filename] = file.read_text()

    return result