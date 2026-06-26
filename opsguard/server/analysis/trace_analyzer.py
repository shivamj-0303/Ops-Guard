from opsguard.server.analysis.parsers.python_parser import (
    extract_python_traceback
)


def analyze_trace(logs: str):
    python_result = extract_python_traceback(logs)

    if python_result:
        return python_result

    return None