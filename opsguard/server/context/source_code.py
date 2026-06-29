from pathlib import Path


def collect_source_context(

    repo_path,

    trace,

    radius=20

):

    file_path = Path(repo_path) / trace["file"].lstrip("/")

    if not file_path.exists():

        return {}

    lines = file_path.read_text().splitlines()

    line = trace["line"]

    start = max(0, line-radius)

    end = min(len(lines), line+radius)

    snippet = []

    for i in range(start, end):

        snippet.append(

            {

                "line": i+1,

                "code": lines[i]

            }

        )

    return {

        "file": str(file_path),

        "snippet": snippet

    }