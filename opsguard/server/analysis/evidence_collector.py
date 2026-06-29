def collect_evidence(
    report,
    analysis,
    trace
):
    evidence = []

    if analysis.get("crash_type"):
        evidence.append(
            {
                "type": "crash_type",
                "value": analysis["crash_type"]
            }
        )

    if trace.get("exception"):
        evidence.append(
            {
                "type": "exception",
                "value": trace["exception"]
            }
        )

    if trace.get("file"):
        evidence.append(
            {
                "type": "file",
                "value": trace["file"]
            }
        )

    if report.get("exit_code") is not None:
        evidence.append(
            {
                "type": "exit_code",
                "value": report["exit_code"]
            }
        )

    return evidence