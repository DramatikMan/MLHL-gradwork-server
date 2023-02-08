import subprocess as sp

import typer as t

from gwserver.core import config

api = t.Typer()


@api.command(name="start")
def start(
    workers: int = t.Option(config.API_WORKERS),
    port: int = t.Option(config.API_PORT),
) -> None:
    sp.run(
        [
            "gunicorn",
            "gwserver.api:app",
            f"--workers={workers}",
            "--worker-class=uvicorn.workers.UvicornWorker",
            f"--bind=0.0.0.0:{port}",
        ],
        check=True,
    )
