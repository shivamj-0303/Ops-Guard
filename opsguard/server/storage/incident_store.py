import json

from pathlib import Path


def get_incident_directory():
    incident_dir = (
        Path.cwd()
        / ".opsguard"
        / "incidents"
    )

    incident_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return incident_dir


def save_incident(incident):
    incident_dir = get_incident_directory()

    file_path = (
        incident_dir
        / f"{incident['incident_id']}.json"
    )

    with open(file_path, "w") as file:
        json.dump(
            incident,
            file,
            indent=4
        )


def get_all_incidents():
    incident_dir = get_incident_directory()

    incidents = []

    for file in sorted(
        incident_dir.glob("*.json")
    ):
        with open(file) as f:
            incidents.append(
                json.load(f)
            )

    return incidents


def get_incident_by_id(
    incident_id
):
    incident_dir = get_incident_directory()

    file_path = (
        incident_dir
        / f"{incident_id}.json"
    )

    if not file_path.exists():
        return None

    with open(file_path) as file:
        return json.load(file)