from datetime import datetime
from threading import Lock
from opsguard.server.remediation.planner import (
    build_remediation_plan
)
from opsguard.server.remediation.approvals import (
    save_approval_request
)

active_incidents = {}
incident_history = []
incident_counter = 0
incident_lock = Lock()

def create_incident(container_id, container_name):
    global incident_counter

    with incident_lock:

        if container_id in active_incidents:
            return None

        incident_counter += 1

        incident = {
            "incident_id": f"INC-{incident_counter:04d}",
            "container_id": container_id,
            "container_name": container_name,
            "status": "OPEN",
            "created_at": datetime.utcnow().isoformat()
        }

        active_incidents[container_id] = incident

        return incident


def get_incident(container_id):
    return active_incidents.get(container_id)


def close_incident(container_id):
    with incident_lock:
        active_incidents.pop(container_id, None)

def archive_incident(incident):
    incident_history.append(incident)
