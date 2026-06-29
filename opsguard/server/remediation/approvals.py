from pathlib import Path
import json

APPROVALS_DIR = (
    Path(".opsguard")
    / "approvals"
)

APPROVALS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def save_approval_request(
    incident_id,
    plan
):
    path = (
        APPROVALS_DIR
        / f"{incident_id}.json"
    )

    path.write_text(
        json.dumps(
            plan,
            indent=4
        )
    )

    return str(path)