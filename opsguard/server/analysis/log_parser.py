import re


def detect_language(logs: str):
    logs_lower = logs.lower()

    if "traceback" in logs:
        return "python"

    if (
        "node:" in logs_lower
        or "npm" in logs_lower
        or "javascript heap out of memory" in logs_lower
    ):
        return "node"

    if "panic:" in logs_lower:
        return "go"

    if "exception in thread" in logs_lower:
        return "java"

    return "unknown"


def extract_error_signals(logs: str):
    signals = []

    logs_lower = logs.lower()

    # ------------------------
    # Network
    # ------------------------

    if (
        "connection refused" in logs_lower
        or "econnrefused" in logs_lower
    ):
        signals.append("connection_refused")

    if (
        "temporary failure in name resolution" in logs_lower
        or "name or service not known" in logs_lower
        or "getaddrinfo failed" in logs_lower
        or "dns" in logs_lower
    ):
        signals.append("dns_failure")

    if (
        "network is unreachable" in logs_lower
        or "host unreachable" in logs_lower
    ):
        signals.append("network_unreachable")

    # ------------------------
    # Dependencies
    # ------------------------

    if (
        "modulenotfounderror" in logs_lower
        or "importerror" in logs_lower
        or "cannot find module" in logs_lower
        or "no module named" in logs_lower
    ):
        signals.append("missing_dependency")

    # ------------------------
    # Exceptions
    # ------------------------

    if "traceback" in logs:
        signals.append("traceback")
        signals.append("unhandled_exception")

    if "exception" in logs_lower:
        signals.append("exception")

    if "panic:" in logs_lower:
        signals.append("unhandled_exception")

    # ------------------------
    # Memory
    # ------------------------

    if (
        "out of memory" in logs_lower
        or "oom" in logs_lower
        or "javascript heap out of memory" in logs_lower
        or "killed" in logs
    ):
        signals.append("memory_issue")

    # ------------------------
    # Configuration
    # ------------------------

    if (
        "missing environment variable" in logs_lower
        or "environment variable not set" in logs_lower
        or "invalid configuration" in logs_lower
        or "config error" in logs_lower
    ):
        signals.append("configuration_error")

    if (
        "keyerror:" in logs_lower
        and "env" in logs_lower
    ):
        signals.append("missing_env_var")

    # ------------------------
    # Database
    # ------------------------

    if (
        "database connection failed" in logs_lower
        or "could not connect to database" in logs_lower
        or "sqlstate" in logs_lower
        or "psycopg" in logs_lower
        or "mysql connection" in logs_lower
    ):
        signals.append("database_error")

    if (
        "authentication failed for user" in logs_lower
        or "access denied for user" in logs_lower
    ):
        signals.append("db_connection_failed")

    # ------------------------
    # Permissions
    # ------------------------

    if (
        "permission denied" in logs_lower
        or "eacces" in logs_lower
        or "[errno 13]" in logs_lower
    ):
        signals.append("permission_denied")

    # ------------------------
    # Timeouts
    # ------------------------

    if (
        "timeout" in logs_lower
        or "timed out" in logs_lower
        or "deadline exceeded" in logs_lower
    ):
        signals.append("timeout")

    # ------------------------
    # Resource exhaustion
    # ------------------------

    if (
        "no space left on device" in logs_lower
        or "disk full" in logs_lower
    ):
        signals.append("disk_full")

    if (
        "too many open files" in logs_lower
        or "emfile" in logs_lower
    ):
        signals.append("too_many_open_files")

    # ------------------------
    # Startup failures
    # ------------------------

    if (
        "failed to start" in logs_lower
        or "startup failed" in logs_lower
        or "application startup failed" in logs_lower
    ):
        signals.append("startup_failure")

    # Remove duplicates while preserving order
    return list(dict.fromkeys(signals))