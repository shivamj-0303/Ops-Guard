from dataclasses import dataclass
from typing import Optional


@dataclass
class InvestigationContext:

    logs: str

    trace: dict

    docker: dict

    git: dict

    source: dict

    dependencies: dict