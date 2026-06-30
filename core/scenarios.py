from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


def scenario_path(config_dir: str, module: str, scenario: str) -> Path:
    return Path(config_dir) / module / f"{scenario}.json"


def load_scenario_config(
    config_dir: str,
    module: str,
    scenario: str,
    fallback: Optional[str] = "default",
) -> Dict[str, Any]:
    candidates = [scenario]
    if fallback and fallback not in candidates:
        candidates.append(fallback)

    for candidate in candidates:
        path = scenario_path(config_dir, module, candidate)
        if path.exists():
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            if not isinstance(data, dict):
                raise ValueError(f"Scenario file must contain a JSON object: {path}")
            return data

    return {}

