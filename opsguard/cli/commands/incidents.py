import json

from pathlib import Path


def list_incidents():
    incident_dir = (
        Path.cwd()
        / ".opsguard"
        / "incidents"
    )

    if not incident_dir.exists():
        print(
            "No incidents found"
        )
        return

    files = sorted(
        incident_dir.glob("*.json")
    )

    if not files:
        print(
            "No incidents found"
        )
        return

    print(
        "\nOpsGuard Incidents\n"
    )

    for file in files:
        with open(file) as f:
            incident = json.load(f)

        summary = (
            incident["analysis"]
            .get("summary")
        )

        print(
            f"{incident['incident_id']} | "
            f"{incident['status']} | "
            f"{summary}"
        )