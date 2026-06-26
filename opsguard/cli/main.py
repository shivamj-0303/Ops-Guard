import sys

from opsguard.cli.commands.init import (
    init_project
)

from opsguard.cli.commands.start import (
    start_opsguard
)

from opsguard.cli.commands.register_container import (
    register_container_command
)

from opsguard.cli.commands.incidents import (
    list_incidents
)

from opsguard. cli.commands.incident import (
    show_incident
)

from opsguard.cli.commands.containers import (
    list_containers
)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: opsguard <command>"
        )
        return

    command = sys.argv[1]

    if command == "init":
        init_project()
        return

    if command == "containers":
        list_containers()
        return

    if command == "register-container":
        if len(sys.argv) < 3:
            print(
                "Usage: opsguard register-container <name>"
            )
            return

        register_container_command(
            sys.argv[2]
        )
        return
    
    if command == "incidents":
        list_incidents()
        return
    
    if command == "incident":
        if len(sys.argv) < 3:
            print(
                "Usage: opsguard incident <id>"
            )
            return

        show_incident(
            sys.argv[2]
        )
        return

    if command == "start":
        start_opsguard()
        return

    print(
        f"Unknown command: {command}"
    )