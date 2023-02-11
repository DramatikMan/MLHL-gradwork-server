import subprocess as sp

import typer as t

from gwserver.core import config

api = t.Typer(help="API server.")


@api.command(help="Start API server.")
def start(
    workers: int = t.Option(config.API_WORKERS, help="Nubmer of workers."),
    port: int = t.Option(config.API_PORT, help="Server port."),
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
