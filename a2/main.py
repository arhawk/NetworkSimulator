from __future__ import annotations

import argparse
import os
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core import SimulationConfig, format_result

try:
    from .module import ReliableTransportModule
except ImportError:  # pragma: no cover
    from module import ReliableTransportModule


def getSimulatorParameter():
    print("Network Simulator")
    nMsgSim = int(input("Enter number of messages to simulate (> 0): "))
    if nMsgSim <= 0:
        print("Number of Messages must be > 0")
        sys.exit()

    loss = float(input("Enter the packet loss probability (0.0 for no loss): "))
    if (loss < 0) or (loss > 1):
        print("packet loss probability must be > 0.0 and < 1.0")
        sys.exit()

    corrupt = float(
        input("Enter the packet corruption probability (0.0 for no corruption): ")
    )
    if (corrupt < 0) or (corrupt > 1):
        print("packet corruption probability must be > 0.0 and < 1.0")
        sys.exit()

    delay = float(
        input(
            "Enter the average time between messages from the sender's application layer (> 0.0): "
        )
    )
    if delay < 0:
        print("Number of Messages must be > 0.0")
        sys.exit()

    seed = 10
    trace = 1
    return nMsgSim, loss, corrupt, delay, seed, trace


def run_interactive():
    maxMsgs, loss, corrupt, delay, seed, trace = getSimulatorParameter()
    config = SimulationConfig(
        module="a2",
        params={
            "max_messages": maxMsgs,
            "loss_prob": loss,
            "corrupt_prob": corrupt,
            "avg_delay": delay,
        },
        seed=seed,
        trace=trace,
    )
    result = ReliableTransportModule(config).simulate()
    print(format_result(result))
    return result


def simulate(config=None):
    config = config or {}
    if isinstance(config, SimulationConfig):
        sim_config = config
    else:
        sim_config = SimulationConfig(
            module="a2",
            params=dict(config),
            seed=int(config.get("seed", 10)),
            trace=int(config.get("trace", 1)),
        )
    return ReliableTransportModule(sim_config).simulate()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A2 reliable transport simulator")
    parser.add_argument("--scenario", default="default", help="scenario name")
    parser.add_argument("--seed", type=int, default=10, help="random seed")
    parser.add_argument("--trace", type=int, default=1, help="trace level")
    parser.add_argument("--config-dir", default="scenarios", help="scenario config directory")
    parser.add_argument("--param", action="append", default=[], metavar="KEY=VALUE", help="extra module params")
    return parser


def _parse_params(items):
    params = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"Invalid --param value: {item}")
        key, value = item.split("=", 1)
        params[key] = value
    return params


def main():
    if len(sys.argv) == 1:
        run_interactive()
        return 0

    parser = build_parser()
    args = parser.parse_args()
    config = SimulationConfig(
        module="a2",
        scenario=args.scenario,
        seed=args.seed,
        trace=args.trace,
        params=_parse_params(args.param),
        config_dir=args.config_dir,
    )
    result = ReliableTransportModule(config).simulate()
    print(format_result(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
