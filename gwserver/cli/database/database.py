import alembic
import typer as t

from .migrations import config

cmd = t.Typer(help="Database management.")


@cmd.command(help="Create migration to current ORM state.")
def revision(message: str = t.Argument(..., help="Migration description.")) -> None:
    alembic.command.revision(config.alembic_config, message=message, autogenerate=True)


@cmd.command(help="Upgrade database schema to target version.")
def upgrade(target: str = t.Argument(..., help="Upgrade to target version.")) -> None:
    alembic.command.upgrade(config.alembic_config, target.lower())


@cmd.command(help="Downgrade database schema to target version.")
def downgrade(target: str = t.Argument(..., help="Downgrade to target version.")) -> None:
    alembic.command.downgrade(config.alembic_config, target.lower())
