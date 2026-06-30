import argparse
from opsguard.cli.commands.init import init_project
from opsguard.cli.commands.start import start
from opsguard.cli.commands.register_container import register_container_command
from opsguard.cli.commands.status import status


def main():
    parser = argparse.ArgumentParser(
        prog="opsguard",
        description="OpsGuard - Incident detection & remediation system"
    )

    subparsers = parser.add_subparsers(dest="command")

    # init
    subparsers.add_parser("init", help="Initialize OpsGuard in project")

    # start
    subparsers.add_parser("start", help="Start OpsGuard daemon")

    # register container (IMPORTANT for usability)
    register_parser = subparsers.add_parser("register-container")
    register_parser.add_argument("--name", required=True)

    # status (debugging UX for users)
    subparsers.add_parser("status", help="Show OpsGuard state")

    args = parser.parse_args()

    if args.command == "init":
        init_project()

    elif args.command == "start":
        start()

    elif args.command == "register-container":
        register_container_cmd(args.name)

    elif args.command == "status":
        status()

    else:
        parser.print_help()