import json


def build_investigation_context(
    report,
    analysis,
    context,
    commits,
    evidence,
    commit_analysis
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
        "trace": context.trace,
        "recent_commits": commits,
        "docker": context.docker,
        "git": context.git,
        "source": context.source,
        "dependencies": context.dependencies,
        "logs": truncated_logs,
        "evidence": evidence,
        "commit_analysis": commit_analysis
    }

    return json.dumps(context, indent=2)