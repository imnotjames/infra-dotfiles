from __future__ import unicode_literals

import os
import os.path
from tempfile import TemporaryDirectory
import re
from functools import lru_cache, reduce
from itertools import accumulate
from hashlib import md5

import yaml
import shutil
from git import Repo
import click

from infra_cli.entity.project import find_projects
from infra_cli.entity.application import find_applications


VENDOR_CHART_PATH = "vendor"
VENDOR_CHART_GITHUB_HOST = "github.com"
VENDOR_CHART_STACK_PATH = "stacks"
VENDOR_CHART_ADDONS_PATH = "addons"
DEFAULT_CHART_REF = 'master'
VENDOR_CHART_TEMP = TemporaryDirectory()


DEFAULT_STACK_PROJECT = os.environ.get("DEFAULT_STACK_PROJECT", "imnotjames/infra-dotfiles-charts")
DEFAULT_ADDON_PROJECT = os.environ.get("DEFAULT_ADDON_PROJECT", "imnotjames/infra-dotfiles-charts")


@lru_cache(maxsize=None)
def clone_repository(git_url, ref=None):
    directory = os.path.join(VENDOR_CHART_TEMP.name, md5(git_url.encode()).hexdigest(), md5(ref.encode()).hexdigest())

    # Clone repository to this directory
    try:
        repo = Repo.clone_from(git_url, directory, depth=1)

        if ref:
            if ref in repo.tags:
                repo.tags[ref].checkout()
            elif hasattr(repo.heads, ref):
                getattr(repo.heads, ref).checkout()
            else:
                raise ValueError('Invalid Ref')

        return directory
    except Exception:
        shutil.rmtree(directory)
        raise


@lru_cache(maxsize=1024)
def fetch_vendor_chart(root, chart_project, chart_path, chart_ref):
    if re.match('^([\w,\-,\_]+)\/([\w,\-,\_]+)$', chart_project):
        # This is a chart in the format of `username/password` which usually means github
        git_url = "git@{}:{}.git".format(VENDOR_CHART_GITHUB_HOST.rstrip("/"), chart_project)
        chart_namespace = VENDOR_CHART_GITHUB_HOST.replace("/", "-")
    else:
        git_url = chart_project
        match = re.match('^(\w+://)?(.+@)*([\w\d\.]+)(:[\d]+){0,1}/*(.*)$', chart_project)
        if match:
            chart_namespace = match[3]
        else:
            chart_namespace = chart_project.split('/')[0]

    chart_ref = chart_ref if chart_ref else DEFAULT_CHART_REF

    local_path = os.path.join(
        VENDOR_CHART_PATH,
        re.sub('[^0-9a-zA-Z\.]', '_', chart_namespace),
        os.path.join(*chart_project.split("/")),
        os.path.join(*chart_path.split("/")),
        re.sub('[^0-9a-zA-Z\.]', '_', chart_ref)
    )

    cloned_path = clone_repository(git_url, chart_ref)
    repo_chart_path = os.path.join(cloned_path, chart_path)

    if not os.path.isdir(repo_chart_path):
        raise ValueError("%s not found in %s" % (chart_path, chart_project))

    shutil.copytree(repo_chart_path, os.path.join(root, local_path))

    return local_path


def generate_environment_chart(root, project, application, environment):
    def _dump(file, o):
        yaml.dump(
            o,
            open(file, 'w+'),
            Dumper=yaml.SafeDumper,
            explicit_start=True,
            default_flow_style=False,
            encoding='utf-8'
        )

    chart_name = "{}-{}-{}".format(
        project.name.replace('-', ''),
        application.name.replace('-', ''),
        environment.name.replace('-', '')
    )

    chart_path = os.path.join(root, chart_name)

    try:
        os.makedirs(chart_path)
    except FileExistsError:
        pass

    manifest_file = os.path.join(chart_path, 'Chart.yaml')
    requirements_file = os.path.join(chart_path, 'requirements.yaml')
    values_file = os.path.join(chart_path, 'values.yaml')

    requirements = []
    values = {}

    stack = environment.stack

    stack_project = stack.project if stack.project else DEFAULT_STACK_PROJECT
    stack_chart = environment.stack.type
    stack_ref = stack.version

    stack_chart = os.path.join(VENDOR_CHART_STACK_PATH, stack_chart)

    vendor_chart_path = fetch_vendor_chart(root, stack_project, stack_chart, stack_ref)
    local_path = os.path.join("..", vendor_chart_path)

    requirements.append({
        "name": stack_chart,
        "repository": "file://%s" % local_path,
        "alias": "stack"
    })

    values["namespace"] = {
        "project": project.name,
        "application": application.name,
        "environment": environment.name,
    }

    values["stack"] = environment.parameters.as_dict()

    for addon in environment.addons:
        addon_project = addon.project if addon.project else DEFAULT_ADDON_PROJECT
        addon_chart = addon.type
        addon_ref = addon.version
        addon_as = addon.alias
        addon_parameters = addon.parameters.as_dict()

        addon_chart = os.path.join(VENDOR_CHART_ADDONS_PATH, addon_chart)

        addon_vendor_chart_path = fetch_vendor_chart(root, addon_project, addon_chart, addon_ref)
        addon_local_path = os.path.join("..", addon_vendor_chart_path)

        addon_alias = "addon-{}".format(addon_as.replace("_", "-").lower())

        requirements.append({
            "name": addon_chart,
            "repository": "file://%s" % addon_local_path,
            "alias": addon_alias
        })

        values[addon_alias] = {}
        values[addon_alias].update(addon_parameters)
        values[addon_alias]['injection'] = addon_as

    requirements = {"dependencies": requirements}

    manifest = {
        "name": chart_name,
        "apiVersion": "v1",
        "appVersion": project.version,
        "description": "A Helm chart for Kubernetes",
        "version": "0.1.0"
    }

    _dump(manifest_file, manifest)
    _dump(requirements_file, requirements)
    _dump(values_file, values)


@click.command()
@click.option('--output', default='helm', type=click.Path(exists=False, resolve_path=True, file_okay=False))
@click.option('--force', is_flag=True)
@click.pass_context
def charts(context, output, force):
    root = context.obj['ROOT']

    # Check if the output directory is empty.  If it's not, complain.
    if os.listdir(root):
        if force:
            shutil.rmtree(output)
        else:
            raise click.BadOptionUsage("--output", "Output directory must be empty (or --force)")

    # mkdirp
    for d in accumulate(os.path.split(output), lambda a, b: os.path.join(a, b)):
        if not os.path.exists(d):
            os.mkdir(d)

    with VENDOR_CHART_TEMP:
        for project in find_projects(root):
            for application in find_applications(project):

                for environment_name in application.environments:
                    environment = application.get_environment(environment_name)

                    generate_environment_chart(output, project, application, environment)
