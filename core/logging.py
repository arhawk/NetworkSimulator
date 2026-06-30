from dataclasses import dataclass, field
from typing import List


@dataclass
class SimulationLogger:
    enabled: bool = True
    lines: List[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        self.lines.append(message)
        if self.enabled:
            print(message)

    def section(self, title: str) -> None:
        self.log(f"\n=== {title} ===")

