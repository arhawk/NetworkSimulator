from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class StepRecord:
    name: str
    details: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationResult:
    module: str
    scenario: str
    success: bool = True
    summary: str = ""
    steps: List[StepRecord] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

