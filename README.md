# NetworkSimulator

This repository packages three undergraduate networking assignments into one shared simulation framework.

The goal of the refactor is not to force all three projects to share the same business logic. Instead, it gives them a common runtime:

- one launcher
- one config format
- one reporting format
- one module registry
- one place to add scenarios, logging, and output

That makes the repo much easier to present on GitHub, extend for demos, and discuss in interviews.

## What is in here

- `a1` - transport demos
  - TCP / UDP style socket demos
  - simple send/receive flow
  - good for showing basic networking and client/server structure
- `a2` - reliable transport simulation
  - sender / receiver
  - packet loss, corruption, delay, timers
  - good for showing protocol design and event-driven simulation
- `a3` - routing simulation
  - nodes, routing tables, topology propagation
  - good for showing distributed-systems style thinking

## Unified architecture

The shared framework lives in `core/` and defines the common lifecycle:

- `simulate()`
- `load_scenario()`
- `reset()`
- `report()`

Module-specific hooks remain separate:

- `send_packet()` for transport-style demos
- `handle_event()` for event-driven logic
- `update_routes()` for routing logic

Scenarios are externalized under:

```text
scenarios/<module>/<scenario>.json
```

That means most run-time behavior can be adjusted without editing code.

## How to run

Primary launcher:

```bash
python3 main.py a1 --scenario tcp
python3 main.py a2 --scenario default
python3 main.py a3 --scenario default --param num_nodes=3 --param link_changes=false
```

Useful flags:

- `--scenario` selects a scenario file
- `--seed` sets the simulation seed
- `--trace` controls verbosity
- `--config-dir` points to the scenario directory
- `--param KEY=VALUE` overrides scenario values from the command line

Legacy course entrypoints still work where preserved:

```bash
python3 a2/main.py
python3 a2/main.py --scenario default --param max_messages=1
```

## Example outputs

The unified report prints the same structure for every module:

- module name
- scenario name
- success state
- summary
- metrics
- ordered steps

That makes the repo easier to read quickly and easier to show in screenshots or demo recordings.

## Project structure

- `core/` - shared framework, config, registry, reporting, scenario loading
- `a1/` - transport demo module
- `a2/` - reliable transport simulator
- `a3/` - routing simulator
- `scenarios/` - externalized run configurations
- `main.py` - top-level unified CLI

## Why this is a stronger portfolio project

- It shows systems thinking, not just a single assignment submission.
- It separates framework concerns from algorithm concerns.
- It supports multiple simulation styles under one interface.
- It is easier to extend, benchmark, and present as a coherent engineering project.

## Notes

- Existing coursework logic is preserved.
- The refactor is intentionally incremental so each module can still be inspected on its own.
- The framework is designed to be improved further with better scenario coverage, richer reports, and tighter CLI integration.
