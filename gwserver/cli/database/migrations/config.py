from alembic.config import Config

from gwserver import model
from gwserver.core import config

alembic_config = Config()
alembic_config.set_main_option("script_location", "gwserver.cli.database:migrations")
alembic_config.set_main_option("sqlalchemy.url", config.DB_URL)

_ = model
