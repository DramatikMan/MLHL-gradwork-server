import alembic
import typer as t

from .migrations import config

database = t.Typer()


@database.command()
def revision(message: str = t.Argument(...)) -> None:
    alembic.command.revision(config.alembic_config, message=message, autogenerate=True)
