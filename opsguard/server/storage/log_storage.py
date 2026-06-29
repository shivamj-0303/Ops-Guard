from pathlib import Path
from opsguard.cli.utils.project import (
    get_opsguard_dir
)

def save_logs(
    incident_id,
    logs
):
    logs_dir = (
        get_opsguard_dir()
        / "incidents"
        / "logs"
    )

    logs_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    path = logs_dir / f"{incident_id}.log"

    path.write_text(logs)

    return str(path)