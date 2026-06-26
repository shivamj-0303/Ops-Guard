import json

from pathlib import Path


def show_incident(
    incident_id
):
    file_path = (
        Path.cwd()
        / ".opsguard"
        / "incidents"
        / f"{incident_id}.json"
    )

    if not file_path.exists():
        print(
            "Incident not found"
        )
        return

    with open(file_path) as file:
        incident = json.load(file)

    print(
        json.dumps(
            incident,
            indent=4
        )
    )