import typer as t

from .database import database
from .start import start

entrypoint = t.Typer(name="gwserver")
entrypoint.add_typer(database, name="db")
entrypoint.add_typer(start, name="start")
