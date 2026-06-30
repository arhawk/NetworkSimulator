from __future__ import annotations

from typing import Dict, Iterable, Optional, Type

from .base import SimulationModule

_MODULES: Dict[str, Type[SimulationModule]] = {}


def register_module(name: str, module_cls: Optional[Type[SimulationModule]] = None):
    if module_cls is not None:
        _MODULES[name] = module_cls
        return module_cls

    def decorator(cls: Type[SimulationModule]) -> Type[SimulationModule]:
        _MODULES[name] = cls
        return cls

    return decorator


def get_module(name: str) -> Type[SimulationModule]:
    if name not in _MODULES:
        raise KeyError(f"Unknown module: {name}")
    return _MODULES[name]


def available_modules() -> Iterable[str]:
    return sorted(_MODULES)
