from pathlib import Path


def save_logs(
    incident_id,
    logs
):
    logs_dir = (
        Path(".opsguard")
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