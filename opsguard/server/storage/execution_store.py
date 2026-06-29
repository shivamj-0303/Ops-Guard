from pathlib import Path
import json

EXECUTIONS_DIR = (
    Path(".opsguard")
    / "executions"
)

EXECUTIONS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def save_execution(
    incident_id,
    execution
):
    path = (
        EXECUTIONS_DIR
        / f"{incident_id}.json"
    )

    path.write_text(
        json.dumps(
            execution,
            indent=4
        )
    )

    return str(path)