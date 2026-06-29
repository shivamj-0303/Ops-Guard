from pathlib import Path


def analyze_commit_relevance(
    trace,
    commits
):
    trace_file = trace.get("file")

    if not trace_file:
        return []

    trace_name = Path(trace_file).name

    matches = []

    for commit in commits:
        changed_files = commit.get(
            "files_changed",
            []
        )

        for file in changed_files:
            if Path(file).name == trace_name:
                matches.append(
                    {
                        "commit": commit["hash"],
                        "message": commit["message"],
                        "file": file
                    }
                )

    return matches