from __future__ import annotations

from importlib import import_module
from typing import Any

_EXPORTS: dict[str, str] = {
    "HomePage": "homepage",
    "PWHomePage": "pw_homepage",
}

__all__ = list(_EXPORTS)


def __getattr__(name: str) -> Any:
    module_name = _EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module = import_module(f"{__name__}.{module_name}")

    try:
        value = getattr(module, name)
    except AttributeError as e:
        raise AttributeError(
            f"Module {module.__name__!r} does not define {name!r}"
        ) from e

    globals()[name] = value  # cache it
    return value
