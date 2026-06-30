from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .config import SimulationConfig
from .logging import SimulationLogger
from .results import SimulationResult


class SimulationModule(ABC):
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.logger = SimulationLogger(enabled=config.trace > 0)
        self.result = SimulationResult(module=config.module, scenario=config.scenario)

    def load_scenario(self) -> None:
        return None

    def reset(self) -> None:
        self.result = SimulationResult(module=self.config.module, scenario=self.config.scenario)

    @abstractmethod
    def simulate(self) -> SimulationResult:
        raise NotImplementedError

    def report(self) -> SimulationResult:
        return self.result

    def send_packet(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("send_packet is not implemented for this module")

    def handle_event(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("handle_event is not implemented for this module")

    def update_routes(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("update_routes is not implemented for this module")

