from pathlib import Path


def get_opsguard_dir():
    current = Path.cwd()

    opsguard_dir = current / ".opsguard"

    if not opsguard_dir.exists():
        raise Exception(
            "OpsGuard not initialized. Run 'opsguard init'"
        )

    return opsguard_dir