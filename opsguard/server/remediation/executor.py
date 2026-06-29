from datetime import datetime

from opsguard.server.execution.dispatcher import (
    dispatch_action
)

from opsguard.server.storage.execution_store import (
    save_execution
)


def execute_remediation_plan(
    incident_id,
    plan
):
    execution = {
        "incident_id": incident_id,
        "status": "RUNNING",
        "started_at": datetime.utcnow().isoformat(),
        "steps": []
    }

    for action in plan["actions"]:

        result = dispatch_action(
            action
        )

        execution["steps"].append(
            {
                "tool": action["tool"],
                "arguments": action["arguments"],
                "result": result
            }
        )

    execution["status"] = "SUCCESS"

    execution["finished_at"] = (
        datetime.utcnow().isoformat()
    )

    save_execution(
        incident_id,
        execution
    )

    return execution