from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ModuleConfig:
    name: str
    scenario: str = "default"
    seed: int = 10
    trace: int = 1
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationConfig:
    module: str
    scenario: str = "default"
    seed: int = 10
    trace: int = 1
    params: Dict[str, Any] = field(default_factory=dict)
    config_dir: str = "scenarios"
    output_dir: Optional[str] = None
