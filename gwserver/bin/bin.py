import typer as t

from .api import api
from .database import database

entrypoint = t.Typer(name="gwserver")
entrypoint.add_typer(database, name="db")
entrypoint.add_typer(api, name="api")
