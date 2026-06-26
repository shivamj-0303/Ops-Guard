from opsguard.server.analysis.log_parser import extract_error_signals


def analyze_crash(report):
    logs = report.get("logs_tail", "")
    exit_code = report.get("exit_code")
    oom_killed = report.get("oom_killed", False)

    signals = extract_error_signals(logs)

    result = {
        "summary": "Unknown failure",
        "severity": "low",
        "confidence": "low",
        "likely_cause": "Not enough data",
        "crash_type": "UNKNOWN",
        "evidence": signals,
        "suspected_layer": "unknown",
        "next_action_suggestion": "Inspect logs manually",
    }

    # OOM (highest confidence)
    if oom_killed:
        result["summary"] = (
            "Container terminated due to out-of-memory condition"
        )
        result["likely_cause"] = (
            "Application exhausted available memory"
        )
        result["crash_type"] = "OOM_KILL"
        result["severity"] = "high"
        result["confidence"] = "high"
        result["suspected_layer"] = "application"
        result["evidence"].append("oom_killed")

        return result

    # Missing dependencies
    elif "missing_dependency" in signals:
        result["summary"] = (
            "Application missing required package or module"
        )
        result["likely_cause"] = (
            "Broken dependency installation or missing runtime package"
        )
        result["crash_type"] = "MISSING_DEPENDENCY"
        result["severity"] = "medium"
        result["confidence"] = "high"
        result["suspected_layer"] = "build"

    # Configuration problems
    elif (
        "configuration_error" in signals
        or "invalid_config" in signals
        or "missing_env_var" in signals
    ):
        result["summary"] = (
            "Application failed because of invalid configuration"
        )
        result["likely_cause"] = (
            "Missing or incorrect configuration values"
        )
        result["crash_type"] = "CONFIGURATION_ERROR"
        result["severity"] = "medium"
        result["confidence"] = "medium"
        result["suspected_layer"] = "configuration"

    # Database failures
    elif (
        "database_error" in signals
        or "db_connection_failed" in signals
    ):
        result["summary"] = (
            "Application failed while communicating with database"
        )
        result["likely_cause"] = (
            "Database unavailable or credentials incorrect"
        )
        result["crash_type"] = "DATABASE_FAILURE"
        result["severity"] = "high"
        result["confidence"] = "medium"
        result["suspected_layer"] = "database"

    # Network failures
    elif (
        "connection_refused" in signals
        or "dns_failure" in signals
        or "network_unreachable" in signals
    ):
        result["summary"] = (
            "Application could not reach a required service"
        )
        result["likely_cause"] = (
            "Dependency service unavailable or networking issue"
        )
        result["crash_type"] = "NETWORK_FAILURE"
        result["severity"] = "high"
        result["confidence"] = "medium"
        result["suspected_layer"] = "network"

    # Timeout failures
    elif (
        "timeout" in signals
        or "request_timeout" in signals
    ):
        result["summary"] = (
            "Operation exceeded configured timeout"
        )
        result["likely_cause"] = (
            "Dependency too slow or timeout value too aggressive"
        )
        result["crash_type"] = "TIMEOUT"
        result["severity"] = "medium"
        result["confidence"] = "medium"
        result["suspected_layer"] = "application"

    # Permission failures
    elif (
        "permission_denied" in signals
        or "eacces" in signals
    ):
        result["summary"] = (
            "Application lacked required permissions"
        )
        result["likely_cause"] = (
            "Filesystem, container, or OS permission issue"
        )
        result["crash_type"] = "PERMISSION_ERROR"
        result["severity"] = "medium"
        result["confidence"] = "high"
        result["suspected_layer"] = "infrastructure"

    # Resource exhaustion
    elif (
        "disk_full" in signals
        or "too_many_open_files" in signals
    ):
        result["summary"] = (
            "Application exhausted a critical system resource"
        )
        result["likely_cause"] = (
            "Disk space, file descriptors, or system limits exceeded"
        )
        result["crash_type"] = "RESOURCE_EXHAUSTION"
        result["severity"] = "high"
        result["confidence"] = "high"
        result["suspected_layer"] = "infrastructure"

    # Startup failures
    elif (
        "startup_failure" in signals
        or "failed_to_start" in signals
    ):
        result["summary"] = (
            "Application failed during startup"
        )
        result["likely_cause"] = (
            "Initialization or bootstrapping process failed"
        )
        result["crash_type"] = "STARTUP_FAILURE"
        result["severity"] = "high"
        result["confidence"] = "medium"
        result["suspected_layer"] = "application"

    # Unhandled exceptions
    elif (
        "traceback" in signals
        or "exception" in signals
        or "unhandled_exception" in signals
    ):
        result["summary"] = (
            "Application crashed due to an unhandled exception"
        )
        result["likely_cause"] = (
            "Runtime exception was not caught by the application"
        )
        result["crash_type"] = "UNHANDLED_EXCEPTION"
        result["severity"] = "high"
        result["confidence"] = "medium"
        result["suspected_layer"] = "application"

    # SIGKILL / SIGTERM
    elif exit_code in (137, 143):
        result["summary"] = (
            "Container was terminated by an external signal"
        )
        result["likely_cause"] = (
            "Manual stop, orchestrator restart, or infrastructure action"
        )
        result["crash_type"] = "MANUAL_TERMINATION"
        result["severity"] = "medium"
        result["confidence"] = "low"
        result["suspected_layer"] = "infrastructure"

    return result