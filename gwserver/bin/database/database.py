import alembic
import typer as t

from .migrations import config

database = t.Typer()


@database.command()
def revision(message: str = t.Argument(...)) -> None:
    alembic.command.revision(config.alembic_config, message=message, autogenerate=True)


@database.command()
def upgrade(target: str = t.Argument(...)) -> None:
    alembic.command.upgrade(config.alembic_config, target.lower())


@database.command()
def downgrade(target: str = t.Argument(...)) -> None:
    alembic.command.downgrade(config.alembic_config, target.lower())
