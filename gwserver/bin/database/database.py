import alembic
import typer as t

from .migrations import config

database = t.Typer(help="Database management.")


@database.command(help="Create migration to current ORM state.")
def revision(message: str = t.Argument(..., help="Migration description.")) -> None:
    alembic.command.revision(config.alembic_config, message=message, autogenerate=True)


@database.command(help="Upgrade database schema to target version.")
def upgrade(target: str = t.Argument(..., help="Upgrade target version.")) -> None:
    alembic.command.upgrade(config.alembic_config, target.lower())


@database.command(help="Downgrade database schema to target version.")
def downgrade(target: str = t.Argument(..., help="Downgrade target version.")) -> None:
    alembic.command.downgrade(config.alembic_config, target.lower())
