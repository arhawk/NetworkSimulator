from __future__ import annotations

import argparse

from core import SimulationConfig, available_modules, format_result, get_module

# importing modules registers them
import a1.module  # noqa: F401
import a2.module  # noqa: F401
import a3.module  # noqa: F401


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NetworkSimulator framework")
    parser.add_argument("module", nargs="?", choices=list(available_modules()), help="module to run")
    parser.add_argument("--scenario", default="default", help="scenario name")
    parser.add_argument("--seed", type=int, default=10, help="random seed")
    parser.add_argument("--trace", type=int, default=1, help="trace level")
    parser.add_argument("--config-dir", default="scenarios", help="scenario config directory")
    parser.add_argument("--param", action="append", default=[], metavar="KEY=VALUE", help="extra module params")
    return parser


def parse_params(items):
    params = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"Invalid --param value: {item}")
        key, value = item.split("=", 1)
        params[key] = value
    return params


def run_module(module_name: str, args: argparse.Namespace):
    module_cls = get_module(module_name)
    config = SimulationConfig(
        module=module_name,
        scenario=args.scenario,
        seed=args.seed,
        trace=args.trace,
        params=parse_params(args.param),
        config_dir=args.config_dir,
    )
    module = module_cls(config)
    result = module.simulate()
    print(format_result(result))
    return result


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.module:
        print("Available modules:", ", ".join(available_modules()))
        return 0
    run_module(args.module, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
