import json

from pathlib import Path

from opsguard.server.ai.context_builder_execution import (
    build_execution_context
)

PROMPT = (
    Path(__file__).parent
    / "prompts"
    / "execution_plan.txt"
)


def build_execution_plan(
    provider,
    investigation,
    container_name,
    repo_path
):
    system_prompt = PROMPT.read_text()

    context = build_execution_context(
        investigation,
        container_name,
        repo_path
    )

    response = provider.investigate(
        system_prompt
        + "\n\n"
        + context
    )

    return json.loads(response)