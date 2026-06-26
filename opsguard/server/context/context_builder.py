def build_incident_context(
    incident,
    analysis,
    commits,
    report
):
    return {
        "incident": incident,
        "analysis": analysis,
        "container": {
            "id": report["container_id"],
            "name": report["name"]
        },
        "logs": report["logs_tail"],
        "recent_commits": commits
    }