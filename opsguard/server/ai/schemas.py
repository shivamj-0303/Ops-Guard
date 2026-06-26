from dataclasses import dataclass
from typing import List


@dataclass
class RepairStep:
    step: int
    action: str
    reason: str


@dataclass
class InvestigationResult:
    root_cause: str
    confidence: float
    severity: str
    explanation: str
    repair_steps: List[RepairStep]