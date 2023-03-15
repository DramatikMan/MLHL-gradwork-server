import typer as t

from .database import cmd as database
from .init import cmd as init
from .start import cmd as start

entrypoint = t.Typer(name="gwserver")
entrypoint.add_typer(database, name="db")
entrypoint.add_typer(init, name="init")
entrypoint.add_typer(start, name="start")
