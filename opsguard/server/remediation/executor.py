from datetime import datetime
from pathlib import Path
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
        tool = action["tool"]

        arguments = action["arguments"]

        if tool == "filesystem.find_file":

            result = dispatch_action(action)

            arguments["file_path"] = result["file_path"]

        elif tool in [
            "filesystem.read_file",
            "filesystem.replace_text"
        ]:

            if "file_path" not in arguments:

                root = Path(arguments["repo_path"])

                matches = list(
                    root.rglob(arguments["filename"])
                )

                if not matches:
                    raise Exception(
                        f'{arguments["filename"]} not found'
                    )

                arguments["file_path"] = str(matches[0])

            result = dispatch_action(action)

        else:

            try:

                result = dispatch_action(action)

                execution["steps"].append({

                    "tool": action["tool"],

                    "arguments": action["arguments"],

                    "status": "SUCCESS",

                    "result": result

                })

            except Exception as e:

                execution["steps"].append({

                    "tool": action["tool"],

                    "arguments": action["arguments"],

                    "status": "FAILED",

                    "error": str(e)

                })

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