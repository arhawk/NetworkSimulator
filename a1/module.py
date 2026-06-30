from __future__ import annotations

from dataclasses import dataclass

from core import (
    SimulationConfig,
    SimulationModule,
    SimulationResult,
    StepRecord,
    load_scenario_config,
    register_module,
)


@dataclass
class TransportDemoScenario:
    name: str
    protocol: str
    description: str


DEFAULT_SCENARIOS = {
    "udp": TransportDemoScenario("udp", "UDP", "Datagram socket echo demo."),
    "tcp": TransportDemoScenario("tcp", "TCP", "Stream socket echo demo."),
    "multi-client": TransportDemoScenario(
        "multi-client",
        "TCP",
        "Multi-client socket demo with concurrent connections.",
    ),
}


@register_module("a1")
class TransportDemoModule(SimulationModule):
    def load_scenario(self) -> None:
        data = load_scenario_config(self.config.config_dir, self.config.module, self.config.scenario)
        defaults = DEFAULT_SCENARIOS["udp"]
        merged = {
            "name": data.get("name", self.config.scenario),
            "protocol": data.get("protocol", defaults.protocol),
            "description": data.get("description", defaults.description),
        }
        self.scenario_obj = TransportDemoScenario(**merged)

    def send_packet(self, transport: str, payload: str, stage: str) -> StepRecord:
        return StepRecord(
            name=f"{transport}:{stage}",
            details=payload,
            metadata={"transport": transport, "payload_size": len(payload)},
        )

    def simulate(self) -> SimulationResult:
        self.reset()
        self.load_scenario()
        self.logger.section(f"a1 transport demo: {self.scenario_obj.name}")

        steps = [
            self.send_packet(self.scenario_obj.protocol, "client -> server", "send"),
            StepRecord(
                name=f"{self.scenario_obj.protocol}:transform",
                details="server processes payload and returns response",
            ),
            self.send_packet(self.scenario_obj.protocol, "server -> client", "recv"),
        ]
        if self.scenario_obj.name == "multi-client":
            steps.append(
                StepRecord(
                    name="multi-client:concurrency",
                    details="multiple clients connect and are handled independently",
                )
            )

        self.result.steps = steps
        self.result.summary = self.scenario_obj.description
        self.result.metrics = {"protocol": self.scenario_obj.protocol, "demo_count": 3}
        return self.report()


def build_module(config: SimulationConfig) -> TransportDemoModule:
    return TransportDemoModule(config)
