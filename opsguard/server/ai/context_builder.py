import json


def build_investigation_context(
    report,
    analysis,
    trace,
    commits
):
    logs = report.get("logs_tail", "") or ""

    # Keep only the most recent portion of logs
    truncated_logs = logs[-15000:]

    context = {
        "container": {
            "id": report.get("container_id"),
            "name": report.get("name"),
            "exit_code": report.get("exit_code"),
            "reason": report.get("reason")
        },
        "analysis": analysis,
        "trace": trace,
        "recent_commits": commits,
        "logs": truncated_logs
    }

    return json.dumps(context, indent=2)