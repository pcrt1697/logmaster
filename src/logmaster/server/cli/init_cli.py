import click

from logmaster.server.core.kafka.connect.service import initialize_connector


@click.command()
@click.option(
    '--force',
    is_flag=True,
    type=bool,
    default=False,
    help="If True, the MongoDB sink connector is re-created."
)
def init(force: bool = False):
    """ Initialize the application. """
    initialize_connector(force)
