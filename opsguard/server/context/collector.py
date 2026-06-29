from opsguard.server.context.models import InvestigationContext

from opsguard.server.context.source_code import (
    collect_source_context
)

from opsguard.server.context.git_context import (
    collect_git_context
)

from opsguard.server.context.docker_context import (
    collect_docker_context
)

from opsguard.server.context.dependency_context import (
    collect_dependencies
)


def collect_context(

    report,

    trace,

    repo_path

):

    return InvestigationContext(

        logs=report.get(
            "logs_tail",
            ""
        ),

        trace=trace,

        docker=collect_docker_context(

            report["container_id"]

        ),

        git=collect_git_context(

            repo_path

        ),

        source=collect_source_context(

            repo_path,

            trace

        ),

        dependencies=collect_dependencies(

            repo_path

        )

    )