import logging

from . import api, cli, core, model, tasks

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


__all__ = (
    "api",
    "cli",
    "core",
    "model",
    "tasks",
)
