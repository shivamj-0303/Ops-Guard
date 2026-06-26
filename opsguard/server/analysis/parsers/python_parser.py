import re

PYTHON_TRACEBACK_PATTERN = re.compile(
    r'File "([^"]+)", line (\d+)',
    re.MULTILINE
)

EXCEPTION_PATTERN = re.compile(
    r"([A-Za-z_]+Error):"
)

def extract_python_traceback(logs: str):
    matches = PYTHON_TRACEBACK_PATTERN.findall(logs)

    exception_match = EXCEPTION_PATTERN.search(logs)

    exception_type = (
        exception_match.group(1)
        if exception_match
        else None
    )
    if not matches:
        return None

    last_match = matches[-1]

    return {
        "language": "python",
        "file": last_match[0],
        "line": int(last_match[1]),
        "exception": exception_type
    }