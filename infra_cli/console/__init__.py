import os
import logging
from pkg_resources import get_distribution, DistributionNotFound

import click
import click_log

from .commands import export
from .commands import init


logger = logging.getLogger()
click_log.basic_config(logger)


try:
    VERSION = get_distribution('infra-cli').version
except DistributionNotFound:
    VERSION = 'unknown'


def _get_log_level(verbose):
    verbosity = [
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]

    return verbosity[min(len(verbosity) - 1, verbose)]


@click.group(name=__package__)
@click.option('--root', default='.', type=click.Path(exists=True, resolve_path=True, file_okay=False),
              help="The root to search from, defaulting to CWD.")
@click.version_option(VERSION, '-V', '--version')
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, root, verbose):
    ctx.ensure_object(dict)

    if root:
        ctx.obj['ROOT'] = root
    else:
        ctx.obj['ROOT'] = os.getcwd()

    logger.setLevel(_get_log_level(verbose))


cli.add_command(export)
cli.add_command(init)


def run():
    cli(auto_envvar_prefix='INFRA')
