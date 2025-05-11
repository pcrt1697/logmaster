import os

import click

from logmaster.server.api.app import run_app
from logmaster.core.config import EnvVars


@click.command()
@click.option(
    '-p',
    '--port',
    type=int,
    default=os.environ.get(EnvVars.BACKEND_PORT, 5050),
    help="Port used to expose the APIs."
)
@click.option(
    '--dev',
    is_flag=True,
    type=bool,
    default=False,
    help="If true, developer APIs are exposed as a separate version."
)
def run(port: int, dev: bool):
    """ Run the backend application """
    run_app(port, dev)
