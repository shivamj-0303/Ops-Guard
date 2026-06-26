from pathlib import Path
import json
from opsguard.server.ai.context_builder import (
    build_investigation_context
)


PROMPT_PATH = (
    Path(__file__)
    .parent
    / "prompts"
    / "incident_analysis.txt"
)


def investigate_incident(
    provider,
    report,
    analysis,
    trace,
    commits
):
    with open(PROMPT_PATH) as f:
        system_prompt = f.read()

    context = build_investigation_context(
        report,
        analysis,
        trace,
        commits
    )

    full_prompt = (
        system_prompt
        + "\n\n"
        + context
    )
    print("\n===== PROMPT =====\n")
    print(full_prompt)


    response = provider.investigate(full_prompt)
    return json.loads(response)