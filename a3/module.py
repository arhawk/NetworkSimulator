from __future__ import annotations

from core import (
    SimulationConfig,
    SimulationModule,
    SimulationResult,
    StepRecord,
    load_scenario_config,
    register_module,
)

try:
    from .NetworkSimulator import NetworkSimulator
except ImportError:  # pragma: no cover
    from NetworkSimulator import NetworkSimulator


def _coerce_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


@register_module("a3")
class RoutingSimulatorModule(SimulationModule):
    def load_scenario(self) -> None:
        params = load_scenario_config(self.config.config_dir, self.config.module, self.config.scenario)
        params.update(self.config.params)
        self.scenario_obj = {
            "seed": int(params.get("seed", self.config.seed)),
            "trace": int(params.get("trace", self.config.trace)),
            "num_nodes": int(params.get("num_nodes", 9)),
            "link_changes": _coerce_bool(params.get("link_changes", True)),
        }

    def update_routes(self):
        return None

    def simulate(self) -> SimulationResult:
        self.reset()
        self.load_scenario()
        simulator = NetworkSimulator(
            seed=self.scenario_obj["seed"],
            trace=self.scenario_obj["trace"],
            num_nodes=self.scenario_obj["num_nodes"],
            link_changes=self.scenario_obj["link_changes"],
        )
        simulator.runSimulator()
        self.result.steps = [
            StepRecord(name="routing-simulation", details="distance-vector propagation completed")
        ]
        self.result.summary = "Distributed routing simulation"
        self.result.metrics = {
            "num_nodes": self.scenario_obj["num_nodes"],
            "link_changes": self.scenario_obj["link_changes"],
        }
        return self.report()


def build_module(config: SimulationConfig) -> RoutingSimulatorModule:
    return RoutingSimulatorModule(config)
