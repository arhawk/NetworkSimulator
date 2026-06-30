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
    from .NetworkSimulator import A2Scenario, NetworkSimulator
except ImportError:  # pragma: no cover
    from NetworkSimulator import A2Scenario, NetworkSimulator


@register_module("a2")
class ReliableTransportModule(SimulationModule):
    def load_scenario(self) -> None:
        params = load_scenario_config(self.config.config_dir, self.config.module, self.config.scenario)
        params.update(self.config.params)
        self.scenario_obj = A2Scenario(
            max_messages=int(params.get("max_messages", 5)),
            loss_prob=float(params.get("loss_prob", 0.0)),
            corrupt_prob=float(params.get("corrupt_prob", 0.0)),
            avg_delay=float(params.get("avg_delay", 1.0)),
            seed=self.config.seed,
            trace=self.config.trace,
        )

    def simulate(self) -> SimulationResult:
        self.reset()
        self.load_scenario()
        simulator = NetworkSimulator()
        simulator.initSimulator(
            self.scenario_obj.max_messages,
            self.scenario_obj.loss_prob,
            self.scenario_obj.corrupt_prob,
            self.scenario_obj.avg_delay,
            self.scenario_obj.seed,
            self.scenario_obj.trace,
        )
        delivered = simulator.simulate()
        self.result.steps = [
            StepRecord(name="reliable-transport", details="sender/receiver exchange completed")
        ]
        self.result.summary = "Reliable transport protocol simulation"
        self.result.metrics = {
            "delivered": len(delivered),
            "loss_prob": self.scenario_obj.loss_prob,
            "corrupt_prob": self.scenario_obj.corrupt_prob,
        }
        return self.report()


def build_module(config: SimulationConfig) -> ReliableTransportModule:
    return ReliableTransportModule(config)
