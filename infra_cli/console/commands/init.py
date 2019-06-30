import os

import click
from semver import VersionInfo

from infra_cli.entity.project.models import Project
from infra_cli.entity.project.repository import get_project, save_project


def _validate_semver(ctx, param, value):
    try:
        return VersionInfo.parse(value)
    except ValueError:
        raise click.BadParameter("Invalid Version: Must be Semantic Version")


@click.command()
@click.option('--name', required=True, default=lambda: os.path.basename(os.getcwd()), prompt='Project Name')
@click.option('--version', default='0.0.1', callback=_validate_semver, prompt='Project Version')
@click.option('--repository', default='', prompt=True, show_default="No Repository")
@click.pass_context
def init(context, name, version, repository):
    root = context.obj['ROOT']

    try:
        project = get_project(root)
    except ValueError:
        project = None

    if project:
        click.echo("Project %s already exists at %s" % (project.name, root))
        return context.abort()

    project_kwargs = {
        "name": name,
        "version": version
    }

    if repository:
        project_kwargs["repository"] = repository

    project = Project(root, **project_kwargs)

    save_project(project)




