from pathlib import Path

import alembic
import typer as t

from gwserver.cli.database.migrations.config import alembic_config
from gwserver.core import config
from gwserver.core.s3 import s3

cmd = t.Typer(help="Application initialization.")


def init_database() -> None:
    alembic.command.upgrade(alembic_config, "head")


def init_model() -> None:
    path = Path(config.MODEL_VOLUME)

    if not path.exists():
        raise RuntimeError("Model volume path does not exist.")

    path.chmod(0o666)

    with open(path.joinpath(config._MODEL_FNAME), "wb") as handle:
        handle.write(s3.download(config.MODEL_KEY))


database = cmd.command(name="database", help="Initialize database.")(init_database)
model = cmd.command(name="model", help="Download model for inference.")(init_model)


@cmd.command(name="all", help="Run full initializtion logic.")
def full() -> None:
    init_database()
    init_model()
