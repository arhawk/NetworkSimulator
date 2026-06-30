from __future__ import annotations

from .results import SimulationResult


def format_result(result: SimulationResult) -> str:
    lines = [
        "=== Simulation Report ===",
        f"module: {result.module}",
        f"scenario: {result.scenario}",
        f"success: {result.success}",
        f"summary: {result.summary}",
    ]
    if result.metrics:
        lines.append("metrics:")
        for key in sorted(result.metrics):
            lines.append(f"  - {key}: {result.metrics[key]}")
    if result.steps:
        lines.append("steps:")
        for index, step in enumerate(result.steps, start=1):
            lines.append(f"  {index}. {step.name}")
            if step.details:
                lines.append(f"     {step.details}")
            if step.metadata:
                lines.append(f"     metadata: {step.metadata}")
    return "\n".join(lines)
